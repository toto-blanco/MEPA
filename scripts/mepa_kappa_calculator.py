#!/usr/bin/env python3
"""
================================================================================
MEPA V7-alpha rev. 2.1 — mepa_kappa_calculator.py
================================================================================
Statut           : EXTENSION V7
Cible            : /data/mepa/scripts/mepa_kappa_calculator.py
Remplace         : mepa_kappa_calculator.py v2.0 (V6.2)
Rétrocompatibilité :
  - API publique V6.2 intégralement préservée :
      calculer_cci(path_a, path_b) -> dict
      calculer_kappa(path_a, path_b) -> dict (alias)
      afficher_rapport(rapport) -> None
  - Les fonctions internes (_extraire_valeur, _accord_continu, _calculer_friction,
    _cci_global_depuis_details, _kappa_cohen_categoriel) sont INCHANGÉES au bit près.
  - Le flux de calcul (Phase 1 extraction → Phase 6 valeurs finales) est INCHANGÉ.
  - Les seuils de validation (0.70, 0.75, 0.55) sont INCHANGÉS.
  - Le format du rapport de sortie est INCHANGÉ dans sa structure V6.2 —
    il contient juste plus de variables dans 'detail_variables' si la fiche est V7.

Version          : 3.0.0
MEPA version     : 7.0-alpha rev. 2.1
Dépendances      : json, sys, math, os, numpy, scipy (V6.2 inchangées)

================================================================================

Extensions V7 vs V6.2 :
-----------------------

[V7-K1] VAR_DEFS étendu par fusion :
        Le dict VAR_DEFS utilisé pour le calcul CCI est désormais construit par
        fusion de CONSTANTS["variables_mepa"] (9 variables V6.2) + 
        CONSTANTS["variables_v7_alpha_rev2_1"] (6 variables V7). Cela permet
        au calcul CCI de traiter automatiquement les six variables V7
        (m_r, mu_m, phi, psi_noyau, psi_cible, gamma_local) sans toucher au
        code de calcul. Si une fiche V6.2 est passée en entrée, les variables V7
        sont simplement absentes de la fiche et ne sont pas comptabilisées
        (comportement identique à V6.2 pour toute variable absente).

[V7-K2] Fallback embarqué étendu :
        Le fallback de _charger_constants() contient désormais les 6 variables V7
        avec leurs seuils CCI appropriés (0.15 pour continues, exact pour m_r).

[V7-K3] NC BLOQUANTES étendues :
        La liste nc_bloquantes inclut désormais psi_noyau et gamma_local
        (déjà reflété dans mepa_constants.json v1.3.0).

[V7-K4] Gestion spéciale psi_cible (null positif) :
        psi_cible peut légitimement valoir null avec justification textuelle
        (règle E3 rev. 2.1). _extraire_valeur reconnaît null comme valeur
        valide non-NC pour psi_cible — pas de propagation NC. Ce traitement
        est assuré via un type "continue_ou_null" dans VAR_DEFS.

================================================================================

Rôle dans le pipeline WF1 :
  Nœud 6b — κ inter-codeurs CONV-E vs CONV-B.
  Entrées :
    - fiche_A.json (CONV-E) et fiche_B.json (CONV-B) — au même format JSON
  Sortie :
    - rapport CCI avec champs cci, kappa_sa, variables_nc, verdict, 
      friction_vecteur, detail_variables, valeurs_finales_provisoires

Usage :
  python3 mepa_kappa_calculator.py fiche_A.json fiche_B.json [output.json]
"""

import json
import sys
import math
import os
from typing import Optional, Tuple, List, Dict, Any

import numpy as np
from scipy import stats

# ── CHEMIN CONSTANTS (fallback embarqué si fichier absent) ────────────────────
MEPA_SCRIPTS_DIR = os.environ.get("MEPA_SCRIPTS_DIR", "/data/mepa/scripts")
CONSTANTS_PATH   = os.path.join(MEPA_SCRIPTS_DIR, "mepa_constants.json")

# ── CHARGEMENT mepa_constants.json ────────────────────────────────────────────

def _charger_constants() -> dict:
    """
    Charge mepa_constants.json v1.3.0.
    Si absent, retourne le fallback embarqué (identique au fichier V7).
    Garantit la robustesse sur Pi5 (HDD débranché, fichier corrompu).
    """
    try:
        with open(CONSTANTS_PATH) as f:
            return json.load(f)
    except Exception:
        # Fallback embarqué — synchronisé avec mepa_constants.json v1.3.0
        return {
            # --- Variables V6.2 (inchangées) ---
            "variables_mepa": {
                "E_split": {"type": "continue", "echelle": [0.0, 1.0],  "seuil_cci": 0.15, "obligatoire": True},
                "gamma":   {"type": "continue", "echelle": [0.0, 1.0],  "seuil_cci": 0.15, "obligatoire": True},
                "A_d_eff": {"type": "continue", "echelle": [0.0, 10.0], "seuil_cci": 1.5,  "obligatoire": True},
                "A_r_c":   {"type": "continue", "echelle": [0.0, 1.0],  "seuil_cci": 0.15, "obligatoire": True},
                "A_r_ne":  {"type": "continue", "echelle": [0.0, 1.0],  "seuil_cci": 0.15, "obligatoire": True},
                "Cs":      {"type": "continue", "echelle": [0.0, 1.0],  "seuil_cci": 0.15, "obligatoire": True},
                "L_t":     {"type": "continue", "echelle": [0.0, 1.0],  "seuil_cci": 0.15, "obligatoire": True},
                "EROI":    {"type": "continue", "echelle": [0.0, 50.0], "seuil_cci": 1.5,  "obligatoire": True},
                "Sa":      {"type": "categorielle", "valeurs_valides": [2, 4, 6, 7], "obligatoire": True},
            },
            # --- Variables V7-alpha rev. 2.1 (NOUVEAU) ---
            "variables_v7_alpha_rev2_1": {
                "m_r":         {"type": "categorielle", "valeurs_valides": [1, 2, 3], "obligatoire": True,
                                "note": "Stade matrice religieuse Todd. C1 (α) : m_r ∈ {1, 2}."},
                "mu_m":        {"type": "continue", "echelle": [0.0, 1.0], "seuil_cci": 0.15, "obligatoire": True,
                                "note": "Polarisation mimétique girardienne. C1 (α) : μ_m > 0.60."},
                "phi":         {"type": "continue", "echelle": [0.0, 1.0], "seuil_cci": 0.15, "obligatoire": True,
                                "note": "Fragmentation symbolique. Module σ(Φ)."},
                "psi_noyau":   {"type": "continue", "echelle": [0.0, 1.0], "seuil_cci": 0.05, "obligatoire": True,
                                "note": "Proportion population engagée noyau. C2 : Ψ × γ_local > σ(Φ). NC bloquant."},
                "psi_cible":   {"type": "continue_ou_null", "echelle": [0.0, 1.0], "seuil_cci": 0.05, "obligatoire": True,
                                "note": "Proportion population cible. Null positif autorisé (règle E3 rev. 2.1). C3 : Ψ_cible ≠ null."},
                "gamma_local": {"type": "continue", "echelle": [0.0, 1.0], "seuil_cci": 0.10, "obligatoire": True,
                                "note": "Capacité organisationnelle noyau. C2 : Ψ × γ_local > σ(Φ). NC bloquant."},
            },
            # --- Seuils V6.2 (inchangés) ---
            "seuils_validation": {
                "cci":        {"certifie": 0.70, "revision": 0.50},
                "kappa_sa":   {"certifie": 0.70, "revision": 0.50},
                "cci_global": {"certifie": 0.75, "revision": 0.55},
                "friction_outlier_seuil": {"valeur": 2.0},
            },
            # --- NC bloquantes étendues V7 ---
            "nc_protocol": {
                "valeur_sentinel":         "NC",
                "variables_nc_bloquantes": ["E_split", "gamma", "EROI", "Sa", "psi_noyau", "gamma_local"],
            },
        }


CONSTANTS = _charger_constants()

# ── CONSTRUCTION VAR_DEFS — FUSION V6.2 + V7 ─────────────────────────────────
# [V7-K1] VAR_DEFS contient les 9 variables V6.2 + les 6 variables V7-α rev. 2.1.
# Si mepa_constants.json v1.3.0 est disponible, on fusionne les deux sections.
# Sinon, on utilise le fallback qui contient déjà les deux sections.
def _construire_var_defs(constants: dict) -> Dict[str, dict]:
    """
    Construit le dict VAR_DEFS par fusion de variables_mepa (V6.2) et
    variables_v7_alpha_rev2_1 (V7). Filtre les clés de métadonnées ($description, etc.).
    """
    out = {}
    # V6.2 en premier (ordre préservé pour rapports lisibles)
    v62 = constants.get("variables_mepa", {})
    for k, v in v62.items():
        if not k.startswith("$") and isinstance(v, dict):
            out[k] = v
    # V7 ensuite
    v7 = constants.get("variables_v7_alpha_rev2_1", {})
    for k, v in v7.items():
        if not k.startswith("$") and isinstance(v, dict):
            out[k] = v
    return out


VAR_DEFS = _construire_var_defs(CONSTANTS)

SEUILS    = CONSTANTS["seuils_validation"]
NC_SENTINEL           = CONSTANTS["nc_protocol"]["valeur_sentinel"]
NC_BLOQUANTES         = set(CONSTANTS["nc_protocol"]["variables_nc_bloquantes"])
FRICTION_OUTLIER_SEUIL = CONSTANTS["seuils_validation"]["friction_outlier_seuil"]["valeur"]

# Seuils de validation (inchangés V6.2)
SEUIL_CERTIFIE   = SEUILS["cci"]["certifie"]        # 0.70
SEUIL_REVISION   = SEUILS["cci"]["revision"]         # 0.50
SEUIL_CERTIFIE_G = SEUILS["cci_global"]["certifie"]  # 0.75
SEUIL_REVISION_G = SEUILS["cci_global"]["revision"]  # 0.55
SEUIL_KAPPA_SA   = SEUILS["kappa_sa"]["certifie"]    # 0.70


# ── EXTRACTION DE VALEUR DEPUIS FICHE (étendue V7) ───────────────────────────

def _extraire_valeur(fiche: dict, var: str) -> Tuple[Any, bool]:
    """
    Extrait la valeur d'une variable depuis une fiche de codage.
    Retourne (valeur, is_nc).

    V7 : cherche aussi dans fiche.variables_v7{} (bloc dédié) pour les 6 variables V7,
    puis en fallback dans fiche.variables{} comme pour V6.2.

    V7 : pour psi_cible, reconnaît null comme valeur positive légitime (règle E3 rev. 2.1).
    Le null positif n'est PAS traité comme NC — la valeur retournée est None et is_nc est False.
    Le calcul CCI sur psi_cible est alors désactivé pour cette paire
    (la variable n'est pas scorable), ce qui est le comportement souhaité.
    """
    # Priorité 1 : bloc variables_v7 dédié (V7)
    vars_v7 = fiche.get("variables_v7", {})
    if var in vars_v7 and isinstance(vars_v7[var], dict):
        entry = vars_v7[var]
    else:
        # Priorité 2 : bloc variables (V6.2 + V7 mélangées dans le même bloc)
        vars_obj = fiche.get("variables", {})
        if var in vars_obj and isinstance(vars_obj[var], dict):
            entry = vars_obj[var]
        else:
            return (None, False)

    valeur = entry.get("valeur")

    # Cas 1 : valeur NC (sentinelle string)
    if isinstance(valeur, str) and valeur.strip().upper() == NC_SENTINEL:
        return (None, True)

    # Cas 2 : psi_cible null (règle E3 rev. 2.1 — null positif, pas NC)
    if var == "psi_cible" and valeur is None:
        return (None, False)

    # Cas 3 : valeur numérique normale
    if valeur is None:
        return (None, False)

    # Conversion type
    try:
        # m_r est un entier (catégoriel)
        if var == "m_r" or (VAR_DEFS.get(var, {}).get("type") == "categorielle"):
            return (int(valeur), False)
        # Autres : float
        return (float(valeur), False)
    except (ValueError, TypeError):
        return (valeur, False)  # pass-through si conversion échoue


# ── ACCORD SUR VARIABLE CONTINUE ──────────────────────────────────────────────

def _accord_continu(val_a: float, val_b: float, seuil_cci: float) -> dict:
    """
    Détermine si deux valeurs continues sont en accord au seuil.
    Retourne {accord: bool, ecart: float}.
    """
    if val_a is None or val_b is None:
        return {"accord": None, "ecart": None}
    ecart = abs(val_a - val_b)
    return {"accord": ecart <= seuil_cci, "ecart": round(ecart, 4)}


# ── ACCORD KAPPA COHEN POUR VARIABLE CATÉGORIELLE ────────────────────────────

def _kappa_cohen_categoriel(val_a: Any, val_b: Any, var: str) -> dict:
    """
    Détermine l'accord strict pour une variable catégorielle.
    Sur un seul WP, κ = 1.0 si accord exact, 0.0 sinon.
    Le κ de Cohen corpus-wide sera calculé séparément dans friction_profile.
    """
    meta = VAR_DEFS.get(var, {})
    valides = meta.get("valeurs_valides", [])

    if val_a is None or val_b is None:
        return {"accord": None, "ecart": None, "scorable": False}

    # Conversion entier si possible
    try:
        a_int = int(val_a)
        b_int = int(val_b)
    except (ValueError, TypeError):
        return {"accord": False, "ecart": None, "scorable": False}

    # Validation plages
    if valides and a_int not in valides:
        return {"accord": False, "ecart": None, "scorable": False}
    if valides and b_int not in valides:
        return {"accord": False, "ecart": None, "scorable": False}

    accord = (a_int == b_int)
    return {"accord": accord, "ecart": 0 if accord else 1, "scorable": True}


# ── CALCUL FRICTION ───────────────────────────────────────────────────────────

def _calculer_friction(val_a: float, val_b: float, seuil_cci: float, is_nc: bool) -> Optional[float]:
    """
    Calcule la friction F(v,h) = |val_a - val_b| / seuil_cci.
    Proxy de désaccord normalisé pour mepa_friction_profile.json.
    F ∈ [0, ∞) — F=0 accord parfait, F=1 désaccord au seuil exact, F>1 désaccord sig.
    """
    if is_nc or val_a is None or val_b is None:
        return None
    return round(abs(val_a - val_b) / seuil_cci, 4) if seuil_cci > 0 else None


# ── CALCUL CCI GLOBAL ICC(3,1) ────────────────────────────────────────────────

def _cci_global_depuis_details(details: List[dict]) -> Optional[dict]:
    """
    Calcule le CCI global ICC(3,1) sur les variables continues normalisées
    et scorables. Retourne un dict avec icc, ci_low, ci_high, F, p, n.
    Retourne None si moins de 2 variables scorables.
    """
    paires = []
    for r in details:
        if r["type"] != "continue" or r["nc"] or not r["scorable"]:
            continue
        if r["val_a"] is None or r["val_b"] is None:
            continue
        # Normalisation par plage (max - min) pour comparer les variables
        # sur une échelle commune. Les plages sont dans VAR_DEFS[var]["echelle"].
        meta = VAR_DEFS.get(r["variable"], {})
        echelle = meta.get("echelle", [0.0, 1.0])
        plage = echelle[1] - echelle[0]
        if plage <= 0:
            continue
        a_norm = (float(r["val_a"]) - echelle[0]) / plage
        b_norm = (float(r["val_b"]) - echelle[0]) / plage
        paires.append([a_norm, b_norm])

    if len(paires) < 2:
        return None

    data = np.array(paires)  # shape (n, 2)
    n = data.shape[0]

    # ICC(3,1) two-way mixed, single measures, consistency
    # Formule : ICC = (MSR - MSE) / (MSR + (k-1)*MSE)
    # où MSR = variance entre sujets (rows), MSE = variance résiduelle, k = nb codeurs
    mean_per_row = data.mean(axis=1)    # moyenne par variable
    mean_per_col = data.mean(axis=0)    # moyenne par codeur
    grand_mean   = data.mean()

    # Somme des carrés
    ss_rows = 2 * np.sum((mean_per_row - grand_mean) ** 2)  # k=2 codeurs
    ss_cols = n * np.sum((mean_per_col - grand_mean) ** 2)
    ss_total = np.sum((data - grand_mean) ** 2)
    ss_err  = ss_total - ss_rows - ss_cols

    df_rows = n - 1
    df_cols = 1   # k - 1 = 2 - 1
    df_err  = (n - 1) * 1

    ms_rows = ss_rows / df_rows if df_rows > 0 else 0
    ms_err  = ss_err / df_err if df_err > 0 else 0

    if ms_rows + ms_err <= 0:
        return None

    icc = (ms_rows - ms_err) / (ms_rows + ms_err)

    # Intervalle de confiance 95% (approximation Fisher)
    f_stat = ms_rows / ms_err if ms_err > 0 else 0
    try:
        f_low  = f_stat / stats.f.ppf(0.975, df_rows, df_err)
        f_high = f_stat * stats.f.ppf(0.975, df_err, df_rows)
        ci_low  = (f_low - 1)  / (f_low + 1)  if f_low  > 0 else 0
        ci_high = (f_high - 1) / (f_high + 1) if f_high > 0 else 0
        p = 1 - stats.f.cdf(f_stat, df_rows, df_err)
    except Exception:
        ci_low, ci_high, p = None, None, None

    return {
        "icc":     round(max(0.0, min(1.0, icc)), 4),
        "ci_low":  round(ci_low, 4)  if ci_low  is not None else None,
        "ci_high": round(ci_high, 4) if ci_high is not None else None,
        "F":       round(f_stat, 4),
        "p":       round(p, 4) if p is not None else None,
        "n":       n,
    }


# ── CHARGEMENT FICHE ──────────────────────────────────────────────────────────

def charger_fiche(path: str) -> dict:
    with open(path) as f:
        fiche = json.load(f)
    # Validation minimale
    if "variables" not in fiche and "wp_id" not in fiche:
        raise ValueError(
            f"{path} : format non reconnu — champ 'variables' ou 'wp_id' attendu."
        )
    return fiche


# ── POINT D'ENTRÉE PRINCIPAL ──────────────────────────────────────────────────

def calculer_cci(path_a: str, path_b: str) -> dict:
    """
    Point d'entrée principal. Calcule le CCI inter-codeurs entre deux fiches MEPA.

    Retourne le rapport complet compatible avec :
      - mepa_passeport_schema.py v3.0 (champs 'cci', 'kappa_sa', 'variables_nc')
      - mepa_friction_profile.json (champ 'friction_vecteur')
      - mepa_node2_audit_v7.js (champ 'variables_nc' pour contrôle C13)

    V7 : si les fiches contiennent les 6 variables V7, elles sont automatiquement
    intégrées au calcul CCI. Si les fiches sont V6.2, seules les 9 variables V6.2
    sont calculées (comportement rétrocompatible).
    """
    fiche_a = charger_fiche(path_a)
    fiche_b = charger_fiche(path_b)

    wp_id    = fiche_a.get("wp_id", fiche_b.get("wp_id", "?"))
    codeur_a = fiche_a.get("codeur", "CONV-E")
    codeur_b = fiche_b.get("codeur", "CONV-B")

    # Détection du format V7 (présence de variables_v7 ou d'au moins une variable V7)
    est_v7 = "variables_v7" in fiche_a or "variables_v7" in fiche_b
    if not est_v7:
        vars_v7_possibles = ["m_r", "mu_m", "phi", "psi_noyau", "psi_cible", "gamma_local"]
        for v7key in vars_v7_possibles:
            if v7key in fiche_a.get("variables", {}) or v7key in fiche_b.get("variables", {}):
                est_v7 = True
                break

    # ── Phase 1 : extraction et détection NC ──────────────────────────────────
    details       = []
    variables_nc  = []
    nc_bloquantes = []

    for var, meta in VAR_DEFS.items():
        val_a, is_nc_a = _extraire_valeur(fiche_a, var)
        val_b, is_nc_b = _extraire_valeur(fiche_b, var)
        is_nc = is_nc_a or is_nc_b

        seuil_cci = meta.get("seuil_cci")  # None pour Sa / m_r

        # Cas spécial V7 : psi_cible null positif sur les DEUX fiches = accord sur null
        # Pas de calcul CCI mais marquée scorable=False et accord=True
        if var == "psi_cible" and val_a is None and val_b is None and not is_nc:
            entry = {
                "variable": var,
                "type":     meta["type"],
                "val_a":    None,
                "val_b":    None,
                "nc":       False,
                "nc_a":     False,
                "nc_b":     False,
                "scorable": False,
                "accord":   True,   # accord sur null positif (règle E3)
                "ecart":    0,
                "seuil":    "null_positif",
                "friction": 0,
                "friction_outlier": False,
                "note":     "psi_cible=null sur les deux fiches (accord règle E3 rev. 2.1)",
            }
            details.append(entry)
            continue

        # Friction
        friction = None
        if meta["type"] == "continue" and not is_nc and seuil_cci:
            friction = _calculer_friction(val_a, val_b, seuil_cci, is_nc)

        # Accord subsidiaire (pour rapport détaillé)
        accord_detail = None
        ecart         = None
        scorable      = False

        if is_nc:
            accord_detail = None
            scorable      = False
        elif meta["type"] == "continue":
            if val_a is not None and val_b is not None:
                r = _accord_continu(val_a, val_b, seuil_cci)
                accord_detail = r["accord"]
                ecart         = r["ecart"]
                scorable      = True
        elif meta["type"] == "continue_ou_null":
            # psi_cible : scorable seulement si les deux ont valeur numérique
            if val_a is not None and val_b is not None:
                r = _accord_continu(val_a, val_b, seuil_cci)
                accord_detail = r["accord"]
                ecart         = r["ecart"]
                scorable      = True
            elif val_a is None and val_b is None:
                # Gestion déjà traitée ci-dessus (ne devrait pas atteindre ce bloc)
                accord_detail = True
                scorable      = False
            else:
                # Une fiche null, l'autre non : désaccord majeur
                accord_detail = False
                ecart         = None
                scorable      = False
        elif meta["type"] == "categorielle":
            r = _kappa_cohen_categoriel(val_a, val_b, var)
            accord_detail = r["accord"]
            ecart         = r["ecart"]
            scorable      = r["scorable"]

        entry = {
            "variable": var,
            "type":     meta["type"],
            "val_a":    val_a if not is_nc_a else NC_SENTINEL,
            "val_b":    val_b if not is_nc_b else NC_SENTINEL,
            "nc":       is_nc,
            "nc_a":     is_nc_a,
            "nc_b":     is_nc_b,
            "scorable": scorable,
            "accord":   accord_detail,
            "ecart":    ecart,
            "seuil":    seuil_cci if seuil_cci else "exact",
            "friction": friction,
            "friction_outlier": (friction is not None and friction > FRICTION_OUTLIER_SEUIL),
        }
        details.append(entry)

        if is_nc:
            variables_nc.append(var)
            if var in NC_BLOQUANTES:
                nc_bloquantes.append(var)

    # ── Phase 2 : CCI par variable continue ───────────────────────────────────
    cci_par_variable = {}
    for r in details:
        var  = r["variable"]
        meta = VAR_DEFS.get(var, {})
        if meta.get("type") not in ("continue", "continue_ou_null") or r["nc"] or not r["scorable"]:
            cci_par_variable[var] = {"cci": None, "nc": r["nc"], "ecart": r["ecart"]}
            continue
        seuil_cci = meta.get("seuil_cci", 0.15)
        ecart_norm = r["ecart"] / seuil_cci if (r["ecart"] is not None and seuil_cci > 0) else None
        cci_par_variable[var] = {
            "cci":          None,
            "ecart":        r["ecart"],
            "ecart_norm":   round(ecart_norm, 4) if ecart_norm is not None else None,
            "accord_seuil": r["accord"],
            "nc":           False,
        }

    # ── Phase 3 : CCI global ──────────────────────────────────────────────────
    cci_global_result = _cci_global_depuis_details(details)
    cci_global        = cci_global_result["icc"] if cci_global_result else None

    # ── Phase 4 : κ de Cohen pour Sa ──────────────────────────────────────────
    sa_detail  = next((r for r in details if r["variable"] == "Sa"), None)
    kappa_sa   = None

    if sa_detail and not sa_detail["nc"] and sa_detail["scorable"]:
        kappa_sa = 1.0 if sa_detail["accord"] else 0.0

    # ── Phase 4bis : κ pour m_r (nouveau V7) ──────────────────────────────────
    kappa_m_r = None
    if est_v7:
        mr_detail = next((r for r in details if r["variable"] == "m_r"), None)
        if mr_detail and not mr_detail["nc"] and mr_detail["scorable"]:
            kappa_m_r = 1.0 if mr_detail["accord"] else 0.0

    # ── Phase 5 : verdict global ──────────────────────────────────────────────
    if nc_bloquantes:
        verdict_global = "DONNÉES_INSUFFISANTES"
    elif cci_global is None:
        verdict_global = "NON_CALCULABLE"
    elif cci_global >= SEUIL_CERTIFIE_G:
        verdict_global = "CERTIFIÉ"
    elif cci_global >= SEUIL_REVISION_G:
        verdict_global = "RÉVISION"
    else:
        verdict_global = "REJET"

    # ── Phase 6 : valeurs finales provisoires ─────────────────────────────────
    valeurs_finales = {}
    desaccords      = []
    instructions    = []

    for r in details:
        var  = r["variable"]
        meta = VAR_DEFS.get(var, {})

        if r["nc"]:
            valeurs_finales[var] = NC_SENTINEL
            continue

        if not r["scorable"]:
            # Cas spécial psi_cible null positif : valeur finale = null
            if var == "psi_cible" and r["val_a"] is None and r["val_b"] is None:
                valeurs_finales[var] = None
            else:
                valeurs_finales[var] = None
            continue

        if r["accord"] is True:
            valeurs_finales[var] = r["val_a"]
        elif r["accord"] is False:
            desaccords.append(r)
            if meta["type"] in ("continue", "continue_ou_null"):
                seuil_cci   = meta.get("seuil_cci", 0.15)
                seuil_resol = 2.0 * seuil_cci
                if (r["ecart"] is not None and r["ecart"] <= seuil_resol
                        and r["val_a"] is not None and r["val_b"] is not None):
                    valeurs_finales[var] = round((r["val_a"] + r["val_b"]) / 2, 4)
                    instructions.append({
                        "variable": var,
                        "action":   "MOYENNE_AUTO",
                        "detail":   f"Écart {r['ecart']} ≤ 2×seuil ({seuil_resol}) — moyenne automatique = {valeurs_finales[var]}",
                    })
                else:
                    valeurs_finales[var] = None
                    instructions.append({
                        "variable": var,
                        "action":   "CONFRONTATION_SOURCES",
                        "detail":   f"Écart {r['ecart']} > 2×seuil ({seuil_resol}) — confrontation des sources requise",
                    })
            else:
                valeurs_finales[var] = None
                instructions.append({
                    "variable": var,
                    "action":   "CONFRONTATION_CATEGORIELLE",
                    "detail":   f"Variable catégorielle — désaccord obligatoire à trancher par sources primaires",
                })

    # ── Statistiques ──────────────────────────────────────────────────────────
    n_continues_scorables = sum(1 for r in details
                                 if r["type"] in ("continue", "continue_ou_null") and r["scorable"] and not r["nc"])
    n_accords_seuil       = sum(1 for r in details if r["accord"] is True and not r["nc"])
    n_desaccords          = sum(1 for r in details if r["accord"] is False and not r["nc"])
    Po_seuil              = n_accords_seuil / len(details) if details else 0.0

    # ── Friction vecteur pour mepa_friction_profile.json ──────────────────────
    friction_vecteur = {r["variable"]: r["friction"] for r in details
                        if r["friction"] is not None}

    # ── Construction du rapport ──────────────────────────────────────────────
    return {
        # ── Métadonnées ───────────────────────────────────────────────────────
        "wp_id":              wp_id,
        "codeur_a":           codeur_a,
        "codeur_b":           codeur_b,
        "est_v7":             est_v7,
        "mepa_version":       "7.0-alpha rev. 2.1" if est_v7 else "6.2",

        # ── Scores principaux ────────────────────────────────────────────────
        "cci":                cci_global,
        "kappa":              cci_global,  # alias compatibilité V6.1 → V6.2
        "cci_detail":         cci_global_result,
        "kappa_sa":           kappa_sa,
        "kappa_m_r":          kappa_m_r,  # V7 — nouveau

        # ── NC ────────────────────────────────────────────────────────────────
        "variables_nc":       variables_nc,
        "nc_bloquantes":      nc_bloquantes,
        "n_nc":               len(variables_nc),

        # ── Verdict ───────────────────────────────────────────────────────────
        "verdict":       verdict_global,
        "seuils":        {
            "cci_certifie":    SEUIL_CERTIFIE,
            "cci_global_cert": SEUIL_CERTIFIE_G,
            "cci_revision":    SEUIL_REVISION,
        },

        # ── Statistiques ──────────────────────────────────────────────────────
        "n_variables":            len(VAR_DEFS),
        "n_continues_scorables":  n_continues_scorables,
        "n_accords_seuil":        n_accords_seuil,
        "n_desaccords":           n_desaccords,
        "Po_seuil":               round(Po_seuil, 4),

        # ── Détail par variable ───────────────────────────────────────────────
        "detail_variables":              details,
        "cci_par_variable":              cci_par_variable,
        "friction_vecteur":              friction_vecteur,

        # ── Résolution ────────────────────────────────────────────────────────
        "desaccords":                    desaccords,
        "instructions_resolution":       instructions,
        "valeurs_finales_provisoires":   valeurs_finales,

        # ── Note méthodologique ───────────────────────────────────────────────
        "note_methodologique": (
            "CCI ICC(3,1) two-way mixed consistency (Shrout & Fleiss, 1979). "
            "Calculé sur les variables continues normalisées par leur plage corpus. "
            "κ de Cohen maintenu pour Sa (catégorielle). "
            + ("κ de Cohen aussi pour m_r (V7 — catégorielle ordinale à 3 niveaux). "
               "Variables V7 continues (mu_m, phi, psi_noyau, gamma_local) incluses dans le CCI global. "
               "psi_cible avec null positif traité comme accord sur règle E3 rev. 2.1. "
               if est_v7 else "")
            + "Le CCI par variable individuelle nécessite le corpus multi-WP "
            "(mepa_friction_profile.json). "
            "La reproductibilité mesurée est conditionnelle au modèle LLM — "
            "non une indépendance absolue inter-codeurs (Addendum V6.2 Pilier 1 / Cadre V7-α rev. 2.1 §2ter)."
        ),
    }


# ── ALIAS DE COMPATIBILITÉ ────────────────────────────────────────────────────

def calculer_kappa(path_a: str, path_b: str) -> dict:
    """
    Alias de compatibilité V6.1 → V6.2 → V7.
    Appelle calculer_cci() et retourne le même rapport.
    """
    return calculer_cci(path_a, path_b)


# ── AFFICHAGE CONSOLE ─────────────────────────────────────────────────────────

def afficher_rapport(rapport: dict) -> None:
    """Affichage console lisible pour debug et validation manuelle."""
    est_v7 = rapport.get("est_v7", False)
    version_label = "V7-α rev. 2.1" if est_v7 else "V6.2"

    print(f"\n{'='*66}")
    print(f"  RAPPORT CCI MEPA {version_label} — {rapport['wp_id']}")
    print(f"  Codeur A : {rapport['codeur_a']}  |  Codeur B : {rapport['codeur_b']}")
    print(f"{'='*66}")

    # Score CCI
    cci = rapport['cci']
    if cci is not None:
        print(f"  CCI global = {cci:.4f}  →  {rapport['verdict']}")
        detail = rapport.get('cci_detail')
        if detail:
            print(f"  CI 95%    : [{detail['ci_low']:.4f}, {detail['ci_high']:.4f}]"
                  f"  F={detail['F']:.3f}  p={detail['p']:.4f}  n={detail['n']}")
    else:
        print(f"  CCI global = N/A  →  {rapport['verdict']}")

    if rapport['kappa_sa'] is not None:
        print(f"  κ (Sa)     = {rapport['kappa_sa']:.4f}")

    if est_v7 and rapport.get('kappa_m_r') is not None:
        print(f"  κ (m_r)    = {rapport['kappa_m_r']:.4f}")

    # Variables NC
    if rapport['variables_nc']:
        print(f"\n  ⚠ VARIABLES NC ({len(rapport['variables_nc'])}) : "
              f"{', '.join(rapport['variables_nc'])}")
        if rapport['nc_bloquantes']:
            print(f"  ⛔ NC BLOQUANTES : {', '.join(rapport['nc_bloquantes'])}")

    # Détail par variable
    print(f"\n  DÉTAIL PAR VARIABLE ({len(rapport['detail_variables'])} variables) :")
    for r in rapport['detail_variables']:
        var = r['variable']
        if r['nc']:
            status = '⊘ NC'
        elif r['accord'] is True:
            status = '✓ OK'
        elif r['accord'] is False:
            status = '✗'
        else:
            status = '?'

        ecart_str    = f"  écart={r['ecart']}" if r['ecart'] is not None else ""
        friction_str = f"  F={r['friction']}" if r['friction'] is not None else ""
        note_str     = f"  [{r.get('note', '')}]" if r.get('note') else ""
        print(f"  {status:<5} {var:<14}  A={r['val_a']}  B={r['val_b']}"
              f"{ecart_str}{friction_str}{note_str}")

    # Instructions résolution
    if rapport['instructions_resolution']:
        print(f"\n  RÉSOLUTION REQUISE ({len(rapport['instructions_resolution'])} variables) :")
        for ins in rapport['instructions_resolution']:
            action = ins['action']
            print(f"  → {ins['variable']} [{action}] : {ins['detail']}")

    # Verdict final
    print(f"\n  VERDICT : {rapport['verdict']}")
    verdicts_msg = {
        "CERTIFIÉ":              "✓ CCI ≥ 0.75 — WP validé pour production CONV-A.",
        "RÉVISION":              "⚠ CCI 0.55–0.74 — Résolution désaccords requise, puis recalcul.",
        "REJET":                 "⛔ CCI < 0.55 — Recodage complet requis.",
        "DONNÉES_INSUFFISANTES": "⛔ Variable(s) NC bloquante(s) — Escalade Architecte. WP non simulable en l'état.",
        "NON_CALCULABLE":        "? CCI non calculable — données insuffisantes pour le calcul.",
    }
    msg = verdicts_msg.get(rapport['verdict'], "")
    if msg:
        print(f"  {msg}")

    print(f"{'='*66}\n")


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage : python3 mepa_kappa_calculator.py fiche_A.json fiche_B.json [output.json]")
        print()
        print("  fiche_A.json  : fiche produite par CONV-E (Historien-Codeur)")
        print("  fiche_B.json  : fiche produite par CONV-B (Auditeur, codage indépendant)")
        print("  output.json   : optionnel — rapport complet JSON (alimente friction_profile)")
        print()
        print("Sorties JSON clés :")
        print("  cci              → score CCI global [0,1]")
        print("  kappa            → alias cci (compatibilité V6.1)")
        print("  kappa_sa         → κ Cohen pour Sa")
        print("  kappa_m_r        → κ Cohen pour m_r (V7)")
        print("  variables_nc     → liste des variables NC détectées")
        print("  nc_bloquantes    → variables NC qui bloquent la simulation")
        print("  verdict          → CERTIFIÉ | RÉVISION | REJET | DONNÉES_INSUFFISANTES")
        print("  friction_vecteur → {var: F(v,h)} pour mepa_friction_profile.json")
        print("  est_v7           → True si fiches V7, False si V6.2")
        sys.exit(1)

    path_a   = sys.argv[1]
    path_b   = sys.argv[2]
    path_out = sys.argv[3] if len(sys.argv) >= 4 else None

    rapport = calculer_cci(path_a, path_b)
    afficher_rapport(rapport)

    if path_out:
        with open(path_out, "w", encoding="utf-8") as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        print(f"Rapport JSON sauvegardé : {path_out}")
