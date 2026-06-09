"""
Helpers partagés pour les tests MEPA V6.2.

fiche_to_runner_config() réplique la logique de construction du runner_config
effectuée par mepa_node2_audit_v62.js (nœud n8n Node 2).
"""
import glob
import hashlib
import json
import os
import sys
from pathlib import Path

REPO_ROOT  = Path(__file__).parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
CONFIG_DIR  = REPO_ROOT / "config"
GOLDEN_DIR  = Path(__file__).parent / "golden"

# scripts/ sur sys.path pour l'import du runner
sys.path.insert(0, str(SCRIPTS_DIR))

# MEPA_SCRIPTS_DIR : le runner lit mepa_constants.json depuis ce chemin.
# En dev le fichier est dans config/ ; on pointe vers config/ pour éviter
# les RuntimeWarning "theta_FR introuvable". Sur Pi5, c'est /data/mepa/scripts/.
os.environ.setdefault("MEPA_SCRIPTS_DIR", str(CONFIG_DIR))

# ── P_DEFAULTS ────────────────────────────────────────────────────────────────
# Miroir de _P_DEFAULTS_FALLBACK dans mepa_node2_audit_v62.js.
_P_DEFAULTS_FALLBACK = {
    'p1': 0.08, 'p2': 0.045, 'p2b': 0.06, 'p3': 0.02, 'p4': 0.40,
    'p5': 0.05, 'p6': 0.12,  'p7': 0.04,  'p8': 0.03, 'p9': 0.06,
    'p10': 0.80, 'p11a': 0.60, 'p11b': 0.15, 'p13': 1.2,
    'lam': 0.68, 'mu': 0.38, 'nu': 0.62, 'rho': 0.06,
}

CMD_KEYS = ["T", "Mob", "R", "Ref", "Rc", "Rn", "E", "gamma", "EROI", "Pop"]


def _load_p_defaults() -> dict:
    """Charge P_DEFAULTS depuis config/mepa_constants.json, avec fallback."""
    try:
        with open(CONFIG_DIR / "mepa_constants.json", encoding="utf-8") as f:
            constants = json.load(f)
        bp = constants.get("bornes_parametres_dynamiques", {})
        out = dict(_P_DEFAULTS_FALLBACK)
        for k in out:
            if k in bp and "defaut" in bp[k]:
                out[k] = bp[k]["defaut"]
        return out
    except Exception:
        return dict(_P_DEFAULTS_FALLBACK)


P_DEFAULTS = _load_p_defaults()


def fiche_to_runner_config(fiche: dict) -> dict:
    """
    Convertit une fiche WP en runner_config accepté par run_wp().

    Réplique la construction effectuée dans mepa_node2_audit_v62.js :
      - conditions_initiales → y0 [S0, L0, C0, I0]
      - commandes (sans 'note') → cmd
      - parametres_simulation.{theta_C, theta_I, t_max} → racine + params
      - P_DEFAULTS fusionné avec fiche.params_p → params
      - cmd_linear nettoyé (clé 'note' retirée)
    """
    ci = fiche.get("conditions_initiales", {})
    if isinstance(ci, list):
        defaults = [1.0, 0.5, 0.1, 3.5]
        y0 = [float(ci[i]) if i < len(ci) else defaults[i] for i in range(4)]
    else:
        y0 = [
            float(ci.get("S0", 1.0)),
            float(ci.get("L0", 0.5)),
            float(ci.get("C0", 0.1)),
            float(ci.get("I0", 3.5)),
        ]

    params_sim = fiche.get("parametres_simulation", {})
    theta_C = float(params_sim.get("theta_C", fiche.get("theta_C", 0.30)))
    theta_I = float(params_sim.get("theta_I", fiche.get("theta_I", 0.22)))
    t_max   = int(params_sim.get("t_max",   fiche.get("t_max",   300)))

    # params_p : surcharges de calibration spécifiques au WP (ex. Rwanda I10)
    params_p_fiche = {
        k: v for k, v in fiche.get("params_p", {}).items()
        if not k.startswith("$")
    }
    params_runner = {**P_DEFAULTS, **params_p_fiche, "theta_C": theta_C, "theta_I": theta_I}

    cmd_raw = fiche.get("commandes", {})
    cmd_clean = {}
    for key in CMD_KEYS:
        if key in cmd_raw:
            val = cmd_raw[key]
            if isinstance(val, str) and val.strip().upper() == "NC":
                cmd_clean[key] = "NC"
            else:
                try:
                    cmd_clean[key] = float(val)
                except (TypeError, ValueError):
                    cmd_clean[key] = val

    cmd_linear = fiche.get("cmd_linear")
    if isinstance(cmd_linear, dict):
        cmd_linear = {k: v for k, v in cmd_linear.items() if k != "note"}
        if not cmd_linear:
            cmd_linear = None

    return {
        "wp_id":                fiche.get("wp_id"),
        "cas":                  fiche.get("cas"),
        "cluster":              fiche.get("cluster"),
        "trajectoire_attendue": fiche.get("trajectoire_attendue"),
        "sa":                   int(fiche.get("sa", 4)),
        "y0":                   y0,
        "t_max":                t_max,
        "theta_C":              theta_C,
        "theta_I":              theta_I,
        "cmd":                  cmd_clean,
        "cmd_linear":           cmd_linear,
        "params":               params_runner,
    }


def load_fiche(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def collect_fiches() -> list:
    """Retourne la liste triée (test_id, chemin) pour les 27 WP + 2 étalons.

    test_id = wp_id pour les fiches WP, wp_id + "_etalon" pour les étalons.
    Garantit l'unicité des IDs et des fichiers golden.
    """
    result = []
    for p in sorted(glob.glob(str(CONFIG_DIR / "WP-*.json"))):
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        result.append((d.get("wp_id", Path(p).stem), p))
    for p in sorted(glob.glob(str(CONFIG_DIR / "fiche_etalon_*.json"))):
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        test_id = d.get("wp_id", Path(p).stem) + "_etalon"
        result.append((test_id, p))
    return result


def stable_fields(result: dict) -> dict:
    """Extrait les champs stables pour la comparaison golden (exclut meta)."""
    keys = [
        "simulation", "verdict", "stress_n1", "stress_n2",
        "params", "cmd_base", "cmd_linear", "y0", "t_max",
    ]
    return {k: result[k] for k in keys if k in result}


def canonical_hash(obj: dict) -> str:
    """SHA-256 de la sérialisation JSON déterministe (clés triées, compact)."""
    canon = json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return hashlib.sha256(canon.encode()).hexdigest()


