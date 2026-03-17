#!/usr/bin/env python3
"""
================================================================================
MEPA V6.2 — Générateur de Passeport de Certification
================================================================================
Statut           : REMPLACEMENT
Cible            : /data/mepa/scripts/mepa_passeport_schema.py
Remplace         : mepa_passeport_schema.py v1.x
Rétrocompatibilité :
    - Champ 'kappa' maintenu en alias de 'cci' (compatibilité CONV-D v1.x).
    - Nouveau champ 'cci' (CCI ICC(3,1)) remplace 'kappa' pour variables continues.
    - Nouveau champ 'kappa_sa' : κ de Cohen pour Sa (catégorielle).
    - Nouveau champ 'variables_nc' : liste des variables NC non bloquantes.
    - Nouveau champ 'nc_non_bloquantes' : alias de variables_nc.
    - Hash SHA-256 : calculé sur result.json ET sur rapport.md si présent.
    - Champ 'statut_nc' : OK | NC_WARNINGS | DONNÉES_INSUFFISANTES.
    - Compatible mepa_friction_profile.json (champ friction_vecteur propagé).
Version          : 2.0.0
MEPA version     : 6.2 Fortifiée
Dépendances      : json, sys, hashlib, datetime, os, pathlib (stdlib uniquement)
================================================================================

Rôle dans le pipeline WF1 :
  Nœud 7 (Export) appelle ce script après simulation réussie.
  Entrées :
    - result.json     : sortie du Runner (mepa_runner_v2_gamma.py)
    - rapport.md      : rédigé par CONV-A (optionnel mais recommandé)
    - cci_rapport.json: sortie de mepa_kappa_calculator.py (optionnel)
  Sortie :
    - passeport.json  : certificat de traçabilité complet

Structure du passeport :
  § identite        : wp_id, cas, cluster, Sa, trajectoire, date
  § certification   : CCI, κ_Sa, verdict_inter_codeurs, statut_nc
  § simulation      : résultats Runner (traj, t_bascule, dC_rel, dI_rel...)
  § hash_intégrité  : SHA-256 de result.json + rapport.md
  § provenance_ia   : modèle, version, température
  § mepa_version    : V6.2 Fortifiée
  § friction_vecteur: {var: F(v,h)} pour friction_profile (si cci_rapport)

Usage :
  python3 mepa_passeport_schema.py result.json [rapport.md] [cci_rapport.json] [passeport_out.json]

  result.json       : obligatoire
  rapport.md        : optionnel (hash inclus si présent)
  cci_rapport.json  : optionnel (CCI, kappa_sa, variables_nc, friction_vecteur)
  passeport_out.json: optionnel (défaut : <wp_id>_passeport.json dans même dir)
"""

import json
import sys
import hashlib
import datetime
import os
import pathlib
from typing import Optional

# ── Chemin canonique Pi5 ──────────────────────────────────────────────────────
MEPA_SCRIPTS_DIR = os.environ.get("MEPA_SCRIPTS_DIR", "/data/mepa/scripts")
MEPA_OUTPUT_DIR  = os.environ.get("MEPA_OUTPUT_DIR",  "/data/mepa/outputs")

# ── Métadonnées IA codeur (traçabilité provenance) ────────────────────────────
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
        "conditionnelle au modèle — non une indépendance absolue inter-codeurs."
    ),
}

MEPA_VERSION_META = {
    "version":          "6.2",
    "sous_version":     "Fortifiée",
    "label":            "MEPA V6.2 Fortifiée",
    "runner":           "mepa_runner_v2_gamma v2.0",
    "audit":            "mepa_node2_audit_v62 v2.0",
    "kappa_calc":       "mepa_kappa_calculator v2.0",
    "passeport":        "mepa_passeport_schema v2.0",
    "constants":        "mepa_constants v1.0",
    "whitelist":        "mepa_whitelist_keys v2.0",
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


# ── Extraction depuis result.json ─────────────────────────────────────────────

def _extraire_identite(result: dict) -> dict:
    """Extrait les champs d'identité depuis le résultat Runner."""
    meta = result.get("meta", {})
    sim  = result.get("simulation", {})
    vrd  = result.get("verdict", {})
    return {
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
    }


def _extraire_simulation_digest(result: dict) -> dict:
    """Extrait les indicateurs clés de simulation pour le passeport."""
    sim = result.get("simulation", {})
    vrd = result.get("verdict", {})
    sn1 = result.get("stress_n1", {})
    return {
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


# ── Construction du passeport ─────────────────────────────────────────────────

def generer_passeport(
    result_path:      str,
    rapport_path:     Optional[str] = None,
    cci_rapport_path: Optional[str] = None,
    passeport_out:    Optional[str] = None,
) -> dict:
    """
    Génère le passeport de certification MEPA V6.2 pour un WP.

    Paramètres :
      result_path      : chemin vers <wp_id>_result.json (Runner)
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

        # Réconcilier statut_nc
        if nc_bloquantes:
            statut_nc = "DONNÉES_INSUFFISANTES"
        elif variables_nc:
            statut_nc = "NC_WARNINGS"
        else:
            statut_nc = "OK"
    else:
        # Lire depuis meta runner si disponible
        meta_r = result.get("meta", {})
        variables_nc  = meta_r.get("nc_non_bloquantes", [])
        nc_bloquantes = meta_r.get("nc_bloquantes", [])

    # ── Hash d'intégrité ──────────────────────────────────────────────────────
    hash_result_json  = _sha256_file(result_path)
    hash_result_canon = _sha256_dict(result)  # hash du dict canonique (indép. formatage)
    hash_rapport_md   = _sha256_file(rapport_path) if rapport_path else None

    # Hash composite du passeport (result + rapport si dispo)
    empreinte_parts = [hash_result_canon]
    if hash_rapport_md:
        empreinte_parts.append(hash_rapport_md)
    empreinte_composite = _sha256_str("|".join(empreinte_parts))

    # ── Construction du passeport ─────────────────────────────────────────────
    passeport = {
        "$schema":      "mepa-passeport-v2.0",
        "$description": (
            "Passeport de certification MEPA V6.2 Fortifiée. "
            "Atteste la traçabilité complète de la chaîne : "
            "Codage CONV-E → Audit CONV-B → CCI → Simulation → Rapport CONV-A."
        ),
        "generated_at": ts_now,

        # ── § 1 : Identité WP ─────────────────────────────────────────────────
        "identite": {
            "wp_id":               wp_id,
            "cas":                 identite["cas"],
            "cluster":             identite["cluster"],
            "sa":                  identite["sa"],
            "sa_modulator":        identite["sa_modulator"],
            "trajectoire_attendue":identite["trajectoire_attendue"],
            "trajectoire_diagn":   identite["trajectoire_diagn"],
            "concordance":         identite["concordance"],
        },

        # ── § 2 : Certification inter-codeurs ─────────────────────────────────
        "certification": {
            "cci":              cci_global,      # CCI ICC(3,1) — variables continues
            "kappa":            cci_global,      # alias de compatibilité V6.1 → V6.2
            "kappa_sa":         kappa_sa,        # κ Cohen pour Sa (catégorielle)
            "verdict_cci":      verdict_cci,
            "variables_nc":     variables_nc,    # NC non bloquantes détectées
            "nc_bloquantes":    nc_bloquantes,   # NC bloquantes (simulation impossible)
            "nc_non_bloquantes":variables_nc,    # alias
            "statut_nc":        statut_nc,
            "note_methodologie": (
                "CCI ICC(3,1) two-way mixed consistency (Shrout & Fleiss, 1979). "
                "Reproductibilité conditionnelle au modèle LLM — non indépendance absolue. "
                "κ maintenu pour Sa (catégorielle ordinale à 4 niveaux). "
                "Voir Addendum Théorique V6.2, Pilier 1."
            ),
        },

        # ── § 3 : Simulation ──────────────────────────────────────────────────
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

        # ── § 7 : Friction (pour mepa_friction_profile.json) ─────────────────
        "friction_vecteur": friction_vecteur,

        # ── § 8 : Paramètres effectifs ────────────────────────────────────────
        "params_effectifs": {k: v for k, v in result.get("params", {}).items()
                             if not k.startswith("_")},
        "cmd_base":          result.get("cmd_base", {}),
        "y0":                result.get("y0", []),
        "t_max":             result.get("t_max"),
        "theta_C_effectif":  identite["theta_C_effectif"],
        "theta_I_effectif":  identite["theta_I_effectif"],

        # ── § 9 : Statut global ───────────────────────────────────────────────
        "statut_global": _calculer_statut_global(
            concordance   = identite["concordance"],
            robustesse    = identite["robustesse"],
            statut_nc     = statut_nc,
            verdict_cci   = verdict_cci,
        ),
    }

    # ── Écriture sur disque ───────────────────────────────────────────────────
    if passeport_out is None:
        # Chemin auto : même répertoire que result.json
        base = os.path.dirname(result_path)
        passeport_out = os.path.join(base, f"{wp_id}_passeport.json")

    with open(passeport_out, "w", encoding="utf-8") as f:
        json.dump(passeport, f, indent=2, ensure_ascii=False)

    print(f"✓  Passeport écrit : {passeport_out}")
    print(f"   WP              : {wp_id}")
    print(f"   Trajectoire     : {sim_digest['traj']}  (attendue : {identite['trajectoire_attendue']})")
    print(f"   Concordance     : {'✓' if identite['concordance'] else '✗'}")
    print(f"   Robustesse      : {sim_digest['robustesse']}")
    print(f"   Statut NC       : {statut_nc}")
    print(f"   CCI             : {cci_global}  (verdict : {verdict_cci})")
    print(f"   Empreinte SHA-256: {empreinte_composite[:16]}…")
    print(f"   Statut global   : {passeport['statut_global']['code']}")

    return passeport


def _calculer_statut_global(
    concordance:  bool,
    robustesse:   str,
    statut_nc:    str,
    verdict_cci:  str,
) -> dict:
    """
    Calcule le statut global du passeport.

    Niveaux :
      CERTIFIÉ    : concordance + ROBUSTE + CCI ≥ 0.70 + pas de NC bloquant
      CERTIFIÉ_NC : idem mais avec NC non bloquants (warnings)
      MÉTASTABLE  : concordance + MÉTASTABLE + CCI ≥ 0.70
      RÉVISION    : CCI en révision (0.50–0.70) ou non concordant
      REJET       : CCI rejeté ou NC bloquant
      INCOMPLET   : CCI non calculé
    """
    if statut_nc == "DONNÉES_INSUFFISANTES":
        return {
            "code": "REJET_NC",
            "label": "Données Insuffisantes",
            "detail": "Variable(s) NC bloquante(s). Simulation non certifiable.",
        }

    if verdict_cci == "REJET":
        return {
            "code": "REJET_CCI",
            "label": "CCI Insuffisant",
            "detail": f"CCI < 0.50 — désaccord inter-codeurs trop élevé.",
        }

    if verdict_cci == "RÉVISION":
        return {
            "code": "RÉVISION",
            "label": "Révision Requise",
            "detail": "CCI 0.50–0.70 — désaccords résiduels. Confrontation sources requise.",
        }

    if verdict_cci in ("CERTIFIÉ", "NON_CALCULÉ"):
        if not concordance:
            return {
                "code": "RÉVISION_CONCORDANCE",
                "label": "Révision — Non-concordance",
                "detail": (
                    "Trajectoire simulée ≠ trajectoire attendue. "
                    "Revoir codage ou paramètres."
                ),
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
                }
            return {
                "code": "CERTIFIÉ",
                "label": "Certifié",
                "detail": "Concordance + Robustesse + CCI validés.",
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
            }

    return {
        "code": "INCOMPLET",
        "label": "Incomplet",
        "detail": "CCI non calculé — passeport partiel (simulation seule).",
    }


# ── Génération depuis result.json seul (mode minimal) ────────────────────────

def passeport_depuis_result(result: dict, result_path: str = "?") -> dict:
    """
    API pour appel depuis Nœud 7 n8n (pas de fichier disque).
    Génère le passeport directement depuis le dict result en mémoire.
    Retourne le dict sans écriture disque.
    """
    ts_now   = datetime.datetime.now(datetime.timezone.utc).isoformat()
    identite = _extraire_identite(result)
    sim_dig  = _extraire_simulation_digest(result)
    wp_id    = identite["wp_id"]

    meta_r        = result.get("meta", {})
    variables_nc  = meta_r.get("nc_non_bloquantes", [])
    nc_bloquantes = meta_r.get("nc_bloquantes", [])
    statut_nc     = meta_r.get("statut_nc", "OK")

    hash_result_canon    = _sha256_dict(result)
    empreinte_composite  = hash_result_canon  # pas de rapport.md en mode mémoire

    return {
        "$schema":      "mepa-passeport-v2.0",
        "generated_at": ts_now,
        "identite": {
            "wp_id":                wp_id,
            "cas":                  identite["cas"],
            "cluster":              identite["cluster"],
            "sa":                   identite["sa"],
            "trajectoire_attendue": identite["trajectoire_attendue"],
            "trajectoire_diagn":    identite["trajectoire_diagn"],
            "concordance":          identite["concordance"],
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
        ),
    }


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python3 mepa_passeport_schema.py result.json [rapport.md] [cci.json] [passeport_out.json]")
        print()
        print("  result.json       : obligatoire — sortie Runner")
        print("  rapport.md        : optionnel  — rédigé par CONV-A (hash inclus)")
        print("  cci.json          : optionnel  — sortie mepa_kappa_calculator.py")
        print("  passeport_out.json: optionnel  — défaut: <wp_id>_passeport.json")
        sys.exit(1)

    result_p     = sys.argv[1]
    rapport_p    = sys.argv[2] if len(sys.argv) >= 3 else None
    cci_p        = sys.argv[3] if len(sys.argv) >= 4 else None
    passeport_p  = sys.argv[4] if len(sys.argv) >= 5 else None

    # Normaliser les placeholders "SKIP" (envoyés par N6b quand arg absent)
    if rapport_p  == "SKIP": rapport_p  = None
    if cci_p      == "SKIP": cci_p      = None
    if passeport_p == "SKIP": passeport_p = None

    # Détecter si arg2 est un .json (cci) ou .md (rapport)
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
