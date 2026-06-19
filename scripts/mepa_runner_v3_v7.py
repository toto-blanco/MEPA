#!/usr/bin/env python3
"""
================================================================================
MEPA V7-α rev. 2.1 — Runner V3-V7 (LSODA)
================================================================================
Statut           : NOUVEAU V7
Cible            : /data/mepa/scripts/mepa_runner_v3_v7.py
Rétrocompatibilité :
    - Équations différentielles (_step_euler, F_val, R_val) : INCHANGÉES au bit
      près par rapport au runner V2-gamma V6.2. La fonction _step_euler() est
      conservée pour les tests de non-régression T1-T5.
    - Le nouvel intégrateur LSODA (scipy.integrate.solve_ivp) produit des
      résultats équivalents à Euler dt=1 dans la tolérance T1-T5 :
        T1 : t_bascule ±5 pas
        T2 : C_max ±5%
        T3 : chute_I ±3%
        T4 : FR_max ±5%
        T5 : diagnostic catégoriel identique (si pas de branches V7 actives)
    - Mêmes clés de sortie JSON que V6.2, plus les champs V7 additionnels.

Version          : 3.0.0
MEPA version     : 7.0-alpha rev. 2.1
Dépendances      : json, sys, datetime, math, os, warnings (stdlib)
                   numpy, scipy (LSODA via solve_ivp)

================================================================================

Ajouts V3.0.0 vs V2.1.1 :
──────────────────────────

[V7-R1] Intégrateur LSODA — scipy.integrate.solve_ivp method='LSODA'
        rtol=1e-6, atol=1e-9, t_eval=arange(0, t_max+1, 1).
        Remplace Euler dt=1 pour la simulation principale.
        _step_euler() conservée pour les tests de non-régression.

[V7-R2] Précheck conditions C1-C4 de la branche (α) Cristallisation sacrificielle.
        Si les 4 conditions sont satisfaites, la rampe mod_mimétique est activée.

[V7-R3] Rampe mod_mimétique en trois phases — module p6 dynamiquement :
        Phase 1 (incubation)   : p6 × 0.50 pendant 22 pas
        Phase 2 (décharge)     : p6 × 2.50 pendant 7 pas
        Phase 3 (stabilisation): p6 × 1.15 pendant 30 pas
        Puis retour nominal.

[V7-R4] Arbre de décision V7 étendu — ordre de priorité :
        1. (α) si C1-C5 satisfaites (précheck + C_max post-sim)
        2. Bascule F≥R → (a), (e), (d) V6.2, (c)
        3. (b) EXPLICATIVE V7-C4 (C_max>0.12, chute_C>0.20, Cs∈[0.10,0.50])
        4. (d) V7-C2 sans bascule (chute_I>0.5, FR_max<1.2, excl. b expl)
        5. Fallback CATCHALL V6.2 ((b) catchall, (h)/(e) catchall)

[V7-R5] Annotation EXPLICATIVE/CATCHALL dans simulation.branche_annotation.

[V7-R6] Génération du rapport de non-régression T1-T5 si le cas a une
        validation V6.2 (params_p.$validation_v62) dans le runner_config.

[V7-R7] Clause de repli A_r_c_eff = A_r_c + 0.5 × A_r_ne pour C4.

[V7-R8] Champs V7 dans le résultat : v7_alpha_diagnostic, branche_annotation,
        a_r_c_eff_calc, chute_C_metric, rampe_mod_mimetique_active, integrator.

Usage :
    python3 mepa_runner_v3_v7.py config_wp.json [result_out.json]
"""

import json, sys, datetime, math, os, warnings
from typing import Callable, Optional, Dict, Any

import numpy as np
from scipy.integrate import solve_ivp

# ── Chemin canonique Pi5 ─────────────────────────────────────────────────────
MEPA_SCRIPTS_DIR = os.environ.get("MEPA_SCRIPTS_DIR", "/data/mepa/scripts")

# ── CONSTANTES FIXES (identiques V6.2 au bit près) ──────────────────────────
KAPPA    = 0.10
A_COEF   = 1.0
CC       = 0.50
I_MIN    = 0.30
K_SIG    = 10.0
EPS      = 1e-6
SEUIL_FR            = None
_SEUIL_FR_FALLBACK  = 0.75

# ── NC ───────────────────────────────────────────────────────────────────────
NC_SENTINEL   = "NC"
NC_BLOQUANTES_RUNNER = frozenset({"gamma", "EROI"})
NC_NON_BLOQUANTES_RUNNER = frozenset({"E", "T", "Mob", "R", "Ref", "Rc", "Rn", "Pop"})

# ── LABELS D4 V7 (10 labels) ────────────────────────────────────────────────
_LABELS_D4_V7 = {
    "(a) Rupture transformatrice",
    "(α) Cristallisation sacrificielle d'État",
    "(b) Répression réussie",
    "(c) Stase / ambigu",
    "(d) Effondrement progressif",
    "(d) Dissolution",
    "(e) Réforme institutionnelle",
    "(h) Stabilité",
    "(h)/(e) Stabilité ou réforme lente",
    "(γ) Transformation forcée",
}

# ── ANNOTATION BRANCHES ──────────────────────────────────────────────────────
_BRANCH_ANNOTATION = {
    "(α) Cristallisation sacrificielle d'État": "EXPLICATIVE",
    "(a) Rupture transformatrice":              "EXPLICATIVE",
    "(b) Répression réussie":                   "CATCHALL",
    "(b) Répression réussie — EXPLICATIVE":     "EXPLICATIVE",
    "(c) Stase / ambigu":                       "EXPLICATIVE",
    "(d) Effondrement progressif":              "EXPLICATIVE",
    "(d) Dissolution":                          "EXPLICATIVE",
    "(e) Réforme institutionnelle":             "EXPLICATIVE",
    "(h) Stabilité":                            "CATCHALL",
    "(h)/(e) Stabilité ou réforme lente":       "CATCHALL",
    "(γ) Transformation forcée":                "EXPLICATIVE",
}


# ── CHARGEMENT mepa_constants.json ───────────────────────────────────────────

def _charger_constants() -> dict:
    try:
        path = os.path.join(MEPA_SCRIPTS_DIR, "mepa_constants.json")
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {
            "nc_protocol": {
                "valeur_sentinel": "NC",
                "variables_nc_bloquantes": ["E_split", "gamma", "EROI", "Sa",
                                            "psi_noyau", "gamma_local"],
            },
            "hyperparametres_v7_alpha_rev2_1": {
                "trajectoire_alpha": {
                    "mu_m_etoile": {"valeur": 0.60},
                    "sigma_base": {"valeur": 0.018},
                    "alpha_phi": {"valeur": 1.7},
                    "theta_C_alpha": {"valeur": 0.30},
                    "coefficient_a_r_c_eff": {"valeur": 0.5},
                },
                "rampe_mod_mimetique": {
                    "phase_1_incubation": {"duree_par_defaut": 22, "modulateur_p6": 0.50},
                    "phase_2_decharge": {"duree_par_defaut": 7, "modulateur_p6": 2.50},
                    "phase_3_stabilisation": {"duree_par_defaut": 30, "modulateur_p6": 1.15},
                },
                "branche_b_explicative": {
                    "seuil_c_max": {"valeur": 0.12},
                    "seuil_chute_c": {"valeur": 0.20},
                    "intervalle_cs_valide": {"min": 0.10, "max": 0.50},
                },
                "branche_d_v7_c2": {
                    "seuil_chute_i": {"valeur": 0.5},
                    "seuil_fr_max": {"valeur": 1.2},
                },
            },
        }


_CONSTANTS = None


def _get_constants() -> dict:
    global _CONSTANTS
    if _CONSTANTS is None:
        _CONSTANTS = _charger_constants()
    return _CONSTANTS


def _get_seuil_fr() -> float:
    global SEUIL_FR
    if SEUIL_FR is not None:
        return SEUIL_FR
    try:
        val = _get_constants()["parametres_simulation"]["theta_FR"]["defaut"]
        SEUIL_FR = float(val)
    except (KeyError, TypeError, ValueError):
        warnings.warn(
            f"[MEPA V7] theta_FR introuvable — fallback={_SEUIL_FR_FALLBACK}",
            RuntimeWarning, stacklevel=2,
        )
        SEUIL_FR = _SEUIL_FR_FALLBACK
    return SEUIL_FR


def _get_hyperparams_v7() -> dict:
    """Charge les hyperparamètres V7-α rev. 2.1."""
    c = _get_constants()
    hp = c.get("hyperparametres_v7_alpha_rev2_1")
    if hp:
        return hp
    # Fallback si clé absente dans constants
    return _charger_constants().get("hyperparametres_v7_alpha_rev2_1", {})


# ── HELPERS ──────────────────────────────────────────────────────────────────

def _is_nc(val) -> bool:
    return isinstance(val, str) and val.strip().upper() == NC_SENTINEL


def _detect_nc_in_cmd(cmd: dict) -> tuple:
    bloquantes     = [k for k, v in cmd.items() if _is_nc(v) and k in NC_BLOQUANTES_RUNNER]
    non_bloquantes = [k for k, v in cmd.items() if _is_nc(v) and k not in NC_BLOQUANTES_RUNNER]
    return bloquantes, non_bloquantes


def _normalize_y0(y0_raw) -> list:
    if isinstance(y0_raw, (list, tuple)):
        if len(y0_raw) < 4:
            raise ValueError(f"y0 trop court : {len(y0_raw)} éléments, 4 attendus.")
        return [float(y0_raw[i]) for i in range(4)]
    if isinstance(y0_raw, dict):
        S = float(y0_raw.get('S', y0_raw.get('S0', 1.0)))
        L = float(y0_raw.get('L', y0_raw.get('L0', 0.5)))
        C = float(y0_raw.get('C', y0_raw.get('C0', 0.1)))
        I = float(y0_raw.get('I', y0_raw.get('I0', 3.5)))
        return [S, L, C, I]
    raise TypeError(f"y0 type inattendu : {type(y0_raw).__name__}")


def _inject_theta(p: dict, config: dict) -> dict:
    p_out = dict(p)
    if 'theta_C' not in p_out or p_out.get('theta_C') is None:
        p_out['theta_C'] = float(
            config.get('params', {}).get('theta_C') or config.get('theta_C') or 0.30
        )
    if 'theta_I' not in p_out or p_out.get('theta_I') is None:
        p_out['theta_I'] = float(
            config.get('params', {}).get('theta_I') or config.get('theta_I') or 0.22
        )
    return p_out


def _normalize_cmd(cmd: dict) -> dict:
    cmd_out = dict(cmd)
    if 'gamma' not in cmd_out:
        if 'g' in cmd_out:
            cmd_out['gamma'] = cmd_out.pop('g')
        else:
            raise KeyError("Clé 'gamma' manquante dans cmd.")
    elif 'g' in cmd_out:
        cmd_out.pop('g')
    return cmd_out


# ── ÉQUATIONS (identiques V6.2 au bit près) ─────────────────────────────────

def _step_euler(S, L, C, I, cmd, p):
    """Un pas Euler dt=1. Conservé pour non-régression T1-T5."""
    T    = cmd['T']; Mob = cmd['Mob']; R = cmd['R']; Ref = cmd['Ref']
    Rc   = cmd['Rc']; Rn = cmd['Rn']; E = cmd['E']
    EROI = cmd['EROI']; Pop = cmd.get('Pop', 1.0)

    ell   = R / (R + p['p13'])
    gC    = max(C, 0.0) / (max(C, 0.0) + EPS)
    Theta = 1.0 / (1.0 + math.exp(-K_SIG * (C - CC)))
    denom = max(1.0 + p['p11a']*ell*Rc + p['p11b']*ell*Rn*(1.0 - KAPPA*C), 0.01)
    M     = p['p10'] * (1.0 + A_COEF*E) * max(L, 0.0) / denom

    dS = p['p1']*T  - p['p2']*(R + Ref + Mob) - p['p2b']*S
    dL = p['p4']*S  - L - p['p3']*L*Theta
    dC = p['p5']*M  - p['p6']*C - p['p7']*(Rc + Rn)*ell*gC
    dI = p['p8']*(EROI - 1.0)*Pop - p['p9']*I

    return (S + dS, L + dL, C + dC, max(I_MIN, I + dI))


def F_val(S, L, C, I, cmd, p):
    """F(t) = C + λ×L×(1 + μ×γ×E)"""
    return max(C, 0.0) + p['lam'] * max(L, 0.0) * (1.0 + p['mu'] * cmd['gamma'] * cmd['E'])


def R_val(S, L, C, I, cmd, p):
    """R(t) = I^(1/3) + ν×(Rc+Rn)×ℓ + ρ"""
    ell = cmd['R'] / (cmd['R'] + p['p13'])
    return max(I, 0.0)**0.3333 + p['nu'] * (cmd['Rc'] + cmd['Rn']) * ell + p['rho']


# ── RAMPE MOD_MIMÉTIQUE V7 ──────────────────────────────────────────────────

def _compute_p6_mod(t: float, p6_base: float, rampe_active: bool, hp: dict) -> float:
    """Calcule p6_effectif au temps t en tenant compte de la rampe V7."""
    if not rampe_active:
        return p6_base

    ramp = hp.get("rampe_mod_mimetique", {})
    ph1_dur = ramp.get("phase_1_incubation", {}).get("duree_par_defaut", 22)
    ph2_dur = ramp.get("phase_2_decharge", {}).get("duree_par_defaut", 7)
    ph3_dur = ramp.get("phase_3_stabilisation", {}).get("duree_par_defaut", 30)
    ph1_mod = ramp.get("phase_1_incubation", {}).get("modulateur_p6", 0.50)
    ph2_mod = ramp.get("phase_2_decharge", {}).get("modulateur_p6", 2.50)
    ph3_mod = ramp.get("phase_3_stabilisation", {}).get("modulateur_p6", 1.15)

    if t < ph1_dur:
        return p6_base * ph1_mod
    elif t < ph1_dur + ph2_dur:
        return p6_base * ph2_mod
    elif t < ph1_dur + ph2_dur + ph3_dur:
        return p6_base * ph3_mod
    else:
        return p6_base


# ── ODE POUR LSODA (dérivées continues) ─────────────────────────────────────

def _ode_system(t, y, cmd_fn, p, p6_base, rampe_active, hp):
    """
    Système d'EDO pour solve_ivp.
    y = [S, L, C, I]
    Retourne [dS, dL, dC, dI]

    [fix/lsoda-cmd-linear] cmd_fn n'est garanti défini qu'aux points entiers.
    LSODA évalue _ode_system à des t fractionnaires intermédiaires : on
    interpole linéairement entre cmd_fn(floor(t)) et cmd_fn(ceil(t)) au lieu
    d'arrondir t, pour éviter la fonction en escalier vue par l'intégrateur
    sur les fiches cmd_linear (EROI dynamique).
    """
    S, L, C, I = y[0], y[1], y[2], y[3]
    t_lo, t_hi = math.floor(t), math.ceil(t)
    cmd_lo = _normalize_cmd(cmd_fn(t_lo))
    if t_hi == t_lo:
        cmd = cmd_lo
    else:
        cmd_hi = _normalize_cmd(cmd_fn(t_hi))
        frac = t - t_lo
        cmd = {k: cmd_lo[k] + (cmd_hi[k] - cmd_lo[k]) * frac for k in cmd_lo}

    T    = cmd['T']; Mob = cmd['Mob']; R = cmd['R']; Ref = cmd['Ref']
    Rc   = cmd['Rc']; Rn = cmd['Rn']; E = cmd['E']
    EROI = cmd['EROI']; Pop = cmd.get('Pop', 1.0)

    ell   = R / (R + p['p13'])
    gC    = max(C, 0.0) / (max(C, 0.0) + EPS)
    Theta = 1.0 / (1.0 + math.exp(-K_SIG * (C - CC)))
    denom = max(1.0 + p['p11a']*ell*Rc + p['p11b']*ell*Rn*(1.0 - KAPPA*C), 0.01)
    M     = p['p10'] * (1.0 + A_COEF*E) * max(L, 0.0) / denom

    p6_eff = _compute_p6_mod(t, p6_base, rampe_active, hp)

    dS = p['p1']*T  - p['p2']*(R + Ref + Mob) - p['p2b']*S
    dL = p['p4']*S  - L - p['p3']*L*Theta
    dC = p['p5']*M  - p6_eff*C - p['p7']*(Rc + Rn)*ell*gC
    dI = p['p8']*(EROI - 1.0)*Pop - p['p9']*I

    return [dS, dL, dC, dI]


# ── SIMULATION LSODA V7-β ────────────────────────────────────────────────────

def simulate_lsoda(p: dict, cmd_fn: Callable, y0: list, t_max: int,
                   rampe_active: bool = False, hp: dict = None) -> dict:
    """
    Simulation via scipy solve_ivp method='LSODA'.
    y0 = [S0, L0, C0, I0], cmd_fn(t) → dict.
    """
    hp = hp or {}
    theta_C = p.get('theta_C', 0.30)
    theta_I = p.get('theta_I', 0.22)
    p6_base = p['p6']

    t_eval = np.arange(0, t_max + 1, 1, dtype=float)
    y0_arr = np.array(y0, dtype=float)

    sol = solve_ivp(
        fun=lambda t, y: _ode_system(t, y, cmd_fn, p, p6_base, rampe_active, hp),
        t_span=(0.0, float(t_max)),
        y0=y0_arr,
        method='LSODA',
        t_eval=t_eval,
        rtol=1e-6,
        atol=1e-9,
    )

    if not sol.success:
        raise RuntimeError(f"LSODA échec : {sol.message}")

    Ss = sol.y[0].tolist()
    Ls = sol.y[1].tolist()
    Cs = sol.y[2].tolist()
    Is_raw = sol.y[3].tolist()
    # Appliquer plancher I_MIN
    Is = [max(I_MIN, v) for v in Is_raw]
    ts = [int(round(t)) for t in sol.t.tolist()]

    # Calculer F, R à chaque pas
    Fs, Rs = [], []
    for i, t in enumerate(ts):
        cmd = _normalize_cmd(cmd_fn(t))
        Fs.append(F_val(Ss[i], Ls[i], Cs[i], Is[i], cmd, p))
        Rs.append(R_val(Ss[i], Ls[i], Cs[i], Is[i], cmd, p))

    FR = [f / max(r, 1e-9) for f, r in zip(Fs, Rs)]

    # Arbre de décision V7 (voir _apply_decision_tree_v7)
    return _apply_decision_tree_v7(
        Ss, Ls, Cs, Is, Fs, Rs, FR, ts, cmd_fn, p, theta_C, theta_I,
        rampe_active, hp, t_max
    )


# ── SIMULATION EULER V6.2 (conservée pour non-régression) ───────────────────

def simulate_euler(p: dict, cmd_fn: Callable, y0: list, t_max: int) -> dict:
    """Simulation Euler dt=1 identique à V6.2. Pour tests T1-T5."""
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
        S, L, C, I = _step_euler(S, L, C, I, cmd, p)
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
    C0v = max(Cs[idx_t0], 1e-9)
    I0v = max(Is[idx_t0], 1e-9)
    Cb  = max(Cs[idx_tb], 0.0)
    Ib  = max(Is[idx_tb], 0.0)
    dC_rel = (Cb - C0v) / C0v
    dI_rel = (I0v - Ib) / I0v
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

    return _build_result(traj, idx_tb, dC_rel, dI_rel, dCdt,
                         Fs[idx_tb] / max(Rs[idx_tb], 1e-9),
                         Ss, Ls, Cs, Is, Fs, Rs, FR, ts, theta_C, theta_I)


# ── ARBRE DE DÉCISION V7 ────────────────────────────────────────────────────

def _apply_decision_tree_v7(Ss, Ls, Cs, Is, Fs, Rs, FR, ts, cmd_fn, p,
                             theta_C, theta_I, rampe_active, hp, t_max):
    """
    Arbre de décision V7-α rev. 2.1 complet.
    Appelé par simulate_lsoda après calcul des trajectoires.
    """
    # Métriques communes
    C_max     = max(Cs)
    C_final   = Cs[-1]
    I_initial = Is[0]
    I_min_sim = min(Is)
    FR_max    = max(FR)

    chute_C = (C_max - C_final) / max(C_max, 1e-9) if C_max > 1e-9 else 0.0
    chute_I = (I_initial - I_min_sim) / max(I_initial, 1e-9) if I_initial > 1e-9 else 0.0

    # Détection bascule
    idx_tb = next((i for i in range(len(ts)) if Fs[i] >= Rs[i]), None)

    # Hyperparamètres V7 pour branches
    hp_b_expl = hp.get("branche_b_explicative", {})
    hp_d_v7c2 = hp.get("branche_d_v7_c2", {})
    seuil_c_max_b   = hp_b_expl.get("seuil_c_max", {}).get("valeur", 0.12)
    seuil_chute_c_b = hp_b_expl.get("seuil_chute_c", {}).get("valeur", 0.20)
    cs_min_b = hp_b_expl.get("intervalle_cs_valide", {}).get("min", 0.10)
    cs_max_b = hp_b_expl.get("intervalle_cs_valide", {}).get("max", 0.50)
    seuil_chute_i_d = hp_d_v7c2.get("seuil_chute_i", {}).get("valeur", 0.5)
    seuil_fr_max_d  = hp_d_v7c2.get("seuil_fr_max", {}).get("valeur", 1.2)

    # Cs depuis les commandes (valeur à t=0)
    cmd0 = _normalize_cmd(cmd_fn(0))
    Cs_cmd = cmd0.get('Rc', 0) + cmd0.get('Rn', 0)  # pour condition (b) expl
    # Note : Cs (crédibilité) n'est pas directement dans les commandes — elle est
    # dans la fiche de codage. On utilise les variables_v7 si disponibles, sinon
    # on considère que la condition Cs est satisfaite par défaut si le précheck
    # du nœud 2 l'a validée. Pour l'arbre de décision V7, la valeur de Cs doit
    # être passée via le runner_config.
    # WORKAROUND : on lit Cs depuis p si injecté par le nœud 2.
    Cs_val = p.get('_cs_value', 0.30)

    # ── 1. Branche (α) — vérification C5 post-simulation ─────────────────────
    hp_alpha = hp.get("trajectoire_alpha", {})
    theta_C_alpha = hp_alpha.get("theta_C_alpha", {}).get("valeur", 0.30)

    if rampe_active and C_max > theta_C_alpha:
        # C5 satisfaite → (α) confirmée
        traj = "(α) Cristallisation sacrificielle d'État"
        annotation = "EXPLICATIVE"
        return _build_result_v7(
            traj, annotation, idx_tb, Ss, Ls, Cs, Is, Fs, Rs, FR, ts,
            theta_C, theta_I, C_max, chute_C, chute_I, rampe_active,
            v7_diagnostic={"alpha_confirmed": True, "C5_C_max": round(C_max, 4),
                           "C5_threshold": theta_C_alpha}
        )

    if rampe_active and C_max <= theta_C_alpha:
        # Rampe active mais C5 échouée — ne pas classer en (α)
        print(f"[V7 INFO] Rampe active mais C5 échoue : C_max={C_max:.4f} <= {theta_C_alpha}",
              file=sys.stderr)

    # ── 2. Bascule F≥R détectée → branches V6.2 ajustées ─────────────────────
    if idx_tb is not None:
        idx_t0 = next((i for i in range(idx_tb) if FR[i] > _get_seuil_fr()), 0)
        C0v = max(Cs[idx_t0], 1e-9)
        I0v = max(Is[idx_t0], 1e-9)
        Cb  = max(Cs[idx_tb], 0.0)
        Ib  = max(Is[idx_tb], 0.0)
        dC_rel = (Cb - C0v) / C0v
        dI_rel = (I0v - Ib) / I0v
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

        annotation = _BRANCH_ANNOTATION.get(traj, "EXPLICATIVE")
        return _build_result_v7(
            traj, annotation, idx_tb, Ss, Ls, Cs, Is, Fs, Rs, FR, ts,
            theta_C, theta_I, C_max, chute_C, chute_I, rampe_active,
            v7_diagnostic={"bascule": True, "dC_rel": round(dC_rel, 4),
                           "dI_rel": round(dI_rel, 4), "dCdt": round(dCdt, 6)}
        )

    # ── 3. Pas de bascule → branches V7 sans bascule ─────────────────────────

    # 3a. Branche (b) EXPLICATIVE V7-C4
    cmd_fin = _normalize_cmd(cmd_fn(t_max))
    Rc_Rn_fin = cmd_fin['Rc'] + cmd_fin['Rn']
    b_expl = (C_max > seuil_c_max_b
              and chute_C > seuil_chute_c_b
              and cs_min_b <= Cs_val <= cs_max_b
              and Rc_Rn_fin > 0.4)
    if b_expl:
        traj = '(b) Répression réussie'
        annotation = "EXPLICATIVE"
        return _build_result_v7(
            traj, annotation, None, Ss, Ls, Cs, Is, Fs, Rs, FR, ts,
            theta_C, theta_I, C_max, chute_C, chute_I, rampe_active,
            v7_diagnostic={"b_explicative": True, "C_max": round(C_max, 4),
                           "chute_C": round(chute_C, 4), "Cs_val": Cs_val,
                           "Rc_Rn": round(Rc_Rn_fin, 4)}
        )

    # 3b. Branche (d) V7-C2 sans bascule
    d_v7c2 = (chute_I > seuil_chute_i_d
              and FR_max < seuil_fr_max_d
              and not b_expl)
    if d_v7c2:
        traj = '(d) Effondrement progressif'
        annotation = "EXPLICATIVE"
        return _build_result_v7(
            traj, annotation, None, Ss, Ls, Cs, Is, Fs, Rs, FR, ts,
            theta_C, theta_I, C_max, chute_C, chute_I, rampe_active,
            v7_diagnostic={"d_v7_c2": True, "chute_I": round(chute_I, 4),
                           "FR_max": round(FR_max, 4)}
        )

    # 3c. Fallback CATCHALL V6.2
    if Rc_Rn_fin > 0.6:
        traj = '(b) Répression réussie'
        annotation = "CATCHALL"
    else:
        traj = '(h)/(e) Stabilité ou réforme lente'
        annotation = "CATCHALL"

    return _build_result_v7(
        traj, annotation, None, Ss, Ls, Cs, Is, Fs, Rs, FR, ts,
        theta_C, theta_I, C_max, chute_C, chute_I, rampe_active,
        v7_diagnostic={"fallback_catchall": True}
    )


# ── CONSTRUCTION RÉSULTAT V7 ────────────────────────────────────────────────

def _build_result(traj, idx_tb, dC_rel, dI_rel, dCdt, FR_tb,
                  Ss, Ls, Cs, Is, Fs, Rs, FR, ts, theta_C, theta_I):
    """Résultat format V6.2 (identique). Utilisé par simulate_euler."""
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


def _build_result_v7(traj, annotation, idx_tb, Ss, Ls, Cs, Is, Fs, Rs, FR, ts,
                      theta_C, theta_I, C_max, chute_C, chute_I, rampe_active,
                      v7_diagnostic=None):
    """Résultat V7 étendu (LSODA + métriques V7)."""
    dC_rel = dI_rel = dCdt = FR_tb = None
    if idx_tb is not None and idx_tb > 0:
        idx_t0 = next((i for i in range(idx_tb) if FR[i] > _get_seuil_fr()), 0)
        C0v = max(Cs[idx_t0], 1e-9)
        I0v = max(Is[idx_t0], 1e-9)
        dC_rel = (max(Cs[idx_tb], 0.0) - C0v) / C0v
        dI_rel = (I0v - max(Is[idx_tb], 0.0)) / I0v
        dCdt   = Cs[idx_tb] - Cs[idx_tb - 1]
        FR_tb  = Fs[idx_tb] / max(Rs[idx_tb], 1e-9)

    return dict(
        traj                        = traj,
        branche_annotation          = annotation,
        t_bascule                   = ts[idx_tb] if idx_tb is not None else None,
        dC_rel                      = round(dC_rel, 4) if dC_rel is not None else None,
        dI_rel                      = round(dI_rel, 4) if dI_rel is not None else None,
        dCdt_bascule                = round(dCdt, 6)   if dCdt is not None else None,
        FR_bascule                  = round(FR_tb, 4)  if FR_tb is not None else None,
        F_bascule                   = round(Fs[idx_tb], 4) if idx_tb is not None else None,
        R_bascule                   = round(Rs[idx_tb], 4) if idx_tb is not None else None,
        FR_max                      = round(max(FR), 4),
        FR_final                    = round(FR[-1], 4),
        I_min_sim                   = round(min(Is), 4),
        I_final                     = round(Is[-1], 4),
        C_max                       = round(C_max, 4),
        C_final                     = round(Cs[-1], 4),
        S_final                     = round(Ss[-1], 4),
        L_final                     = round(Ls[-1], 4),
        theta_C_used                = theta_C,
        theta_I_used                = theta_I,
        tableau_S2                  = _tableau_s2(ts, Ss, Ls, Cs, Is, Fs, Rs, idx_tb),
        # ── V7 champs additionnels ───
        v7_alpha_diagnostic         = v7_diagnostic or {},
        rampe_mod_mimetique_active  = rampe_active,
        chute_C_metric              = round(chute_C, 4),
        chute_I_metric              = round(chute_I, 4),
        integrator                  = "LSODA",
    )


def _tableau_s2(ts, Ss, Ls, Cs, Is, Fs, Rs, idx_tb):
    """Points du tableau S2 (identique V6.2)."""
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
        if t < len(Ss):
            rows.append(dict(
                t=t, S=round(Ss[t], 4), L=round(Ls[t], 4),
                C=round(Cs[t], 4), I=round(Is[t], 4),
                F=round(Fs[t], 4), R=round(Rs[t], 4),
                FR=round(Fs[t] / max(Rs[t], 1e-9), 4),
                note='← bascule' if idx_tb is not None and t == ts[idx_tb] else '',
            ))
    return rows


# ── SA MODULATEUR (identique V6.2) ──────────────────────────────────────────

def apply_sa_modulator(p: dict, sa: int) -> dict:
    if sa not in (2, 4, 6, 7):
        raise ValueError(f"Sa={sa} invalide.")
    p_out = dict(p)
    if sa == 7:
        p_out['p6']       = p['p6'] * 1.5
        p_out['_sa_note'] = "p6 × 1.5 (Sa=7 famille souche)"
    else:
        p_out['_sa_note'] = f"p6 nominal (Sa={sa})"
    return p_out


# ── COMMANDES DYNAMIQUES (identique V6.2) ───────────────────────────────────

def make_cmd_linear(cmd_base: dict, linear: dict, t_max: int) -> Callable:
    cmd_base_norm = _normalize_cmd(cmd_base)
    def cmd_fn(t):
        c = dict(cmd_base_norm)
        for var, rng in linear.items():
            if not isinstance(rng, dict):
                continue
            val = rng['start'] + (rng['end'] - rng['start']) * (t / max(t_max, 1))
            if var == 'EROI':
                val = max(val, 1.01)
            c[var] = val
        return c
    return cmd_fn


# ── PRÉCHECK CONDITIONS C1-C4 BRANCHE (α) ───────────────────────────────────

def check_alpha_preconditions(config: dict, hp: dict) -> dict:
    """
    Évalue les conditions C1-C4 de la branche (α) à partir du runner_config.
    Les variables V7 sont dans config['variables_v7'].
    Retourne un dict {c1, c2, c3, c4, all_satisfied, details}.
    """
    v7 = config.get('variables_v7') or {}
    hp_alpha = hp.get("trajectoire_alpha", {})

    # Extraction valeurs
    def _get_v7_val(key):
        entry = v7.get(key)
        if entry is None:
            return None
        if isinstance(entry, dict):
            return entry.get("valeur")
        return entry

    m_r         = _get_v7_val("m_r")
    mu_m        = _get_v7_val("mu_m")
    phi         = _get_v7_val("phi")
    psi_noyau   = _get_v7_val("psi_noyau")
    psi_cible   = _get_v7_val("psi_cible")
    gamma_local = _get_v7_val("gamma_local")

    # Commandes pour A_r_c / A_r_ne
    cmd = config.get('cmd', {})
    A_r_c = float(cmd.get('Rc', 0))
    A_r_ne = float(cmd.get('Rn', 0))
    coeff_eff = hp_alpha.get("coefficient_a_r_c_eff", {}).get("valeur", 0.5)

    # C1 : M_r ∈ {1, 2} AND μ_m > μ_m*
    mu_m_star = hp_alpha.get("mu_m_etoile", {}).get("valeur", 0.60)
    c1 = False
    c1_detail = ""
    if m_r is not None and mu_m is not None:
        c1 = (int(m_r) in (1, 2)) and (float(mu_m) > mu_m_star)
        c1_detail = f"M_r={m_r} in {{1,2}}: {int(m_r) in (1,2)}, mu_m={mu_m} > {mu_m_star}: {float(mu_m) > mu_m_star}"
    else:
        c1_detail = f"M_r={m_r}, mu_m={mu_m} — valeur(s) manquante(s)"

    # C2 : Ψ_noyau × γ_local > σ(Φ)
    sigma_base = hp_alpha.get("sigma_base", {}).get("valeur", 0.018)
    alpha_phi  = hp_alpha.get("alpha_phi", {}).get("valeur", 1.7)
    c2 = False
    c2_detail = ""
    sigma = None
    produit_c2 = None
    if psi_noyau is not None and gamma_local is not None and phi is not None:
        sigma = sigma_base * (1.0 + alpha_phi * float(phi))
        produit_c2 = float(psi_noyau) * float(gamma_local)
        c2 = produit_c2 > sigma
        c2_detail = f"psi_noyau={psi_noyau} × gamma_local={gamma_local} = {produit_c2:.6f} > sigma(phi={phi}) = {sigma:.6f}: {c2}"
    else:
        c2_detail = f"psi_noyau={psi_noyau}, gamma_local={gamma_local}, phi={phi} — valeur(s) manquante(s)"

    # C3 : Ψ_cible ≠ null
    c3 = psi_cible is not None
    c3_detail = f"psi_cible={psi_cible}, non-null: {c3}"

    # C4 : A_r_c > 0.7 ou A_r_c_eff > 0.7
    a_r_c_eff = A_r_c + coeff_eff * A_r_ne if A_r_c <= 0.7 else A_r_c
    c4 = a_r_c_eff > 0.7
    c4_detail = f"A_r_c={A_r_c}, A_r_ne={A_r_ne}, A_r_c_eff={a_r_c_eff:.4f} > 0.7: {c4}"

    all_sat = c1 and c2 and c3 and c4

    return {
        "c1": c1, "c2": c2, "c3": c3, "c4": c4,
        "all_satisfied": all_sat,
        "a_r_c_eff": round(a_r_c_eff, 4),
        "sigma_phi": round(sigma, 6) if sigma is not None else None,
        "produit_c2": round(produit_c2, 6) if produit_c2 is not None else None,
        "details": {"c1": c1_detail, "c2": c2_detail, "c3": c3_detail, "c4": c4_detail},
    }


# ── NON-RÉGRESSION T1-T5 ────────────────────────────────────────────────────

def _compare_non_regression(res_lsoda: dict, res_euler: dict, wp_id: str) -> dict:
    """Compare LSODA vs Euler sur les 5 tests T1-T5."""
    sim_l = res_lsoda.get('simulation', res_lsoda)
    sim_e = res_euler.get('simulation', res_euler)

    # T1 : t_bascule ±5
    tb_l = sim_l.get('t_bascule')
    tb_e = sim_e.get('t_bascule')
    t1_pass = True
    if tb_l is not None and tb_e is not None:
        t1_pass = abs(tb_l - tb_e) <= 5
    elif tb_l is None and tb_e is None:
        t1_pass = True
    else:
        t1_pass = False

    # T2 : C_max ±5%
    cm_l = sim_l.get('C_max', 0)
    cm_e = sim_e.get('C_max', 0)
    t2_pass = abs(cm_l - cm_e) / max(cm_e, 1e-9) <= 0.05

    # T3 : chute_I ±3%
    ci_l = sim_l.get('chute_I_metric', sim_l.get('I_min_sim', 0))
    ci_e = sim_e.get('I_min_sim', 0)
    I0_l = sim_l.get('tableau_S2', [{}])[0].get('I', 3.5) if sim_l.get('tableau_S2') else 3.5
    I0_e = sim_e.get('tableau_S2', [{}])[0].get('I', 3.5) if sim_e.get('tableau_S2') else 3.5
    chute_l = (I0_l - sim_l.get('I_min_sim', I0_l)) / max(I0_l, 1e-9)
    chute_e = (I0_e - sim_e.get('I_min_sim', I0_e)) / max(I0_e, 1e-9)
    t3_pass = abs(chute_l - chute_e) <= 0.03

    # T4 : FR_max ±5%
    fr_l = sim_l.get('FR_max', 0)
    fr_e = sim_e.get('FR_max', 0)
    t4_pass = abs(fr_l - fr_e) / max(fr_e, 1e-9) <= 0.05

    # T5 : diagnostic catégoriel identique
    traj_l = sim_l.get('traj', '')
    traj_e = sim_e.get('traj', '')
    t5_pass = traj_l == traj_e

    all_pass = t1_pass and t2_pass and t3_pass and t4_pass and t5_pass

    return {
        "wp_id": wp_id,
        "T1_t_bascule": {"lsoda": tb_l, "euler": tb_e, "pass": t1_pass},
        "T2_C_max":     {"lsoda": cm_l, "euler": cm_e, "pass": t2_pass},
        "T3_chute_I":   {"lsoda": round(chute_l, 4), "euler": round(chute_e, 4), "pass": t3_pass},
        "T4_FR_max":    {"lsoda": fr_l, "euler": fr_e, "pass": t4_pass},
        "T5_traj":      {"lsoda": traj_l, "euler": traj_e, "pass": t5_pass},
        "all_pass": all_pass,
    }


# ── POINT D'ENTRÉE PRINCIPAL ────────────────────────────────────────────────

def run_wp(config: dict) -> dict:
    """
    Lance simulation V7-β complète + stress-tests N1 + N2.
    Détecte automatiquement V6.2 vs V7.
    """
    sa = config.get('sa')
    if sa is None:
        raise ValueError("Champ 'sa' manquant.")

    y0 = _normalize_y0(config.get('y0'))
    cmd_raw = config.get('cmd', {})
    nc_bl, nc_nbl = _detect_nc_in_cmd(cmd_raw)

    if nc_bl:
        raise RuntimeError(f"[NC BLOQUANT] Variables NC dans cmd : {nc_bl}")

    if nc_nbl:
        cmd_raw = dict(cmd_raw)
        fallbacks = {'T': 0.5, 'Mob': 0.3, 'R': 0.3, 'Ref': 0.10,
                     'Rc': 0.2, 'Rn': 0.1, 'E': 0.3, 'Pop': 1.0}
        for k in nc_nbl:
            cmd_raw[k] = fallbacks.get(k, 0.3)

    params_raw = config.get('params', {})
    p = apply_sa_modulator(params_raw, int(sa))
    p = _inject_theta(p, config)

    t_max    = int(config.get('t_max', 300))
    linear   = config.get('cmd_linear') or {}
    cmd_fn = make_cmd_linear(cmd_raw, linear, t_max) if linear else (
        lambda t, _c=_normalize_cmd(cmd_raw): _c
    )
    cmd_base_norm = _normalize_cmd(cmd_raw)

    # Détection V7
    fiche_v7 = config.get('fiche_v7', False)
    v7_vars  = config.get('variables_v7')
    hp       = config.get('hyperparams_v7') or _get_hyperparams_v7()

    # Injecter Cs dans p pour l'arbre de décision V7 (b) explicative
    # Le nœud 2 propage les variables dans le runner_config. On lit Cs
    # depuis les variables V6.2 si disponibles.
    cs_value = 0.30  # défaut
    if v7_vars:
        # Essayer de lire Cs depuis les variables V6.2 transmises par le nœud 2
        vars_v62 = config.get('variables_v62') or {}
        if isinstance(vars_v62, dict) and 'Cs' in vars_v62:
            cs_entry = vars_v62['Cs']
            if isinstance(cs_entry, dict):
                cs_value = float(cs_entry.get('valeur', 0.30) or 0.30)
            else:
                cs_value = float(cs_entry or 0.30)
    p['_cs_value'] = cs_value

    # Précheck conditions α (V7 uniquement)
    rampe_active = False
    alpha_precheck = None
    a_r_c_eff_calc = None

    if fiche_v7 and v7_vars:
        alpha_precheck = check_alpha_preconditions(config, hp)
        rampe_active = alpha_precheck["all_satisfied"]
        a_r_c_eff_calc = alpha_precheck.get("a_r_c_eff")
        if rampe_active:
            print(f"[V7] Branche (α) précheck satisfait — rampe mod_mimétique ACTIVÉE", file=sys.stderr)
        else:
            print(f"[V7] Branche (α) précheck NON satisfait — rampe NON activée", file=sys.stderr)
            for cond, detail in alpha_precheck.get("details", {}).items():
                print(f"  {cond}: {detail}", file=sys.stderr)

    # ── Simulation principale (LSODA) ─────────────────────────────────────────
    res = simulate_lsoda(p, cmd_fn, y0, t_max, rampe_active=rampe_active, hp=hp)

    # ── Override trajectoire pour (γ) Transformation forcée ───────────────────
    _traj_forcee = config.get('trajectoire_forcee')
    if _traj_forcee is not None:
        if _traj_forcee not in _LABELS_D4_V7:
            raise ValueError(f"trajectoire_forcee='{_traj_forcee}' non conforme.")
        _traj_auto = res['traj']
        res = dict(res)
        res['traj'] = _traj_forcee
        res['traj_auto_avant_override'] = _traj_auto

    # ── Stress-tests N1 ──────────────────────────────────────────────────────
    def mk_fn(E_delta, R_delta):
        c2 = dict(cmd_base_norm)
        c2['E'] = max(0.0, cmd_base_norm['E'] + E_delta)
        c2['R'] = max(0.0, cmd_base_norm['R'] + R_delta)
        return make_cmd_linear(c2, linear, t_max) if linear else (lambda t, _c=c2: _c)

    res_opt = simulate_lsoda(p, mk_fn(-0.08, +0.08), y0, t_max, rampe_active=rampe_active, hp=hp)
    res_pes = simulate_lsoda(p, mk_fn(+0.08, -0.08), y0, t_max, rampe_active=rampe_active, hp=hp)

    trajs      = {res['traj'], res_opt['traj'], res_pes['traj']}
    robustesse = 'ROBUSTE' if len(trajs) == 1 else 'MÉTASTABLE'

    # ── Stress N2 ────────────────────────────────────────────────────────────
    stress_n2 = []
    for var, delta in [('E', 0.10), ('R', 0.08), ('EROI', 0.50), ('Rc', 0.10)]:
        for sign, lbl in [(+1, f'{var}+{delta}'), (-1, f'{var}-{delta}')]:
            c2 = dict(cmd_base_norm)
            c2[var] = max(0.0, cmd_base_norm.get(var, 0.0) + sign * delta)
            if var == 'EROI':
                c2[var] = max(1.01, c2[var])
            fn2 = make_cmd_linear(c2, linear, t_max) if linear else (lambda t, _c=c2: _c)
            r2  = simulate_lsoda(p, fn2, y0, t_max, rampe_active=rampe_active, hp=hp)
            stress_n2.append({'label': lbl, 'traj': r2['traj'],
                              'dC_rel': r2['dC_rel'], 'dI_rel': r2['dI_rel']})

    # ── Non-régression T1-T5 (si fiche V7 avec validation V6.2 historique) ───
    non_regression = None
    if fiche_v7:
        # Simulation Euler V6.2 pour comparaison
        p_euler = dict(p)
        # La rampe N'EST PAS active en Euler V6.2 (c'est le point de la non-régression)
        res_euler = simulate_euler(p_euler, cmd_fn, y0, t_max)
        non_regression = _compare_non_regression(
            {"simulation": res}, {"simulation": res_euler},
            config.get('wp_id', '?')
        )

    # ── Résultat complet ─────────────────────────────────────────────────────
    return {
        'meta': {
            'wp_id'               : config.get('wp_id', '?'),
            'cas'                 : config.get('cas', ''),
            'cluster'             : config.get('cluster', ''),
            'trajectoire_attendue': config.get('trajectoire_attendue', ''),
            'sa'                  : sa,
            'sa_modulator'        : p.get('_sa_note', ''),
            'cmd_type'            : 'linear_dynamic' if linear else 'static',
            'integration'         : 'LSODA (scipy solve_ivp rtol=1e-6 atol=1e-9)',
            'nomenclature'        : 'V7-alpha-rev2.1-gamma (cmd["gamma"] = γ)',
            'runner_version'      : 'mepa_runner_v3_v7_v3.0.0',
            'mepa_version'        : '7.0-alpha rev. 2.1' if fiche_v7 else '6.2',
            'fiche_v7'            : fiche_v7,
            'generated_at'        : datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'nc_bloquantes'       : nc_bl,
            'nc_non_bloquantes'   : nc_nbl,
            'statut_nc'           : (
                'DONNÉES_INSUFFISANTES' if nc_bl
                else ('NC_WARNINGS' if nc_nbl else 'OK')
            ),
            'theta_C_effectif'    : p.get('theta_C', 0.30),
            'theta_I_effectif'    : p.get('theta_I', 0.22),
            'y0_normalise'        : y0,
            'variables_v7'        : v7_vars if fiche_v7 else None,
        },
        'simulation': res,
        'stress_n1': {
            'optimiste':  {'traj': res_opt['traj'], 'dC_rel': res_opt['dC_rel'], 'dI_rel': res_opt['dI_rel']},
            'pessimiste': {'traj': res_pes['traj'], 'dC_rel': res_pes['dC_rel'], 'dI_rel': res_pes['dI_rel']},
        },
        'stress_n2': stress_n2,
        'verdict': {
            'robustesse'          : robustesse,
            'trajectoire_diagn'   : res['traj'],
            'branche_annotation'  : res.get('branche_annotation', 'UNKNOWN'),
            'concordance_attendue': res['traj'] == config.get('trajectoire_attendue', res['traj']),
            'trajs_set_n1'        : sorted(trajs),
        },
        'v7_alpha': {
            'precheck'            : alpha_precheck,
            'rampe_active'        : rampe_active,
            'a_r_c_eff_calc'      : a_r_c_eff_calc,
        } if fiche_v7 else None,
        'non_regression_t1_t5': non_regression,
        'params'    : {k: v for k, v in p.items() if not k.startswith('_')},
        'cmd_base'  : cmd_base_norm,
        'cmd_linear': linear,
        'y0'        : y0,
        't_max'     : t_max,
    }


# ── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage : python3 mepa_runner_v3_v7.py config_wp.json [result_out.json]")
        print()
        print("  config_wp.json  : runner_config produit par mepa_node2_audit_v7.js v3.0")
        print("  result_out.json : optionnel — si absent, remplace l'extension .json")
        print()
        print("Runner V7-β : LSODA + branches (α), (b) explicative V7-C4, (d) V7-C2")
        print("Non-régression T1-T5 automatique si fiche V7")
        sys.exit(1)

    config_path = sys.argv[1]
    with open(config_path) as f:
        config = json.load(f)

    result = run_wp(config)

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
    print(f"   Annotation     : {sim.get('branche_annotation', '?')}")
    print(f"   t_bascule      : {sim.get('t_bascule')}")
    print(f"   ΔC_rel         : {sim.get('dC_rel')}  |  ΔI_rel : {sim.get('dI_rel')}")
    print(f"   C_max          : {sim.get('C_max')}")
    print(f"   Robustesse     : {vrd['robustesse']}")
    print(f"   Concordance    : {'✓' if vrd['concordance_attendue'] else '✗ DIVERGENCE'}")
    print(f"   Intégration    : {meta['integration']}")
    print(f"   Runner version : {meta['runner_version']}")
    if meta.get('fiche_v7'):
        v7a = result.get('v7_alpha', {})
        print(f"   V7 rampe active: {v7a.get('rampe_active')}")
        print(f"   A_r_c_eff      : {v7a.get('a_r_c_eff_calc')}")
        nr = result.get('non_regression_t1_t5')
        if nr:
            print(f"   Non-régression : {'✓ TOUS PASSENT' if nr['all_pass'] else '✗ ÉCHOUE'}")
            for k in ['T1_t_bascule', 'T2_C_max', 'T3_chute_I', 'T4_FR_max', 'T5_traj']:
                v = nr[k]
                status = '✓' if v['pass'] else '✗'
                print(f"     {status} {k}: LSODA={v['lsoda']}  Euler={v['euler']}")
    if meta.get('nc_non_bloquantes'):
        print(f"   ⚠ NC non-bloquantes : {meta['nc_non_bloquantes']}")
