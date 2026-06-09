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
import pytest

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
