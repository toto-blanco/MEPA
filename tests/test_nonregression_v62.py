"""
Harnais de non-régression MEPA V6.2.

Usage :
    # 1. Générer les golden (première fois, ou après changement intentionnel validé)
    export MEPA_SCRIPTS_DIR="$(pwd)/scripts"
    pytest tests/ --generate-golden -v

    # 2. Vérification de régression (usage courant)
    export MEPA_SCRIPTS_DIR="$(pwd)/scripts"
    pytest tests/ -v
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import mepa_sensitivity_n1 as sensitivity  # noqa: E402

from _mepa_helpers import (
    GOLDEN_DIR,
    canonical_hash,
    collect_fiches,
    fiche_to_runner_config,
    load_fiche,
    stable_fields,
)
from mepa_runner_v2_gamma import run_wp

FICHES = collect_fiches()
GOLDEN_DIR.mkdir(exist_ok=True)


# ── Helpers locaux ────────────────────────────────────────────────────────────

def _run_wp_id(wp_id: str) -> dict:
    for wid, path in FICHES:
        if wid == wp_id:
            return run_wp(fiche_to_runner_config(load_fiche(path)))
    raise KeyError(f"WP non trouvé : {wp_id}")


def _config_for_wp_id(wp_id: str) -> dict:
    for wid, path in FICHES:
        if wid == wp_id:
            return fiche_to_runner_config(load_fiche(path))
    raise KeyError(f"WP non trouvé : {wp_id}")


# ── Tests de régression golden ────────────────────────────────────────────────

@pytest.mark.parametrize("wp_id,fiche_path", FICHES, ids=[x[0] for x in FICHES])
def test_golden(wp_id, fiche_path, generate_golden):
    """Exécute chaque WP/étalon et compare au snapshot golden (SHA-256)."""
    fiche  = load_fiche(fiche_path)
    config = fiche_to_runner_config(fiche)
    result = run_wp(config)
    stable = stable_fields(result)
    golden_path = GOLDEN_DIR / f"{wp_id}_result.json"

    if generate_golden:
        with open(golden_path, "w", encoding="utf-8") as f:
            json.dump(stable, f, indent=2, ensure_ascii=False, sort_keys=True)
        return

    assert golden_path.exists(), (
        f"Golden manquant pour {wp_id}. Générer avec : pytest --generate-golden"
    )
    with open(golden_path, encoding="utf-8") as f:
        golden = json.load(f)

    current_hash = canonical_hash(stable)
    golden_hash  = canonical_hash(golden)
    assert current_hash == golden_hash, (
        f"RÉGRESSION {wp_id}\n"
        f"  hash golden  : {golden_hash}\n"
        f"  hash current : {current_hash}\n"
        f"  traj golden  : {golden.get('simulation', {}).get('traj')}\n"
        f"  traj current : {stable.get('simulation', {}).get('traj')}"
    )


# ── Invariants de comportement ────────────────────────────────────────────────

@pytest.mark.xfail(
    strict=False,
    reason=(
        "WP-C1-1 fiche non encore complètement codée par CONV-E : "
        "concordance_attendue=False dans l'état courant V6.2. "
        "À dé-xfail quand CONV-E aura finalisé les variables continues."
    ),
)
def test_haiti_dissolution():
    """WP-C1-1 Haïti doit produire la trajectoire (d) Dissolution."""
    result = _run_wp_id("WP-C1-1")
    traj = result['simulation']['traj']
    assert traj == "(d) Dissolution", (
        f"WP-C1-1 : attendu '(d) Dissolution', obtenu '{traj}'"
    )


def test_egypte_repression_reussie():
    """WP-C2-1 Égypte doit produire la trajectoire (b) Répression réussie."""
    result = _run_wp_id("WP-C2-1")
    traj = result['simulation']['traj']
    assert traj == "(b) Répression réussie", (
        f"WP-C2-1 : attendu '(b) Répression réussie', obtenu '{traj}'"
    )


def test_nc_bloquant_raises():
    """gamma=NC (NC bloquant) doit lever RuntimeError avant toute simulation."""
    config = _config_for_wp_id("WP-C2-1")
    config['cmd']['gamma'] = 'NC'
    with pytest.raises(RuntimeError, match="NC bloquant"):
        run_wp(config)


def test_nc_non_bloquant_no_crash():
    """E=NC (NC non bloquant) → simulation avec fallback, meta renseigné, pas de crash."""
    config = _config_for_wp_id("WP-C2-1")
    config['cmd']['E'] = 'NC'
    result = run_wp(config)
    assert 'E' in result['meta']['nc_non_bloquantes'], (
        "E NC non bloquant attendu dans meta['nc_non_bloquantes']"
    )


def test_sa7_p6_modulation():
    """WP-I3, I4, I9 (Sa=7) → params['p6'] dans le résultat == p6_base × 1.5."""
    for wp_id in ["WP-I3-1", "WP-I4-1", "WP-I9-1"]:
        config = _config_for_wp_id(wp_id)
        assert config['sa'] == 7, f"{wp_id} : sa attendu 7, obtenu {config['sa']}"
        p6_base = config['params']['p6']
        result  = run_wp(config)
        p6_final = result['params']['p6']
        expected = p6_base * 1.5
        assert abs(p6_final - expected) < 0.001, (
            f"{wp_id} : p6_final={p6_final:.4f} ≠ p6_base×1.5={expected:.4f}"
        )


def test_cmd_linear_c1_eroi_dynamic():
    """WP-C1-1 (cluster C1) → cmd_linear présent dans le résultat et contient EROI."""
    result = _run_wp_id("WP-C1-1")
    assert result['cmd_linear'], (
        "WP-C1-1 devrait avoir cmd_linear non vide dans le résultat"
    )
    assert 'EROI' in result['cmd_linear'], (
        f"cmd_linear devrait contenir 'EROI', contenu : {result['cmd_linear']}"
    )


# ── Mission 2 — Bug theta dans mepa_sensitivity_n1 ───────────────────────────

def test_theta_injection_sensitivity_baseline():
    """
    Prouve que _inject_theta() est maintenant appelé dans run_sensitivity_n1().

    Construit un config avec theta_C=0.40 / theta_I=0.30 à la racine mais
    ABSENT de config['params'] (format v1.x qui déclenchait le bug).
    Vérifie que la traj_baseline de sensitivity_n1 correspond à celle de run_wp()
    avec les mêmes theta effectifs.
    """
    from mepa_runner_v2_gamma import _inject_theta, apply_sa_modulator

    base = _config_for_wp_id("WP-C2-1")

    # Construire un config v1.x : theta à la racine, absent de params
    custom_theta_C = 0.40
    custom_theta_I = 0.30
    config = dict(base)
    config['theta_C'] = custom_theta_C
    config['theta_I'] = custom_theta_I
    params_sans_theta = {k: v for k, v in base['params'].items()
                         if k not in ('theta_C', 'theta_I')}
    config['params'] = params_sans_theta

    # Vérifier que _inject_theta propage bien les valeurs racine dans p
    p_sa = apply_sa_modulator(config['params'], config['sa'])
    p_injected = _inject_theta(p_sa, config)
    assert abs(p_injected['theta_C'] - custom_theta_C) < 1e-9, (
        f"_inject_theta : theta_C attendu {custom_theta_C}, obtenu {p_injected['theta_C']}"
    )
    assert abs(p_injected['theta_I'] - custom_theta_I) < 1e-9, (
        f"_inject_theta : theta_I attendu {custom_theta_I}, obtenu {p_injected['theta_I']}"
    )

    # Vérifier que run_wp et sensitivity_n1 partagent la même traj de référence
    result_runner   = run_wp(config)
    rapport_n1      = sensitivity.run_sensitivity_n1(config)

    assert rapport_n1['traj_baseline'] == result_runner['simulation']['traj'], (
        f"Divergence theta : sensitivity baseline='{rapport_n1['traj_baseline']}' "
        f"≠ runner traj='{result_runner['simulation']['traj']}'"
    )


@pytest.mark.parametrize("wp_id,fiche_path",
                         [(wid, p) for wid, p in FICHES if wid.startswith("WP-")],
                         ids=[wid for wid, _ in FICHES if wid.startswith("WP-")])
def test_sensitivity_no_error(wp_id, fiche_path):
    """Aucune exception sur les 27 WP après correction du bug theta."""
    fiche  = load_fiche(fiche_path)
    config = fiche_to_runner_config(fiche)
    sensitivity.run_sensitivity_n1(config)  # doit terminer sans exception


# ── Mission 4 — Validation paramètres requis ─────────────────────────────────

def test_params_manquants_raises():
    """config['params'] sans 'p6' → ValueError mentionnant 'p6'."""
    config = _config_for_wp_id("WP-C2-1")
    del config['params']['p6']
    with pytest.raises(ValueError, match="p6"):
        run_wp(config)


# ── Mission 3 — Provenance et versions dans mepa_passeport_schema ────────────

import importlib
import mepa_passeport_schema as passeport_schema  # noqa: E402


def _make_minimal_result(wp_id: str = "WP-C2-1") -> dict:
    """Construit un result dict minimal valide pour passeport_depuis_result()."""
    fiche  = load_fiche(str(next(p for wid, p in FICHES if wid == wp_id)))
    config = fiche_to_runner_config(fiche)
    return run_wp(config)


def test_passeport_modele_env_var(monkeypatch):
    """MEPA_IA_MODEL=claude-test → provenance_ia['modele'] == 'claude-test'."""
    monkeypatch.setenv("MEPA_IA_MODEL", "claude-test")
    # Recharger le module pour que os.environ.get() soit réévalué
    importlib.reload(passeport_schema)

    result    = _make_minimal_result()
    passeport = passeport_schema.passeport_depuis_result(result)

    assert passeport["provenance_ia"]["modele"] == "claude-test", (
        f"modele attendu 'claude-test', obtenu '{passeport['provenance_ia']['modele']}'"
    )

    # Restaurer l'état du module après le test
    monkeypatch.delenv("MEPA_IA_MODEL", raising=False)
    importlib.reload(passeport_schema)


def test_passeport_modele_conv_e_meta():
    """_conv_e_meta dans result → prioritaire sur env var."""
    result = _make_minimal_result()
    result["_conv_e_meta"] = {"modele": "claude-opus-custom"}

    passeport = passeport_schema.passeport_depuis_result(result)

    assert passeport["provenance_ia"]["modele"] == "claude-opus-custom", (
        f"_conv_e_meta non prioritaire : obtenu '{passeport['provenance_ia']['modele']}'"
    )


def test_passeport_versions_reelles():
    """mepa_version reflète les versions réelles des scripts (runner 2.1.1, constants 1.2.3)."""
    result    = _make_minimal_result()
    passeport = passeport_schema.passeport_depuis_result(result)
    mv        = passeport["mepa_version"]

    assert "2.1.1" in mv["runner"], (
        f"runner attendu contenir '2.1.1', obtenu '{mv['runner']}'"
    )
    assert "2.1.1" in mv["audit"], (
        f"audit attendu contenir '2.1.1', obtenu '{mv['audit']}'"
    )
    assert "1.2.3" in mv["constants"], (
        f"constants attendu contenir '1.2.3', obtenu '{mv['constants']}'"
    )


def test_passeport_structure_valide():
    """Le passeport contient toutes les sections obligatoires (équivalent validate())."""
    CLES_OBLIGATOIRES = [
        "$schema", "generated_at", "identite", "certification",
        "simulation", "hash_integrite", "provenance_ia", "mepa_version",
        "statut_global",
    ]
    result    = _make_minimal_result()
    passeport = passeport_schema.passeport_depuis_result(result)

    manquantes = [k for k in CLES_OBLIGATOIRES if k not in passeport]
    assert not manquantes, f"Clés obligatoires manquantes dans le passeport : {manquantes}"

    assert passeport["$schema"] == "mepa-passeport-v2.0", (
        f"$schema inattendu : '{passeport['$schema']}'"
    )
    assert passeport["provenance_ia"].get("modele"), "provenance_ia.modele vide"
    assert passeport["mepa_version"].get("label") == "MEPA V6.2 Fortifiée"
