#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mepa_deploy_check.py
Version          : 1.0.0
MEPA version     : 7.0-alpha rev. 2.1
Dépendances      : hashlib, json, os, sys, re (stdlib uniquement)

OBJET (cible DEP3 de l'audit CTO)
  Le déploiement Nextcloud manuel ne garantit pas que les scripts présents sur
  le Pi correspondent aux versions validées/committées. Un écart de version
  silencieux est déjà survenu (Pi en v3.0.1 alors que le correctif était v3.0.2)
  et n'a été détecté que par lecture fortuite d'un champ de passeport.

  Ce script transforme cet écart silencieux en BLOCAGE explicite : il compare le
  sha256 de chaque fichier critique déployé à un manifeste de référence.

MODÈLE DE CONFIANCE
  Le manifeste de référence est la VÉRITÉ. Il doit être (re)généré à partir
  d'un déploiement validé connu-bon, puis committé dans le repo. Le contrôle au
  démarrage compare l'état déployé à ce manifeste.

USAGE
  Générer le manifeste (après un déploiement validé) :
    python3 mepa_deploy_check.py --generate --scripts-dir /data/mepa/scripts \\
            --out /data/mepa/scripts/mepa_deploy_manifest.json

  Vérifier (au démarrage du pipeline / en CI) :
    python3 mepa_deploy_check.py --check --scripts-dir /data/mepa/scripts \\
            --manifest /data/mepa/scripts/mepa_deploy_manifest.json

  Exit 0 = conforme ; 1 = dérive (hash/fichier) ; 2 = erreur (manifeste absent).
"""

import hashlib
import json
import os
import re
import sys

DEFAULT_SCRIPTS_DIR = os.environ.get("MEPA_SCRIPTS_DIR", "/data/mepa/scripts")

# Fichiers critiques suivis. Un fichier absent du disque mais présent au
# manifeste = dérive bloquante.
TRACKED = [
    "mepa_runner_v3_v7.py",
    "mepa_runner_v2_gamma.py",
    "mepa_passeport_schema.py",
    "mepa_kappa_calculator.py",
    "mepa_node2_audit_v7.js",
    "mepa_dev1_advisory_v7.py",
    "mepa_sensitivity_n1.py",
    "mepa_constants.json",
    "mepa_consistency_check.py",
]

MANIFEST_VERSION = "1.0.0"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_version(path):
    """Best-effort : version lisible pour le rapport. Le hash reste la vérité."""
    try:
        if path.endswith(".json"):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            meta = data.get("$meta", {}) if isinstance(data, dict) else {}
            return meta.get("version") or meta.get("$version")
        with open(path, encoding="utf-8", errors="replace") as f:
            head = f.read(4000)
        # En-tête Python "Version          : 3.0.2"
        m = re.search(r"Version\s*:\s*([0-9]+\.[0-9]+(?:\.[0-9]+)?)", head)
        if m:
            return m.group(1)
        # Commentaire JS "v3.0" / "version 3.0.0"
        m = re.search(r"\bv(?:ersion)?\s*[:= ]\s*([0-9]+\.[0-9]+(?:\.[0-9]+)?)", head, re.I)
        if m:
            return m.group(1)
    except Exception:
        pass
    return None


def generate(scripts_dir):
    entries = {}
    missing = []
    for name in TRACKED:
        p = os.path.join(scripts_dir, name)
        if not os.path.isfile(p):
            missing.append(name)
            continue
        entries[name] = {
            "version": extract_version(p),
            "sha256": sha256_file(p),
            "bytes": os.path.getsize(p),
        }
    return {
        "$manifest_version": MANIFEST_VERSION,
        "$description": "Manifeste d'intégrité de déploiement MEPA (DEP3). "
                        "sha256 des scripts critiques validés. Régénérer après "
                        "tout déploiement validé.",
        "scripts_dir_source": scripts_dir,
        "files": entries,
        "_warnings": ([f"absent à la génération : {m}" for m in missing] or None),
    }


def check(scripts_dir, manifest_path):
    """Renvoie (ok, lignes)."""
    out = []
    if not os.path.isfile(manifest_path):
        return None, [f"✗ Manifeste introuvable : {manifest_path}"]
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)
    files = manifest.get("files", {})
    if not files:
        return None, ["✗ Manifeste vide (aucune entrée 'files')."]

    ok = True
    for name, ref in files.items():
        p = os.path.join(scripts_dir, name)
        if not os.path.isfile(p):
            ok = False
            out.append(f"  ✗ MANQUANT   {name} (présent au manifeste, absent du disque)")
            continue
        got = sha256_file(p)
        if got != ref.get("sha256"):
            ok = False
            vref = ref.get("version") or "?"
            vgot = extract_version(p) or "?"
            out.append(f"  ✗ DÉRIVE     {name}")
            out.append(f"               version déployée={vgot}  attendue={vref}")
            out.append(f"               sha256 déployé ={got[:16]}…")
            out.append(f"               sha256 attendu ={str(ref.get('sha256'))[:16]}…")
        else:
            v = ref.get("version") or "?"
            out.append(f"  ✓ {name}  (v{v})")
    # Fichiers suivis présents sur disque mais absents du manifeste = warning
    for name in TRACKED:
        if name not in files and os.path.isfile(os.path.join(scripts_dir, name)):
            out.append(f"  ⚠ NON SUIVI  {name} présent mais absent du manifeste "
                       f"(régénérer le manifeste).")
    return ok, out


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    mode = "--generate" if "--generate" in argv else "--check"
    scripts_dir = DEFAULT_SCRIPTS_DIR
    if "--scripts-dir" in argv:
        scripts_dir = argv[argv.index("--scripts-dir") + 1]
    manifest = os.path.join(scripts_dir, "mepa_deploy_manifest.json")
    if "--manifest" in argv:
        manifest = argv[argv.index("--manifest") + 1]
    out_path = manifest
    if "--out" in argv:
        out_path = argv[argv.index("--out") + 1]

    if mode == "--generate":
        man = generate(scripts_dir)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(man, f, ensure_ascii=False, indent=2)
        print(f"Manifeste généré : {out_path}")
        print(f"  {len(man['files'])} fichier(s) suivis.")
        if man.get("_warnings"):
            for w in man["_warnings"]:
                print(f"  ⚠ {w}")
        return 0

    print("=" * 64)
    print(" MEPA — Intégrité de déploiement (DEP3)")
    print(f" Scripts : {scripts_dir}")
    print(f" Manifeste : {manifest}")
    print("=" * 64)
    ok, lignes = check(scripts_dir, manifest)
    for l in lignes:
        print(l)
    print("-" * 64)
    if ok is None:
        print("RÉSULTAT : ✗ ERREUR (manifeste absent/vide).")
        return 2
    if ok:
        print("RÉSULTAT : ✓ CONFORME — scripts déployés == manifeste.")
        return 0
    print("RÉSULTAT : ✗ DÉRIVE DE DÉPLOIEMENT — un script déployé ne correspond")
    print("           pas à la version de référence. Corriger AVANT tout run.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
