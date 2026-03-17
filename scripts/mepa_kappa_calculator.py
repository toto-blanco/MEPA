#!/usr/bin/env python3
"""
================================================================================
MEPA V6.2 — Calculateur CCI inter-codeurs
================================================================================
Statut           : REMPLACEMENT
Cible            : /data/mepa/scripts/mepa_kappa_calculator.py
Remplace         : mepa_kappa_calculator.py v1.x (kappa Cohen pour variables continues)
Rétrocompatibilité :
    - Nouveau champ 'cci' remplace 'kappa' pour les variables continues.
    - Champ 'kappa' maintenu en alias (= cci) pour la session de transition.
    - Champ 'kappa_sa' ajouté pour Sa (catégorielle — kappa Cohen maintenu).
    - Champ 'variables_nc' ajouté — liste des variables NC détectées.
    - Structure 'detail_variables' : ajout du champ 'nc' (bool) par variable.
    - Structure 'valeurs_finales_provisoires' : propage "NC" au lieu de None.
    - Compatible avec mepa_passeport_schema.py v2.0 et mepa_friction_profile.json.
Version          : 2.0.0
MEPA version     : 6.2 Fortifiée
Dépendances      : numpy >= 1.20, scipy >= 1.6 (stdlib : json, sys, math, os)
                   Disponibles dans l'environnement Docker n8n Pi5 confirmé.
================================================================================

Protocole inter-codeurs MEPA V6.2 :

  Métriques :
    Variables continues (8 var.) → CCI ICC(3,1) two-way mixed, consistency
                                    Shrout & Fleiss (1979), McGraw & Wong (1996)
    Variable Sa (catégorielle)   → κ de Cohen exact
                                    (catégorielle ordinale à 4 niveaux — CCI inadapté)

  Seuils de validation (depuis mepa_constants.json, fallback embarqué) :
    CCI / κ ≥ 0.70 → CERTIFIÉ
    CCI / κ ∈ [0.50, 0.70) → RÉVISION
    CCI / κ < 0.50 → REJET

  Variable NC (Non-Codable — Silence Socratique) :
    Une variable est NC si l'une ou les deux fiches portent valeur = "NC".
    Les variables NC sont exclues du calcul CCI (non scorables).
    Elles sont listées dans 'variables_nc' et propagées dans 'valeurs_finales_provisoires'.
    Si une variable NC bloquante est détectée (E_split, gamma, EROI, Sa),
    le verdict global est DONNÉES_INSUFFISANTES — indépendamment du CCI.

Usage :
    python3 mepa_kappa_calculator.py fiche_A.json fiche_B.json [output.json]

    fiche_A.json : fiche produite par CONV-E (Historien-Codeur)
    fiche_B.json : fiche produite par CONV-B (Auditeur, codage indépendant)
    output.json  : optionnel — rapport complet en JSON (alimente friction_profile)
"""

import json, sys, math, os
from typing import Optional, Tuple, List, Dict, Any

import numpy as np
from scipy import stats

# ── CHEMIN CONSTANTS (fallback embarqué si fichier absent) ────────────────────
MEPA_SCRIPTS_DIR = os.environ.get("MEPA_SCRIPTS_DIR", "/data/mepa/scripts")
CONSTANTS_PATH   = os.path.join(MEPA_SCRIPTS_DIR, "mepa_constants.json")

# ── CHARGEMENT mepa_constants.json ────────────────────────────────────────────

def _charger_constants() -> dict:
    """
    Charge mepa_constants.json.
    Si absent, retourne le fallback embarqué (identique au fichier).
    Garantit la robustesse sur Pi5 (HDD débranché, fichier corrompu).
    """
    try:
        with open(CONSTANTS_PATH) as f:
            return json.load(f)
    except Exception:
        # Fallback embarqué — synchronisé avec mepa_constants.json v1.0
        return {
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
            "seuils_validation": {
                "cci":        {"certifie": 0.70, "revision": 0.50},
                "kappa_sa":   {"certifie": 0.70, "revision": 0.50},
                "cci_global": {"certifie": 0.75, "revision": 0.55},
                "friction_outlier_seuil": {"valeur": 2.0},
            },
            "nc_protocol": {
                "valeur_sentinel":         "NC",
                "variables_nc_bloquantes": ["E_split", "gamma", "EROI", "Sa"],
            },
        }


CONSTANTS = _charger_constants()
# Filtrer les clés de métadonnées ($description, etc.) — ne garder que les vraies variables
VAR_DEFS  = {k: v for k, v in CONSTANTS["variables_mepa"].items()
             if not k.startswith("$") and isinstance(v, dict)}
SEUILS    = CONSTANTS["seuils_validation"]
NC_SENTINEL           = CONSTANTS["nc_protocol"]["valeur_sentinel"]
NC_BLOQUANTES         = set(CONSTANTS["nc_protocol"]["variables_nc_bloquantes"])
FRICTION_OUTLIER_SEUIL = CONSTANTS["seuils_validation"]["friction_outlier_seuil"]["valeur"]

# Seuils de validation
SEUIL_CERTIFIE   = SEUILS["cci"]["certifie"]        # 0.70
SEUIL_REVISION   = SEUILS["cci"]["revision"]         # 0.50
SEUIL_CERTIFIE_G = SEUILS["cci_global"]["certifie"]  # 0.75
SEUIL_REVISION_G = SEUILS["cci_global"]["revision"]  # 0.55
SEUIL_KAPPA_SA   = SEUILS["kappa_sa"]["certifie"]    # 0.70


# ── EXTRACTION DE VALEUR DEPUIS FICHE ────────────────────────────────────────

def _extraire_valeur(fiche: dict, var: str) -> Tuple[Any, bool]:
    """
    Extrait la valeur d'une variable depuis une fiche de codage.

    Retourne (valeur, is_nc) où :
      - valeur : float | int | None | "NC"
      - is_nc  : True si la valeur est la sentinelle NC

    Gère les deux formats de fiche :
      Format A : fiche["variables"][var]["valeur"]  (standard V6.2)
      Format B : fiche[var]                          (format simplifié)
    """
    # Format A (standard)
    entry = fiche.get("variables", {}).get(var)
    if entry is not None:
        val = entry.get("valeur")
    else:
        # Format B (fallback)
        val = fiche.get(var)

    if val is None:
        return None, False

    # Détection NC
    if isinstance(val, str) and val.strip().upper() == NC_SENTINEL:
        return NC_SENTINEL, True

    # Conversion numérique
    if isinstance(val, str) and val.lower() in ("null", "none", ""):
        return None, False

    try:
        meta = VAR_DEFS.get(var, {})
        if meta.get("type") == "categorielle":
            return int(float(val)), False
        return float(val), False
    except (ValueError, TypeError):
        return None, False


# ── CCI ICC(3,1) — TWO-WAY MIXED, CONSISTENCY ────────────────────────────────

def _cci_icc31(values_a: List[float], values_b: List[float]) -> dict:
    """
    Calcule le CCI ICC(3,1) — Two-way mixed, single measures, consistency.

    Formule ANOVA à deux facteurs (Shrout & Fleiss, 1979) :
        MSr = carré moyen inter-sujets (variance entre cas historiques)
        MSe = carré moyen résiduel (erreur de mesure)
        MSc = carré moyen inter-codeurs (biais de codeur)

        ICC(3,1) = (MSr - MSe) / (MSr + (k-1) * MSe)
        avec k = 2 codeurs

    Intervalle de confiance 95% selon Shrout & Fleiss (1979) eq. 16.

    Retourne un dict avec icc, ci_low, ci_high, F, df1, df2, p, n.
    Retourne None si n < 2 (pas assez de données).
    """
    a = np.array(values_a, dtype=float)
    b = np.array(values_b, dtype=float)
    n = len(a)
    k = 2

    if n < 2:
        return None

    X          = np.column_stack([a, b])
    grand_mean = X.mean()
    row_means  = X.mean(axis=1)
    col_means  = X.mean(axis=0)

    SSr = k * float(np.sum((row_means - grand_mean) ** 2))
    SSc = n * float(np.sum((col_means - grand_mean) ** 2))
    SSt = float(np.sum((X - grand_mean) ** 2))
    SSe = SSt - SSr - SSc

    df_r = n - 1
    df_e = (n - 1) * (k - 1)

    MSr = SSr / df_r if df_r > 0 else 0.0
    MSe = SSe / df_e if df_e > 0 else 0.0

    # Cas dégénérés
    if MSr == 0.0 and MSe == 0.0:
        # Accord parfait (toutes valeurs identiques)
        return {"icc": 1.0, "ci_low": 1.0, "ci_high": 1.0,
                "F": float("inf"), "df1": df_r, "df2": df_e, "p": 0.0, "n": n}
    if MSe == 0.0:
        return {"icc": 1.0, "ci_low": 1.0, "ci_high": 1.0,
                "F": float("inf"), "df1": df_r, "df2": df_e, "p": 0.0, "n": n}

    icc     = float(np.clip((MSr - MSe) / (MSr + (k - 1) * MSe), -1.0, 1.0))
    F_ratio = MSr / MSe

    # Intervalle de confiance 95%
    alpha = 0.05
    try:
        F_L     = F_ratio / stats.f.ppf(1 - alpha / 2, df_r, df_e)
        F_U     = F_ratio * stats.f.ppf(1 - alpha / 2, df_e, df_r)
        ci_low  = float(np.clip((F_L - 1) / (F_L + k - 1), -1.0, 1.0))
        ci_high = float(np.clip((F_U - 1) / (F_U + k - 1), -1.0, 1.0))
    except Exception:
        ci_low, ci_high = -1.0, 1.0

    p_val = float(1 - stats.f.cdf(F_ratio, df_r, df_e))

    return {
        "icc":     round(icc,     4),
        "ci_low":  round(ci_low,  4),
        "ci_high": round(ci_high, 4),
        "F":       round(F_ratio, 4),
        "df1":     df_r,
        "df2":     df_e,
        "p":       round(p_val,   6),
        "n":       n,
    }


# ── KAPPA DE COHEN (pour Sa — variable catégorielle) ─────────────────────────

def _kappa_cohen_categoriel(val_a: Any, val_b: Any, var: str) -> dict:
    """
    κ de Cohen pour une variable catégorielle à valeurs nominales/ordinales.
    Sur une seule paire de valeurs (n=1 par WP) :
      accord = 1 si val_a == val_b, 0 sinon
    Le κ est calculé sur l'ensemble du corpus (multi-WP) via kappa_corpus().
    Ici, retourne l'accord binaire pour un WP individuel.
    """
    if val_a is None or val_b is None:
        return {"accord": None, "ecart": None, "scorable": False}

    accord = (val_a == val_b)
    ecart  = 0 if accord else abs(val_a - val_b) if isinstance(val_a, (int, float)) else 1
    return {
        "accord":   accord,
        "ecart":    float(ecart),
        "scorable": True,
    }


def _kappa_cohen_corpus(accords_sa: List[bool]) -> float:
    """
    κ de Cohen sur la série des accords/désaccords Sa pour l'ensemble des WP.
    Formule binaire correcte (Fleiss, 1971) :
        Po = proportion d'accords observés
        Pe = Po² + (1-Po)²   [pour variable binaire accord/désaccord]
        κ  = (Po - Pe) / (1 - Pe)
    """
    n = len(accords_sa)
    if n == 0:
        return 0.0
    Po = sum(1 for a in accords_sa if a is True) / n
    Pe = Po ** 2 + (1 - Po) ** 2
    if Pe >= 1.0:
        return 1.0
    kappa = (Po - Pe) / (1 - Pe)
    return round(float(kappa), 4)


# ── ACCORD VARIABLE CONTINUE (pour detail par WP) ────────────────────────────

def _accord_continu(val_a: float, val_b: float, seuil: float) -> dict:
    """
    Accord binaire sur une variable continue pour un WP donné.
    Utilisé dans le rapport détaillé et le calcul de friction.
    L'accord au seuil n'entre PAS dans le CCI — c'est une information subsidiaire.
    """
    ecart = abs(val_a - val_b)
    accord = ecart <= seuil
    return {
        "accord": accord,
        "ecart":  round(ecart, 4),
        "seuil":  seuil,
    }


# ── RÉSOLUTION DES DÉSACCORDS ─────────────────────────────────────────────────

def _resolution_desaccords(resultats: List[dict]) -> List[dict]:
    """
    Protocole §2.3 — Instructions de résolution pour les variables en désaccord.
    Seuil de résolution automatique (moyenne) : écart ≤ 2 × seuil_cci.
    """
    instructions = []
    for r in resultats:
        if r.get("accord") is False and not r.get("nc"):
            var   = r["variable"]
            meta  = VAR_DEFS.get(var, {})
            ecart = r.get("ecart")

            if meta.get("type") == "categorielle":
                instructions.append({
                    "variable": var,
                    "action":   "CONFRONTATION_OBLIGATOIRE",
                    "detail":   (
                        f"Sa/trajectoire : désaccord exact. Valeurs : A={r['val_a']} B={r['val_b']}. "
                        "Pas de moyenne possible sur variable ordinale. "
                        "Confrontation sources obligatoire — troisième codeur si pas de consensus."
                    ),
                })
            elif ecart is not None:
                seuil_cci    = meta.get("seuil_cci", 0.15)
                seuil_resol  = 2.0 * seuil_cci
                if ecart <= seuil_resol and r["val_a"] is not None and r["val_b"] is not None:
                    moyenne = (r["val_a"] + r["val_b"]) / 2
                    instructions.append({
                        "variable":        var,
                        "action":          "MOYENNE",
                        "valeur_retenue":  round(moyenne, 4),
                        "detail":          (
                            f"Écart {ecart:.4f} ≤ 2×seuil ({seuil_resol:.4f}) "
                            f"→ valeur retenue = {moyenne:.4f}"
                        ),
                    })
                else:
                    instructions.append({
                        "variable": var,
                        "action":   "CONFRONTATION_SOURCES",
                        "detail":   (
                            f"Écart {ecart:.4f} > 2×seuil ({seuil_resol:.4f}) "
                            f"— source la plus haute (N1→N6) prioritaire. "
                            f"Valeurs : A={r['val_a']} B={r['val_b']}"
                        ),
                    })
    return instructions


# ── CALCUL CCI GLOBAL ─────────────────────────────────────────────────────────

def _cci_global_depuis_details(details: List[dict]) -> Optional[dict]:
    """
    CCI global calculé sur l'ensemble des valeurs continues scorables (hors NC, hors Sa).
    Agrège toutes les paires (val_a, val_b) des variables continues scorables.
    N.B. : les variables continues sont sur des échelles différentes.
    On normalise par la plage [min, max] de chaque variable avant d'agréger.
    """
    all_a, all_b = [], []
    for r in details:
        var  = r["variable"]
        meta = VAR_DEFS.get(var, {})
        if meta.get("type") != "continue":
            continue
        if r.get("nc") or not r.get("scorable"):
            continue
        if r["val_a"] is None or r["val_b"] is None:
            continue
        echelle = meta.get("echelle", [0.0, 1.0])
        plage   = echelle[1] - echelle[0] if echelle[1] > echelle[0] else 1.0
        # Normalisation [0,1]
        all_a.append((r["val_a"] - echelle[0]) / plage)
        all_b.append((r["val_b"] - echelle[0]) / plage)

    if len(all_a) < 2:
        return None

    return _cci_icc31(all_a, all_b)


# ── CALCUL FRICTION ───────────────────────────────────────────────────────────

def _calculer_friction(val_a: Optional[float], val_b: Optional[float],
                       seuil_cci: float, is_nc: bool) -> Optional[float]:
    """
    F(v, h) = |val_a - val_b| / seuil_cci(v)
    F = None si NC ou non scorable.
    F ∈ [0, ∞) — F=0 accord parfait, F=1 désaccord au seuil exact, F>1 désaccord sig.
    """
    if is_nc or val_a is None or val_b is None:
        return None
    return round(abs(val_a - val_b) / seuil_cci, 4) if seuil_cci > 0 else None


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
      - mepa_passeport_schema.py v2.0 (champs 'cci', 'kappa_sa', 'variables_nc')
      - mepa_friction_profile.json (champ 'friction_vecteur')
      - mepa_node2_audit_v62.js (champ 'variables_nc' pour contrôle C13)
    """
    fiche_a = charger_fiche(path_a)
    fiche_b = charger_fiche(path_b)

    wp_id    = fiche_a.get("wp_id", fiche_b.get("wp_id", "?"))
    codeur_a = fiche_a.get("codeur", "CONV-E")
    codeur_b = fiche_b.get("codeur", "CONV-B")

    # ── Phase 1 : extraction et détection NC ──────────────────────────────────
    details       = []
    variables_nc  = []
    nc_bloquantes = []

    for var, meta in VAR_DEFS.items():
        val_a, is_nc_a = _extraire_valeur(fiche_a, var)
        val_b, is_nc_b = _extraire_valeur(fiche_b, var)
        is_nc = is_nc_a or is_nc_b

        seuil_cci = meta.get("seuil_cci")  # None pour Sa

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
    # Le CCI par variable nécessite plusieurs WP (corpus).
    # Sur un seul WP, on calcule le CCI global depuis les détails multi-variables normalisées.
    # Pour le rapport par WP, on rapporte l'écart normalisé comme proxy.
    cci_par_variable = {}
    for r in details:
        var  = r["variable"]
        meta = VAR_DEFS.get(var, {})
        if meta.get("type") != "continue" or r["nc"] or not r["scorable"]:
            cci_par_variable[var] = {"cci": None, "nc": r["nc"], "ecart": r["ecart"]}
            continue
        # Sur un seul WP : l'écart normalisé comme information
        seuil_cci = meta.get("seuil_cci", 0.15)
        ecart_norm = r["ecart"] / seuil_cci if (r["ecart"] is not None and seuil_cci > 0) else None
        cci_par_variable[var] = {
            "cci":          None,          # calculable uniquement sur corpus multi-WP
            "ecart":        r["ecart"],
            "ecart_norm":   round(ecart_norm, 4) if ecart_norm is not None else None,
            "accord_seuil": r["accord"],   # accord au seuil (info subsidiaire)
            "nc":           False,
        }

    # ── Phase 3 : CCI global (sur les variables continues scorables) ───────────
    cci_global_result = _cci_global_depuis_details(details)
    cci_global        = cci_global_result["icc"] if cci_global_result else None

    # ── Phase 4 : κ de Cohen pour Sa ──────────────────────────────────────────
    sa_detail  = next((r for r in details if r["variable"] == "Sa"), None)
    kappa_sa   = None
    sa_accord  = None

    if sa_detail and not sa_detail["nc"] and sa_detail["scorable"]:
        sa_accord = sa_detail["accord"]
        # κ sur 1 paire = accord (1.0) ou désaccord (0.0 ou négatif selon la formule)
        # On rapporte l'accord binaire — le κ corpus sera calculé dans friction_profile
        kappa_sa = 1.0 if sa_accord else 0.0

    # ── Phase 5 : verdict global ───────────────────────────────────────────────
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

    for r in details:
        var  = r["variable"]
        meta = VAR_DEFS.get(var, {})

        if r["nc"]:
            valeurs_finales[var] = NC_SENTINEL
            continue

        if not r["scorable"]:
            valeurs_finales[var] = None
            continue

        if r["accord"] is True:
            valeurs_finales[var] = r["val_a"]
        elif r["accord"] is False:
            desaccords.append(r)
            # Résolution automatique si écart ≤ 2 × seuil
            if meta["type"] == "continue":
                seuil_cci   = meta.get("seuil_cci", 0.15)
                seuil_resol = 2.0 * seuil_cci
                if (r["ecart"] is not None and r["ecart"] <= seuil_resol
                        and r["val_a"] is not None and r["val_b"] is not None):
                    valeurs_finales[var] = round((r["val_a"] + r["val_b"]) / 2, 4)
                else:
                    valeurs_finales[var] = None  # confrontation requise
            else:
                valeurs_finales[var] = None      # confrontation obligatoire Sa
        else:
            valeurs_finales[var] = None

    # ── Phase 7 : instructions de résolution ──────────────────────────────────
    instructions = _resolution_desaccords(desaccords)

    # ── Phase 8 : vecteur de friction (pour friction_profile) ─────────────────
    friction_vecteur = {
        r["variable"]: r["friction"] for r in details
    }

    # ── Statistiques de synthèse ───────────────────────────────────────────────
    n_continues_scorables = sum(
        1 for r in details
        if VAR_DEFS.get(r["variable"], {}).get("type") == "continue"
        and r["scorable"]
    )
    n_accords_seuil = sum(1 for r in details if r.get("accord") is True)
    n_desaccords    = len(desaccords)
    Po_seuil        = round(n_accords_seuil / max(n_continues_scorables + (1 if sa_accord is not None else 0), 1), 4)

    # ── Rapport final ──────────────────────────────────────────────────────────
    return {
        # ── Identité ──────────────────────────────────────────────────────────
        "wp_id":     wp_id,
        "codeur_a":  codeur_a,
        "codeur_b":  codeur_b,

        # ── Scores principaux ─────────────────────────────────────────────────
        "cci":           cci_global,       # CCI global (variables continues normalisées)
        "cci_detail":    cci_global_result, # Dict complet avec CI, F, p
        "kappa_sa":      kappa_sa,          # κ de Cohen pour Sa (1.0 ou 0.0 sur 1 WP)
        "kappa":         cci_global,        # ALIAS de compatibilité transitoire — = cci

        # ── Variables NC ──────────────────────────────────────────────────────
        "variables_nc":       variables_nc,   # Toutes les variables NC (bloquantes + non-bloquantes)
        "nc_bloquantes":      nc_bloquantes,  # Variables NC qui bloquent la simulation
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
        "n_nc":                   len(variables_nc),
        "Po_seuil":               Po_seuil,

        # ── Détail par variable ────────────────────────────────────────────────
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
            "Le CCI par variable individuelle nécessite le corpus multi-WP "
            "(mepa_friction_profile.json). "
            "La reproductibilité mesurée est conditionnelle au modèle LLM — "
            "non une indépendance absolue inter-codeurs (Addendum V6.2, Pilier 1)."
        ),
    }


# ── ALIAS DE COMPATIBILITÉ ────────────────────────────────────────────────────

def calculer_kappa(path_a: str, path_b: str) -> dict:
    """
    Alias de compatibilité V6.1 → V6.2.
    Appelle calculer_cci() et retourne le même rapport.
    Permet aux scripts non encore migrés d'appeler l'ancienne signature.
    """
    return calculer_cci(path_a, path_b)


# ── AFFICHAGE CONSOLE ─────────────────────────────────────────────────────────

def afficher_rapport(rapport: dict) -> None:
    """Affichage console lisible pour debug et validation manuelle."""
    print(f"\n{'='*66}")
    print(f"  RAPPORT CCI MEPA V6.2 — {rapport['wp_id']}")
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

    # Variables NC
    if rapport['variables_nc']:
        print(f"\n  ⚠ VARIABLES NC ({len(rapport['variables_nc'])}) : "
              f"{', '.join(rapport['variables_nc'])}")
        if rapport['nc_bloquantes']:
            print(f"  ⛔ NC BLOQUANTES : {', '.join(rapport['nc_bloquantes'])}")

    # Détail par variable
    print(f"\n  DÉTAIL PAR VARIABLE :")
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
        print(f"  {status:<5} {var:<12}  A={r['val_a']}  B={r['val_b']}"
              f"{ecart_str}{friction_str}")

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
        print("  variables_nc     → liste des variables NC détectées")
        print("  nc_bloquantes    → variables NC qui bloquent la simulation")
        print("  verdict          → CERTIFIÉ | RÉVISION | REJET | DONNÉES_INSUFFISANTES")
        print("  friction_vecteur → {var: F(v,h)} pour mepa_friction_profile.json")
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
