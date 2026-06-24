#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mepa_consistency_check.py
Version          : 1.0.0
MEPA version     : 7.0-alpha rev. 2.1
Dépendances      : json, os, sys, importlib (stdlib uniquement)

OBJET (cible D1/D2 de l'audit CTO)
  Les seuils de certification (CCI, κ) existent en plusieurs exemplaires :
    1. mepa_constants.json                  → SOURCE DE VÉRITÉ
    2. mepa_kappa_calculator.py (_charger_constants → fallback embarqué)
    3. mepa_passeport_schema.py (constantes SEUIL_* hardcodées)
  Ces copies sont synchronisées À LA MAIN. Une édition de constants.json non
  répliquée crée une dérive SILENCIEUSE qui ne se manifeste qu'au moment où le
  fichier est absent (fallback) ou via statut_global (passeport) — soit
  exactement quand on ne peut plus s'en apercevoir.

  Ce script compare, CLÉ PAR CLÉ sur le sous-ensemble critique pour la
  certification (et non par hash global, car les fallbacks sont des miroirs
  PARTIELS volontaires), chaque copie à la source de vérité.

  Sous-ensemble vérifié :
    - seuils_validation.{cci,kappa_sa,cci_global}.{certifie,revision}
    - seuil_cci de chaque variable (variables_mepa + variables_v7_alpha_rev2_1)
    - SEUIL_CCI_CERTIFIE / SEUIL_CCI_GLOBAL_CERT / SEUIL_REVISION (passeport)

  PÉRIMÈTRE : seuils de CERTIFICATION uniquement (ceux qui affectent un verdict).
  Les paramètres de SIMULATION répliqués dans le runner et node2 (modulateurs p6,
  theta_FR, branche-b) relèvent d'un autre mode de défaillance et ne sont pas
  couverts ici (extension possible sur le même patron — voir audit CTO).

USAGE
  python3 mepa_consistency_check.py [--scripts-dir DIR]
  Exit 0 = cohérent ; Exit 1 = dérive détectée.
  À câbler : (a) au démarrage du pipeline (avant le 1er WP d'un run),
             (b) en CI (sur tout commit touchant constants/kappa_calc/passeport).
"""

import json
import os
import sys
import importlib.util

DEFAULT_SCRIPTS_DIR = os.environ.get("MEPA_SCRIPTS_DIR", "/data/mepa/scripts")

# Chemins (tuples) des seuils de certification à vérifier dans constants.json
CERT_THRESHOLD_PATHS = [
    ("seuils_validation", "cci", "certifie"),
    ("seuils_validation", "cci", "revision"),
    ("seuils_validation", "kappa_sa", "certifie"),
    ("seuils_validation", "kappa_sa", "revision"),
    ("seuils_validation", "cci_global", "certifie"),
    ("seuils_validation", "cci_global", "revision"),
]
# Sections dont on vérifie le seuil_cci de chaque variable
VAR_SECTIONS = ["variables_mepa", "variables_v7_alpha_rev2_1"]


def _dig(d, path):
    """Renvoie (trouvé: bool, valeur)."""
    cur = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return (False, None)
        cur = cur[k]
    return (True, cur)


def load_canonical(scripts_dir):
    path = os.path.join(scripts_dir, "mepa_constants.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_kappa_fallback(script_path):
    """Importe kappa_calculator et FORCE le chemin fallback embarqué."""
    spec = importlib.util.spec_from_file_location("_mepa_kc", script_path)
    kc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kc)
    # Force le fallback en pointant CONSTANTS_PATH vers un chemin absent
    kc.CONSTANTS_PATH = os.path.join(os.sep, "__mepa_force_fallback__.json")
    return kc._charger_constants()


def load_passeport_consts(script_path):
    """Importe passeport_schema et lit les constantes SEUIL_* hardcodées.
    Renvoie un mapping {chemin_constants -> valeur_hardcodée}."""
    spec = importlib.util.spec_from_file_location("_mepa_ps", script_path)
    ps = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ps)
    return {
        ("seuils_validation", "cci", "certifie"):        ps.SEUIL_CCI_CERTIFIE,
        ("seuils_validation", "cci_global", "certifie"): ps.SEUIL_CCI_GLOBAL_CERT,
        ("seuils_validation", "cci_global", "revision"): ps.SEUIL_REVISION,
    }


def _path_str(path):
    return ".".join(path)


def check(scripts_dir):
    """Renvoie (ok: bool, lignes_rapport: list[str])."""
    out = []
    ok = True

    canonical = load_canonical(scripts_dir)

    # ── 1. Fallback kappa_calculator ─────────────────────────────────────────
    kc_path = os.path.join(scripts_dir, "mepa_kappa_calculator.py")
    out.append("[1] kappa_calculator (fallback embarqué) vs constants.json")
    try:
        fb = load_kappa_fallback(kc_path)
        # seuils de certification
        for p in CERT_THRESHOLD_PATHS:
            f_ok, ref = _dig(canonical, p)
            g_ok, val = _dig(fb, p)
            if not f_ok:
                ok = False
                out.append(f"    ✗ {_path_str(p)} ABSENT de constants.json (source corrompue ?)")
            elif not g_ok:
                ok = False
                out.append(f"    ✗ {_path_str(p)} ABSENT du fallback")
            elif ref != val:
                ok = False
                out.append(f"    ✗ DÉRIVE {_path_str(p)} : fallback={val}  ref={ref}")
        # seuil_cci par variable
        for section in VAR_SECTIONS:
            c_sec = canonical.get(section, {})
            f_sec = fb.get(section, {})
            for var, cdef in c_sec.items():
                if "seuil_cci" not in cdef:
                    continue
                ref = cdef.get("seuil_cci")
                val = f_sec.get(var, {}).get("seuil_cci")
                if val != ref:
                    ok = False
                    out.append(f"    ✗ DÉRIVE {section}.{var}.seuil_cci : fallback={val}  ref={ref}")
        if ok:
            out.append("    ✓ cohérent")
    except Exception as e:
        ok = False
        out.append(f"    ✗ ÉCHEC import/lecture : {e!r}")

    # ── 2. Constantes hardcodées passeport_schema ────────────────────────────
    ps_path = os.path.join(scripts_dir, "mepa_passeport_schema.py")
    out.append("[2] passeport_schema (SEUIL_* hardcodés) vs constants.json")
    try:
        ps_consts = load_passeport_consts(ps_path)
        section_ok = True
        for p, val in ps_consts.items():
            f_ok, ref = _dig(canonical, p)
            if not f_ok:
                ok = False; section_ok = False
                out.append(f"    ✗ {_path_str(p)} ABSENT de constants.json")
            elif ref != val:
                ok = False; section_ok = False
                out.append(f"    ✗ DÉRIVE (≈{_path_str(p)}) : hardcodé={val}  ref={ref}")
        if section_ok:
            out.append("    ✓ cohérent")
    except Exception as e:
        ok = False
        out.append(f"    ✗ ÉCHEC import/lecture : {e!r}")

    return ok, out


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    scripts_dir = DEFAULT_SCRIPTS_DIR
    if "--scripts-dir" in argv:
        i = argv.index("--scripts-dir")
        scripts_dir = argv[i + 1]

    print("=" * 64)
    print(" MEPA — Vérification de cohérence des seuils de certification (D1/D2)")
    print(f" Source de vérité : {os.path.join(scripts_dir, 'mepa_constants.json')}")
    print("=" * 64)
    try:
        ok, lignes = check(scripts_dir)
    except FileNotFoundError as e:
        print(f"ERREUR : {e}")
        return 2
    for l in lignes:
        print(l)
    print("-" * 64)
    if ok:
        print("RÉSULTAT : ✓ COHÉRENT — aucune dérive de seuil détectée.")
        return 0
    print("RÉSULTAT : ✗ DÉRIVE DÉTECTÉE — un seuil de certification a divergé.")
    print("           Corriger AVANT tout run : une dérive de seuil peut")
    print("           silencieusement changer un verdict de certification.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
