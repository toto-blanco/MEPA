#!/usr/bin/env python3
"""
MEPA V6.2 — Dry run pipeline bout en bout
==========================================
Exécute la chaîne complète pour une fiche WP, vérifie la compatibilité de
format à chaque jointure, et produit un rapport de friction transmissible
à la conversation n8n pour le câblage du workflow.

Usage :
    export MEPA_SCRIPTS_DIR="$(pwd)/config"
    python3 tools/dry_run_pipeline.py config/WP-C2-1_Egypte2011_v62.json
    python3 tools/dry_run_pipeline.py config/WP-C1-1_Haiti_v62.json

Chaîne exécutée :
    [1] Node 2 audit (JS)     ─▶  runner_config
    [2] Runner (py)           ─▶  result
    [3] Sensitivity N1 (py)   ─▶  rapport_n1     (consomme runner_config)
    [4] Kappa CCI (py)        ─▶  cci_rapport    (consomme fiche × 2)
    [5] Passeport (py)        ─▶  passeport      (consomme result + cci_rapport)
"""

import sys
import os
import json
import tempfile
import subprocess
from pathlib import Path
from typing import Optional

# ── Chemins ──────────────────────────────────────────────────────────────────
REPO_ROOT   = Path(__file__).parent.parent.resolve()
SCRIPTS_DIR = REPO_ROOT / "scripts"
CONFIG_DIR  = REPO_ROOT / "config"
TESTS_DIR   = REPO_ROOT / "tests"
OUTPUT_DIR  = REPO_ROOT / "outputs" / "dry_run"

# Runner Python : mepa_constants.json est dans config/ en développement
os.environ.setdefault("MEPA_SCRIPTS_DIR", str(CONFIG_DIR))

sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(TESTS_DIR))   # pour _mepa_helpers

import mepa_runner_v2_gamma as runner_mod
from mepa_runner_v2_gamma import run_wp, PARAMS_REQUIS
import mepa_sensitivity_n1 as sensitivity_mod
from mepa_kappa_calculator import calculer_cci
import mepa_passeport_schema as passeport_mod
from _mepa_helpers import fiche_to_runner_config

# ── Passeport : clés obligatoires ────────────────────────────────────────────
PASSEPORT_CLES_OBLIGATOIRES = [
    "$schema", "generated_at", "identite", "certification",
    "simulation", "hash_integrite", "provenance_ia", "mepa_version",
    "statut_global",
]

# ── Console ───────────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def _ok(msg):   print(f"  {GREEN}✓{RESET} {msg}")
def _err(msg):  print(f"  {RED}✗{RESET} {msg}")
def _warn(msg): print(f"  {YELLOW}⚠{RESET} {msg}")

def _banner_step(n, name):
    print(f"\n{BOLD}{CYAN}[ÉTAPE {n}]{RESET}{BOLD} {name}{RESET}")

def _banner_junction(label):
    print(f"\n  {CYAN}⟶ JOINTURE{RESET} {label}")


# ─────────────────────────────────────────────────────────────────────────────
# ÉTAPE 1 — Node 2 Audit (JS)
# ─────────────────────────────────────────────────────────────────────────────

def run_step1_node2_audit(fiche_path: Path) -> dict:
    """
    Lance mepa_node2_audit_v62.js via Node.js avec un shim $input.

    Le fichier JS est un nœud n8n : il utilise `$input.item.json` (API n8n)
    et un `return [...]` au niveau racine. Le wrapper utilise `new Function`
    pour injecter le mock $input et rendre le return valide hors n8n.
    """
    _banner_step(1, f"Node 2 Audit (JS) — {fiche_path.name}")

    audit_js = SCRIPTS_DIR / "mepa_node2_audit_v62.js"
    fiche_path_str  = json.dumps(str(fiche_path))
    audit_js_str    = json.dumps(str(audit_js))

    wrapper_code = f"""
"use strict";
const fs   = require('fs');
const fiche = JSON.parse(fs.readFileSync({fiche_path_str}, 'utf8'));
const $input = {{ item: {{ json: fiche }} }};
const auditCode = fs.readFileSync({audit_js_str}, 'utf8');
let result;
try {{
    result = (new Function('$input', 'require', auditCode))($input, require);
}} catch (e) {{
    result = [{{ json: {{ statut_audit: 'ERROR', message: String(e) }} }}];
}}
process.stdout.write(JSON.stringify(result, null, 2));
"""

    env = os.environ.copy()
    env["MEPA_SCRIPTS_DIR"] = str(SCRIPTS_DIR)  # JS lit whitelist dans scripts/

    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.js', delete=False,
        encoding='utf-8', dir=tempfile.gettempdir()
    ) as f:
        f.write(wrapper_code)
        wrapper_path = f.name

    try:
        proc = subprocess.run(
            ["node", wrapper_path],
            capture_output=True, text=True, env=env, timeout=30
        )
    finally:
        try:
            os.unlink(wrapper_path)
        except OSError:
            pass

    if proc.returncode != 0:
        raise RuntimeError(
            f"Node.js subprocess échec (code={proc.returncode}):\n{proc.stderr.strip()}"
        )

    audit_output = json.loads(proc.stdout)
    node_result  = audit_output[0]["json"]

    statut = node_result.get("statut_audit", "?")
    if statut == "VALIDE":
        _ok(
            f"statut_audit = VALIDE "
            f"({node_result.get('nb_erreurs', 0)} erreur(s), "
            f"{node_result.get('nb_warnings', 0)} warning(s))"
        )
    elif statut == "DONNÉES_INSUFFISANTES":
        _warn("statut_audit = DONNÉES_INSUFFISANTES — NC bloquant détecté")
    else:
        _err(f"statut_audit = {statut} : {node_result.get('message', '')}")

    # ── Jointure Node 2 → Runner ──────────────────────────────────────────────
    _banner_junction("Node 2 → Runner")
    frictions = []
    rc = node_result.get("runner_config", {})

    for cle in ("wp_id", "sa", "y0", "t_max", "cmd", "params"):
        if cle in rc:
            _ok(f"runner_config.{cle} présent")
        else:
            _err(f"runner_config.{cle} ABSENT")
            frictions.append(f"runner_config.{cle} manquant en sortie Node 2")

    if isinstance(rc.get("y0"), list):
        _ok(f"y0 normalisé en liste {rc['y0']}")
    else:
        _err(f"y0 non normalisé : {type(rc.get('y0'))}")
        frictions.append("y0 non normalisé en liste [S,L,C,I] (ARCH-013)")

    cmd = rc.get("cmd", {})
    if "g" in cmd and "gamma" not in cmd:
        _err("cmd utilise 'g' au lieu de 'gamma' — violation C4")
        frictions.append("cmd.g résiduel au lieu de cmd.gamma — violation C4")
    else:
        _ok("cmd.gamma présent, pas de 'g' résiduel (C4 OK)")

    manquants = PARAMS_REQUIS - set(rc.get("params", {}).keys())
    if manquants:
        _err(f"params manquants dans runner_config : {sorted(manquants)}")
        frictions.append(
            f"params manquants dans runner_config.params : {sorted(manquants)}"
        )
    else:
        _ok(f"params complets ({len(rc.get('params', {}))} clés dont theta_C/I)")

    node_result["_frictions"] = frictions
    return node_result


# ─────────────────────────────────────────────────────────────────────────────
# ÉTAPE 2 — Runner Python
# ─────────────────────────────────────────────────────────────────────────────

def run_step2_runner(runner_config: dict) -> dict:
    """Lance run_wp(). Retourne le result dict enrichi de _frictions."""
    _banner_step(2, "Runner Python — run_wp()")

    result = run_wp(runner_config)
    traj   = result.get("simulation", {}).get("traj", "?")
    _ok(f"Simulation terminée — trajectoire : {traj!r}")

    frictions = []

    # ── Jointure Runner → Sensitivity ─────────────────────────────────────────
    _banner_junction("Runner → Sensitivity")
    _ok(
        "Sensitivity consomme runner_config (même entrée que le runner). "
        "Branches parallèles dans n8n — pas de transform."
    )

    # ── Jointure Runner → Passeport ───────────────────────────────────────────
    _banner_junction("Runner → Passeport")
    for cle in ("simulation", "verdict", "params", "cmd_base", "y0", "t_max", "meta"):
        if cle in result:
            _ok(f"result.{cle} présent")
        else:
            _err(f"result.{cle} ABSENT — passeport_schema l'attend")
            frictions.append(f"result.{cle} manquant pour passeport_schema")

    result["_frictions"] = frictions
    return result


# ─────────────────────────────────────────────────────────────────────────────
# ÉTAPE 3 — Sensitivity N1
# ─────────────────────────────────────────────────────────────────────────────

def run_step3_sensitivity(runner_config: dict, traj_runner: str) -> dict:
    """Lance run_sensitivity_n1(). Vérifie la cohérence baseline/runner."""
    _banner_step(3, "Sensitivity N1 — run_sensitivity_n1()")

    rapport = sensitivity_mod.run_sensitivity_n1(runner_config)
    _ok(f"Rapport N1 produit — traj_baseline : {rapport['traj_baseline']!r}")
    _ok(f"Verdict N1 : {rapport['resume']['verdict_n1']}")

    frictions = []

    # ── Jointure Sensitivity ↔ Runner ─────────────────────────────────────────
    _banner_junction("Sensitivity baseline ↔ Runner traj")
    if rapport["traj_baseline"] == traj_runner:
        _ok(f"Cohérence baseline/runner confirmée : {traj_runner!r}")
    else:
        _err(
            f"Divergence ! sensitivity.traj_baseline={rapport['traj_baseline']!r} "
            f"≠ runner.traj={traj_runner!r}"
        )
        frictions.append(
            f"Divergence traj_baseline sensitivity vs runner — "
            f"bug theta possible (cf. Mission 2)"
        )

    rapport["_frictions"] = frictions
    return rapport


# ─────────────────────────────────────────────────────────────────────────────
# ÉTAPE 4 — Kappa CCI
# ─────────────────────────────────────────────────────────────────────────────

def run_step4_kappa(fiche_path: Path) -> dict:
    """
    Lance calculer_cci() avec la fiche comme codeur A ET B.

    Format test uniquement : en production, fiche B est produite par CONV-B
    (codeur indépendant — protocole double aveugle). Le CCI obtenu ici (≈1.0)
    n'est pas représentatif d'un accord réel. L'objectif est de vérifier que
    la sortie du calculateur est compatible avec l'entrée de passeport_schema.
    """
    _banner_step(4, "Kappa CCI — calculer_cci() [format test]")

    _warn(
        "Fiche utilisée comme codeur A ET B (test format uniquement). "
        "En production : coordination humaine requise — CONV-B code "
        "indépendamment (contrainte double aveugle, pas un problème n8n)."
    )

    rapport = calculer_cci(str(fiche_path), str(fiche_path))

    cci     = rapport.get("cci")
    ksa     = rapport.get("kappa_sa")
    verdict = rapport.get("verdict", "?")
    _ok(
        f"CCI global : {cci:.4f}" if isinstance(cci, float) else f"CCI global : {cci}"
    )
    _ok(
        f"kappa_sa : {ksa:.4f}" if isinstance(ksa, float) else f"kappa_sa : {ksa}"
    )
    _ok(f"Verdict : {verdict}")

    # ── Jointure Kappa → Passeport ────────────────────────────────────────────
    _banner_junction("Kappa → Passeport (cci_rapport.json)")
    frictions = []
    for cle in ("cci", "kappa_sa", "variables_nc", "friction_vecteur", "verdict"):
        if cle in rapport:
            _ok(f"cci_rapport.{cle!r} présent")
        else:
            _err(f"cci_rapport.{cle!r} ABSENT — passeport_schema l'attend")
            frictions.append(f"cci_rapport['{cle}'] manquant pour passeport_schema")

    rapport["_frictions"] = frictions
    return rapport


# ─────────────────────────────────────────────────────────────────────────────
# ÉTAPE 5 — Passeport
# ─────────────────────────────────────────────────────────────────────────────

def run_step5_passeport(result: dict, cci_rapport: dict, wp_id: str) -> dict:
    """
    Génère le passeport en deux modes :
      a) Mémoire seule via passeport_depuis_result() (sans CCI) — mode n8n N7.
      b) Complet via generer_passeport() avec result.json + cci.json sur disque.
    """
    _banner_step(5, "Passeport — generer_passeport() + passeport_depuis_result()")

    frictions = []
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Mode a) — mémoire, sans CCI
    result_clean = {k: v for k, v in result.items() if not k.startswith("_")}
    passeport_min = passeport_mod.passeport_depuis_result(result_clean)
    _ok(
        f"Mode mémoire (sans CCI) : "
        f"statut_global = {passeport_min.get('statut_global')!r}"
    )

    # Mode b) — complet avec CCI sur disque
    result_path   = OUTPUT_DIR / f"{wp_id}_result.json"
    cci_path      = OUTPUT_DIR / f"{wp_id}_cci.json"
    passeport_path = OUTPUT_DIR / f"{wp_id}_passeport.json"

    result_path.write_text(
        json.dumps(result_clean, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    cci_clean = {k: v for k, v in cci_rapport.items() if not k.startswith("_")}
    cci_has_data = bool(cci_clean)
    if cci_has_data:
        cci_path.write_text(
            json.dumps(cci_clean, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    passeport = passeport_mod.generer_passeport(
        result_path      = str(result_path),
        rapport_path     = None,
        cci_rapport_path = str(cci_path) if cci_has_data else None,
        passeport_out    = str(passeport_path),
    )

    _ok(
        f"Mode complet (avec CCI) : "
        f"statut_global = {passeport.get('statut_global')!r}"
    )
    _ok(f"Passeport écrit : outputs/dry_run/{wp_id}_passeport.json")

    # Vérification structure obligatoire
    manquantes = [k for k in PASSEPORT_CLES_OBLIGATOIRES if k not in passeport]
    if manquantes:
        _err(f"Clés obligatoires manquantes : {manquantes}")
        frictions.append(f"Passeport incomplet — clés manquantes : {manquantes}")
    else:
        _ok("Toutes les clés obligatoires présentes")

    # Vérification intégration CCI
    cert = passeport.get("certification", {})
    if cci_has_data:
        if cert.get("cci") is not None:
            _ok(f"certification.cci intégré : {cert['cci']:.4f}")
        else:
            _warn("certification.cci = None — vérifier format cci_rapport")
            frictions.append(
                "CCI non intégré dans passeport.certification malgré cci_rapport fourni"
            )
    else:
        _warn("Étape 4 sans données — certification.cci = NON_CALCULÉ (attendu)")

    passeport["_frictions"] = frictions
    return passeport


# ─────────────────────────────────────────────────────────────────────────────
# RAPPORT DE FRICTION
# ─────────────────────────────────────────────────────────────────────────────

_FRICTIONS_STRUCTURELLES = [
    (
        "F6", "CORRIGÉ",
        "cmd_linear.note — clé non-numérique transmise par Node 2 au runner",
        (
            "Le Node 2 JS passe cmd_linear tel quel depuis la fiche, incluant la clé "
            "'note' (chaîne descriptive). make_cmd_linear() itérait sans distinction "
            "sur toutes les clés et échouait sur note (TypeError). "
            "Corrigé dans make_cmd_linear : guard isinstance(rng, dict) ignore les "
            "entrées non-numériques. Note persistante dans runner_config.cmd_linear "
            "est sans effet. Goldens inchangés (pytest 69/69)."
        ),
    ),
    (
        "F1", "INFO",
        "Node 2 JS — shim $input hors n8n",
        (
            "mepa_node2_audit_v62.js utilise $input.item.json (API n8n) et return [...] "
            "au niveau racine. Hors n8n, un wrapper new Function est nécessaire. "
            "Dans n8n, le nœud Code reçoit la fiche via $input directement — "
            "aucun wrapper requis en production."
        ),
    ),
    (
        "F2", "PROTOCOLE",
        "Kappa CCI — coordination humaine requise (double aveugle)",
        (
            "Le calculateur CCI attend deux fiches codées indépendamment (CONV-E + CONV-B). "
            "La disponibilité simultanée est une contrainte du protocole double aveugle, "
            "pas un problème de câblage n8n. Le nœud Kappa dans le workflow doit attendre "
            "que CONV-E ET CONV-B aient tous deux livré leur coding avant de s'exécuter. "
            "Dans n8n : utiliser un nœud Wait ou Merge pour synchroniser les deux branches."
        ),
    ),
    (
        "F3", "INFO",
        "Sensitivity et Runner — consommateurs parallèles de runner_config",
        (
            "sensitivity_n1 et runner consomment le même runner_config produit par Node 2. "
            "Dans n8n, les nœuds Runner (N3) et Sensitivity (N4) sont deux branches "
            "parallèles depuis la sortie de Node 2 — pas une chaîne séquentielle. "
            "Un nœud Split/Fan-out est nécessaire pour distribuer runner_config aux deux."
        ),
    ),
    (
        "F4", "INFO",
        "rapport.md (CONV-A) — étape LLM exclue du dry run",
        (
            "Le passeport peut intégrer le rapport rédigé par CONV-A (hash SHA-256). "
            "Cette étape est non déterministe (LLM) et exclue du dry run. "
            "Dans n8n, le nœud Passeport reçoit rapport_path depuis la sortie de CONV-A "
            "et peut générer le passeport final avec le hash du rapport inclus."
        ),
    ),
    (
        "F5", "DÉPLOIEMENT",
        "MEPA_SCRIPTS_DIR — contextes Python et JS divergents",
        (
            "Le runner Python cherche mepa_constants.json dans MEPA_SCRIPTS_DIR. "
            "Sur Pi5 en production : /data/mepa/scripts (constants.json co-localisé). "
            "En développement : constants.json est dans config/ — "
            "définir MEPA_SCRIPTS_DIR=$(pwd)/config pour Python. "
            "Le nœud JS Node 2 cherche mepa_whitelist_keys.json dans MEPA_SCRIPTS_DIR "
            "(scripts/) — les deux scripts ont des attentes différentes sur ce répertoire. "
            "Sur Pi5, les deux fichiers sont dans /data/mepa/scripts : pas de friction. "
            "En dev, penser à distinguer les deux chemins dans les tests."
        ),
    ),
]


def _print_friction_report(steps_frictions: dict):
    print(f"\n{'='*65}")
    print(f"{BOLD}  RAPPORT DE FRICTION INTER-SCRIPTS — MEPA V6.2{RESET}")
    print(f"  À transmettre à la conversation n8n pour le câblage.")
    print(f"{'='*65}")

    dynamic = [
        (step, msg)
        for step, msgs in steps_frictions.items()
        for msg in msgs
    ]

    if dynamic:
        print(f"\n{RED}{BOLD}  FRICTIONS DÉTECTÉES DANS CE RUN :{RESET}")
        for step, msg in dynamic:
            print(f"  {RED}✗{RESET} [{step}] {msg}")
    else:
        print(f"\n{GREEN}  Aucune friction dynamique détectée dans ce run.{RESET}")

    n_corriges = sum(1 for _, cat, *_ in _FRICTIONS_STRUCTURELLES if cat == "CORRIGÉ")
    print(
        f"\n{BOLD}  FRICTIONS STRUCTURELLES DOCUMENTÉES "
        f"({len(_FRICTIONS_STRUCTURELLES)}, dont {n_corriges} corrigée(s)) :{RESET}"
    )
    cat_colors = {"INFO": CYAN, "PROTOCOLE": YELLOW, "DÉPLOIEMENT": YELLOW, "CORRIGÉ": GREEN}
    for code, cat, titre, desc in _FRICTIONS_STRUCTURELLES:
        col = cat_colors.get(cat, CYAN)
        print(f"\n  {col}[{code} — {cat}]{RESET} {BOLD}{titre}{RESET}")
        # Wrap à 70 car
        words, line, lines = desc.split(), [], []
        for w in words:
            if sum(len(x) + 1 for x in line) + len(w) > 70:
                lines.append(" ".join(line))
                line = [w]
            else:
                line.append(w)
        if line:
            lines.append(" ".join(line))
        for l in lines:
            print(f"    {l}")

    print(f"\n{'='*65}\n")


# ─────────────────────────────────────────────────────────────────────────────
# POINT D'ENTRÉE PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def dry_run(fiche_path: Path, verbose: bool = True) -> dict:
    """
    Pipeline complet pour une fiche WP.

    Retourne un dict résumé :
        { wp_id, statut, traj, passeport_statut_global }
    Statut possible : "OK" | "OK_AVEC_FRICTIONS" | "ÉCHEC" | "INTERROMPU"
    """
    fiche_data = json.loads(fiche_path.read_text(encoding="utf-8"))
    wp_id = fiche_data.get("wp_id", fiche_path.stem)

    if verbose:
        print(f"\n{BOLD}{'='*65}")
        print(f"  DRY RUN PIPELINE — {wp_id}")
        print(f"  Fiche : {fiche_path.name}")
        print(f"{'='*65}{RESET}")

    steps_frictions: dict = {}

    # ── Étape 1 — Node 2 audit (JS) ───────────────────────────────────────────
    runner_config = None
    try:
        audit_out = run_step1_node2_audit(fiche_path)
        steps_frictions["Étape 1 — Node2"] = audit_out.get("_frictions", [])
        if audit_out.get("statut_audit") == "VALIDE":
            runner_config = audit_out["runner_config"]
        else:
            steps_frictions["Étape 1 — Node2"].append(
                f"Audit non VALIDE : statut={audit_out.get('statut_audit')}"
            )
    except Exception as exc:
        if verbose:
            _err(f"Node.js indisponible ou erreur ({exc}). Fallback Python.")
        steps_frictions["Étape 1 — Node2"] = [
            f"Node.js échec : {exc} — fallback fiche_to_runner_config() utilisé"
        ]

    if runner_config is None:
        # Fallback : équivalent Python du Node 2 (utilisé par les tests)
        if verbose:
            _warn("Fallback : fiche_to_runner_config() (équivalent Python de Node 2)")
        runner_config = fiche_to_runner_config(fiche_data)

    # ── Étape 2 — Runner ─────────────────────────────────────────────────────
    try:
        result = run_step2_runner(runner_config)
        steps_frictions["Étape 2 — Runner"] = result.get("_frictions", [])
        traj_runner = result.get("simulation", {}).get("traj", "?")
    except Exception as exc:
        if verbose:
            _err(f"Runner ÉCHEC : {exc}")
        steps_frictions["Étape 2 — Runner"] = [str(exc)]
        return {"wp_id": wp_id, "statut": "ÉCHEC", "etape": 2, "erreur": str(exc)}

    # ── Étape 3 — Sensitivity N1 ─────────────────────────────────────────────
    try:
        rapport_n1 = run_step3_sensitivity(runner_config, traj_runner)
        steps_frictions["Étape 3 — Sensitivity"] = rapport_n1.get("_frictions", [])
    except Exception as exc:
        if verbose:
            _err(f"Sensitivity ÉCHEC : {exc}")
        steps_frictions["Étape 3 — Sensitivity"] = [str(exc)]
        rapport_n1 = {}

    # ── Étape 4 — Kappa CCI ──────────────────────────────────────────────────
    try:
        cci_rapport = run_step4_kappa(fiche_path)
        steps_frictions["Étape 4 — Kappa"] = cci_rapport.get("_frictions", [])
    except Exception as exc:
        if verbose:
            _err(f"Kappa ÉCHEC : {exc}")
        steps_frictions["Étape 4 — Kappa"] = [str(exc)]
        cci_rapport = {}

    # ── Étape 5 — Passeport ──────────────────────────────────────────────────
    try:
        passeport = run_step5_passeport(result, cci_rapport, wp_id)
        steps_frictions["Étape 5 — Passeport"] = passeport.get("_frictions", [])
    except Exception as exc:
        if verbose:
            _err(f"Passeport ÉCHEC : {exc}")
        steps_frictions["Étape 5 — Passeport"] = [str(exc)]
        return {"wp_id": wp_id, "statut": "ÉCHEC", "etape": 5, "erreur": str(exc)}

    # ── Rapport de friction ───────────────────────────────────────────────────
    if verbose:
        _print_friction_report(steps_frictions)

    any_dynamic = any(steps_frictions.values())
    statut = "OK_AVEC_FRICTIONS" if any_dynamic else "OK"

    if verbose:
        col = GREEN if statut == "OK" else YELLOW
        print(f"{BOLD}  RÉSUMÉ {wp_id} : {col}{statut}{RESET}")
        print(f"  Trajectoire     : {traj_runner}")
        print(f"  Passeport       : {passeport.get('statut_global')}")
        print(f"  Fichier sortie  : outputs/dry_run/{wp_id}_passeport.json")
        print()

    return {
        "wp_id":                  wp_id,
        "statut":                 statut,
        "traj":                   traj_runner,
        "passeport_statut_global": passeport.get("statut_global"),
        "steps_frictions":        steps_frictions,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage : python3 tools/dry_run_pipeline.py <fiche.json> [fiche2.json ...]"
        )
        sys.exit(1)

    resultats = []
    for arg in sys.argv[1:]:
        p = Path(arg).resolve()
        if not p.exists():
            print(f"{RED}Fiche introuvable : {arg}{RESET}", file=sys.stderr)
            sys.exit(1)
        resultats.append(dry_run(p))

    hard_fails = [r for r in resultats if r.get("statut") in ("ÉCHEC", "INTERROMPU")]
    sys.exit(1 if hard_fails else 0)
