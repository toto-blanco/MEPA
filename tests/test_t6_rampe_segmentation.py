#!/usr/bin/env python3
"""
================================================================================
MEPA V7 — Test de non-régression T6 : invariance à la segmentation de la rampe
================================================================================
Statut      : garde-fou T6 (issu de l'audit externe Juin 2026) — v1.1 : chemins du dépôt,
              entrées certifiées pour Rwanda, exécutable par pytest
Cible        : /data/mepa/scripts/mepa_test_rampe_segmentation.py
MEPA version : 7.0-alpha rev. 2.1

CONTEXTE
────────
Un audit externe (Axe 1) a soulevé un risque d'artefact LSODA lié à des
fonctions non-lisses. Le point était mal ciblé (les seuils θ_FR/θ_C/θ_I de
l'arbre de décision sont POST-simulation, pas dans l'EDO). La seule
discontinuité réelle du membre de droite est la rampe mod_mimétique
(_compute_p6_mod) : p6 saute aux instants t = 22, 29, 59. Or simulate_lsoda
intègre [0, t_max] en UN SEUL solve_ivp, sans events ni segmentation : un pas
LSODA peut donc chevaucher une frontière de phase.

HYPOTHÈSE TESTÉE
────────────────
H1 : l'intégration monobloc franchit « à l'aveugle » les sauts de p6 et diverge
     d'une intégration segmentée aux frontières de phase (intégrateur redémarré
     proprement à chaque frontière, RHS continu par segment).
H0 : l'écart est sous les tolérances de non-régression → imprécision cosmétique.

CRITÈRE PRÉ-ENREGISTRÉ (tolérances natives T1–T5 du runner V7)
────────────────────────────────────────────────────────────
Segmentation jugée NÉCESSAIRE (échec) si l'un de :
   T1  |Δ t_bascule|  > 5 pas
   T2  |Δ C_max| / C_max         > 5 %
   T3  |Δ chute_I|                > 3 %  (absolu)
   T4  |Δ FR_max| / FR_max        > 5 %
   T6  diagnostic catégoriel différent

RÉSULTAT DE RÉFÉRENCE (Rwanda WP-I10-1, Sa=6, rampe active — Juin 2026)
──────────────────────────────────────────────────────────────────────
   Version initiale (entrées approchées) : écart max ≈ 2 e-6, diagnostic identique.
   v1.1 (entrées certifiées) : voir sortie du test ; C_max certifié = 1.6587.

PORTÉE / VIGILANCE
──────────────────
Régime non couvert par le corpus actuel mais à surveiller : Sa=7 (p6 × 1.5)
COMBINÉ à une rampe active. Aucun cas du pilote V7-γ n'est Sa=7. Ce test sert
de garde-fou : il échouera si un tel cas futur fait diverger les deux schémas.

Usage :
    python3 mepa_test_rampe_segmentation.py [chemin_runner_v3_v7]
    (par défaut : runner importé depuis le PYTHONPATH ou /data/mepa/scripts)
Code retour 0 si tous les cas PASSENT, 1 sinon.
================================================================================
"""
import sys, os, json

_ICI = os.path.dirname(os.path.abspath(__file__))
RUNNER_DIR = (sys.argv[1] if (__name__ == "__main__" and len(sys.argv) > 1)
              else os.environ.get("MEPA_SCRIPTS_DIR", os.path.join(_ICI, "..", "scripts")))
for cand in (RUNNER_DIR, os.path.join(_ICI, "..", "scripts"), "/data/mepa/scripts"):
    if cand and os.path.isfile(os.path.join(cand, "mepa_runner_v3_v7.py")):
        sys.path.insert(0, cand)
        break

import numpy as np
from scipy.integrate import solve_ivp
import mepa_runner_v3_v7 as R

# ── Tolérances pré-enregistrées ──────────────────────────────────────────────
TOL = {"T1_t_bascule_pas": 5, "T2_C_max_rel": 0.05,
       "T3_chute_I_abs": 0.03, "T4_FR_max_rel": 0.05}

# Valeurs de test (copie des P_DEFAULTS du Nœud 2) — fixture du test, pas une source de constantes
P_DEFAULTS = dict(p1=0.08, p2=0.045, p2b=0.06, p3=0.02, p4=0.40,
                  p5=0.05, p6=0.12, p7=0.04, p8=0.03, p9=0.06,
                  p10=0.80, p11a=0.60, p11b=0.15, p13=1.2,
                  lam=0.68, mu=0.38, nu=0.62, rho=0.06)

# ── Cas-tests : rampe FORCÉE active (on teste la primitive d'intégration) ────
CAS = [
    {
        # Entrées certifiées V7.0-P1 (result.json du 19 juin 2026, sha256 b47bb3c5…)
        "wp_id": "WP-I10-1", "cas": "Rwanda (entrées certifiées)", "sa": 6, "t_max": 400,
        "params_override": {"p5": 0.20, "lam": 0.72},
        "cmd": dict(T=1.0, Mob=0.05, R=0.15, Ref=0.1, Rc=0.9, Rn=0.1,
                    E=0.82, gamma=0.55, EROI=3.0, Pop=1.0),
        "cmd_linear": {"EROI": {"start": 3.0, "end": 3.0}},
        "y0": [1.5, 0.12, 0.1, 1.5],
    },
    # Sentinelle worst-case : Sa=7 synthétique (p6 × 1.5) + rampe active.
    # Hors corpus pilote, présent pour faire échouer le test AVANT prod si un
    # tel cas est un jour introduit sans vérification.
    {
        "wp_id": "SYNTH-Sa7", "cas": "Synthétique Sa=7 (sentinelle)", "sa": 7,
        "t_max": 200, "params_override": {"p5": 0.20},
        "cmd": dict(T=1.0, Mob=0.05, R=0.15, Ref=0.1, Rc=0.6, Rn=0.1,
                    E=0.8, gamma=0.55, EROI=3.0, Pop=1.0),
        "cmd_linear": {"EROI": {"start": 3.0, "end": 3.0}},
        "y0": [1.5, 0.1, 0.1, 1.5],
    },
]


def _build_p(case):
    p = dict(P_DEFAULTS); p.update(case["params_override"])
    p = R.apply_sa_modulator(p, case["sa"])
    p["theta_C"] = 0.30; p["theta_I"] = 0.22
    return p


def _metrics(Y, ts, cmd_fn, p, hp, t_max):
    Ss, Ls, Cs, Is_raw = (Y[0].tolist(), Y[1].tolist(),
                          Y[2].tolist(), Y[3].tolist())
    Is = [max(R.I_MIN, v) for v in Is_raw]
    tsi = [int(round(t)) for t in ts]
    Fs, Rs = [], []
    for i, t in enumerate(tsi):
        c = R._normalize_cmd(cmd_fn(t))
        Fs.append(R.F_val(Ss[i], Ls[i], Cs[i], Is[i], c, p))
        Rs.append(R.R_val(Ss[i], Ls[i], Cs[i], Is[i], c, p))
    FR = [f / max(r, 1e-9) for f, r in zip(Fs, Rs)]
    res = R._apply_decision_tree_v7(Ss, Ls, Cs, Is, Fs, Rs, FR, tsi,
                                    cmd_fn, p, 0.30, 0.22, True, hp, t_max)
    I0 = Is[0]; chute_I = (I0 - min(Is)) / max(I0, 1e-9)
    return {"traj": res.get("traj"), "t_bascule": res.get("t_bascule"),
            "C_max": float(res.get("C_max") or 0.0),
            "FR_max": max(FR), "chute_I": chute_I}


def run_case(case):
    hp = R._get_hyperparams_v7()
    p = _build_p(case); p6_base = p["p6"]; t_max = case["t_max"]
    cmd_fn = R.make_cmd_linear(case["cmd"], case["cmd_linear"], t_max)
    fun = lambda t, y: R._ode_system(t, y, cmd_fn, p, p6_base, True, hp)
    ts = np.arange(0, t_max + 1, 1, dtype=float)
    y0 = np.array(case["y0"], float)

    # A — monobloc (code de production)
    A = solve_ivp(fun, (0.0, float(t_max)), y0, method="LSODA",
                  t_eval=ts, rtol=1e-6, atol=1e-9)
    assert A.success, A.message

    # B — segmenté aux frontières de phase
    rm = hp["rampe_mod_mimetique"]
    d1 = rm["phase_1_incubation"]["duree_par_defaut"]
    d2 = rm["phase_2_decharge"]["duree_par_defaut"]
    d3 = rm["phase_3_stabilisation"]["duree_par_defaut"]
    bnd = sorted(set([0.0, float(d1), float(d1 + d2),
                      float(d1 + d2 + d3), float(t_max)]))
    segs, y_cur = [], y0.copy()
    for a, b in zip(bnd[:-1], bnd[1:]):
        s = solve_ivp(fun, (a, b), y_cur, method="LSODA",
                      dense_output=True, rtol=1e-6, atol=1e-9)
        assert s.success, s.message
        segs.append((a, b, s)); y_cur = s.y[:, -1]

    def sample(t):
        for i, (a, b, s) in enumerate(segs):
            if (a <= t < b) or (i == len(segs) - 1 and a <= t <= b):
                return s.sol(t)
        return segs[-1][2].sol(t)
    B = np.array([sample(float(t)) for t in ts]).T

    mA = _metrics(A.y, ts, cmd_fn, p, hp, t_max)
    mB = _metrics(B, ts, cmd_fn, p, hp, t_max)

    tbA, tbB = mA["t_bascule"], mB["t_bascule"]
    t1 = (abs(tbA - tbB) if (tbA is not None and tbB is not None) else 0)
    t2 = abs(mA["C_max"] - mB["C_max"]) / max(abs(mB["C_max"]), 1e-9)
    t3 = abs(mA["chute_I"] - mB["chute_I"])
    t4 = abs(mA["FR_max"] - mB["FR_max"]) / max(abs(mB["FR_max"]), 1e-9)
    t6 = (mA["traj"] == mB["traj"])
    max_state = float(np.max(np.abs(A.y - B)))

    checks = {
        "T1_t_bascule": (t1 <= TOL["T1_t_bascule_pas"], t1),
        "T2_C_max":     (t2 <= TOL["T2_C_max_rel"], round(t2, 6)),
        "T3_chute_I":   (t3 <= TOL["T3_chute_I_abs"], round(t3, 6)),
        "T4_FR_max":    (t4 <= TOL["T4_FR_max_rel"], round(t4, 6)),
        "T6_traj":      (t6, mA["traj"]),
    }
    return all(c[0] for c in checks.values()), checks, max_state, mA, mB


def main():
    print("=" * 72)
    print("T6 — Invariance du diagnostic à la segmentation de la rampe")
    print("=" * 72)
    all_ok = True
    for case in CAS:
        ok, checks, max_state, mA, mB = run_case(case)
        all_ok &= ok
        flag = "✓ PASS" if ok else "✗ FAIL"
        print(f"\n[{flag}] {case['wp_id']} — {case['cas']} (Sa={case['sa']})")
        print(f"   écart max |monobloc-segmenté| sur S,L,C,I : {max_state:.2e}")
        print(f"   diagnostic monobloc={mA['traj']!r}  segmenté={mB['traj']!r}")
        for k, (passed, val) in checks.items():
            print(f"     {'✓' if passed else '✗'} {k}: {val}")
    print("\n" + "=" * 72)
    print("RÉSULTAT GLOBAL :", "✓ TOUS PASSENT" if all_ok else "✗ ÉCHEC")
    print("=" * 72)
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()


# ── Point d'entrée pytest (harnais tests/) ───────────────────────────────────
def test_t6_invariance_segmentation_rampe():
    for case in CAS:
        ok, checks, max_state, mA, mB = run_case(case)
        assert ok, f"{case['wp_id']} : {checks} (écart max {max_state:.2e})"
