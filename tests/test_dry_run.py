"""
Tests de la chaîne dry_run_pipeline bout en bout — Mission 5.

Vérifie que les deux cas représentatifs produisent un passeport complet
sans erreur fatale. Le statut "OK_AVEC_FRICTIONS" est accepté (frictions
structurelles documentées, pas des erreurs).
"""
import sys
from pathlib import Path

import pytest

# tools/ sur le path pour importer dry_run_pipeline
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
import dry_run_pipeline as drp

CONFIG_DIR = Path(__file__).parent.parent / "config"

FICHE_EGYPTE = CONFIG_DIR / "WP-C2-1_Egypte2011_v62.json"
FICHE_HAITI  = CONFIG_DIR / "WP-C1-1_Haiti_v62.json"


def _run(fiche: Path) -> dict:
    """Lance le dry run en mode silencieux (verbose=False)."""
    return drp.dry_run(fiche, verbose=False)


# ── WP-C2-1 Égypte (statique, EROI dynamique C2) ─────────────────────────────

def test_dry_run_egypte_statut():
    """Pipeline WP-C2-1 sans erreur fatale — statut OK ou OK_AVEC_FRICTIONS."""
    r = _run(FICHE_EGYPTE)
    assert r["statut"] in ("OK", "OK_AVEC_FRICTIONS"), (
        f"Statut inattendu pour WP-C2-1 : {r['statut']} — erreur : {r.get('erreur')}"
    )


def test_dry_run_egypte_trajectoire():
    """WP-C2-1 → trajectoire '(b) Répression réussie' bout en bout."""
    r = _run(FICHE_EGYPTE)
    assert r.get("traj") == "(b) Répression réussie", (
        f"Trajectoire inattendue : {r.get('traj')!r}"
    )


def test_dry_run_egypte_passeport():
    """WP-C2-1 → passeport avec statut_global renseigné."""
    r = _run(FICHE_EGYPTE)
    sg = r.get("passeport_statut_global")
    assert sg is not None, "passeport_statut_global absent du résumé"
    # statut_global est un dict ou une string selon l'implémentation
    assert sg, "passeport_statut_global vide"


def test_dry_run_egypte_pas_de_friction_runner():
    """Aucune friction dynamique sur Étape 2 (Runner) pour WP-C2-1."""
    r = _run(FICHE_EGYPTE)
    frictions_runner = r.get("steps_frictions", {}).get("Étape 2 — Runner", [])
    assert not frictions_runner, (
        f"Frictions Runner inattendues pour WP-C2-1 : {frictions_runner}"
    )


# ── WP-C1-1 Haïti (C1 dynamique cmd_linear) ──────────────────────────────────

def test_dry_run_haiti_statut():
    """Pipeline WP-C1-1 sans erreur fatale — statut OK ou OK_AVEC_FRICTIONS."""
    r = _run(FICHE_HAITI)
    assert r["statut"] in ("OK", "OK_AVEC_FRICTIONS"), (
        f"Statut inattendu pour WP-C1-1 : {r['statut']} — erreur : {r.get('erreur')}"
    )


def test_dry_run_haiti_cmd_linear_coherence():
    """
    WP-C1-1 (cmd_linear EROI dynamique) : traj_baseline sensitivity == runner traj.
    Vérifie que le cmd_linear est bien appliqué dans les deux branches.
    """
    r = _run(FICHE_HAITI)
    frictions_sens = r.get("steps_frictions", {}).get("Étape 3 — Sensitivity", [])
    assert not frictions_sens, (
        f"Divergence traj_baseline/runner sur WP-C1-1 (cmd_linear) : {frictions_sens}"
    )


def test_dry_run_haiti_passeport_produit():
    """WP-C1-1 → passeport créé sur disque (même si non-concordance attendue)."""
    _run(FICHE_HAITI)
    passeport_path = drp.OUTPUT_DIR / "WP-C1-1_passeport.json"
    assert passeport_path.exists(), (
        f"Passeport WP-C1-1 non trouvé : {passeport_path}"
    )
