#!/usr/bin/env python3
"""
================================================================================
MEPA V7-alpha rev. 2.1 — mepa_passeport_schema.py
================================================================================
Statut           : EXTENSION V7
Cible            : /data/mepa/scripts/mepa_passeport_schema.py
Remplace         : mepa_passeport_schema.py v2.0.0 (V6.2)
Rétrocompatibilité :
  - API publique V6.2 intégralement préservée :
      generer_passeport(result_path, rapport_path, cci_rapport_path, passeport_out)
      passeport_depuis_result(result, result_path)
  - Les fiches V6.2 continuent à produire des passeports identiques au format V6.2
    (aucun champ V7 ajouté si _result.json ne contient pas de section v7_alpha).
  - Les fiches V7 (présence de meta.mepa_version = "7.0-alpha rev. 2.1" ou
    simulation.v7_alpha_diagnostic) déclenchent l'enrichissement V7 automatique
    dans le bloc simulation et dans statut_global.
  - Hash SHA-256 : calcul inchangé (result.json canonique + rapport.md si présent).
  - Champs NC : inchangés. Ajout de psi_noyau et gamma_local dans la liste des
    NC bloquantes V7.

Version          : 3.0.0
MEPA version     : 7.0-alpha rev. 2.1
Dépendances      : json, sys, hashlib, datetime, os (stdlib uniquement)
================================================================================

Extensions V7 vs V6.2 :
-----------------------

[V7-P1] LABELS_D4 étendus à 10 labels (ajout (α) Cristallisation sacrificielle).
        Utilisé pour la validation des trajectoires dans le passeport.

[V7-P2] Champs V7 ajoutés dans le bloc 'simulation' du passeport :
        - v7_alpha_diagnostic     : détail de l'évaluation des conditions C1-C5
        - branche_annotation       : EXPLICATIVE | CATCHALL (V7-C4 rev. 2.1)
        - a_r_c_eff_calc           : valeur calculée de la clause de repli
        - chute_C_metric           : (C_max - C_final) / C_max (pour branche b expl)
        - rampe_mod_mimetique_active : bool (la rampe a-t-elle été activée ?)

[V7-P3] Champs V7 ajoutés dans le bloc 'identite' du passeport :
        - variables_v7             : les six variables codées (résumé)
        - fiche_v7                 : bool (la fiche d'entrée était-elle V7 ?)

[V7-P4] statut_global étendu pour les cas V7 :
        - CONDITIONNELLE_V7        : trajectoire attendue non produite mais
          échec pré-enregistré (cas Allemagne nazie, Décision V7-D1 rev. 4 §5)
        - Le verdict global reflète les conditions de certification V7-γ rev. 2.

[V7-P5] Hash SHA-256 : inchangé. Le hash du result.json canonique capture
        automatiquement les nouveaux champs V7 dans simulation.v7_alpha_diagnostic.

Rôle dans le pipeline WF1 :
  Nœud 7 (Export) appelle ce script après simulation réussie.
  Entrées :
    - result.json     : sortie du Runner (mepa_runner_v3_v7.py en V7, ou v2_gamma en V6.2)
    - rapport.md      : rédigé par CONV-A (optionnel mais recommandé)
    - cci_rapport.json: sortie de mepa_kappa_calculator.py (optionnel)
  Sortie :
    - passeport.json  : certificat de traçabilité complet (V6.2 ou V7)

Usage :
  python3 mepa_passeport_schema.py result.json [rapport.md] [cci_rapport.json] [passeport_out.json]
"""

import json
import sys
import hashlib
import datetime
import os
from typing import Optional

# ── Chemins canoniques Pi5 ────────────────────────────────────────────────────
MEPA_SCRIPTS_DIR = os.environ.get("MEPA_SCRIPTS_DIR", "/data/mepa/scripts")
MEPA_OUTPUT_DIR  = os.environ.get("MEPA_OUTPUT_DIR",  "/data/mepa/outputs")

# ── Métadonnées IA codeur (traçabilité provenance) — inchangées V6.2 ─────────
IA_CODEUR = {
    "modele":           "claude-sonnet-4-6",
    "famille":          "Claude 4",
    "fournisseur":      "Anthropic",
    "role_pipeline":    "CONV-E (Historien-Codeur) / CONV-B (Auditeur) / CONV-A (Rédacteur)",
    "temperature":      0.0,
    "protocole":        "Double aveugle n8n — étanchéité informationnelle garantie par le workflow",
    "note":             (
        "Les valeurs codées sont produites sous protocole d'inférence contrôlé "
        "(Addendum Théorique V6.2, Pilier 4). La reproductibilité mesurée est "
        "conditionnelle au modèle LLM — non une indépendance absolue inter-codeurs."
    ),
}

MEPA_VERSION_META = {
    "version":          "7.0",
    "sous_version":     "alpha rev. 2.1",
    "label":            "MEPA V7-alpha rev. 2.1",
    "runner":           "mepa_runner_v3_v7 v3.0 (LSODA)",
    "runner_legacy":    "mepa_runner_v2_gamma v2.1.1 (Euler dt=1, cas V6.2)",
    "audit":            "mepa_node2_audit_v7 v3.0",
    "kappa_calc":       "mepa_kappa_calculator v3.0",
    "passeport":        "mepa_passeport_schema v3.0",
    "constants":        "mepa_constants v1.3.0",
    "whitelist":        "mepa_whitelist_keys v3.0.0",
    "cadre_theorique":  "MEPA_cadre_theorique_V7_alpha_rev2_1.docx",
    "decision_gouvernance": "MEPA_Decision_V7_D1_rev4.md",
    "addendum_ingenierie":  "MEPA_Addendum_V7_beta_ING.md",
}

# ── Labels D4 officiels V7 (10 labels) ────────────────────────────────────────
LABELS_D4_V7 = [
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
]

# ── Annotation EXPLICATIVE/CATCHALL des branches (V7-C4 rev. 2.1) ─────────────
BRANCHES_ANNOTATION_V7 = {
    "(α) Cristallisation sacrificielle d'État": "EXPLICATIVE",
    "(d) V7-C2 sans bascule":                   "EXPLICATIVE",
    "(a) Rupture transformatrice":              "EXPLICATIVE",
    "(b) Répression réussie — explicative":     "EXPLICATIVE",
    "(b) Répression réussie — catchall":        "CATCHALL",
    "(b) Répression réussie":                   "CATCHALL",  # fallback V6.2
    "(c) Stase polarisée":                      "EXPLICATIVE",
    "(c) Stase / ambigu":                       "EXPLICATIVE",  # fallback V6.2
    "(e) Réforme institutionnelle":             "EXPLICATIVE",
    "(f) Réforme technologique":                "EXPLICATIVE",
    "(g) Dérive oligarchique":                  "EXPLICATIVE",
    "(h) Stabilité basse — catchall":           "CATCHALL",
    "(h) Stabilité":                            "CATCHALL",  # fallback V6.2
    "(i) Blocage anomique":                     "EXPLICATIVE",
    "(d) Effondrement progressif":              "EXPLICATIVE",
    "(d) Dissolution":                          "EXPLICATIVE",
    "(γ) Transformation forcée":                "EXPLICATIVE",
}

# ── Seuils de certification (miroir mepa_constants.json) ─────────────────────
SEUIL_CCI_CERTIFIE    = 0.70
SEUIL_CCI_GLOBAL_CERT = 0.75
SEUIL_REVISION        = 0.55


# ── Utilitaires hash ──────────────────────────────────────────────────────────

def _sha256_file(path: str) -> Optional[str]:
    """Calcule le SHA-256 d'un fichier. Retourne None si fichier absent."""
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except FileNotFoundError:
        return None
    except Exception as e:
        return f"ERREUR:{e}"


def _sha256_str(s: str) -> str:
    """SHA-256 d'une chaîne UTF-8."""
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _sha256_dict(d: dict) -> str:
    """SHA-256 d'un dict sérialisé en JSON canonique (clés triées)."""
    canonical = json.dumps(d, sort_keys=True, ensure_ascii=False)
    return _sha256_str(canonical)


# ── Détection fiche V7 depuis result.json ────────────────────────────────────

def _est_result_v7(result: dict) -> bool:
    """
    Détecte si le result.json provient d'une simulation V7-beta.
    Critères (OR) :
      - meta.mepa_version contient "7.0" ou "v7"
      - meta.runner contient "v3_v7" ou "v7" ou "LSODA"
      - simulation.v7_alpha_diagnostic présent
      - simulation.rampe_mod_mimetique_active présent
      - meta.fiche_v7 == True
    """
    meta = result.get("meta", {})
    sim = result.get("simulation", {})

    mepa_ver = str(meta.get("mepa_version", "")).lower()
    runner = str(meta.get("runner", "")).lower()

    if "7.0" in mepa_ver or "v7" in mepa_ver:
        return True
    if "v3_v7" in runner or "v7" in runner or "lsoda" in runner:
        return True
    if "v7_alpha_diagnostic" in sim:
        return True
    if "rampe_mod_mimetique_active" in sim:
        return True
    if meta.get("fiche_v7") is True:
        return True
    return False


# ── Extraction depuis result.json ─────────────────────────────────────────────

def _extraire_identite(result: dict) -> dict:
    """Extrait les champs d'identité depuis le résultat Runner."""
    meta = result.get("meta", {})
    sim  = result.get("simulation", {})
    vrd  = result.get("verdict", {})

    est_v7 = _est_result_v7(result)

    identite = {
        "wp_id":               meta.get("wp_id", "?"),
        "cas":                 meta.get("cas", ""),
        "cluster":             meta.get("cluster", ""),
        "sa":                  meta.get("sa"),
        "sa_modulator":        meta.get("sa_modulator", ""),
        "trajectoire_attendue":meta.get("trajectoire_attendue", ""),
        "trajectoire_diagn":   sim.get("traj", ""),
        "concordance":         vrd.get("concordance_attendue", False),
        "robustesse":          vrd.get("robustesse", ""),
        "t_bascule":           sim.get("t_bascule"),
        "dC_rel":              sim.get("dC_rel"),
        "dI_rel":              sim.get("dI_rel"),
        "FR_max":              sim.get("FR_max"),
        "theta_C_effectif":    meta.get("theta_C_effectif", sim.get("theta_C_used", 0.30)),
        "theta_I_effectif":    meta.get("theta_I_effectif", sim.get("theta_I_used", 0.22)),
        "cmd_type":            meta.get("cmd_type", ""),
        "integration":         meta.get("integration", "Euler_explicite_dt1"),
        "generated_at_runner": meta.get("generated_at", ""),
        "fiche_v7":            est_v7,
    }

    # --- V7 : ajout du bloc variables_v7 dans identite si fiche V7 ---
    if est_v7:
        vars_v7 = meta.get("variables_v7") or sim.get("variables_v7") or {}
        identite["variables_v7"] = {
            "m_r":          (vars_v7.get("m_r") or {}).get("valeur") if isinstance(vars_v7.get("m_r"), dict) else vars_v7.get("m_r"),
            "mu_m":         (vars_v7.get("mu_m") or {}).get("valeur") if isinstance(vars_v7.get("mu_m"), dict) else vars_v7.get("mu_m"),
            "phi":          (vars_v7.get("phi") or {}).get("valeur") if isinstance(vars_v7.get("phi"), dict) else vars_v7.get("phi"),
            "psi_noyau":    (vars_v7.get("psi_noyau") or {}).get("valeur") if isinstance(vars_v7.get("psi_noyau"), dict) else vars_v7.get("psi_noyau"),
            "psi_cible":    (vars_v7.get("psi_cible") or {}).get("valeur") if isinstance(vars_v7.get("psi_cible"), dict) else vars_v7.get("psi_cible"),
            "gamma_local":  (vars_v7.get("gamma_local") or {}).get("valeur") if isinstance(vars_v7.get("gamma_local"), dict) else vars_v7.get("gamma_local"),
        }

    return identite


def _extraire_simulation_digest(result: dict) -> dict:
    """Extrait les indicateurs clés de simulation pour le passeport. Étendu V7."""
    sim = result.get("simulation", {})
    vrd = result.get("verdict", {})
    sn1 = result.get("stress_n1", {})

    digest = {
        "traj":             sim.get("traj"),
        "t_bascule":        sim.get("t_bascule"),
        "dC_rel":           sim.get("dC_rel"),
        "dI_rel":           sim.get("dI_rel"),
        "dCdt_bascule":     sim.get("dCdt_bascule"),
        "FR_bascule":       sim.get("FR_bascule"),
        "FR_max":           sim.get("FR_max"),
        "FR_final":         sim.get("FR_final"),
        "C_max":            sim.get("C_max"),
        "C_final":          sim.get("C_final"),
        "I_min_sim":        sim.get("I_min_sim"),
        "I_final":          sim.get("I_final"),
        "S_final":          sim.get("S_final"),
        "L_final":          sim.get("L_final"),
        "theta_C_used":     sim.get("theta_C_used"),
        "theta_I_used":     sim.get("theta_I_used"),
        "robustesse":       vrd.get("robustesse"),
        "trajs_set_n1":     vrd.get("trajs_set_n1", []),
        "concordance":      vrd.get("concordance_attendue"),
        "stress_n1_opt":    sn1.get("optimiste", {}).get("traj"),
        "stress_n1_pes":    sn1.get("pessimiste", {}).get("traj"),
        "tableau_s2_rows":  len(sim.get("tableau_S2", [])),
    }

    # --- V7 : enrichissement si result V7 ---
    if _est_result_v7(result):
        digest["v7_alpha_diagnostic"]      = sim.get("v7_alpha_diagnostic", {})
        digest["rampe_mod_mimetique_active"] = sim.get("rampe_mod_mimetique_active", False)
        digest["a_r_c_eff_calc"]           = sim.get("a_r_c_eff_calc")
        digest["chute_C_metric"]           = sim.get("chute_C_metric")
        digest["integrator"]               = "LSODA"

        # Annotation EXPLICATIVE/CATCHALL de la branche.
        # Priorité : valeur calculée par le runner V7 (déjà correcte dans sim).
        # Fallback dict pour fiches V6.2 sans ce champ.
        # Ne pas recalculer depuis traj seul : "(b) Répression réussie" est
        # utilisé pour EXPLICATIVE et CATCHALL — seul le runner sait lequel.
        traj = sim.get("traj", "")
        digest["branche_annotation"] = (
            sim.get("branche_annotation")
            or BRANCHES_ANNOTATION_V7.get(traj, "UNKNOWN")
        )

    return digest


# ── Construction du passeport ─────────────────────────────────────────────────

def generer_passeport(
    result_path:      str,
    rapport_path:     Optional[str] = None,
    cci_rapport_path: Optional[str] = None,
    passeport_out:    Optional[str] = None,
) -> dict:
    """
    Génère le passeport de certification MEPA pour un WP.

    Paramètres :
      result_path      : chemin vers <wp_id>_result.json (Runner V6.2 ou V7)
      rapport_path     : chemin vers <wp_id>_rapport.md  (CONV-A, optionnel)
      cci_rapport_path : chemin vers <wp_id>_cci.json    (kappa_calculator, optionnel)
      passeport_out    : chemin de sortie du passeport (auto si None)

    Retourne le dict passeport.
    """
    # ── Chargement result.json ────────────────────────────────────────────────
    if not os.path.isfile(result_path):
        raise FileNotFoundError(f"result.json introuvable : {result_path}")

    with open(result_path) as f:
        result = json.load(f)

    # ── Chargement cci_rapport.json (optionnel) ───────────────────────────────
    cci_rapport = None
    if cci_rapport_path and os.path.isfile(cci_rapport_path):
        try:
            with open(cci_rapport_path) as f:
                cci_rapport = json.load(f)
        except Exception as e:
            print(f"[PASSEPORT WARN] cci_rapport.json illisible : {e}", file=sys.stderr)

    # ── Métadonnées de base ───────────────────────────────────────────────────
    ts_now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    identite = _extraire_identite(result)
    sim_digest = _extraire_simulation_digest(result)
    wp_id = identite["wp_id"]
    est_v7 = identite["fiche_v7"]

    # ── Certification inter-codeurs ───────────────────────────────────────────
    cci_global  = None
    kappa_sa    = None
    variables_nc = []
    nc_bloquantes = []
    friction_vecteur = {}
    verdict_cci = "NON_CALCULÉ"
    statut_nc   = result.get("meta", {}).get("statut_nc", "OK")

    if cci_rapport:
        cci_global    = cci_rapport.get("cci")
        kappa_sa      = cci_rapport.get("kappa_sa")
        variables_nc  = cci_rapport.get("variables_nc", [])
        nc_bloquantes = cci_rapport.get("nc_bloquantes", [])
        friction_vecteur = cci_rapport.get("friction_vecteur", {})
        verdict_cci   = cci_rapport.get("verdict", "NON_CALCULÉ")

        if nc_bloquantes:
            statut_nc = "DONNÉES_INSUFFISANTES"
        elif variables_nc:
            statut_nc = "NC_WARNINGS"
        else:
            statut_nc = "OK"
    else:
        meta_r = result.get("meta", {})
        variables_nc  = meta_r.get("nc_non_bloquantes", [])
        nc_bloquantes = meta_r.get("nc_bloquantes", [])

    # ── Hash d'intégrité ──────────────────────────────────────────────────────
    hash_result_json  = _sha256_file(result_path)
    hash_result_canon = _sha256_dict(result)
    hash_rapport_md   = _sha256_file(rapport_path) if rapport_path else None

    empreinte_parts = [hash_result_canon]
    if hash_rapport_md:
        empreinte_parts.append(hash_rapport_md)
    empreinte_composite = _sha256_str("|".join(empreinte_parts))

    # ── Description adaptée V6.2 / V7 ─────────────────────────────────────────
    description = (
        "Passeport de certification MEPA V7-alpha rev. 2.1. "
        "Atteste la traçabilité complète de la chaîne : "
        "Codage CONV-E (6.2+V7) → Audit CONV-B → CCI → Simulation LSODA → Rapport CONV-A. "
        "Branches diagnostiquées annotées EXPLICATIVE/CATCHALL selon V7-C4 rev. 2.1."
    ) if est_v7 else (
        "Passeport de certification MEPA V6.2 Fortifiée. "
        "Atteste la traçabilité complète de la chaîne : "
        "Codage CONV-E → Audit CONV-B → CCI → Simulation → Rapport CONV-A."
    )

    schema_version = "mepa-passeport-v3.0" if est_v7 else "mepa-passeport-v2.0"

    # ── Construction du passeport ─────────────────────────────────────────────
    passeport = {
        "$schema":      schema_version,
        "$description": description,
        "generated_at": ts_now,

        # ── § 1 : Identité WP (étendue V7) ───────────────────────────────────
        "identite": {
            "wp_id":                wp_id,
            "cas":                  identite["cas"],
            "cluster":              identite["cluster"],
            "sa":                   identite["sa"],
            "sa_modulator":         identite["sa_modulator"],
            "trajectoire_attendue": identite["trajectoire_attendue"],
            "trajectoire_diagn":    identite["trajectoire_diagn"],
            "concordance":          identite["concordance"],
            "fiche_v7":             est_v7,
            **({"variables_v7": identite.get("variables_v7", {})} if est_v7 else {}),
        },

        # ── § 2 : Certification inter-codeurs ─────────────────────────────────
        "certification": {
            "cci":              cci_global,
            "kappa":            cci_global,
            "kappa_sa":         kappa_sa,
            "verdict_cci":      verdict_cci,
            "variables_nc":     variables_nc,
            "nc_bloquantes":    nc_bloquantes,
            "nc_non_bloquantes":variables_nc,
            "statut_nc":        statut_nc,
            "note_methodologie": (
                "CCI ICC(3,1) two-way mixed consistency (Shrout & Fleiss, 1979). "
                "Reproductibilité conditionnelle au modèle LLM — non indépendance absolue. "
                "κ maintenu pour Sa (catégorielle ordinale à 4 niveaux). "
                + ("NC bloquantes V7 étendues à psi_noyau et gamma_local "
                   "(sans ces valeurs, condition C2 branche α non évaluable). "
                   if est_v7 else "")
                + "Voir Addendum Théorique V6.2 Pilier 1 / Cadre V7-α rev. 2.1 §2ter."
            ),
        },

        # ── § 3 : Simulation (étendue V7) ─────────────────────────────────────
        "simulation": sim_digest,

        # ── § 4 : Hash d'intégrité ────────────────────────────────────────────
        "hash_integrite": {
            "result_json_sha256":        hash_result_json,
            "result_json_canon_sha256":  hash_result_canon,
            "rapport_md_sha256":         hash_rapport_md,
            "empreinte_composite_sha256":empreinte_composite,
            "rapport_md_path":           rapport_path,
            "result_json_path":          result_path,
            "note": (
                "empreinte_composite = SHA-256(SHA-256(result_canon) | SHA-256(rapport_md)). "
                "Si rapport_md absent : empreinte_composite = SHA-256(result_canon)."
            ),
        },

        # ── § 5 : Provenance IA ───────────────────────────────────────────────
        "provenance_ia": {
            **IA_CODEUR,
            "generated_at_runner": identite["generated_at_runner"],
            "integration":         identite["integration"],
            "cmd_type":            identite["cmd_type"],
        },

        # ── § 6 : Versioning MEPA ─────────────────────────────────────────────
        "mepa_version": MEPA_VERSION_META,

        # ── § 7 : Friction ────────────────────────────────────────────────────
        "friction_vecteur": friction_vecteur,

        # ── § 8 : Paramètres effectifs ────────────────────────────────────────
        "params_effectifs": {k: v for k, v in result.get("params", {}).items()
                             if not k.startswith("_")},
        "cmd_base":          result.get("cmd_base", {}),
        "y0":                result.get("y0", []),
        "t_max":             result.get("t_max"),
        "theta_C_effectif":  identite["theta_C_effectif"],
        "theta_I_effectif":  identite["theta_I_effectif"],

        # ── § 9 : Statut global (étendu V7) ───────────────────────────────────
        "statut_global": _calculer_statut_global(
            concordance   = identite["concordance"],
            robustesse    = identite["robustesse"],
            statut_nc     = statut_nc,
            verdict_cci   = verdict_cci,
            wp_id         = wp_id,
            est_v7        = est_v7,
            trajectoire_attendue = identite["trajectoire_attendue"],
            trajectoire_diagn    = identite["trajectoire_diagn"],
        ),
    }

    # ── Écriture sur disque ───────────────────────────────────────────────────
    if passeport_out is None:
        base = os.path.dirname(result_path)
        passeport_out = os.path.join(base, f"{wp_id}_passeport.json")

    with open(passeport_out, "w", encoding="utf-8") as f:
        json.dump(passeport, f, indent=2, ensure_ascii=False)

    print(f"✓  Passeport écrit : {passeport_out}")
    print(f"   WP              : {wp_id}  {'[V7]' if est_v7 else '[V6.2]'}")
    print(f"   Trajectoire     : {sim_digest['traj']}  (attendue : {identite['trajectoire_attendue']})")
    if est_v7:
        print(f"   Branche         : {sim_digest.get('branche_annotation', 'UNKNOWN')}")
    print(f"   Concordance     : {'✓' if identite['concordance'] else '✗'}")
    print(f"   Robustesse      : {sim_digest['robustesse']}")
    print(f"   Statut NC       : {statut_nc}")
    print(f"   CCI             : {cci_global}  (verdict : {verdict_cci})")
    print(f"   Empreinte SHA-256: {empreinte_composite[:16]}…")
    print(f"   Statut global   : {passeport['statut_global']['code']}")

    return passeport


# ── Calcul du statut global (étendu V7) ──────────────────────────────────────

def _calculer_statut_global(
    concordance:  bool,
    robustesse:   str,
    statut_nc:    str,
    verdict_cci:  str,
    wp_id:        str = "",
    est_v7:       bool = False,
    trajectoire_attendue: str = "",
    trajectoire_diagn:    str = "",
) -> dict:
    """
    Calcule le statut global du passeport.

    Niveaux V6.2 :
      CERTIFIÉ     : concordance + ROBUSTE + CCI ≥ 0.70 + pas de NC bloquant
      CERTIFIÉ_NC  : idem mais avec NC non bloquants (warnings)
      CERTIFIÉ_MÉTASTABLE : concordance + MÉTASTABLE + CCI ≥ 0.70
      RÉVISION_CONCORDANCE : non concordant
      RÉVISION     : CCI en révision (0.50–0.70)
      REJET_CCI    : CCI < 0.50
      REJET_NC     : NC bloquant
      INCOMPLET    : CCI non calculé

    Niveaux V7 supplémentaires :
      CONDITIONNELLE_V7 : cas WP-I4-1 Allemagne nazie — divergence attendue
                          sur condition C2 (Décision V7-D1 rev. 4 §5)
                          Le rapport doit contenir les Réserves 1 et 2 §4bis.
    """
    # statut_global suit les critères V6.2 (CCI ≥ 0.70, concordance, robustesse).
    # Pour les passeports V7, certification_v2 (ajouté par Nœud 15 n8n) suit les
    # critères V7-S7 stricts (CCI ≥ 0.75, CONV-B CERTIFIÉ) — les deux champs
    # peuvent légitimement diverger et mesurent des niveaux distincts.
    _cv = "V6.2 (CCI ≥ 0.70, concordance, robustesse)"

    # --- V7 : cas conditionnel Allemagne nazie ---
    if est_v7 and wp_id == "WP-I4-1" and not concordance:
        return {
            "code": "CONDITIONNELLE_V7",
            "label": "Conditionnelle V7 — Divergence attendue",
            "detail": (
                "Cas WP-I4-1 Allemagne nazie : la divergence sur la trajectoire "
                "(α) est pré-enregistrée comme échec attendu sur la condition C2 "
                "(Ψ_noyau × γ_local < σ(Φ)) par la Décision V7-D1 rev. 4 §5. "
                "Le rapport CONV-A doit contenir les Réserves 1 et 2 du §4bis : "
                "anomalie documentée et hypothèse théorique sous contrainte. "
                "Ce statut ne bloque PAS la certification V7.0 si les cinq autres "
                "conditions du cluster pilote V7-γ rev. 2 sont satisfaites."
            ),
            "cluster_pilote_v7_gamma": True,
            "reference": "Décision V7-D1 rev. 4 §4bis + §5",
            "criteres_version": _cv,
        }

    if statut_nc == "DONNÉES_INSUFFISANTES":
        return {
            "code": "REJET_NC",
            "label": "Données Insuffisantes",
            "detail": "Variable(s) NC bloquante(s). Simulation non certifiable.",
            "criteres_version": _cv,
        }

    if verdict_cci == "REJET":
        return {
            "code": "REJET_CCI",
            "label": "CCI Insuffisant",
            "detail": "CCI < 0.50 — désaccord inter-codeurs trop élevé.",
            "criteres_version": _cv,
        }

    if verdict_cci == "RÉVISION":
        return {
            "code": "RÉVISION",
            "label": "Révision Requise",
            "detail": "CCI 0.50–0.70 — désaccords résiduels. Confrontation sources requise.",
            "criteres_version": _cv,
        }

    if verdict_cci in ("CERTIFIÉ", "NON_CALCULÉ"):
        if not concordance:
            return {
                "code": "RÉVISION_CONCORDANCE",
                "label": "Révision — Non-concordance",
                "detail": (
                    "Trajectoire simulée ≠ trajectoire attendue. "
                    "Revoir codage ou paramètres. "
                    + ("En V7 : appliquer protocole V7-C3 (anomalie documentée + "
                       "hypothèse théorique sous contrainte, Réserves 1 et 2 §4bis). "
                       if est_v7 else "")
                ),
                "criteres_version": _cv,
            }

        if robustesse == "ROBUSTE":
            if statut_nc == "NC_WARNINGS":
                return {
                    "code": "CERTIFIÉ_NC",
                    "label": "Certifié avec Avertissements NC",
                    "detail": (
                        "WP certifié. Variables NC non bloquantes présentes — "
                        "signalées dans le rapport (Silence Socratique V6.2)."
                    ),
                    "criteres_version": _cv,
                }
            return {
                "code": "CERTIFIÉ",
                "label": "Certifié",
                "detail": "Concordance + Robustesse + CCI validés." + (
                    " [V7]" if est_v7 else ""
                ),
                "criteres_version": _cv,
            }

        if robustesse == "MÉTASTABLE":
            return {
                "code": "CERTIFIÉ_MÉTASTABLE",
                "label": "Certifié — Système Métastable",
                "detail": (
                    "WP certifié. Simulation métastable : "
                    "les stress-tests N1 produisent des trajectoires alternatives. "
                    "Mentionner dans le rapport S7."
                ),
                "criteres_version": _cv,
            }

    return {
        "code": "INCOMPLET",
        "label": "Incomplet",
        "detail": "CCI non calculé — passeport partiel (simulation seule).",
        "criteres_version": _cv,
    }


# ── Génération depuis result.json seul (mode minimal) ────────────────────────

def passeport_depuis_result(result: dict, result_path: str = "?") -> dict:
    """
    API pour appel depuis Nœud 7 n8n (pas de fichier disque).
    Génère le passeport directement depuis le dict result en mémoire.
    """
    ts_now   = datetime.datetime.now(datetime.timezone.utc).isoformat()
    identite = _extraire_identite(result)
    sim_dig  = _extraire_simulation_digest(result)
    wp_id    = identite["wp_id"]
    est_v7   = identite["fiche_v7"]

    meta_r        = result.get("meta", {})
    variables_nc  = meta_r.get("nc_non_bloquantes", [])
    nc_bloquantes = meta_r.get("nc_bloquantes", [])
    statut_nc     = meta_r.get("statut_nc", "OK")

    hash_result_canon    = _sha256_dict(result)
    empreinte_composite  = hash_result_canon

    schema_version = "mepa-passeport-v3.0" if est_v7 else "mepa-passeport-v2.0"

    return {
        "$schema":      schema_version,
        "generated_at": ts_now,
        "identite": {
            "wp_id":                wp_id,
            "cas":                  identite["cas"],
            "cluster":              identite["cluster"],
            "sa":                   identite["sa"],
            "trajectoire_attendue": identite["trajectoire_attendue"],
            "trajectoire_diagn":    identite["trajectoire_diagn"],
            "concordance":          identite["concordance"],
            "fiche_v7":             est_v7,
            **({"variables_v7": identite.get("variables_v7", {})} if est_v7 else {}),
        },
        "certification": {
            "cci":              None,
            "kappa":            None,
            "kappa_sa":         None,
            "verdict_cci":      "NON_CALCULÉ",
            "variables_nc":     variables_nc,
            "nc_bloquantes":    nc_bloquantes,
            "nc_non_bloquantes":variables_nc,
            "statut_nc":        statut_nc,
        },
        "simulation":   sim_dig,
        "hash_integrite": {
            "result_json_path":          result_path,
            "result_json_canon_sha256":  hash_result_canon,
            "rapport_md_sha256":         None,
            "empreinte_composite_sha256":empreinte_composite,
        },
        "provenance_ia":   IA_CODEUR,
        "mepa_version":    MEPA_VERSION_META,
        "friction_vecteur":{},
        "params_effectifs":{k: v for k, v in result.get("params", {}).items()
                            if not k.startswith("_")},
        "cmd_base":         result.get("cmd_base", {}),
        "y0":               result.get("y0", []),
        "t_max":            result.get("t_max"),
        "theta_C_effectif": identite["theta_C_effectif"],
        "theta_I_effectif": identite["theta_I_effectif"],
        "statut_global": _calculer_statut_global(
            concordance  = identite["concordance"],
            robustesse   = identite["robustesse"],
            statut_nc    = statut_nc,
            verdict_cci  = "NON_CALCULÉ",
            wp_id        = wp_id,
            est_v7       = est_v7,
            trajectoire_attendue = identite["trajectoire_attendue"],
            trajectoire_diagn    = identite["trajectoire_diagn"],
        ),
    }


# ── Fonction d'enrichissement par audit CONV-B (inchangée V6.2) ─────────────

def enrich_from_audit(passeport: dict, audit_result: dict) -> dict:
    """
    Enrichit un passeport existant avec les résultats d'un audit CONV-B.

    Paramètres :
      passeport    : dict passeport (issu de generer_passeport)
      audit_result : dict avec clés : kappa, verdict, anomalies

    Retourne le passeport enrichi.
    """
    if "certification" not in passeport:
        passeport["certification"] = {}

    passeport["certification"]["cci"]         = audit_result.get("kappa")
    passeport["certification"]["kappa"]       = audit_result.get("kappa")
    passeport["certification"]["verdict_cci"] = audit_result.get("verdict", "NON_CALCULÉ")
    passeport["certification"]["anomalies"]   = audit_result.get("anomalies", [])

    # Recalcul du statut global
    est_v7 = passeport.get("identite", {}).get("fiche_v7", False)
    passeport["statut_global"] = _calculer_statut_global(
        concordance   = passeport.get("identite", {}).get("concordance", False),
        robustesse    = passeport.get("simulation", {}).get("robustesse", ""),
        statut_nc     = passeport.get("certification", {}).get("statut_nc", "OK"),
        verdict_cci   = passeport["certification"]["verdict_cci"],
        wp_id         = passeport.get("identite", {}).get("wp_id", ""),
        est_v7        = est_v7,
        trajectoire_attendue = passeport.get("identite", {}).get("trajectoire_attendue", ""),
        trajectoire_diagn    = passeport.get("identite", {}).get("trajectoire_diagn", ""),
    )

    return passeport


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python3 mepa_passeport_schema.py result.json [rapport.md] [cci.json] [passeport_out.json]")
        print()
        print("  result.json       : obligatoire — sortie Runner (V6.2 ou V7)")
        print("  rapport.md        : optionnel  — rédigé par CONV-A (hash inclus)")
        print("  cci.json          : optionnel  — sortie mepa_kappa_calculator.py")
        print("  passeport_out.json: optionnel  — défaut: <wp_id>_passeport.json")
        sys.exit(1)

    result_p     = sys.argv[1]
    rapport_p    = sys.argv[2] if len(sys.argv) >= 3 else None
    cci_p        = sys.argv[3] if len(sys.argv) >= 4 else None
    passeport_p  = sys.argv[4] if len(sys.argv) >= 5 else None

    if rapport_p  == "SKIP": rapport_p  = None
    if cci_p      == "SKIP": cci_p      = None
    if passeport_p == "SKIP": passeport_p = None

    if rapport_p and rapport_p.endswith(".json"):
        cci_p     = rapport_p
        rapport_p = None

    passeport = generer_passeport(
        result_path      = result_p,
        rapport_path     = rapport_p,
        cci_rapport_path = cci_p,
        passeport_out    = passeport_p,
    )

    print(f"\n   Hash result_canon : {passeport['hash_integrite']['result_json_canon_sha256'][:32]}…")
