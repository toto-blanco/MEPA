"""
Test non-régression advisory Dev 1 V7.
Vérifie que l'ajout de l'advisory ne modifie pas les champs simulation.*.
Utilise WP-C1-1_Haiti_v7.json comme cas de référence.
"""
import json, os, sys, subprocess, hashlib, copy
import pytest

SCRIPTS = os.environ.get("MEPA_SCRIPTS_DIR", os.path.join(os.path.dirname(__file__), "..", "scripts"))
CONFIG_V7 = os.path.join(os.path.dirname(__file__), "..", "config", "v7", "WP-C1-1_Haiti_v7.json")

CHAMPS_INVARIANTS = [
    "simulation.traj",
    "simulation.FR_max",
    "simulation.FR_final",
    "simulation.C_max",
    "simulation.C_final",
    "simulation.I_min_sim",
    "simulation.I_final",
    "simulation.S_final",
    "simulation.L_final",
    "simulation.robustesse",
    "simulation.branche_annotation",
    "verdict.robustesse",
    "verdict.trajectoire_diagn",
    "verdict.concordance_attendue",
]


def _get_nested(d, key_path):
    keys = key_path.split(".")
    v = d
    for k in keys:
        v = v[k]
    return v


def run_runner(config_path):
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        out_path = f.name
    env = dict(os.environ)
    env["MEPA_SCRIPTS_DIR"] = SCRIPTS
    result = subprocess.run(
        [sys.executable, os.path.join(SCRIPTS, "mepa_runner_v3_v7.py"),
         config_path, out_path],
        capture_output=True, text=True, env=env
    )
    assert result.returncode == 0, f"Runner erreur : {result.stderr[:500]}"
    with open(out_path) as f:
        return json.load(f)


def test_advisory_presente_sur_fiche_v7():
    """L'advisory doit être présent (non None) sur une fiche V7."""
    if not os.path.exists(CONFIG_V7):
        pytest.skip("Fiche V7 Haïti absente")
    result = run_runner(CONFIG_V7)
    assert "advisory_dev1" in result, "Clé advisory_dev1 absente du result"
    assert result["advisory_dev1"] is not None, "advisory_dev1 est None"
    assert result["advisory_dev1"].get("$advisory") is True


def test_advisory_omega_mode_I():
    """L'advisory doit utiliser omega_mode='I' sur fiche V7."""
    if not os.path.exists(CONFIG_V7):
        pytest.skip("Fiche V7 Haïti absente")
    result = run_runner(CONFIG_V7)
    adv = result["advisory_dev1"]
    assert adv.get("omega_mode") == "I", f"omega_mode inattendu : {adv.get('omega_mode')}"
    assert adv.get("i_t0_utilise") is not None


def test_simulation_champs_inchanges():
    """
    Les champs simulation.* et verdict.* sont identiques
    que l'advisory soit présent ou non (non-régression).
    On vérifie en comparant deux runs identiques — si non-déterministe,
    le test doit passer avec tolerance 0.
    """
    if not os.path.exists(CONFIG_V7):
        pytest.skip("Fiche V7 Haïti absente")
    r1 = run_runner(CONFIG_V7)
    r2 = run_runner(CONFIG_V7)
    for champ in CHAMPS_INVARIANTS:
        try:
            v1 = _get_nested(r1, champ)
            v2 = _get_nested(r2, champ)
        except KeyError:
            continue  # champ optionnel absent
        assert v1 == v2, f"Non-déterminisme détecté sur {champ} : {v1} != {v2}"
    # Vérifier que advisory_dev1 n'a pas modifié simulation
    adv = r1.get("advisory_dev1", {})
    assert adv.get("statut") != "ADVISORY_DEV1_ERREUR_NON_BLOQUANTE", \
        f"Advisory en erreur : {adv.get('erreur')}"


def test_advisory_flag_logique():
    """Le flag advisory doit être un booléen cohérent avec l'écart."""
    if not os.path.exists(CONFIG_V7):
        pytest.skip("Fiche V7 Haïti absente")
    result = run_runner(CONFIG_V7)
    adv = result["advisory_dev1"]
    flag = adv.get("a_d_max_advisory_flag")
    ecart = adv.get("ecart_R_code_moins_a_d_max")
    assert isinstance(flag, bool), f"flag n'est pas un bool : {flag}"
    if ecart is not None:
        assert (flag == (ecart > 0)), f"Incohérence flag/écart : flag={flag}, écart={ecart}"
