"""
test_golden_v7.py — Non-régression du runner V7 sur les six runs certifiés (V7.0-P1).

Invariant protégé : bit-identité des résultats certifiés (ARCH-AG-01, I-1).
Pour chaque cas, le runner V7 (mepa_runner_v3_v7) est relancé sur les entrées
certifiées ; sa sortie, écrite au format du runner, doit avoir exactement la même
empreinte sha256 que le result.json certifié, elle-même égale à
hash_integrite.result_json_sha256 du passeport de juin 2026.

Toute modification du runner, des constantes ou du solveur qui change un résultat
certifié, même d'un seul bit, fait échouer ce test.

Données : tests/golden_v7/ (MANIFEST.json, {wp}_config.json, {wp}_result.json).
Seules différences neutralisées, toutes deux postérieures à juin 2026 :
  - le bloc advisory_dev1, ajouté au runner après la certification ;
  - meta.generated_at, horodatage d'exécution (remis à sa valeur d'origine).
"""
import copy
import hashlib
import json
import os
import sys
import warnings
from pathlib import Path

import pytest

ICI = Path(__file__).parent
REPO = ICI.parent
GOLDEN = ICI / "golden_v7"

# Les scripts lisent mepa_constants.json dans MEPA_SCRIPTS_DIR ; dans le dépôt, il est
# dans config/. À fixer AVANT l'import du runner, qui lit ses constantes au chargement.
os.environ.setdefault("MEPA_SCRIPTS_DIR", str(REPO / "config"))
sys.path.insert(0, str(REPO / "scripts"))
import mepa_runner_v3_v7 as runner  # noqa: E402

MANIFEST = json.loads((GOLDEN / "MANIFEST.json").read_text(encoding="utf-8"))
CAS = sorted(MANIFEST["cas"])


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def test_golden_v7_integrite_des_references():
    """Les fichiers de référence sont intacts : empreinte = manifeste = passeport."""
    for wp in CAS:
        c = MANIFEST["cas"][wp]
        assert _sha((GOLDEN / c["result"]).read_bytes()) == c["result_sha256"], f"{wp} : result.json de référence altéré"
        assert _sha((GOLDEN / c["config"]).read_bytes()) == c["config_sha256"], f"{wp} : config de référence altérée"


def test_golden_v7_constantes_reelles():
    """Le test tourne sur les vraies constantes, jamais sur un repli silencieux."""
    assert (Path(os.environ["MEPA_SCRIPTS_DIR"]) / "mepa_constants.json").exists(), (
        f"mepa_constants.json introuvable dans MEPA_SCRIPTS_DIR={os.environ['MEPA_SCRIPTS_DIR']}"
    )


@pytest.mark.parametrize("wp", CAS)
def test_golden_v7_bit_identite(wp):
    c = MANIFEST["cas"][wp]
    config = json.loads((GOLDEN / c["config"]).read_text(encoding="utf-8"))
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        sortie = runner.run_wp(copy.deepcopy(config))
    fallback = [str(x.message) for x in w if "fallback" in str(x.message).lower() or "introuvable" in str(x.message)]
    assert not fallback, f"{wp} : constantes en repli pendant le run : {fallback}"

    sortie.pop("advisory_dev1", None)
    sortie["meta"]["generated_at"] = c["generated_at"]
    octets = json.dumps(sortie, indent=2, ensure_ascii=False).encode("utf-8")   # format d'écriture du runner
    obtenu = _sha(octets)
    if obtenu != c["result_sha256"]:
        ref = json.loads((GOLDEN / c["result"]).read_text(encoding="utf-8"))
        blocs = [k for k in set(ref) | set(sortie) if ref.get(k) != sortie.get(k)]
        pytest.fail(f"RÉGRESSION {wp} : sha256 {obtenu[:16]}… ≠ certifié {c['result_sha256'][:16]}… "
                    f"| blocs différents : {sorted(blocs) or 'aucun (mise en forme seulement)'}")
