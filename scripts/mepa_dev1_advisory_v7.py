#!/usr/bin/env python3
"""
================================================================================
MEPA V7 — Module ADVISORY Dev 1 (diagnostic pur, NON CALIBRÉ)
================================================================================
Statut           : V7 — Ω ≡ I(t) (complexité institutionnelle dynamique,
                   décision CV1 juin 2026)
Cible            : /data/mepa/scripts/mepa_dev1_advisory_v7.py
Remplace         : mepa_dev1_advisory_v63.py (V6.3, Ω = Sa/SA_REF provisoire)
Rôle             : Calculer A_d_max DÉRIVÉ depuis la chaîne biophysique Dev 1
                   (EROI → S* → A_d_max) en mode DIAGNOSTIC PUR.
                   Comparé à R_codé (= A_d_eff, mappé sur cmd.R en C9b) pour
                   produire un flag advisory non bloquant.

================================================================================
⚠⚠⚠  AVERTISSEMENT ÉPISTÉMIQUE — LIRE AVANT TOUT USAGE  ⚠⚠⚠
================================================================================
Ce module ne modifie AUCUNE trajectoire. Il n'entre PAS dans les équations
différentielles (_step, F_val, R_val, simulate restent intouchés au bit près).
Sa sortie est PUREMENT DIAGNOSTIQUE et accumulée pour préparer la calibration
V7.

TOUS les paramètres ci-dessous (C_OMEGA, THETA, C_SUB, SA_REF, S_REF) sont
NON CALIBRÉS. Les valeurs A_d_max_advisory_NONCALIBRE produites NE DOIVENT
PAS être utilisées pour de l'inférence, ni pour modifier un codage, ni pour
trancher une trajectoire. Elles servent UNIQUEMENT :
  1. à signaler les WP où R_codé > A_d_max_dérivé (précurseur de dette Dev 2) ;
  2. à constituer la série de valeurs qui PERMETTRA de pinner c_Ω, θ, S*_ref
     et de trancher l'agrégat de dette (CV9) lors de l'ouverture de V7.

La forme fonctionnelle elle-même (proxy Ω = Sa, η = γ, échelle [0,10]) est un
choix advisory PROVISOIRE, à réviser en revue collégiale (cf. Dossier
d'Architecture Dev 2, CV9 et amendement C0). Ne pas figer comme théorie.
================================================================================

Chaîne Dev 1 (source : conversation théorique économique biophysique) :
    net_energy = 1 - 1/EROI                      # fraction nette (Hall, net energy cliff)
    Y_proxy    = net_energy * Pop                # surplus brut normalisé
    C_maint    = C_OMEGA * (Sa/SA_REF)**THETA    # coût de maintenance de la complexité
    S*         = Y_proxy - C_SUB - C_maint       # surplus net
    A_d_max    = eta_D * max(0, S*) / S_REF      # plafond redistributif dérivé
               avec eta_D = gamma (part redistribuable, proxy γ)
    flag       = (R_codé > A_d_max_dérivé_échelle_0_10)

Dépendances : math (stdlib uniquement).
Version      : 0.1.0-advisory
================================================================================
"""

import math

# ── PARAMÈTRES ADVISORY — TOUS NON CALIBRÉS ──────────────────────────────────
# Valeurs indicatives issues de la conversation théorique (θ≈1.35, c_Ω≈0.08).
# AUCUNE n'est calibrée sur le corpus. Surchargées si présentes dans
# mepa_constants.json["advisory_dev1_NONCALIBRE"], sinon ces défauts s'appliquent.
ADVISORY_DEFAULTS_NONCALIBRE = {
    "C_OMEGA": 0.08,   # c_Ω — coût unitaire de maintenance de la complexité
    "THETA":   1.35,   # θ   — exposant de rendements décroissants de la complexité
    "C_SUB":   0.10,   # plancher de subsistance (normalisé)
    "SA_REF":  4.0,    # Sa de référence (nucléaire égalitaire) pour le proxy de complexité
    "S_REF":   0.50,   # S*_ref — normalisation du surplus
    "ECHELLE_A_D": 10.0,  # échelle d'A_d_eff (cmd.R ∈ [0,10]) pour rendre le flag comparable
}

ADVISORY_DISCLAIMER = (
    "VALEUR INDICATIVE — paramètres NON CALIBRÉS (c_Ω, θ, S*_ref advisory). "
    "Ne pas utiliser pour inférence, codage ou décision de trajectoire. "
    "Diagnostic Dev 1 V6.3 — précurseur de la dette Dev 2 (V7)."
)

MODULE_VERSION = "mepa_dev1_advisory_v7 v1.0.0"


def _params_advisory(constants: dict | None) -> dict:
    """
    Retourne les paramètres advisory. Surcharge depuis
    constants["advisory_dev1_NONCALIBRE"]["params"] si présent, sinon défauts.
    Ne lève jamais : tout échec → défauts.
    """
    p = dict(ADVISORY_DEFAULTS_NONCALIBRE)
    try:
        bloc = (constants or {}).get("advisory_dev1_NONCALIBRE", {})
        surcharge = bloc.get("params", {})
        for k in p:
            if k in surcharge:
                p[k] = float(surcharge[k])
    except Exception:
        pass
    return p


def calculer_a_d_max_derive(EROI: float, gamma: float, sa: int, pop: float,
                            params: dict,
                            omega_override: float | None = None) -> dict:
    """
    Calcule A_d_max dérivé (NON CALIBRÉ) et ses intermédiaires.
    Fonction pure — ne lève pas sur entrées valides numériques.
    """
    C_OMEGA = params["C_OMEGA"]
    THETA   = params["THETA"]
    C_SUB   = params["C_SUB"]
    SA_REF  = params["SA_REF"]
    S_REF   = params["S_REF"]
    ECHELLE = params["ECHELLE_A_D"]

    # Fraction d'énergie nette (biophysique). EROI > 1 garanti par le garde-fou runner.
    eroi_eff   = max(EROI, 1.0 + 1e-9)
    net_energy = max(0.0, 1.0 - 1.0 / eroi_eff)

    Y_proxy = net_energy * max(pop, 0.0)
    # V7 — Ω ≡ I(t) si omega_override fourni, Sa/SA_REF sinon (V6.3 provisoire)
    if omega_override is not None:
        Omega = float(omega_override)   # Ω ≡ I(t), valeur directe
    else:
        Omega = max(sa, 0) / SA_REF if SA_REF > 0 else 0.0
    C_maint = C_OMEGA * (Omega ** THETA)
    S_etoile = Y_proxy - C_SUB - C_maint

    eta_D = max(0.0, min(1.0, gamma))   # part redistribuable, proxy γ borné [0,1]
    a_d_max_normalise = eta_D * max(0.0, S_etoile) / S_REF if S_REF > 0 else 0.0
    a_d_max_echelle_0_10 = max(0.0, min(ECHELLE, ECHELLE * a_d_max_normalise))

    return {
        "EROI_utilise":            round(eroi_eff, 6),
        "net_energy_fraction":     round(net_energy, 6),
        "Y_proxy":                 round(Y_proxy, 6),
        "omega_source":            "I(t)_direct" if omega_override is not None else "Sa/SA_REF_provisoire",
        "Omega_valeur":            round(Omega, 6),
        "C_maintenance":           round(C_maint, 6),
        "S_etoile_NONCALIBRE":     round(S_etoile, 6),
        "eta_D_proxy_gamma":       round(eta_D, 6),
        "a_d_max_normalise":       round(a_d_max_normalise, 6),
        "a_d_max_advisory_NONCALIBRE": round(a_d_max_echelle_0_10, 6),
    }


def calculer_advisory_dev1(cmd_base_norm: dict, sa: int, y0: list,
                           cmd_fn=None, t_max: int = 0,
                           constants: dict | None = None,
                           i_t0: float | None = None,
                           i_tmax: float | None = None,
                           omega_mode: str = 'I') -> dict:
    """
    Point d'entrée du module. NE LÈVE JAMAIS — toute erreur est capturée et
    renvoyée dans le bloc (flag = None + raison). Le runner reste non bloqué.

    Compare R_codé (= cmd.R, mappage A_d_eff→cmd.R en C9b) à A_d_max dérivé.
    Calcule au pas initial (t=0) et, si cmd_fn fourni, au pas final (t=t_max)
    pour capter les WP à EROI dynamique (cluster C1).
    """
    try:
        params = _params_advisory(constants)

        # R_codé = A_d_eff codé, mappé sur cmd.R (C9b). Échelle [0,10].
        R_code = float(cmd_base_norm.get("R", 0.0))

        gamma = float(cmd_base_norm.get("gamma", 0.0))
        pop   = float(cmd_base_norm.get("Pop", 1.0))

        # ── Pas initial t=0 ──
        EROI_0 = float(cmd_base_norm.get("EROI", 0.0))
        omega_t0 = i_t0 if (omega_mode == 'I' and i_t0 is not None) else None
        calc_t0 = calculer_a_d_max_derive(EROI_0, gamma, sa, pop, params,
                                           omega_override=omega_t0)
        a_d_max_t0 = calc_t0["a_d_max_advisory_NONCALIBRE"]

        # ── Pas final t=t_max (si EROI dynamique OU I dynamique) ──
        calc_tmax = None
        if cmd_fn is not None and t_max and t_max > 0:
            try:
                cmd_fin = cmd_fn(t_max)
                EROI_fin = float(cmd_fin.get("EROI", EROI_0))
                gamma_fin = float(cmd_fin.get("gamma", gamma))
                pop_fin = float(cmd_fin.get("Pop", pop))
                omega_tmax = i_tmax if (omega_mode == 'I' and i_tmax is not None) else None
                # Calculer si EROI ou I ont changé
                eroi_change = abs(EROI_fin - EROI_0) > 1e-9
                omega_change = (omega_tmax is not None and omega_t0 is not None
                                and abs(omega_tmax - omega_t0) > 1e-9)
                if eroi_change or omega_change:
                    calc_tmax = calculer_a_d_max_derive(EROI_fin, gamma_fin, sa, pop_fin, params,
                                                        omega_override=omega_tmax)
            except Exception:
                calc_tmax = None

        # ── Flag advisory (NON bloquant) ──
        # Allumé si la capacité redistributive codée dépasse le plafond dérivé du
        # surplus énergétique seul → écart à financer (précurseur de dette Dev 2).
        flag = bool(R_code > a_d_max_t0)
        ecart = round(R_code - a_d_max_t0, 6)

        return {
            "$advisory": True,
            "statut": "ADVISORY_DEV1_NONCALIBRE",
            "module_version": MODULE_VERSION,
            "disclaimer": ADVISORY_DISCLAIMER,
            "omega_mode": omega_mode,
            "i_t0_utilise": round(i_t0, 4) if i_t0 is not None else None,
            "i_tmax_utilise": round(i_tmax, 4) if i_tmax is not None else None,
            "R_code_A_d_eff": round(R_code, 6),
            "a_d_max_advisory_flag": flag,
            "ecart_R_code_moins_a_d_max": ecart,
            "interpretation_flag": (
                "R_codé > A_d_max dérivé : capacité redistributive codée supérieure "
                "au plafond du surplus énergétique seul — écart potentiellement financé "
                "par dette (à instruire en Dev 2 / V7). NON CALIBRÉ."
                if flag else
                "R_codé ≤ A_d_max dérivé : pas d'écart advisory détecté au pas initial."
            ),
            "calcul_t0": calc_t0,
            "calcul_tmax": calc_tmax,
            "params_utilises_NONCALIBRE": params,
            "mapping_note": (
                "R_codé = cmd.R (A_d_eff mappé sur cmd.R en C9b). "
                "La commensurabilité R_codé ↔ A_d_max dérivé est elle-même un choix "
                "advisory provisoire (cf. CV9). Échelle alignée sur [0,10]."
            ),
            # Champ réservé V7 — vide en V6.3 (pas de section S0, cf. décision de gel)
            "regime_S_etoile": None,
        }

    except Exception as e:
        # Advisory ne bloque JAMAIS le runner.
        return {
            "$advisory": True,
            "statut": "ADVISORY_DEV1_ERREUR_NON_BLOQUANTE",
            "module_version": MODULE_VERSION,
            "disclaimer": ADVISORY_DISCLAIMER,
            "a_d_max_advisory_flag": None,
            "erreur": f"{type(e).__name__}: {e}",
            "note": "Échec advisory capturé — la simulation principale n'est pas affectée.",
            "regime_S_etoile": None,
        }
