# MEPA — Missions prioritaires Claude Code (pré-lancement 27 WP V6.2)

**Objectif unique :** rendre le socle V6.2 fiable et vérifiable pour produire les 27 WP via le pipeline n8n.
**Hors périmètre :** tout travail V7 (Track A trajectoires ou Track B biophysique), tout refactoring non nécessaire au lancement.
**Contrainte dure transversale :** rétrocompatibilité **bit-identique** des sorties de trajectoire du runner V6.2. Toute mission qui touche au code doit prouver qu'elle ne change aucun champ `simulation` / `verdict` / `stress` sur les 27 WP.

Les missions sont ordonnées. **La Mission 1 doit être faite en premier** : c'est le filet de sécurité qui permet de valider toutes les autres.

---

## Mission 1 — Établir le filet de non-régression (À FAIRE EN PREMIER)

**Pourquoi.** Le projet n'a aucun test automatisé. Sans baseline de référence, aucune des corrections suivantes ne peut être prouvée sûre. C'est l'investissement qui protège tout le reste.

**Tâches.**
1. Construire un harnais qui exécute `mepa_runner_v2_gamma.py` sur les 27 fiches WP + 2 étalons, et capture les sorties dans des fichiers de référence "golden" (snapshots JSON).
2. Le snapshot ne retient que les blocs déterminant la trajectoire : `simulation`, `verdict`, `stress_n1`, `stress_n2`, `params`, `cmd_base`, `cmd_linear`, `y0`, `t_max`. **Exclure** `meta` (timestamps, versions) du hash de comparaison.
3. Écrire `tests/test_nonregression_v62.py` (pytest) qui re-exécute chaque WP et compare au golden via hash SHA-256. Échec si divergence.
4. Ajouter des tests de comportement explicites sur les invariants connus :
   - WP-C1-1 Haïti → trajectoire `(d) Dissolution`
   - WP-C2-1 Égypte → `(b) Répression réussie`
   - NC bloquant (gamma ou EROI = "NC") → `RuntimeError`
   - NC non bloquant → warning + fallback, pas de crash
   - Sa=7 (WP-I3, I4, I9) → `p6_final = p6_base × 1.5`
   - Fiche cluster C1 avec `cmd_linear` → EROI dynamique appliqué

**Définition de terminé.** `pytest tests/` passe à 100 %. Les golden snapshots sont commités. Le harnais tourne en une commande documentée.

**Garde-fou.** Ne modifier AUCUN fichier de production dans cette mission — uniquement créer les tests et les golden.

---

## Mission 2 — Corriger le bug theta dans `mepa_sensitivity_n1.py`

**Pourquoi.** C'est le **seul bug qui produit des résultats silencieusement faux en production V6.2**. `run_sensitivity_n1()` applique `apply_sa_modulator()` mais oublie `_inject_theta()`. Les fiches avec `theta_C` / `theta_I` personnalisés (la majorité) voient leur analyse de sensibilité tourner sur les défauts 0.30/0.22, donc sur des seuils différents de la simulation principale. Les comparaisons de trajectoire N1 sont faussées.

**Tâches.**
1. Dans `run_sensitivity_n1()`, après `p_ref = runner.apply_sa_modulator(config['params'], int(config['sa']))`, ajouter :
   ```python
   p_ref = runner._inject_theta(p_ref, config)
   ```
2. Vérifier que la même injection est appliquée à toutes les configurations perturbées si elles repartent des params de base.
3. Identifier une fiche avec `theta_C`/`theta_I` non standard et prouver qu'après correction, la baseline de sensibilité utilise les mêmes seuils que la simulation principale du runner.

**Définition de terminé.** Sur une fiche à theta personnalisé, `sensitivity_n1` et le runner principal partagent les mêmes `theta_C`/`theta_I`. Le harnais Mission 1 confirme que les sorties du **runner** restent bit-identiques (ce bug ne touche que sensitivity, pas le runner).

**Garde-fou.** Ne pas toucher au runner. Vérifier que les 27 fiches ne lèvent pas d'erreur après correction.

---

## Mission 3 — Fiabiliser la provenance dans `mepa_passeport_schema.py`

**Pourquoi.** Deux défauts touchent la traçabilité, qui est une valeur centrale du projet. (a) Le modèle IA est figé en dur (`"claude-sonnet-4-6"`) : tout changement de modèle dans n8n produira des passeports à provenance erronée. (b) `MEPA_VERSION_META` annonce des versions fausses (runner "v2.0" alors que c'est v2.1.1, audit "v2.0" alors que v2.1.0).

**Tâches.**
1. Lire le modèle depuis l'environnement avec fallback :
   ```python
   IA_CODEUR = {"modele": os.environ.get("MEPA_IA_MODEL", "claude-sonnet-4-6"), ...}
   ```
   Optionnel : surcharge prioritaire depuis `config.get('_conv_e_meta', {}).get('modele')` si présent (déjà prévu dans la whitelist C9).
2. Corriger `MEPA_VERSION_META` pour refléter les versions réelles des fichiers (runner 2.1.1, audit 2.1.0, etc.).
3. Idéalement, centraliser les versions dans `mepa_constants.json` (section `versions_scripts`) et les lire, plutôt que de les hardcoder — mais sans casser la génération du passeport.

**Définition de terminé.** Un passeport généré avec `MEPA_IA_MODEL=claude-test` porte bien `claude-test`. Les versions affichées correspondent aux fichiers réels. Le schéma du passeport reste valide (la fonction `validate()` passe).

**Garde-fou.** Les champs existants du passeport (structure, SHA-256, champs obligatoires) restent inchangés — seuls la provenance et les métadonnées de version évoluent.

---

## Mission 4 — Robustesse d'entrée + reproductibilité

**Pourquoi.** Un paramètre manquant dans `config['params']` provoque aujourd'hui un `KeyError` opaque au milieu de la simulation, très lent à diagnostiquer sur 27 WP. Et l'absence de `requirements.txt` complique le redéploiement sur le Pi5.

**Tâches.**
1. En entrée de `run_wp()` (V6.2), ajouter une validation explicite des paramètres requis :
   ```python
   PARAMS_REQUIS = {'p1','p2','p2b','p3','p4','p5','p6','p7','p8','p9',
                    'p10','p11a','p11b','p13','lam','mu','nu','rho'}
   manquants = PARAMS_REQUIS - set(config.get('params', {}).keys())
   if manquants:
       raise ValueError(f"Paramètres manquants dans config['params'] : {sorted(manquants)}")
   ```
2. Créer `requirements.txt` (`numpy>=1.20`, `scipy>=1.6`).
3. (Optionnel) corriger le pattern fragile `or` sur flottants dans `_inject_theta` (bug #10) en `is not None` — **uniquement si** le harnais Mission 1 confirme zéro changement de sortie (le minimum theta étant 0.10, le comportement ne devrait pas bouger, mais à prouver).

**Définition de terminé.** Une config sans `p6` lève un `ValueError` clair et immédiat. Les 27 fiches valides produisent des sorties bit-identiques au golden (la validation ne déclenche que sur config invalide). `requirements.txt` présent.

**Garde-fou.** La validation ne doit JAMAIS se déclencher sur une config valide. Prouver le bit-identique sur les 27 WP après ajout.

---

## Mission 5 — Validation de la chaîne de bout en bout (pré-n8n)

**Pourquoi.** Les tests unitaires ne couvrent pas l'enchaînement des scripts. Avant de câbler n8n sur 27 WP, il faut prouver que les scripts se chaînent correctement (formats JSON compatibles entre étapes, chemins, parsing).

**Tâches.**
1. Écrire un script `tools/dry_run_pipeline.py` qui, pour une fiche WP donnée, exécute en séquence et passe la sortie de l'un à l'entrée du suivant :
   `node2_audit (JS) → runner → sensitivity_n1 → kappa_calculator → passeport_schema`
2. Le faire tourner sur 2 cas représentatifs : un statique propre (WP-C2-1 Égypte) et un dynamique C1 (WP-C1-1 Haïti, `cmd_linear`).
3. Vérifier à chaque jointure que la sortie du script N est un input valide pour le script N+1 (clés attendues présentes, types corrects). Documenter tout désaccord de format (ex. nom de champ attendu vs produit).
4. Produire un rapport des points de friction inter-scripts à transmettre à la conversation n8n (qui câblera le workflow).

**Définition de terminé.** Les 2 WP produisent un passeport de bout en bout sans intervention manuelle, via le script de dry run. Le rapport de friction inter-scripts est écrit.

**Garde-fou.** Le dry run n'appelle pas l'API Claude (CONV-A/B/E) — il valide la plomberie des scripts déterministes. Les étapes LLM seront câblées dans n8n séparément.

---

## Ce qui reste explicitement hors de ces missions

| Item | Pourquoi exclu | Où il va |
|---|---|---|
| Bug #1 LSODA discontinuité | Concerne `mepa_runner_v3_v7.py` (V7), pas V6.2 | Avant test V7-γ rev2 |
| Bug #5 factorisation V6.2/V7 | Refactoring, non bloquant pour le lancement | Chantier V7 |
| Bug #8 audit node V7 | V7 Track A, décisions non actées | Après V7-D1 |
| Mapping Cs→Mob (#11) | Décision d'architecture (chantier C0) | QG (CONV-C) |
| Méthodologie CCI n=8 (#9) | Documentation théorique, pas code | Addendum Théorique |
| Câblage des nœuds n8n | Configuration workflow, pas code script | Conversation n8n |

---

## Ordre d'exécution recommandé

```
Mission 1 (filet)  ──▶  Mission 2 (theta)  ──▶  Mission 3 (provenance)
                                                      │
                                                      ▼
                          Mission 5 (chaîne)  ◀──  Mission 4 (robustesse)
```

Mission 1 d'abord, toujours. Ensuite 2-3-4 dans n'importe quel ordre (indépendantes, chacune validée par le filet). Mission 5 en dernier, une fois le socle stabilisé. Après Mission 5, V6.2 est prêt pour le câblage n8n et le lancement du corpus.

---

## Note optionnelle — gel V6.3 advisory

Si vous décidez de déployer le gel V6.3 advisory (Dev 1 diagnostic, déjà produit et validé bit-identique), il s'insère **après** la Mission 1 et **avant** le lancement, comme une mission parallèle : déployer `mepa_runner_v2_gamma_v63.py` + `mepa_dev1_advisory_v63.py` + `mepa_constants_v63.json`, puis faire passer le harnais de non-régression de la Mission 1 pour confirmer le bit-identique. Le gel V6.3 n'est pas requis pour produire les WP V6.2 — c'est une option qui ajoute le diagnostic advisory sans changer les trajectoires.
