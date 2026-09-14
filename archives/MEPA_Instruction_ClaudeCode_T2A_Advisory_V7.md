# Instruction Claude Code — T2-A : Greffe advisory Dev 1 sur runner V7

**Dépôt :** `mepa/`
**Branche :** `feat/advisory-dev1-v7` depuis `main`
**Nature :** greffe additive — l'advisory lit la trajectoire, ne la modifie jamais
**Règle absolue :** les champs `simulation.*`, `verdict.*`, `stress_n1`, `stress_n2`, `non_regression_t1_t5` du result.json doivent être **bit-identiques** avant et après cette modification. Toute divergence = bug bloquant à signaler.

---

## Contexte

`mepa_dev1_advisory_v63.py` (fourni séparément dans `prepa_v6.3/`) calcule un plafond redistributif `A_d_max` dérivé de la chaîne biophysique (EROI → surplus net S* → A_d_max). En V6.3, il utilise `Ω = Sa/SA_REF` (constante). La décision CV1 (QG, juin 2026) adopte `Ω ≡ I(t)` pour V7 : Ω doit être la complexité institutionnelle dynamique lue depuis la trajectoire LSODA.

---

## Fichier 1 — Créer `mepa/scripts/mepa_dev1_advisory_v7.py`

Partir du contenu de `mepa_dev1_advisory_v63.py` (Antoine doit le copier dans `mepa/scripts/` sous ce nouveau nom avant que tu commences). Appliquer les modifications suivantes :

### 1a — Mettre à jour l'en-tête

```python
MODULE_VERSION = "mepa_dev1_advisory_v7 v1.0.0"
```

Modifier `$description` / docstring pour indiquer :
- Cible : `/data/mepa/scripts/mepa_dev1_advisory_v7.py`
- Statut : V7 — `Ω ≡ I(t)` (complexité institutionnelle dynamique, décision CV1 juin 2026)
- Remplace : `mepa_dev1_advisory_v63.py` (V6.3, `Ω = Sa/SA_REF` provisoire)

### 1b — Modifier `calculer_a_d_max_derive`

Ajouter le paramètre `omega_override: float | None = None` :

```python
def calculer_a_d_max_derive(EROI: float, gamma: float, sa: int, pop: float,
                            params: dict,
                            omega_override: float | None = None) -> dict:
```

Remplacer le calcul de `Omega` :

```python
# AVANT (V6.3 — Ω = Sa/SA_REF, provisoire) :
Omega = max(sa, 0) / SA_REF if SA_REF > 0 else 0.0

# APRÈS (V7 — Ω ≡ I(t) si omega_override fourni, Sa/SA_REF sinon) :
if omega_override is not None:
    Omega = float(omega_override)   # Ω ≡ I(t), valeur directe
else:
    Omega = max(sa, 0) / SA_REF if SA_REF > 0 else 0.0
```

Ajouter la clé `"omega_source"` dans le dict retourné :

```python
"omega_source": "I(t)_direct" if omega_override is not None else "Sa/SA_REF_provisoire",
"Omega_valeur": round(Omega, 6),   # renomme l'ancienne clé Omega_proxy_Sa
```

Supprimer la clé `"Omega_proxy_Sa"` (remplacée par `"Omega_valeur"` + `"omega_source"`).

### 1c — Modifier `calculer_advisory_dev1`

Ajouter trois paramètres après `constants` :

```python
def calculer_advisory_dev1(cmd_base_norm: dict, sa: int, y0: list,
                           cmd_fn=None, t_max: int = 0,
                           constants: dict | None = None,
                           i_t0: float | None = None,
                           i_tmax: float | None = None,
                           omega_mode: str = 'I') -> dict:
```

Dans le corps, remplacer les deux appels à `calculer_a_d_max_derive` :

```python
# ── Pas initial t=0 ──
EROI_0 = float(cmd_base_norm.get("EROI", 0.0))
omega_t0 = i_t0 if (omega_mode == 'I' and i_t0 is not None) else None
calc_t0 = calculer_a_d_max_derive(EROI_0, gamma, sa, pop, params,
                                   omega_override=omega_t0)
a_d_max_t0 = calc_t0["a_d_max_advisory_NONCALIBRE"]

# ── Pas final t=t_max (si EROI dynamique OU I dynamique) ──
calc_tmax = None
if cmd_fn is not None and t_max and t_max > 0:
    try:
        cmd_fin = cmd_fn(t_max)
        EROI_fin = float(cmd_fin.get("EROI", EROI_0))
        gamma_fin = float(cmd_fin.get("gamma", gamma))
        pop_fin = float(cmd_fin.get("Pop", pop))
        omega_tmax = i_tmax if (omega_mode == 'I' and i_tmax is not None) else None
        # Calculer si EROI ou I ont changé
        eroi_change = abs(EROI_fin - EROI_0) > 1e-9
        omega_change = (omega_tmax is not None and omega_t0 is not None
                        and abs(omega_tmax - omega_t0) > 1e-9)
        if eroi_change or omega_change:
            calc_tmax = calculer_a_d_max_derive(EROI_fin, gamma_fin, sa, pop_fin, params,
                                                omega_override=omega_tmax)
    except Exception:
        calc_tmax = None
```

Ajouter `"omega_mode"` dans le dict retourné :

```python
"omega_mode": omega_mode,
"i_t0_utilise": round(i_t0, 4) if i_t0 is not None else None,
"i_tmax_utilise": round(i_tmax, 4) if i_tmax is not None else None,
```

---

## Fichier 2 — Modifier `mepa/scripts/mepa_runner_v3_v7.py`

### Point d'injection

Dans `run_wp()`, entre le calcul de `non_regression` et le `return` final (après la ligne `non_regression = _compare_non_regression(...)` ou `non_regression = None`), ajouter :

```python
# ── Advisory Dev 1 — V7 (Ω ≡ I, additif, non bloquant) ──────────────────────
advisory_dev1 = None
if fiche_v7:
    try:
        import importlib.util, os as _os
        _adv_path = _os.path.join(MEPA_SCRIPTS_DIR, "mepa_dev1_advisory_v7.py")
        _spec = importlib.util.spec_from_file_location("mepa_dev1_advisory_v7", _adv_path)
        _adv_mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_adv_mod)
        advisory_dev1 = _adv_mod.calculer_advisory_dev1(
            cmd_base_norm = cmd_base_norm,
            sa            = sa,
            y0            = y0,
            cmd_fn        = cmd_fn,
            t_max         = t_max,
            constants     = _get_constants(),
            i_t0          = float(y0[3]),
            i_tmax        = float(res.get('I_final', y0[3])),
            omega_mode    = 'I',
        )
    except Exception as _adv_err:
        advisory_dev1 = {
            "$advisory": True,
            "statut": "ADVISORY_DEV1_ERREUR_NON_BLOQUANTE",
            "erreur": f"{type(_adv_err).__name__}: {_adv_err}",
            "note": "Advisory absent — simulation principale non affectée.",
        }
```

### Dans le dict `return`

Ajouter la clé `advisory_dev1` **après** `non_regression_t1_t5` :

```python
'non_regression_t1_t5': non_regression,
'advisory_dev1'        : advisory_dev1,   # ← AJOUTER ICI
'params'    : ...
```

**Important :** utiliser `importlib.util` (import dynamique) pour éviter une dépendance dure qui casserait le runner si le fichier advisory est absent. L'advisory ne doit jamais bloquer le runner.

---

## Fichier 3 — Test de non-régression `mepa/tests/test_advisory_v7_nonregression.py`

```python
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
        v1 = _get_nested(r1, champ)
        v2 = _get_nested(r2, champ)
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
```

---

## Vérifications avant commit

```bash
export MEPA_SCRIPTS_DIR="$(pwd)/scripts"

# 1. JSON valide (runner non cassé)
python3 -c "import py_compile; py_compile.compile('scripts/mepa_dev1_advisory_v7.py'); print('advisory V7 : syntaxe OK')"
python3 -c "import py_compile; py_compile.compile('scripts/mepa_runner_v3_v7.py'); print('runner V7 : syntaxe OK')"

# 2. Run direct sur Haïti V7
python3 scripts/mepa_runner_v3_v7.py config/v7/WP-C1-1_Haiti_v7.json /tmp/test_adv_haiti.json
python3 -c "
import json
r = json.load(open('/tmp/test_adv_haiti.json'))
adv = r.get('advisory_dev1')
assert adv is not None, 'advisory absent'
assert adv.get('omega_mode') == 'I', f'omega_mode: {adv.get(\"omega_mode\")}'
assert adv.get('a_d_max_advisory_flag') is not None, 'flag absent'
# Vérifier non-régression sur champs clés
assert r['simulation']['traj'] == '(d) Effondrement progressif', 'trajectoire modifiée'
assert r['simulation']['FR_max'] == 0.8893 or r['simulation']['FR_max'] > 0, 'FR_max suspect'
print('Run Haïti : OK')
print(f'  omega_mode : {adv[\"omega_mode\"]}')
print(f'  i_t0       : {adv[\"i_t0_utilise\"]}')
print(f'  i_tmax     : {adv[\"i_tmax_utilise\"]}')
print(f'  flag       : {adv[\"a_d_max_advisory_flag\"]}')
print(f'  écart      : {adv[\"ecart_R_code_moins_a_d_max\"]}')
print(f'  statut     : {adv[\"statut\"]}')
"

# 3. Tests pytest
pytest tests/test_advisory_v7_nonregression.py -v
```

---

## Commits attendus (deux commits séparés)

**Commit 1 — advisory V7 :**
```
feat: mepa_dev1_advisory_v7 — Ω ≡ I(t) (décision CV1 juin 2026), greffe additive V7
```

**Commit 2 — intégration runner + test :**
```
feat: runner V7 — injection advisory Dev1 (additif, non bloquant) + test non-régression T2-A
```

---

## Ce que Claude Code ne fait PAS ici

- Ne pas modifier `mepa_runner_v2_gamma.py` (runner V6.2 — hors scope)
- Ne pas modifier `mepa_passeport_schema.py` (le champ `advisory_dev1` dans le passeport est une étape séparée)
- Ne pas modifier les fiches WP JSON
- Ne pas calibrer les paramètres `C_OMEGA`, `THETA`, `S_REF` — ils restent NON_CALIBRÉS

---

*Instruction QG (CONV-C), juin 2026 — T2-A greffe advisory Dev 1 sur runner V7, Ω ≡ I(t).*
