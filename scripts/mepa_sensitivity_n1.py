#!/usr/bin/env python3
"""
MEPA V6.2 — Script de Sensibilité Niveau 1 (Protocole §3)
================================================================================
Version          : 2.0.0
MEPA version     : 6.2 Fortifiée
Dépendances      : stdlib uniquement (via mepa_runner_v2_gamma.py)
Chemins          : MEPA_SCRIPTS_DIR (défaut /data/mepa/scripts) — ARCH-015
Usage : python3 mepa_sensitivity_n1.py config_wp.json [output_n1.json]

Implémente le Niveau 1 du protocole de stress-test :
  "Chaque variable critique est perturbée de ±20% (variables continues)
   ou d'un cran (variables catégorielles) pendant que toutes les autres
   restent à leur valeur de référence."
  — MEPA_Protocole_Experimental_V6_2 §3, Niveau 1

COMPLÉMENT au runner mepa_runner_v2_gamma.py qui implémente N1 partiel
(E±0.08, R±0.08) et N2 partiel (4 variables).

Ce script ajoute :
  • ±20% sur les 9 variables cmd (toutes, une par une)
  • Rapport de sensibilité par variable : changement de trajectoire O/N
  • Identification automatique des variables les plus sensibles
    → input pour le Niveau 2 (combinaisons critiques)
"""

import json, sys, copy, os
from typing import Callable

# ── Import du runner V6.2 (ARCH-015) ─────────────────────────────────────────
# Chemin canonique Pi5 via variable d'environnement (cohérence avec runner V2.0)
MEPA_SCRIPTS_DIR = os.environ.get("MEPA_SCRIPTS_DIR", "/data/mepa/scripts")

# Ajouter MEPA_SCRIPTS_DIR en premier dans le path de recherche
if MEPA_SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, MEPA_SCRIPTS_DIR)

# Fallback : répertoire du script courant
_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

try:
    import mepa_runner_v2_gamma as runner
except ImportError as e:
    raise ImportError(
        f"mepa_runner_v2_gamma.py introuvable. "
        f"Chemins cherchés : {MEPA_SCRIPTS_DIR}, {_script_dir}. "
        f"Définir MEPA_SCRIPTS_DIR=/data/mepa/scripts ou placer les scripts "
        f"dans le même répertoire. Erreur : {e}"
    )


# ── VARIABLES CMD ET LEURS PERTURBATIONS ────────────────────────────────────
# Protocole §3 Niveau 1 : ±20% sur continues, ±1 cran sur catégorielles
# Pour les commandes MEPA : toutes continues [0,1] ou [0,10] sauf Sa (paramètre, pas cmd)

CMD_PERTURBATIONS = {
    # var : (delta_relatif, min_physique, max_physique)
    'T'    : (0.20, 0.0, 10.0),
    'Mob'  : (0.20, 0.0, 1.0),
    'R'    : (0.20, 0.0, 10.0),
    'Ref'  : (0.20, 0.0, 1.0),
    'Rc'   : (0.20, 0.0, 1.0),
    'Rn'   : (0.20, 0.0, 1.0),
    'E'    : (0.20, 0.0, 1.0),
    'gamma': (0.20, 0.0, 1.0),
    'EROI' : (0.20, 1.01, 100.0),
}

# Perturbations sur les paramètres p1-p13 (sensibilité paramétrique)
PARAM_PERTURBATIONS = {
    'p1': 0.20, 'p2': 0.20, 'p3': 0.20, 'p4': 0.20,
    'p5': 0.20, 'p6': 0.20, 'p7': 0.20, 'p8': 0.20,
    'p9': 0.20, 'p10': 0.20, 'p11a': 0.20, 'p11b': 0.20,
    'p13': 0.20, 'lam': 0.20, 'mu': 0.20, 'nu': 0.20,
}


def perturber_cmd(cmd_base: dict, var: str, signe: int) -> dict:
    """Applique ±20% sur une variable cmd, les autres inchangées."""
    delta_rel, min_val, max_val = CMD_PERTURBATIONS[var]
    val_base = cmd_base.get(var, 0.0)
    delta_abs = abs(val_base) * delta_rel if val_base != 0 else delta_rel * 0.1
    val_new = val_base + signe * delta_abs
    val_new = max(min_val, min(max_val, val_new))
    cmd_new = dict(cmd_base)
    cmd_new[var] = round(val_new, 4)
    return cmd_new


def perturber_param(params_base: dict, var: str, signe: int) -> dict:
    """Applique ±20% sur un paramètre p_k, les autres inchangés."""
    delta_rel = PARAM_PERTURBATIONS[var]
    val_base = params_base.get(var, 0.0)
    delta_abs = abs(val_base) * delta_rel if val_base != 0 else delta_rel * 0.01
    val_new = val_base + signe * delta_abs
    val_new = max(0.0001, val_new)  # pas de paramètre négatif
    params_new = dict(params_base)
    params_new[var] = round(val_new, 6)
    return params_new


def run_sensitivity_n1(config: dict) -> dict:
    """
    Niveau 1 complet : ±20% sur chaque variable cmd + chaque paramètre p_k.

    Retourne :
    - traj_baseline : trajectoire de référence
    - resultats_cmd : { var: { '+20%': {traj, changement}, '-20%': ... } }
    - resultats_params : idem pour paramètres
    - variables_sensibles : variables dont AU MOINS UNE perturbation change la traj
    - recommandation_n2 : top-3 variables les plus sensibles pour le Niveau 2
    """
    # ── Simulation de référence ──────────────────────────────────────────────
    p_ref      = runner.apply_sa_modulator(config['params'], int(config['sa']))
    cmd_base   = runner._normalize_cmd(config['cmd'])
    # Note : normalizeGamma_dict() n'existe pas dans runner V2.0 — _normalize_cmd() est la méthode correcte.
    linear     = config.get('cmd_linear', {})
    y0         = config['y0']
    t_max      = int(config['t_max'])
    cmd_fn_ref = runner.make_cmd_linear(cmd_base, linear, t_max) if linear \
                 else (lambda t, _c=cmd_base: _c)

    ref = runner.simulate(p_ref, cmd_fn_ref, y0, t_max)
    traj_ref = ref['traj']

    # ── Niveau 1 — Variables CMD ─────────────────────────────────────────────
    resultats_cmd = {}
    for var in CMD_PERTURBATIONS:
        resultats_cmd[var] = {}
        for signe, label in [(+1, '+20%'), (-1, '-20%')]:
            cmd_pert = perturber_cmd(cmd_base, var, signe)
            cmd_fn_p = runner.make_cmd_linear(cmd_pert, linear, t_max) if linear \
                       else (lambda t, _c=cmd_pert: _c)
            res = runner.simulate(p_ref, cmd_fn_p, y0, t_max)
            resultats_cmd[var][label] = {
                'traj'       : res['traj'],
                'changement' : res['traj'] != traj_ref,
                'val_base'   : cmd_base.get(var),
                'val_pert'   : cmd_pert.get(var),
                't_b'        : res['t_bascule'],
                'dC_rel'     : res['dC_rel'],
                'dI_rel'     : res['dI_rel'],
            }

    # ── Niveau 1 — Paramètres ────────────────────────────────────────────────
    resultats_params = {}
    for var in PARAM_PERTURBATIONS:
        resultats_params[var] = {}
        for signe, label in [(+1, '+20%'), (-1, '-20%')]:
            params_pert = perturber_param(config['params'], var, signe)
            p_pert = runner.apply_sa_modulator(params_pert, int(config['sa']))
            res = runner.simulate(p_pert, cmd_fn_ref, y0, t_max)
            resultats_params[var][label] = {
                'traj'       : res['traj'],
                'changement' : res['traj'] != traj_ref,
                'val_base'   : config['params'].get(var),
                'val_pert'   : params_pert.get(var),
                't_b'        : res['t_bascule'],
            }

    # ── Identification des variables sensibles ───────────────────────────────
    def score_sensibilite(resultats: dict) -> dict:
        scores = {}
        for var, perturbs in resultats.items():
            n_changements = sum(1 for p in perturbs.values() if p['changement'])
            scores[var] = n_changements  # 0, 1 ou 2
        return scores

    scores_cmd    = score_sensibilite(resultats_cmd)
    scores_params = score_sensibilite(resultats_params)

    vars_sensibles_cmd    = [v for v, s in sorted(scores_cmd.items(),    key=lambda x: -x[1]) if s > 0]
    vars_sensibles_params = [v for v, s in sorted(scores_params.items(), key=lambda x: -x[1]) if s > 0]

    # ── Recommandation N2 (top-3 variables cmd sensibles → combinaisons) ────
    top3 = vars_sensibles_cmd[:3]
    recommandation_n2 = {
        'variables_pivot' : top3,
        'variante_optimiste' : {v: f'{v}+{CMD_PERTURBATIONS[v][0]*100:.0f}%' for v in top3},
        'variante_pessimiste': {v: f'{v}-{CMD_PERTURBATIONS[v][0]*100:.0f}%' for v in top3},
        'instruction': (
            f"Lancer 2 simulations combinées sur {top3} pour le Niveau 2. "
            "Variante optimiste : toutes en +20%. Variante pessimiste : toutes en -20%."
            if top3 else "Aucune variable sensible détectée — système très robuste."
        )
    }

    return {
        'wp_id'             : config.get('wp_id', '?'),
        'niveau'            : 'N1 — Sensibilité individuelle (Protocole §3)',
        'traj_baseline'     : traj_ref,
        't_b_baseline'      : ref['t_bascule'],
        'resultats_cmd'     : resultats_cmd,
        'resultats_params'  : resultats_params,
        'scores_sensibilite_cmd'    : scores_cmd,
        'scores_sensibilite_params' : scores_params,
        'variables_sensibles_cmd'   : vars_sensibles_cmd,
        'variables_sensibles_params': vars_sensibles_params,
        'recommandation_n2' : recommandation_n2,
        'resume' : {
            'n_vars_cmd_testees'    : len(CMD_PERTURBATIONS),
            'n_vars_cmd_sensibles'  : len(vars_sensibles_cmd),
            'n_params_testes'       : len(PARAM_PERTURBATIONS),
            'n_params_sensibles'    : len(vars_sensibles_params),
            'verdict_n1'            : 'SENSIBLE' if vars_sensibles_cmd or vars_sensibles_params
                                       else 'ROBUSTE',
        }
    }


def afficher_rapport_n1(rapport: dict):
    print(f"\n{'='*65}")
    print(f"  RAPPORT SENSIBILITÉ N1 — {rapport['wp_id']}")
    print(f"  Trajectoire baseline : {rapport['traj_baseline']}")
    print(f"{'='*65}")

    print("\n  VARIABLES CMD (±20%) :")
    for var, perturbs in rapport['resultats_cmd'].items():
        row = []
        for label in ['+20%', '-20%']:
            p = perturbs[label]
            sym = '⚡' if p['changement'] else '·'
            row.append(f"{label}: {sym}{p['traj'][:4]}")
        sens = rapport['scores_sensibilite_cmd'][var]
        print(f"  {'⚠' if sens > 0 else ' '} {var:<8} {' | '.join(row)}  [sens={sens}]")

    print("\n  PARAMÈTRES p_k (±20%) :")
    for var, perturbs in rapport['resultats_params'].items():
        row = []
        for label in ['+20%', '-20%']:
            p = perturbs[label]
            sym = '⚡' if p['changement'] else '·'
            row.append(f"{label}: {sym}{p['traj'][:4]}")
        sens = rapport['scores_sensibilite_params'][var]
        print(f"  {'⚠' if sens > 0 else ' '} {var:<8} {' | '.join(row)}  [sens={sens}]")

    print(f"\n  VARIABLES SENSIBLES (cmd) : {rapport['variables_sensibles_cmd'] or 'Aucune'}")
    print(f"  VARIABLES SENSIBLES (params) : {rapport['variables_sensibles_params'] or 'Aucune'}")
    print(f"  VERDICT N1 : {rapport['resume']['verdict_n1']}")
    print(f"\n  → RECOMMANDATION N2 : {rapport['recommandation_n2']['instruction']}")
    print(f"{'='*65}\n")


# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage : python3 mepa_sensitivity_n1.py config_wp.json [output_n1.json]")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        config = json.load(f)

    rapport = run_sensitivity_n1(config)
    afficher_rapport_n1(rapport)

    if len(sys.argv) >= 3:
        with open(sys.argv[2], 'w') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        print(f"Rapport N1 sauvegardé : {sys.argv[2]}")
