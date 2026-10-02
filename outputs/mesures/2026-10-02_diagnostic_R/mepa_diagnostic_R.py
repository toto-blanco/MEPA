"""Diagnostic R (Décision QG 2026-09-30 §5) — runner seul, vraies constantes, sans LLM ni passeport."""
import json, sys, os, copy, importlib.util, warnings
os.environ["MEPA_SCRIPTS_DIR"] = os.environ.get("MEPA_SCRIPTS_DIR_DIAG", "/mnt/project")
spec = importlib.util.spec_from_file_location("rn", os.environ.get("MEPA_RUNNER", "/mnt/project/mepa_runner_v3_v7.py"))
rn = importlib.util.module_from_spec(spec); spec.loader.exec_module(rn)

def config_depuis_result(R):
    m = R["meta"]; p = dict(R["params"])
    if int(m["sa"]) == 7:                     # params archivés = post-modulateur Sa=7 (p6×1.5) :
        p["p6"] = round(p["p6"] / 1.5, 10)     # le runner le réapplique, on repart de la valeur de base
    return {"wp_id": m["wp_id"], "cas": m["cas"], "cluster": m["cluster"],
            "trajectoire_attendue": m["trajectoire_attendue"], "sa": m["sa"],
            "y0": list(R["y0"]), "cmd": dict(R["cmd_base"]), "cmd_linear": R["cmd_linear"],
            "params": p, "t_max": R["t_max"], "fiche_v7": True, "variables_v7": m["variables_v7"]}

def run(R, R_override=None):
    cfg = config_depuis_result(R)
    if R_override is not None: cfg["cmd"]["R"] = float(R_override)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always"); out = rn.run_wp(cfg)
    out["_warnings"] = [str(x.message) for x in w]
    return out

def releve(o):
    s, v = o["simulation"], o["verdict"]
    return {"traj": s["traj"], "robustesse_N1": v["robustesse"], "trajs_set_n1": v["trajs_set_n1"],
            "stress_n1": {k: o["stress_n1"][k]["traj"] for k in ("optimiste", "pessimiste")},
            "stress_n2": {x["label"]: x["traj"] for x in o["stress_n2"]},
            "C_max": s["C_max"], "FR_max": s["FR_max"], "t_bascule": s["t_bascule"],
            "R_simule": o["cmd_base"]["R"], "warnings": o["_warnings"]}

if __name__ == "__main__":
    # usage : diag_R.py <result_juin.json> [R_override]
    R = json.load(open(sys.argv[1]))
    ov = float(sys.argv[2]) if len(sys.argv) > 2 else None
    print(json.dumps(releve(run(R, ov)), ensure_ascii=False))
