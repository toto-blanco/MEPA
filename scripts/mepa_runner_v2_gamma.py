#!/usr/bin/env python3
"""
================================================================================
MEPA V6.2 — Runner standardisé V2-gamma
================================================================================
Statut           : REMPLACEMENT
Cible            : /data/mepa/scripts/mepa_runner_v2_gamma.py
Remplace         : mepa_runner_v2_gamma.py v1.x
Rétrocompatibilité :
    - Équations différentielles (_step, F_val, R_val) : INCHANGÉES au bit près.
    - simulate(), _build_result(), _tableau_s2() : INCHANGÉS.
    - apply_sa_modulator(), stress_test(), make_cmd_linear() : INCHANGÉS.
    - _normalize_cmd() : INCHANGÉE (rétrocompat 'g' → 'gamma' maintenue).
    - run_wp() : 4 ajouts non-disruptifs documentés ci-dessous.
    - Sorties JSON : mêmes champs + champs additionnels (nc_bloquantes,
      nc_non_bloquantes, statut_nc).
Version          : 2.1.1
MEPA version     : 6.2 Fortifiée
Dépendances      : json, sys, datetime, math, warnings, os (stdlib uniquement)
                   numpy / scipy NON requis par ce fichier.
================================================================================

Corrections V2.1.1 vs V2.1.0 :
───────────────────────────────

[BUG-003] RÉSOLU — Variable shadowing 'p' dans _tableau_s2()
    Problème : `pts = sorted(p for p in pts ...)` — la variable d'itération 'p'
    ombrageait le paramètre central 'p: dict' du runner (risk maintenabilité/refactoring).
    Correction : renommée en 'pt' — comportement identique, lisibilité restaurée.

Corrections V2.1.0 vs V2.0 :
───────────────────────────

[ARCH-016] RÉSOLU — theta_FR chargé depuis mepa_constants.json (D5)
    Problème : SEUIL_FR = 0.75 hardcodé (violation source unique de vérité).
    Correction : _get_seuil_fr() lit parametres_simulation.theta_FR.defaut dans
    mepa_constants.json V1.2.0+. Fallback 0.75 maintenu avec RuntimeWarning si
    constants absent ou clé manquante. Valeur mise en cache après premier appel.
    Rétrocompat totale : comportement identique si mepa_constants.json est présent.

Corrections V2.0 vs V1.x :
───────────────────────────

[ARCH-013] RÉSOLU — Normalisation y0 dict → liste
    Problème : Le Nœud 1 peut transmettre y0 comme dict {S:…, L:…, C:…, I:…}.
    simulate() attend y0 = [S0, L0, C0, I0] (liste indexée).
    Correction : _normalize_y0() en tête de run_wp() convertit dict → liste.
    Rétrocompat totale : y0 liste pass-through sans modification.

[ARCH-014] RÉSOLU — Injection theta_C / theta_I depuis la config racine
    Problème : Le Nœud 1 place theta_C / theta_I à la racine de runner_config.
    run_wp() les passait à apply_sa_modulator(config['params'], sa) sans les
    injecter dans params, donc simulate() lisait les valeurs par défaut
    (0.30 / 0.22) même si la fiche spécifiait d'autres valeurs.
    Correction : run_wp() lit theta_C / theta_I depuis config (racine ET params),
    les injecte dans p avant d'appeler simulate().
    Priorité : config['params']['theta_C'] > config['theta_C'] > défaut 0.30.

[ARCH-015] RÉSOLU — Chemins canoniques /data/mepa/scripts/
    Problème : Certains scripts référençaient /opt/mepa/ (chemin inexistant sur Pi5 — canonique : /data/mepa/scripts/).
    Correction : MEPA_SCRIPTS_DIR chargé depuis variable d'environnement,
    défaut = /data/mepa/scripts/. Utilisé pour charger mepa_constants.json.

[NC GARDE-FOU] NOUVEAU — Détection variables NC en entrée de run_wp()
    run_wp() vérifie si cmd contient des valeurs "NC" avant simulation.
    NC bloquant (EROI, gamma) → RuntimeError descriptif (jamais NaN silencieux).
    NC non bloquant → warning stderr + champ nc_non_bloquantes dans meta.

Corrections V1.x (inchangées, rappel) :
    D2 — Intégration Euler explicite dt=1 (vs RK45)
    D3 — θ_C fixe (vs adaptatif)
    D4 — Labels trajectoires stricts (9 labels officiels — (γ) Transformation forcée + (d) Dissolution BUG-007)
    D5 — seuil_FR chargé depuis mepa_constants.json (parametres_simulation.theta_FR.defaut)
         Fallback 0.75 + RuntimeWarning si constants inaccessible. (ARCH-016)
    D6 — Clé 'gamma' remplace 'g' (rétrocompat _normalize_cmd)

Usage :
    python3 mepa_runner_v2_gamma.py config_wp.json
    python3 mepa_runner_v2_gamma.py config_wp.json result_out.json  (sortie explicite)
"""

import json, sys, datetime, math, os, warnings
from typing import Callable, Optional, Union

# ── Chemin canonique Pi5 (ARCH-015) ──────────────────────────────────────────
MEPA_SCRIPTS_DIR = os.environ.get("MEPA_SCRIPTS_DIR", "/data/mepa/scripts")

# ── CONSTANTES FIXES (prompt V3-gamma Partie 2) ──────────────────────────────
KAPPA    = 0.10
A_COEF   = 1.0
CC       = 0.50
I_MIN    = 0.30
K_SIG    = 10.0
EPS      = 1e-6
# D5 / ARCH-016 : seuil_FR chargé depuis mepa_constants.json via _get_seuil_fr().
# Valeur fixée à None ; initialisée au premier appel pour garantir la lecture
# du JSON avant tout usage. Fallback 0.75 si constants inaccessible (RuntimeWarning).
SEUIL_FR            = None
_SEUIL_FR_FALLBACK  = 0.75

# ── NC : sentinelle et variables bloquantes ───────────────────────────────────
NC_SENTINEL   = "NC"
# Variables dont un NC bloquant empêche la simulation
NC_BLOQUANTES_RUNNER = frozenset({"gamma", "EROI"})
# Variables NC non bloquantes pour le runner (dégradent qualité, pas simulation)
NC_NON_BLOQUANTES_RUNNER = frozenset({"E", "T", "Mob", "R", "Ref", "Rc", "Rn", "Pop"})


# ── CHARGEMENT mepa_constants.json (fallback si absent) ──────────────────────

def _charger_constants() -> dict:
    """Charge mepa_constants.json. Retourne fallback minimal si absent."""
    try:
        path = os.path.join(MEPA_SCRIPTS_DIR, "mepa_constants.json")
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {
            "nc_protocol": {
                "valeur_sentinel": "NC",
                "variables_nc_bloquantes": ["E_split", "gamma", "EROI", "Sa"],
            }
        }

_CONSTANTS = None  # chargé à la demande


def _get_constants() -> dict:
    global _CONSTANTS
    if _CONSTANTS is None:
        _CONSTANTS = _charger_constants()
    return _CONSTANTS


def _get_seuil_fr() -> float:
    """
    Charge theta_FR depuis mepa_constants.json (parametres_simulation.theta_FR.defaut).
    Retourne le fallback _SEUIL_FR_FALLBACK (0.75) si constants inaccessible,
    avec RuntimeWarning stderr.

    ARCH-016 : D5 — source unique de vérité dans mepa_constants.json.
    Avant V2.1, SEUIL_FR était hardcodé 0.75 (violation principe source unique).
    La valeur module globale SEUIL_FR est initialisée une seule fois puis mise en
    cache — appels suivants retournent la valeur sans relire le fichier.
    """
    global SEUIL_FR
    if SEUIL_FR is not None:
        return SEUIL_FR
    try:
        val = _get_constants()["parametres_simulation"]["theta_FR"]["defaut"]
        SEUIL_FR = float(val)
    except (KeyError, TypeError, ValueError):
        warnings.warn(
            "[MEPA V6.2 WARNING] theta_FR introuvable dans mepa_constants.json "
            f"— fallback={_SEUIL_FR_FALLBACK} utilisé (D5/ARCH-016). "
            "Vérifier que mepa_constants.json V1.2.0+ est déployé.",
            RuntimeWarning,
            stacklevel=2,
        )
        SEUIL_FR = _SEUIL_FR_FALLBACK
    return SEUIL_FR


# ── HELPERS NC ────────────────────────────────────────────────────────────────

def _is_nc(val) -> bool:
    """True si val est la sentinelle NC."""
    return isinstance(val, str) and val.strip().upper() == NC_SENTINEL


def _detect_nc_in_cmd(cmd: dict) -> tuple:
    """
    Parcourt un dict de commandes et détecte les valeurs NC.
    Retourne (nc_bloquantes: list, nc_non_bloquantes: list).
    """
    bloquantes    = [k for k, v in cmd.items() if _is_nc(v) and k in NC_BLOQUANTES_RUNNER]
    non_bloquantes = [k for k, v in cmd.items() if _is_nc(v) and k not in NC_BLOQUANTES_RUNNER]
    return bloquantes, non_bloquantes


# ── NORMALISATION y0 (ARCH-013) ───────────────────────────────────────────────

def _normalize_y0(y0_raw) -> list:
    """
    Normalise y0 en liste [S0, L0, C0, I0].

    Accepte :
      - liste  [1.0, 0.5, 0.1, 3.5]           → pass-through
      - dict   {S: 1.0, L: 0.5, C: 0.1, I: 3.5} → conversion
      - dict   {S0: 1.0, L0: 0.5, C0: 0.1, I0: 3.5} → conversion

    ARCH-013 : Le Nœud 1 construisait runner_config.y0 comme dict.
    simulate() attend une liste — cette fonction est le point de normalisation unique.
    """
    if isinstance(y0_raw, (list, tuple)):
        if len(y0_raw) < 4:
            raise ValueError(
                f"y0 liste trop courte : {len(y0_raw)} éléments, 4 attendus [S,L,C,I]."
            )
        return [float(y0_raw[0]), float(y0_raw[1]), float(y0_raw[2]), float(y0_raw[3])]

    if isinstance(y0_raw, dict):
        # Accepte {S:…, L:…, C:…, I:…} ou {S0:…, L0:…, C0:…, I0:…}
        try:
            S = float(y0_raw.get('S', y0_raw.get('S0', 1.0)))
            L = float(y0_raw.get('L', y0_raw.get('L0', 0.5)))
            C = float(y0_raw.get('C', y0_raw.get('C0', 0.1)))
            I = float(y0_raw.get('I', y0_raw.get('I0', 3.5)))
            print(
                "[MEPA V6.2 INFO] y0 fourni en dict — conversion automatique en liste "
                f"[{S}, {L}, {C}, {I}]. (ARCH-013 — normalisation Node 2 → Runner)",
                file=sys.stderr
            )
            return [S, L, C, I]
        except (TypeError, ValueError) as e:
            raise ValueError(f"y0 dict invalide : {y0_raw} — {e}")

    raise TypeError(
        f"y0 de type inattendu : {type(y0_raw).__name__}. "
        "Attendu : liste [S,L,C,I] ou dict {S,L,C,I}."
    )


# ── INJECTION theta_C / theta_I (ARCH-014) ───────────────────────────────────

def _inject_theta(p: dict, config: dict) -> dict:
    """
    Injecte theta_C et theta_I dans le dict de paramètres p.

    Priorité (du plus fort au plus faible) :
      1. config['params']['theta_C']  (déjà dans p si fourni par Nœud 1 V6.2 Fortifié)
      2. config['theta_C']            (racine de runner_config — Nœud 1 v1.x)
      3. Défaut 0.30 / 0.22

    ARCH-014 : Dans v1.x, le Nœud 1 plaçait theta_C/I à la RACINE de runner_config
    mais run_wp() les transmettait à simulate() via config['params'] (dict p).
    Si theta_C n'était pas dans params, simulate() lisait p.get('theta_C', 0.30)
    et obtenait toujours 0.30 — les valeurs personnalisées étaient silencieusement
    ignorées. Cette fonction garantit la propagation dans tous les cas.
    """
    p_out = dict(p)
    # theta_C
    if 'theta_C' not in p_out or p_out.get('theta_C') is None:
        p_out['theta_C'] = float(
            config.get('params', {}).get('theta_C')
            or config.get('theta_C')
            or 0.30
        )
    # theta_I
    if 'theta_I' not in p_out or p_out.get('theta_I') is None:
        p_out['theta_I'] = float(
            config.get('params', {}).get('theta_I')
            or config.get('theta_I')
            or 0.22
        )
    return p_out


# ── RÉTROCOMPATIBILITÉ : normalisation clé 'g' → 'gamma' (D6) ────────────────

def _normalize_cmd(cmd: dict) -> dict:
    """
    Normalise un dict de commandes pour garantir la présence de 'gamma'.

    V6.2 : la clé officielle est 'gamma'. Si une ancienne fiche utilise 'g',
    conversion automatique avec avertissement stderr.

    La variable interne gC (utilisée dans _step pour C/(C+ε)) est distincte
    et n'est PAS affectée par cette normalisation.
    """
    cmd_out = dict(cmd)
    if 'gamma' not in cmd_out:
        if 'g' in cmd_out:
            print(
                "[MEPA V6.2 WARNING] Clé 'g' détectée dans cmd — "
                "conversion automatique vers 'gamma' (D6). "
                "Mettre à jour la fiche source pour conformité V6.2.",
                file=sys.stderr
            )
            cmd_out['gamma'] = cmd_out.pop('g')
        else:
            raise KeyError(
                "Clé 'gamma' manquante dans cmd. "
                "V6.2 exige 'gamma' (capacité organisationnelle γ de l'élite). "
                "Ancienne clé 'g' acceptée par rétrocompatibilité."
            )
    elif 'g' in cmd_out:
        print(
            "[MEPA V6.2 WARNING] 'g' et 'gamma' présents simultanément — "
            f"'gamma'={cmd_out['gamma']} utilisé, 'g' ignoré.",
            file=sys.stderr
        )
        cmd_out.pop('g')
    return cmd_out


# ── ÉQUATIONS DIFFÉRENTIELLES (Euler explicite, dt=1) — INCHANGÉES ───────────

def _step(S, L, C, I, cmd, p):
    """
    Un pas Euler dt=1. Retourne (S_new, L_new, C_new, I_new).

    Nomenclature V6.2 :
      cmd['gamma'] = γ — capacité organisationnelle de l'élite [0,1]
                        utilisée dans F(t), PAS dans _step directement.
      gC           = C / (C + ε) — variable interne de saturation,
                        distincte de γ, inchangée par D6. NE PAS RENOMMER.
    """
    T    = cmd['T']
    Mob  = cmd['Mob']
    R    = cmd['R']
    Ref  = cmd['Ref']
    Rc   = cmd['Rc']
    Rn   = cmd['Rn']
    E    = cmd['E']
    EROI = cmd['EROI']
    Pop  = cmd.get('Pop', 1.0)

    ell   = R / (R + p['p13'])
    # gC : variable interne de saturation de C — DISTINCTE de γ (gamma).
    # Ne pas renommer. Représente C/(C+ε) pour éviter la division par zéro.
    gC    = max(C, 0.0) / (max(C, 0.0) + EPS)
    Theta = 1.0 / (1.0 + math.exp(-K_SIG * (C - CC)))
    denom = max(1.0 + p['p11a']*ell*Rc + p['p11b']*ell*Rn*(1.0 - KAPPA*C), 0.01)
    M     = p['p10'] * (1.0 + A_COEF*E) * max(L, 0.0) / denom

    dS = p['p1']*T  - p['p2']*(R + Ref + Mob) - p['p2b']*S
    dL = p['p4']*S  - L - p['p3']*L*Theta
    dC = p['p5']*M  - p['p6']*C - p['p7']*(Rc + Rn)*ell*gC
    dI = p['p8']*(EROI - 1.0)*Pop - p['p9']*I

    return (
        S + dS,
        L + dL,
        C + dC,
        max(I_MIN, I + dI),
    )


def F_val(S, L, C, I, cmd, p):
    """
    F(t) = C + λ×L×(1 + μ×γ×E)
    D6 : cmd['gamma'] remplace cmd['g'].
    """
    return (
        max(C, 0.0)
        + p['lam'] * max(L, 0.0) * (1.0 + p['mu'] * cmd['gamma'] * cmd['E'])
    )


def R_val(S, L, C, I, cmd, p):
    """R(t) = I^(1/3) + ν×(Rc+Rn)×ℓ + ρ"""
    ell = cmd['R'] / (cmd['R'] + p['p13'])
    return max(I, 0.0)**0.3333 + p['nu']*(cmd['Rc'] + cmd['Rn'])*ell + p['rho']


# ── SIMULATION PRINCIPALE — INCHANGÉE ────────────────────────────────────────

def simulate(p: dict, cmd_fn: Callable, y0: list, t_max: int) -> dict:
    """
    Simulation Euler explicite dt=1 de t=0 à t=t_max.

    y0 = [S0, L0, C0, I0]  — doit être une LISTE (garantie par _normalize_y0)
    cmd_fn(t) → dict avec T, Mob, R, Ref, Rc, Rn, E, gamma, EROI, Pop.

    theta_C et theta_I lus depuis p (garantis présents par _inject_theta).
    """
    S, L, C, I = float(y0[0]), float(y0[1]), float(y0[2]), float(y0[3])
    theta_C = p.get('theta_C', 0.30)
    theta_I = p.get('theta_I', 0.22)

    ts = list(range(t_max + 1))
    Ss, Ls, Cs, Is = [S], [L], [C], [I]
    Fs, Rs = [], []
    cmd0 = _normalize_cmd(cmd_fn(0))
    Fs.append(F_val(S, L, C, I, cmd0, p))
    Rs.append(R_val(S, L, C, I, cmd0, p))

    for t in range(1, t_max + 1):
        cmd = _normalize_cmd(cmd_fn(t))
        S, L, C, I = _step(S, L, C, I, cmd, p)
        Ss.append(S); Ls.append(L); Cs.append(C); Is.append(I)
        Fs.append(F_val(S, L, C, I, cmd, p))
        Rs.append(R_val(S, L, C, I, cmd, p))

    FR = [f / max(r, 1e-9) for f, r in zip(Fs, Rs)]

    idx_tb = next((i for i in range(len(ts)) if Fs[i] >= Rs[i]), None)

    if idx_tb is None:
        cmd_fin = _normalize_cmd(cmd_fn(t_max))
        if cmd_fin['Rn'] + cmd_fin['Rc'] > 0.6:
            traj = '(b) Répression réussie'
        else:
            traj = '(h)/(e) Stabilité ou réforme lente'
        return _build_result(traj, None, None, None, None, None,
                             Ss, Ls, Cs, Is, Fs, Rs, FR, ts, theta_C, theta_I)

    idx_t0 = next((i for i in range(idx_tb) if FR[i] > _get_seuil_fr()), 0)

    C0 = max(Cs[idx_t0], 1e-9)
    I0 = max(Is[idx_t0], 1e-9)
    Cb = max(Cs[idx_tb], 0.0)
    Ib = max(Is[idx_tb], 0.0)

    dC_rel = (Cb - C0) / C0
    dI_rel = (I0 - Ib) / I0
    dCdt   = Cs[idx_tb] - Cs[idx_tb - 1] if idx_tb > 0 else 0.0

    cmd_tb = _normalize_cmd(cmd_fn(ts[idx_tb]))
    if dI_rel > theta_I and dC_rel < theta_C and dCdt < 0.02:
        traj = '(d) Effondrement progressif'
    elif dC_rel > theta_C and dCdt > 0:
        if cmd_tb.get('Ref', 0) > 0.35 and (cmd_tb['Rc'] + cmd_tb['Rn']) < 0.35:
            traj = '(e) Réforme institutionnelle'
        else:
            traj = '(a) Rupture transformatrice'
    else:
        traj = '(c) Stase / ambigu'
    # Note D4 : le label '(γ) Transformation forcée' (8e label officiel) ne peut pas être
    # déterminé automatiquement par l'arbre de décision MEPA Lite — il requiert un G exogène
    # fort documenté par le codeur (CONV-E / MEPA Full). Il est produit par override via
    # config.get('trajectoire_forcee') dans run_wp() si le codeur l'a explicitement défini.

    return _build_result(traj, idx_tb, dC_rel, dI_rel, dCdt,
                         Fs[idx_tb] / max(Rs[idx_tb], 1e-9),
                         Ss, Ls, Cs, Is, Fs, Rs, FR, ts, theta_C, theta_I)


def _build_result(traj, idx_tb, dC_rel, dI_rel, dCdt, FR_tb,
                  Ss, Ls, Cs, Is, Fs, Rs, FR, ts, theta_C, theta_I):
    """Construit le dict de résultats normalisé. INCHANGÉ vs v1.x."""
    return dict(
        traj             = traj,
        t_bascule        = ts[idx_tb] if idx_tb is not None else None,
        dC_rel           = round(dC_rel, 4) if dC_rel is not None else None,
        dI_rel           = round(dI_rel, 4) if dI_rel is not None else None,
        dCdt_bascule     = round(dCdt, 6)   if dCdt is not None else None,
        FR_bascule       = round(FR_tb, 4)  if FR_tb is not None else None,
        F_bascule        = round(Fs[idx_tb], 4) if idx_tb is not None else None,
        R_bascule        = round(Rs[idx_tb], 4) if idx_tb is not None else None,
        FR_max           = round(max(FR), 4),
        FR_final         = round(FR[-1], 4),
        I_min_sim        = round(min(Is), 4),
        I_final          = round(Is[-1], 4),
        C_max            = round(max(Cs), 4),
        C_final          = round(Cs[-1], 4),
        S_final          = round(Ss[-1], 4),
        L_final          = round(Ls[-1], 4),
        theta_C_used     = theta_C,
        theta_I_used     = theta_I,
        tableau_S2       = _tableau_s2(ts, Ss, Ls, Cs, Is, Fs, Rs, idx_tb),
    )


def _tableau_s2(ts, Ss, Ls, Cs, Is, Fs, Rs, idx_tb):
    """Points du tableau S2. INCHANGÉ vs v1.x."""
    t_max_local = ts[-1]
    pts = set([0, 25, 50, 75, 100])
    for t in range(150, t_max_local + 1, 50):
        pts.add(t)
    if idx_tb is not None:
        pts.add(ts[idx_tb])
    pts.add(t_max_local)
    pts = sorted(pt for pt in pts if pt <= t_max_local)

    rows = []
    for t in pts:
        rows.append(dict(
            t=t,
            S=round(Ss[t], 4), L=round(Ls[t], 4),
            C=round(Cs[t], 4), I=round(Is[t], 4),
            F=round(Fs[t], 4), R=round(Rs[t], 4),
            FR=round(Fs[t] / max(Rs[t], 1e-9), 4),
            note='← bascule' if idx_tb is not None and t == ts[idx_tb] else '',
        ))
    return rows


# ── SA MODULATEUR — INCHANGÉ ──────────────────────────────────────────────────

def apply_sa_modulator(p: dict, sa: int) -> dict:
    """
    Modulateur Sa : Sa=7 → p6 × 1.5.
    Valeurs valides : {2, 4, 6, 7}. INCHANGÉ vs v1.x.
    """
    if sa not in (2, 4, 6, 7):
        raise ValueError(f"Sa={sa} invalide — valeurs autorisées : 2, 4, 6, 7.")
    p_out = dict(p)
    if sa == 7:
        p_out['p6']       = p['p6'] * 1.5
        p_out['_sa_note'] = "p6 × 1.5 (Sa=7 famille souche)"
    else:
        p_out['_sa_note'] = f"p6 nominal (Sa={sa})"
    return p_out


# ── STRESS-TEST — INCHANGÉ ────────────────────────────────────────────────────

def stress_test(p: dict, cmd_fn: Callable, y0: list, t_max: int,
                perturbations: list) -> list:
    """N1 individuel. INCHANGÉ vs v1.x."""
    results = []
    for label, fn_pert in perturbations:
        res = simulate(p, fn_pert, y0, t_max)
        results.append({'label': label, 'traj': res['traj'],
                        'dC_rel': res['dC_rel'], 'dI_rel': res['dI_rel']})
    return results


# ── COMMANDES DYNAMIQUES — INCHANGÉ ──────────────────────────────────────────

def make_cmd_linear(cmd_base: dict, linear: dict, t_max: int) -> Callable:
    """
    Construit cmd_fn pour EROI (et T) dynamiques linéaires.
    INCHANGÉ vs v1.x.
    """
    cmd_base_norm = _normalize_cmd(cmd_base)

    def cmd_fn(t):
        c = dict(cmd_base_norm)
        for var, rng in linear.items():
            val = rng['start'] + (rng['end'] - rng['start']) * (t / max(t_max, 1))
            if var == 'EROI':
                val = max(val, 1.01)
            c[var] = val
        return c
    return cmd_fn


# ── POINT D'ENTRÉE PRINCIPAL ──────────────────────────────────────────────────

def run_wp(config: dict) -> dict:
    """
    Lance simulation complète + stress-tests N1+N2 pour un WP.

    Ajouts V2.0 (non-disruptifs) :
      A1 — Garde-fou NC : vérifie cmd avant simulation. NC bloquant (gamma, EROI)
           → RuntimeError descriptif. NC non bloquant → warning stderr.
      A2 — _normalize_y0() : y0 dict → liste [S,L,C,I]. (ARCH-013)
      A3 — _inject_theta() : theta_C/I injectés dans p depuis config. (ARCH-014)
      A4 — Champs additionnels dans meta : nc_bloquantes, nc_non_bloquantes,
           statut_nc, runner_version_v2.

    Config JSON V6.2 attendue :
    {
      "wp_id": "WP-C1-1",
      "cas": "Haïti — Crise post-séisme 2010-2024",
      "cluster": "C1",
      "trajectoire_attendue": "(d) Dissolution",
      "sa": 4,
      "y0": [1.5, 0.2, 0.05, 1.5],  ← liste OU dict {S,L,C,I} (ARCH-013)
      "t_max": 300,
      "theta_C": 0.30,               ← racine OU dans params (ARCH-014)
      "theta_I": 0.22,
      "cmd_linear": {"EROI": {"start": 1.2, "end": 2.0}},  ← C1 obligatoire
      "cmd": {
        "T":1.2, "Mob":0.10, "R":0.15, "Ref":0.05,
        "Rc":0.60, "Rn":0.00, "E":0.70,
        "gamma":0.25,                ← V6.2 : 'gamma' remplace 'g'
        "EROI":1.5, "Pop":1.0
      },
      "params": {
        "p1":0.08, ..., "lam":0.68, ...,
        "theta_C":0.30, "theta_I":0.22   ← ici OU à la racine (ARCH-014)
      }
    }

    Rétrocompatibilité :
      - cmd['g'] → converti en 'gamma' par _normalize_cmd() avec warning.
      - y0 dict  → converti en liste par _normalize_y0() avec info stderr.
      - theta_C/I absents de params → lus depuis config racine ou défaut 0.30/0.22.
    """
    # ── Validation de base ────────────────────────────────────────────────────
    sa = config.get('sa')
    if sa is None:
        raise ValueError("Champ 'sa' manquant dans la config. Obligatoire : {2,4,6,7}.")

    # ── A2 : Normalisation y0 dict → liste (ARCH-013) ─────────────────────────
    y0_raw = config.get('y0')
    if y0_raw is None:
        raise ValueError("Champ 'y0' manquant dans la config.")
    y0 = _normalize_y0(y0_raw)

    # ── A1 : Garde-fou NC sur cmd (JAMAIS de NaN silencieux) ──────────────────
    cmd_raw = config.get('cmd', {})
    nc_bloquantes_cmd, nc_non_bloquantes_cmd = _detect_nc_in_cmd(cmd_raw)

    if nc_bloquantes_cmd:
        raise RuntimeError(
            f"[GARDE-FOU NC] run_wp() : variable(s) NC bloquante(s) dans cmd : "
            f"{nc_bloquantes_cmd}. "
            f"La simulation est impossible sans valeur numérique pour ces variables. "
            f"Le pipeline doit s'arrêter en C13 (Node 2) avant d'atteindre le runner. "
            f"Vérifier que mepa_node2_audit_v62.js v2.0 est déployé."
        )

    if nc_non_bloquantes_cmd:
        print(
            f"[MEPA V6.2 WARNING] Variables NC non bloquantes dans cmd : "
            f"{nc_non_bloquantes_cmd}. "
            f"Simulation lancée avec valeurs de fallback pour ces variables.",
            file=sys.stderr
        )
        # Remplacer les NC non bloquants par des valeurs de fallback
        cmd_raw = dict(cmd_raw)
        fallbacks = {
            'T': 0.5, 'Mob': 0.3, 'R': 0.3, 'Ref': 0.10,
            'Rc': 0.2, 'Rn': 0.1, 'E': 0.3, 'Pop': 1.0,
        }
        for k in nc_non_bloquantes_cmd:
            cmd_raw[k] = fallbacks.get(k, 0.3)
            print(
                f"  → cmd.{k} = NC remplacé par fallback {cmd_raw[k]}",
                file=sys.stderr
            )

    # ── A3 : Application Sa + injection theta_C/I (ARCH-014) ──────────────────
    params_raw = config.get('params', {})
    p = apply_sa_modulator(params_raw, int(sa))
    p = _inject_theta(p, config)   # ARCH-014 : garantit theta_C/I dans p

    t_max    = int(config.get('t_max', 300))
    cmd_base = cmd_raw
    linear   = config.get('cmd_linear') or {}

    cmd_fn = make_cmd_linear(cmd_base, linear, t_max) if linear else (
        lambda t, _c=_normalize_cmd(cmd_base): _c
    )

    # ── Simulation principale ──────────────────────────────────────────────────
    res = simulate(p, cmd_fn, y0, t_max)

    # ── Override trajectoire pour (γ) Transformation forcée (D4 — 8e label) ───
    # Le label (γ) ne peut pas être inféré automatiquement par l'arbre MEPA Lite.
    # Si config['trajectoire_forcee'] = '(γ) Transformation forcée', le runner
    # remplace la trajectoire diagnostiquée par l'override du codeur.
    # Ceci s'applique uniquement aux WP T1 (Sécession) et I5 (Espagne) dans V6.2.
    _traj_forcee = config.get('trajectoire_forcee')
    _LABELS_D4_VALIDES = {
        '(a) Rupture transformatrice', '(b) Répression réussie',
        '(c) Stase / ambigu', '(d) Effondrement progressif',
        '(d) Dissolution',              # 9e label — Manuel Gouvernance Annexe A (BUG-007)
                                        # Conditions : F≥R, Ref>0.35, Rc+Rn<0.35
                                        # Non produit par l'arbre automatique — LOI PHYSIQUE 3 passes
        '(e) Réforme institutionnelle',
        '(h) Stabilité',
        '(h)/(e) Stabilité ou réforme lente',
        '(γ) Transformation forcée',    # 8e label officiel D4
    }
    if _traj_forcee is not None:
        if _traj_forcee not in _LABELS_D4_VALIDES:
            raise ValueError(
                f"[D4] trajectoire_forcee='{_traj_forcee}' non conforme. "
                f"Valeurs valides : {sorted(_LABELS_D4_VALIDES)}"
            )
        _traj_auto = res['traj']
        res = dict(res)
        res['traj'] = _traj_forcee
        res['traj_auto_avant_override'] = _traj_auto
        print(
            f"[MEPA V6.2 INFO] trajectoire_forcee='{_traj_forcee}' appliqué ",
            f"(arbre auto : '{_traj_auto}'). Documenter en S3.",
            file=sys.stderr
        )

    # ── Stress-test N1 (Étape D) ───────────────────────────────────────────────
    cmd_base_norm = _normalize_cmd(cmd_base)

    def mk_fn(E_delta, R_delta):
        c2 = dict(cmd_base_norm)
        c2['E'] = max(0.0, cmd_base_norm['E'] + E_delta)
        c2['R'] = max(0.0, cmd_base_norm['R'] + R_delta)
        return make_cmd_linear(c2, linear, t_max) if linear else (lambda t, _c=c2: _c)

    fn_opt   = mk_fn(-0.08, +0.08)
    fn_pes   = mk_fn(+0.08, -0.08)
    res_opt  = simulate(p, fn_opt, y0, t_max)
    res_pes  = simulate(p, fn_pes, y0, t_max)

    trajs      = {res['traj'], res_opt['traj'], res_pes['traj']}
    robustesse = 'ROBUSTE' if len(trajs) == 1 else 'MÉTASTABLE'

    # ── Stress N2 : sensibilité individuelle ───────────────────────────────────
    stress_n2 = []
    for var, delta in [('E', 0.10), ('R', 0.08), ('EROI', 0.50), ('Rc', 0.10)]:
        for sign, lbl in [(+1, f'{var}+{delta}'), (-1, f'{var}-{delta}')]:
            c2 = dict(cmd_base_norm)
            c2[var] = max(0.0, cmd_base_norm.get(var, 0.0) + sign * delta)
            if var == 'EROI':
                c2[var] = max(1.01, c2[var])
            fn2 = make_cmd_linear(c2, linear, t_max) if linear else (lambda t, _c=c2: _c)
            r2  = simulate(p, fn2, y0, t_max)
            stress_n2.append({
                'label': lbl, 'traj': r2['traj'],
                'dC_rel': r2['dC_rel'], 'dI_rel': r2['dI_rel'],
            })

    # ── Résultat complet ───────────────────────────────────────────────────────
    return {
        'meta': {
            'wp_id'               : config.get('wp_id', '?'),
            'cas'                 : config.get('cas', ''),
            'cluster'             : config.get('cluster', ''),
            'trajectoire_attendue': config.get('trajectoire_attendue', ''),
            'sa'                  : sa,
            'sa_modulator'        : p.get('_sa_note', ''),
            'cmd_type'            : 'linear_dynamic' if linear else 'static',
            'integration'         : 'Euler_explicite_dt1',
            'nomenclature'        : 'V6.2-gamma (cmd["gamma"] = γ)',
            'runner_version'      : 'mepa_runner_v2_gamma_v2.1.1',
            'generated_at'        : datetime.datetime.now(datetime.timezone.utc).isoformat(),
            # A4 : champs NC additionnels
            'nc_bloquantes'       : nc_bloquantes_cmd,
            'nc_non_bloquantes'   : nc_non_bloquantes_cmd,
            'statut_nc'           : (
                'DONNÉES_INSUFFISANTES' if nc_bloquantes_cmd
                else ('NC_WARNINGS' if nc_non_bloquantes_cmd else 'OK')
            ),
            # A3 : trace theta effectifs
            'theta_C_effectif'    : p.get('theta_C', 0.30),
            'theta_I_effectif'    : p.get('theta_I', 0.22),
            # A2 : trace y0 normalisé
            'y0_normalise'        : y0,
        },
        'simulation' : res,
        'stress_n1'  : {
            'optimiste' : {
                'traj': res_opt['traj'],
                'dC_rel': res_opt['dC_rel'],
                'dI_rel': res_opt['dI_rel'],
            },
            'pessimiste': {
                'traj': res_pes['traj'],
                'dC_rel': res_pes['dC_rel'],
                'dI_rel': res_pes['dI_rel'],
            },
        },
        'stress_n2'  : stress_n2,
        'verdict'    : {
            'robustesse'          : robustesse,
            'trajectoire_diagn'   : res['traj'],
            'concordance_attendue': res['traj'] == config.get('trajectoire_attendue', res['traj']),
            'trajs_set_n1'        : sorted(trajs),
        },
        'params'     : {k: v for k, v in p.items() if not k.startswith('_')},
        'cmd_base'   : cmd_base_norm,
        'cmd_linear' : linear,
        'y0'         : y0,
        't_max'      : t_max,
    }


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage : python3 mepa_runner_v2_gamma.py config_wp.json [result_out.json]")
        print()
        print("  config_wp.json  : runner_config produit par mepa_node2_audit_v62.js")
        print("  result_out.json : optionnel — si absent, remplace l'extension .json")
        print()
        print("Corrections V2.0 vs V1.x :")
        print("  [ARCH-013] y0 dict → liste [S,L,C,I] normalisé automatiquement")
        print("  [ARCH-014] theta_C/I injectés depuis racine config si absents de params")
        print("  [ARCH-015] Chemin runner via MEPA_SCRIPTS_DIR (défaut /data/mepa/scripts/)")
        print("  [NC]       Garde-fou : NC bloquant → RuntimeError (jamais NaN silencieux)")
        sys.exit(1)

    config_path = sys.argv[1]
    with open(config_path) as f:
        config = json.load(f)

    result = run_wp(config)

    # Chemin de sortie
    if len(sys.argv) >= 3:
        out_path = sys.argv[2]
    else:
        out_path = config_path.replace('_runner_config.json', '_result.json')
        if out_path == config_path:
            out_path = config_path.replace('.json', '_result.json')

    with open(out_path, 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    sim = result['simulation']
    vrd = result['verdict']
    meta = result['meta']
    print(f"✓  {out_path}")
    print(f"   Trajectoire    : {sim['traj']}")
    print(f"   t_bascule      : {sim['t_bascule']}")
    print(f"   ΔC_rel         : {sim['dC_rel']}  |  ΔI_rel : {sim['dI_rel']}")
    print(f"   Robustesse     : {vrd['robustesse']}")
    print(f"   Concordance    : {'✓' if vrd['concordance_attendue'] else '✗ DIVERGENCE'}")
    print(f"   theta_C eff.   : {meta['theta_C_effectif']}  |  theta_I eff. : {meta['theta_I_effectif']}")
    print(f"   Intégration    : {meta['integration']}")
    print(f"   Runner version : {meta['runner_version']}")
    if meta['nc_non_bloquantes']:
        print(f"   ⚠ NC non-bloquantes : {meta['nc_non_bloquantes']}")
