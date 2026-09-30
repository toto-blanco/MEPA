import json, sys, os, copy, importlib.util, warnings
os.environ["MEPA_SCRIPTS_DIR"] = "/mnt/project"          # vraies constantes, pas de fallback
spec = importlib.util.spec_from_file_location("rn", "/mnt/project/mepa_runner_v3_v7.py")
rn = importlib.util.module_from_spec(spec); spec.loader.exec_module(rn)
R = json.load(open("juin_result.json"))
m = R["meta"]
base = {
  "wp_id": m["wp_id"], "cas": m["cas"], "cluster": m["cluster"],
  "trajectoire_attendue": m["trajectoire_attendue"], "sa": m["sa"],
  "y0": list(R["y0"]), "cmd": dict(R["cmd_base"]), "cmd_linear": R["cmd_linear"],
  "params": dict(R["params"]), "t_max": R["t_max"],
  "fiche_v7": True, "variables_v7": m["variables_v7"],
}
L0 = float(sys.argv[1])
cfg = copy.deepcopy(base); cfg["y0"][1] = L0
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    out = rn.run_wp(cfg)
out["_warnings"] = [str(x.message) for x in w]
json.dump(out, open(f"sortie_L0_{L0}.json","w"), ensure_ascii=False, indent=2, default=str)
print("écrit", f"sortie_L0_{L0}.json", "| warnings:", out["_warnings"])
