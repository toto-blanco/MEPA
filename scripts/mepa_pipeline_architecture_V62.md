# MEPA V6.2 — Architecture Pipeline n8n
## Documentation technique — Mars 2026 (révision post-intégration scripts d'audit)

---

## Topologie du pipeline (flux complet 27 WP)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ENTRÉE : Fiche WP brute (JSON)                                         │
│  { wp_id, cas, sa, y0, cmd: {T,Mob,R,Ref,Rc,Rn,E,gamma,EROI}, params, … }│
│  (fiches V6.1 avec clé 'g' : converties automatiquement par Nœud 1)    │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  NŒUD 1 : "Audit & Conformité"  [mepa_n8n_audit_conformite_v62.js]      │
│                                                                         │
│  • Validation structurelle (22 champs, plages physiques)                │
│  • Normalisation g → gamma (D6) : conversion V6.1 ou rejet mode STRICT │
│  • Correction Sa=7 → p6 × 1.5  (avant runner Python)                   │
│  • Construction runner_config_json (compatible mepa_runner_v2_gamma.py) │
│  • Construction llm_context : clé 'gamma' → symbole γ pour rédaction   │
│  • Sortie : { status, runner_cmd, llm_context, audit_log }              │
│                                                                         │
│  Router n8n : status=ERROR → Nœud Alerte Slack/Email                   │
│               status=OK   → Nœuds 2 + 3 en parallèle                  │
└──────────────┬──────────────────────────────────────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
┌──────────────┐  ┌─────────────────────────────────────────────────────┐
│  NŒUD 2 :    │  │  NŒUD 3 : "Write Config File"                       │
│  (attente)   │  │  Écrit runner_config_json → /tmp/WP-Xx_config.json  │
│              │  └────────────────────────┬────────────────────────────┘
│              │                           │
│              │                           ▼
│              │  ┌─────────────────────────────────────────────────────┐
│              │  │  NŒUD 4 : "Execute Command"                          │
│              │  │  Commande : $json.runner_cmd                         │
│              │  │  → python3 mepa_runner_v2_gamma.py config.json      │
│              │  │  → Sortie : _result.json (stdout)                    │
│              │  └────────────────────────┬────────────────────────────┘
│              │                           │
│              │                           ▼
│              │  ┌─────────────────────────────────────────────────────┐
│              │  │  NŒUD 5 : "Parse Runner Result"                      │
│              │  │  JSON.parse(stdout) → { simulation, stress_n1,       │
│              │  │  stress_n2, verdict, meta, params, … }               │
│              │  └────────────────────────┬────────────────────────────┘
└──────────────┘                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  NŒUD 5b : "Sensibilité N1"  [mepa_sensitivity_n1.py]           ★ NOUVEAU│
│                                                                         │
│  • Perturbation ±20% sur les 9 variables cmd + 16 paramètres p_k       │
│  • Identification des variables sensibles (changement de trajectoire)  │
│  • Score de sensibilité par variable [0, 1, 2]                         │
│  • Recommandation N2 : top-3 variables pivot pour combinaisons          │
│  • Sortie : rapport_n1.json → { traj_baseline, variables_sensibles,    │
│             scores_cmd, scores_params, recommandation_n2 }              │
│                                                                         │
│  Router n8n : verdict_n1=SENSIBLE → flag dans Passeport + Nœud 6      │
│               verdict_n1=ROBUSTE  → Nœud 6 direct                     │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  NŒUD 6 : "LLM Rédaction WP" (Claude API / OpenAI)                     │
│                                                                         │
│  Prompt système = prompt_projet_MEPA_V3_gamma.md (injecté en system)   │
│  Prompt user   = llm_context (Nœud 1) + runner_result (Nœud 5)        │
│                + rapport_n1 résumé (Nœud 5b)                           │
│                                                                         │
│  Produit : WP complet (7 sections S1→S7)                               │
│  Variables dans le texte : γ (gamma grec) — JAMAIS 'g' ni 'gamma'      │
│  Labels trajectoire : stricts (D4) pour concordance runner V6.2        │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  NŒUD 6b : "Porte Kappa — Audit Inter-Codeurs"                  ★ NOUVEAU│
│            [mepa_kappa_calculator.py]                                   │
│                                                                         │
│  Entrée : fiche_codage CONV-E + fiche_codage CONV-B (JSON)             │
│  • Calcul κ de Cohen sur 9 variables (seuil accord ±0.15 / ±1.5)       │
│  • Verdict : VALIDÉ (κ ≥ 0.70) | RÉVISION (0.50–0.69) | REJET (< 0.50)│
│  • Instructions de résolution automatique :                             │
│      Continue écart ≤ 2.0 → moyenne                                    │
│      Continue écart > 2.0 → confrontation sources                      │
│      Catégorielle (Sa) → confrontation obligatoire                     │
│  • Sortie : { kappa, verdict, valeurs_finales_provisoires,             │
│              instructions_resolution }                                  │
│                                                                         │
│  Router n8n : VALIDÉ   → Nœud 6c (Passeport)                          │
│               RÉVISION → Boucle re-codage CONV-E/CONV-B (max 2 tours) │
│               REJET    → Alerte Slack + suspension WP                  │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │ (κ ≥ 0.70 confirmé)
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  NŒUD 6c : "Construction Passeport WP"                          ★ NOUVEAU│
│            [mepa_passeport_schema.py → from_result_json()]              │
│                                                                         │
│  • Agrège : _result.json (runner) + κ (Nœud 6b) + RF1/RF2 (S7 du WP) │
│  • Champs obligatoires (17) : wp_id, cas, cluster, sa, traj_attendue,  │
│    traj_diagn, concordant, robustesse, t_b, dC_rel, dI_rel,            │
│    FR_bascule, p6_final, RF1, RF2, kappa, verdict_audit                │
│  • Enrichissement CONV-B : enrich_from_audit()                         │
│  • Validation schéma : validate() → erreurs bloquantes + warnings      │
│  • Vérification labels D4 (traj_attendue + traj_diagn)                 │
│  • Vérification cohérence 'concordant' (calculé vs déclaré)            │
│  • Vérification Sa ∈ {2, 4, 6, 7}                                      │
│  • Sortie : passeport_WP-Xx.json → objet de transit inter-conversations│
│                                                                         │
│  Erreur bloquante → Nœud Alerte Slack + suspension export              │
│  Warnings non bloquants → logués dans passeport.alertes[]              │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  NŒUD 7 : "Export WP"                                                   │
│  → Google Drive / Notion / PDF selon config                             │
│  → Archivage _result.json dans /outputs/cluster_X/                     │
│  → Archivage passeport_WP-Xx.json dans /passeports/                    │
│  → Archivage rapport_n1.json dans /sensitivity/                        │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                         (après 5 WP du cluster)
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  NŒUD 8 : "Merge Cluster"  (n8n Merge node, mode "All Items")          │
│  Agrège les 5 _result.json + 5 passeports du cluster courant           │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  NŒUD 9 : "Méta-Analyse V7"  [mepa_n8n_meta_analyse.js]               │
│                                                                         │
│  • Détection outliers (concordance traj_diag vs traj_attendue)         │
│  • Évaluation P1–P5 Popper agrégée sur le cluster                      │
│  • Recommandations parcimonie p1–p13 (CV, sensibilité N2)              │
│  • Décision readiness calibration bayésienne                            │
│  • Lecture des passeports.kappa pour score qualité cluster              │
│  • Lecture des rapport_n1.variables_sensibles pour cross-cluster        │
│  • Sortie : rapport_cluster_X.json                                      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Règle de non-divergence g / gamma / γ — Points de contrôle dans le pipeline (V6.2)

| Nœud | Clé / Symbole | Comportement V6.2 |
|------|--------------|-------------------|
| Fiche WP brute (entrée) | `gamma` *(V6.2 natif)* | Clé officielle — passe sans modification |
| Fiche WP brute (entrée) | `g` *(V6.1 legacy)* | Converti en `gamma` + warning stderr (mode WARN) ou rejeté (mode STRICT) |
| Nœud 1 Audit (validation) | `gamma` garanti en sortie | `g` absent du payload runner ; `gamma` dans cmd bloqué → erreur |
| runner_config_json (Nœud 3) | `gamma` | Compatible `mepa_runner_v2_gamma.py` — `cmd['gamma']` |
| mepa_runner_v2_gamma.py | `gamma` dans `F_val()` | `cmd['gamma']` lu ; `gC` = variable interne distincte (inchangée) |
| mepa_kappa_calculator.py (Nœud 6b) | `gamma` | Variable scorée sous la clé `'gamma'` dans `VARIABLES` dict |
| mepa_sensitivity_n1.py (Nœud 5b) | `gamma` | Perturbation ±20% sur `cmd['gamma']` — `CMD_PERTURBATIONS['gamma']` |
| mepa_passeport_schema.py (Nœud 6c) | `gamma` / `p6_final` | `gamma` absent du passeport (non exporté) ; p6_final = résultat post-modulation |
| llm_context (Nœud 6) | `gamma` → `γ` | `mepa_full_vars.gamma` traduit en γ par le prompt système |
| Corps WP rédigé (S1→S7) | **γ** | Nomenclature officielle V6.2 — `g` et `gamma` interdits dans le texte |

---

## Correction Sa=7 — Trace d'audit

Le Nœud 1 produit dans `audit_log.sa_modulation` :

```json
{
  "sa": 7,
  "p6_base": 0.12,
  "p6_final": 0.18,
  "mult_applied": true,
  "note": "p6 × 1.5 (Sa=7 famille souche — Japon, Allemagne, Suède)"
}
```

Le runner `apply_sa_modulator()` applique la même opération.
Les deux résultats doivent être identiques — toute divergence > 0.001 est un bug.
Vérification : comparer `audit_log.sa_modulation.p6_final` avec `result.params.p6`.

Le Passeport (Nœud 6c) archive dans `sa_p6_mult: true/false` et `p6_final` la valeur
post-modulation. Le script `mepa_passeport_schema.py` détecte automatiquement la
cohérence via `p.get('_sa_note', '').startswith('p6 × 1.5')`.

**WP concernés par Sa=7 :** WP-I3 (Japon), WP-I4 (Allemagne), WP-I9 (Singapour).

---

## Porte Kappa — Règles de routage (Nœud 6b)

| Verdict κ | Seuil | Action pipeline |
|-----------|-------|-----------------|
| VALIDÉ | κ ≥ 0.70 | Passage direct Nœud 6c |
| RÉVISION | 0.50 ≤ κ < 0.70 | Boucle re-codage (max 2 itérations). Si κ < 0.70 après 2 tours → REJET |
| REJET | κ < 0.50 | Suspension WP. Alerte Slack/Email. Recodage complet CONV-E + CONV-B indépendants |

**Résolution des désaccords (mepa_kappa_calculator.py §resolution_desaccords) :**
- Variable continue, écart ≤ 2.0 → valeur retenue = moyenne (automatique)
- Variable continue, écart > 2.0 → confrontation : source de plus haute priorité (N1 > N6)
- Variable catégorielle (Sa) → confrontation obligatoire, troisième codeur si pas de consensus

---

## Passeport WP — Champs et flux de remplissage (Nœud 6c)

```
CONV-A (runner) produit :          CONV-B (audit) enrichit :
  wp_id, cas, cluster, sa           kappa
  traj_attendue, traj_diagn         verdict_audit
  concordant, robustesse            alertes[] ← anomalies CONV-B
  t_b, dC_rel, dI_rel, FR_bascule
  p6_final
  RF1, RF2 ← extraits de S7
  sa_p6_mult, trajs_set_n1
```

**Champs null autorisés :** `t_b`, `dC_rel`, `dI_rel`, `FR_bascule` (si pas de bascule),
`kappa`, `verdict_audit` (avant audit CONV-B).

**Erreurs bloquantes à la validation :**
- Champ obligatoire manquant ou null non-nullable
- `sa` ∉ {2, 4, 6, 7}
- Label trajectoire invalide (D4) dans `traj_attendue` ou `traj_diagn`
- `robustesse` ∉ {'ROBUSTE', 'MÉTASTABLE'}
- `concordant` incohérent avec comparaison `traj_attendue == traj_diagn`
- `kappa` ∉ [0, 1]

**Warnings non bloquants :**
- `kappa` < 0.70 (WP non certifiable)
- RF1/RF2 ne contenant pas le mot 'réfuté'

---

## Sensibilité N1 — Intégration pipeline (Nœud 5b)

`mepa_sensitivity_n1.py` s'exécute après le runner (Nœud 5) et avant la rédaction (Nœud 6).
Il utilise le même `config.json` que le runner.

**Variables testées :**
- 9 variables cmd : T, Mob, R, Ref, Rc, Rn, E, gamma, EROI — perturbation ±20%
- 16 paramètres p_k : p1–p13, λ, μ, ν — perturbation ±20%

**Sortie injectée dans le prompt Nœud 6 (résumé) :**
```json
{
  "verdict_n1": "SENSIBLE | ROBUSTE",
  "variables_sensibles_cmd": ["E", "gamma", "R"],
  "variables_sensibles_params": ["p6", "p3"],
  "recommandation_n2": "Lancer 2 simulations combinées sur ['E', 'gamma', 'R']..."
}
```

Le LLM intègre ce résumé dans la Section S4 (Stress-test) du WP, en distinguant :
- Le stress-test standard N1 runner (E±0.08, R±0.08)
- Le stress-test étendu N1 complet (±20% toutes variables, via mepa_sensitivity_n1.py)

---

## Ordre de traitement recommandé (Stratification V6.2)

```
Phase 1 — Ancres LOI PHYSIQUE (3 passes, traiter en premier)
  WP-I10  Rwanda 1990–2010     → EROI faible, ancre min
  WP-C1   Islande 2008–2013    → EROI moyen, (e) pure       ← NEXT
  WP-C2   Égypte 2011          → (a) rapide, ancre max C

Phase 2 — Fondateurs calibration bayésienne (5 passes)
  WP-F1   Rome IIIe s.         → (c)→(d), EROI dynamique
  WP-F2   Rome tardive          → (d) effondrement
  WP-I7   URSS 1970–1991       → (d) Todd, Sa=6

Phase 3 — Cœur (5 passes)
  F3, F7, F8, F10, T1, I1, I2, I4, I5, I9, C4

Phase 4 — Zone de stress (10 passes)
  F4, F5, F6, F9, I3, I6, I8, C3, C5, C6
  ⚠ I3 (Japon Sa=7), I4 (Allemagne Sa=7), I9 (Singapour Sa=7)
    → Vérifier p6 × 1.5 dans audit_log avant chaque run
    → Vérifier passeport.sa_p6_mult = true après Nœud 6c
```

---

## Labels de trajectoire valides (D4 — conformité runner + Passeport)

```
(a) Rupture transformatrice
(b) Répression réussie
(c) Stase / ambigu
(d) Effondrement progressif
(e) Réforme institutionnelle
(h) Stabilité
(h)/(e) Stabilité ou réforme lente   ← sortie runner si F < R sur tout t_max
```

**Tout autre label dans le JSON = erreur bloquante** dans :
- Nœud 1 (`mepa_n8n_audit_conformite_v62.js`, validation D4)
- Nœud 6c (`mepa_passeport_schema.py`, champs `traj_attendue` + `traj_diagn`)
- Nœud 9 Méta-Analyse (rejet du WP du calcul d'agrégat cluster)

---

## Répertoire des scripts d'audit V6.2

| Script | Nœud pipeline | Rôle | Seuil bloquant |
|--------|--------------|------|----------------|
| `mepa_runner_v2_gamma.py` | 4 | Simulation ODE + stress N1 partiel | Divergence p6 > 0.001 |
| `mepa_sensitivity_n1.py` | 5b | Sensibilité ±20% complète (9 cmd + 16 params) | verdict_n1 = flag |
| `mepa_kappa_calculator.py` | 6b | κ de Cohen inter-codeurs CONV-E/CONV-B | κ < 0.70 → RÉVISION/REJET |
| `mepa_passeport_schema.py` | 6c | Construction + validation Passeport WP | Toute erreur bloquante |
| `mepa_n8n_audit_conformite_v62.js` | 1 | Validation structurelle + normalisation gamma | status=ERROR |
| `mepa_n8n_meta_analyse.js` | 9 | Méta-Analyse cluster + Popper | Outlier concordance |
