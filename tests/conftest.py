"""Fixtures pytest et option --generate-golden pour les tests MEPA V6.2."""
import sys
from pathlib import Path

# tests/ doit être sur sys.path pour que _mepa_helpers soit importable
# depuis conftest.py et depuis les modules de test.
sys.path.insert(0, str(Path(__file__).parent))

import pytest  # noqa: E402


def pytest_configure(config):
    # Le runner émet ce RuntimeWarning quand MEPA_SCRIPTS_DIR pointe vers scripts/
    # (dev) au lieu de config/ (où mepa_constants.json se trouve). Le fallback
    # theta_FR=0.75 est identique à la valeur dans mepa_constants.json — cosmétique.
    config.addinivalue_line(
        "filterwarnings",
        "ignore:.*theta_FR introuvable.*:RuntimeWarning",
    )


def pytest_addoption(parser):
    parser.addoption(
        "--generate-golden",
        action="store_true",
        default=False,
        help="Régénère les snapshots golden au lieu de comparer.",
    )


@pytest.fixture(scope="session")
def generate_golden(request):
    return request.config.getoption("--generate-golden")
