# CLAUDE.md — Consignes pour Claude Code

> Ce fichier se trouve à la racine du dossier de travail MEPA V6.2.
> Lis-le entièrement avant toute action. MEPA est un modèle scientifique
> en production. La rigueur prime sur la vitesse.

---

## 1. DIRECTIVE PRIMORDIALE — rétrocompatibilité bit-identique

Le socle **V6.2 Fortifiée** est en production. **Toute modification doit
préserver, au bit près, les sorties de trajectoire du runner sur les 27 WP.**

Les blocs qui ne doivent JAMAIS changer suite à une modification :
`simulation`, `verdict`, `stress_n1`, `stress_n2`.
Les champs `meta` (timestamps, versions) peuvent changer.

**Règle de fin de tâche : toute modification est terminée seulement quand
le harnais de non-régression confirme l'identité bit-à-bit des sorties de
trajectoire.** Si le harnais n'existe pas encore, le construire est la
première priorité avant tout autre changement.

---

## 2. CE QUE TU NE MODIFIES PAS sans instruction explicite

Les fonctions suivantes dans `scripts/mepa_runner_v2_gamma.py` sont le
cœur scientifique validé. N'y touche pas pour nettoyer, optimiser ou
adapter :

- `_step()` — intégrateur Euler
- `F_val()`, `R_val()` — forces du modèle
- `simulate()` — boucle d'intégration
- `apply_sa_modulator()` — modulation Sa=7
- `_build_result()`, `_tableau_s2()` — métriques de trajectoire

Si un bug semble venir de ces fonctions : **arrête-toi et demande**
avant toute modification. Le problème est presque toujours dans le
script appelant (parsing, config, chemin), pas dans les équations.

Ne modifie jamais une équation pour adapter une sortie à un consommateur
(n8n, passeport). Adapte le consommateur, pas l'équation.

---

## 3. CONTRAINTES DE DOMAINE — non négociables

**`gamma` — nomenclature absolue.**
La clé JSON/Python pour la capacité organisationnelle de l'élite est
**exclusivement** `gamma`. Jamais `g` (collision avec `gC` interne),
jamais `Gamma`. Le contrôle C4 de l'audit rejette toute autre forme.
Dans les commentaires/texte, le symbole `γ` est admis.

**Sa=7 — modulation obligatoire.**
Les WP à structure familiale souche (Sa=7 : WP-I3 Japon, WP-I4 Allemagne,
WP-I9 Singapour) imposent `p6_final = p6_base × 1.5`. Le runner et l'audit
Node 2 l'appliquent tous les deux — ils doivent produire le même `p6_final`
(tolérance 0.001). Toute divergence est un bug.

**Protocole NC.**
Sentinelle : chaîne `"NC"`.
- NC **bloquantes** : `gamma`, `EROI` → `RuntimeError` (DONNÉES_INSUFFISANTES)
- NC **non bloquantes** : `E`, `T`, `Mob`, `R`, `Ref`, `Rc`, `Rn`, `Pop`
  → warning + fallback, jamais de crash.
Ne change pas cette classification.

**Labels D4 — 9 labels officiels.**
Source de vérité : `config/mepa_constants.json`, clé `labels_trajectoire_d4`.
Tout label produit ou attendu doit appartenir à cet ensemble.
`(d) Dissolution` et `(γ) Transformation forcée` ne sont pas produits par
l'arbre automatique — ils passent par `trajectoire_forcee` ou LOI PHYSIQUE.

**Source unique de vérité.**
`config/mepa_constants.json` porte les bornes, seuils et constantes.
Ne hardcode jamais une valeur qui y figure déjà. Chaque script embarque un
fallback interne qui doit rester identique à ce fichier.

---

## 4. CARTE DES FICHIERS

### Scripts de production (modifier uniquement avec preuve bit-identique)

| Fichier | Rôle | Niveau de prudence |
|---|---|---|
| `scripts/mepa_runner_v2_gamma.py` | Runner ODE v2.1.1 — cœur de simulation | MAXIMALE |
| `scripts/mepa_sensitivity_n1.py` | Sensibilité ±20 % (9 cmd + 16 params) | Haute |
| `scripts/mepa_kappa_calculator.py` | CCI / κ de Cohen inter-codeurs | Haute |
| `scripts/mepa_passeport_schema.py` | Construction + validation du passeport WP | Haute |
| `scripts/mepa_node2_audit_v62.js` | Audit C1–C13, référence documentaire v2.1.0 | Haute |
| `scripts/mepa_whitelist_keys.json` | Clés autorisées des fiches de codage | Moyenne |
| `config/mepa_constants.json` | Source unique de vérité v1.2.3 | MAXIMALE |

> **Note Node 2 :** le nœud N2 réellement exécuté par n8n est embarqué dans
> `mepa_workflow_n8n_V62.json` (version "V6.3 Fortifié", Correctif A6).
> Le fichier `.js` est la référence documentaire — fonctionnellement
> équivalent pour les 13 contrôles C1–C13.

### Configs WP (données scientifiques — ne pas modifier les valeurs codées)

```
config/WP-*.json          ← 27 fiches WP de simulation
config/fiche_etalon_*.json ← étalons d'ancrage EROI (min=Haïti, max=Islande)
config/mepa_friction_profile.json  ← profil de friction (paramètres de base)
config/MEPA_V62_Ordre_de_Marche_1_WP-C1-1.json  ← ordre de passage WP-C1
config/mepa_fiches_WP-F10-1_WP-I10-1.json       ← fiches combinées F10/I10
```

### Instructions des agents Claude (prompts — ne pas modifier sans demande)

```
scripts/CONV-A.md          ← Rédaction des WP (sections S1-S7)
scripts/CONV-B.md          ← Audit scientifique inter-codeurs
scripts/CONV-E.md          ← Codage MEPA Full (historien-codeur)
scripts/CONV-D.md          ← Observatoire résultats
scripts/prompt_projet_MEPA_V3_gamma.md  ← Prompt système CONV-E
```

### Répertoires

```
config/          ← Fiches WP + constantes + profils (entrées pipeline)
scripts/         ← Tous les scripts Python/JS/Markdown
outputs/         ← Sorties générées par le pipeline
  cluster_C1/results/    ← Résultats JSON de simulation
  cluster_C1/rapports/   ← WP rédigés (CONV-A)
  passeports/            ← Passeports de certification
  sensitivity/           ← Résultats sensibilité N1
documentation/   ← Documents .docx/.odt de référence (lecture seule)
archives/        ← Anciennes versions (lecture seule)
prod/            ← Staging déploiement (à ne pas modifier directement)
```

### Workflows n8n (ne pas modifier — câblés par la conversation n8n)

```
mepa_workflow_n8n_V62.json          ← WF2 Protocole Complet (26 nœuds)
mepa_workflow_n8n_V62_multipass.json ← Variante multipass cluster C1
```

---

## 5. CE DOSSIER EST V6.2 UNIQUEMENT

Ce dossier contient exclusivement le socle **V6.2 Fortifiée**.

Il existe un chantier V7 (deux axes : corrections de trajectoires Track A,
et extension biophysique Track B) mais ses fichiers sont dans un dossier
séparé auquel tu n'as pas accès. Si tu croises des références à V7 dans
les documents de `documentation/` (normal — ils anticipent la feuille de
route), tu peux les lire pour contexte mais **n'introduis pas de code V7
dans ce dossier**. Toute question V7 remonte à QG (voir §6).

---

## 6. SCOPE — qui décide quoi

| Type de tâche | Toi (Claude Code) |
|---|---|
| Bugs de code, tests, scripts outils, refactor sûr | ✅ exécute |
| Décisions d'architecture (équations, paramètres théoriques) | ❌ signale → QG |
| Câblage nœuds n8n, expressions, credentials API | ❌ documente → conversation n8n |
| Codage des variables d'un WP (sources historiques) | ❌ → CONV-E |
| Introduction de code V7 | ❌ → QG |
| Interprétation scientifique d'un résultat | ❌ → QG / CONV-A |

Quand une tâche déborde, dis-le explicitement et indique le bon canal.
Ne tranche pas une question d'architecture ou de théorie.

---

## 7. PROTOCOLE DE VÉRIFICATION

**Le harnais de non-régression est ton outil central.**
Une fois construit (`tests/test_nonregression_v62.py`) :

```bash
export MEPA_SCRIPTS_DIR="$(pwd)/scripts"
pytest tests/ -v
```

S'il n'existe pas encore : le construire est la PREMIÈRE priorité.
Il doit (1) exécuter les 27 WP et capturer les sorties actuelles comme
golden, (2) re-exécuter et comparer par hash SHA-256, en excluant `meta`.

**Critère de fin pour toute modification du runner ou des constants :**
`pytest` passe ET les golden de trajectoire sont inchangés.

Si un golden change, c'est soit une régression (à corriger), soit un
changement intentionnel (à signaler, documenter, et obtenir confirmation).

---

## 8. COMMANDES

```bash
# Environnement (toujours définir avant d'exécuter un script)
export MEPA_SCRIPTS_DIR="$(pwd)/scripts"
export MEPA_OUTPUT_DIR="$(pwd)/outputs"

# Simulation directe d'un WP
python3 scripts/mepa_runner_v2_gamma.py \
    config/WP-C2-1_Egypte2011_v62.json \
    outputs/cluster_C1/results/WP-C2-1_result.json

# Sensibilité N1
python3 scripts/mepa_sensitivity_n1.py \
    config/WP-C2-1_Egypte2011_v62.json \
    outputs/sensitivity/WP-C2-1_n1.json

# CCI inter-codeurs
python3 scripts/mepa_kappa_calculator.py \
    fiche_CONV-E.json fiche_CONV-B.json cci_result.json

# Audit Node 2 (Node.js ≥ 18)
node scripts/mepa_node2_audit_v62.js \
    config/WP-C2-1_Egypte2011_v62.json

# Tests (une fois le harnais construit)
pytest tests/ -v
```

Dépendances : Python ≥ 3.9, numpy, scipy (stdlib suffisante pour le runner
V6.2 — scipy est requis uniquement pour le runner V7 qui n'est pas dans ce
dossier) ; Node.js ≥ 18.

---

## 9. CONVENTIONS

- **Nommage** : suffixe `_v63` pour les variantes V6.3 advisory déjà produites.
  Ne pas écraser un fichier de production sans backup dans `archives/`.
- **Encodage** : UTF-8 (le projet utilise `γ`, `α`, `θ`, `Ψ`, `Φ`, accents).
- **Pas de réseau** : les scripts de simulation tournent offline (Raspberry Pi 5).
- **stdlib d'abord** : ne pas ajouter de dépendance externe sans nécessité prouvée.
- **Un commit par mission**, message décrivant le bug corrigé + preuve de
  non-régression.
- **Ne crée pas de fichiers non demandés** — pas de README spontanés, pas de
  docs supplémentaires. Les tests et scripts outils explicitement requis sont OK.

---

## 10. WORKFLOW GIT — à suivre à chaque session

**Ce que tu fais (étapes 1–4) :**

```bash
# Étape 1 — Toujours vérifier l'état avant de commencer
git status
# Si ce n'est pas propre (fichiers modifiés non commités), arrête-toi et demande.

# Étape 2 — Créer une branche dédiée par mission
git checkout -b fix/nom-du-bug
# Exemples : fix/theta-sensitivity, fix/passeport-provenance,
#            feat/test-nonregression, fix/params-validation

# Étape 3 — Travailler sur la mission

# Étape 4 — Commiter régulièrement (pas tout à la fin)
git add -A && git commit -m "fix: description du changement + preuve non-régression"
# Message de commit : commencer par fix:, feat:, test:, ou docs:
# Mentionner la preuve bit-identique : "pytest 27/27 golden inchangés"
```

**Ce que tu NE fais PAS :**

- Tu ne merges **jamais** sur `main` toi-même. Le merge est une décision humaine,
  prise après validation du harnais de votre côté.
- Tu ne fais pas `git push --force`.
- Tu ne commites pas de fichiers de `outputs/` (résultats de simulation générés).
- Tu ne commites pas de fichiers `.env` ou contenant des clés API.

**Convention de nommage des branches :**

| Préfixe | Usage |
|---|---|
| `fix/` | Correction de bug (theta, passeport, params…) |
| `feat/` | Nouvelle fonctionnalité (harnais de test, script outil) |
| `test/` | Ajout ou modification de tests uniquement |
| `docs/` | Documentation seulement, aucun code |

**En fin de session :** indique clairement l'état de la branche — ce qui est
commité, ce qui reste à faire, et si `pytest` passe. L'utilisateur décide
ensuite de merger ou d'abandonner la branche.

---

## 11. EN CAS DE DOUTE

Si une instruction semble contredire la directive bit-identique, ou demande
de toucher aux équations, ou dépasse ton scope : **arrête-toi et demande**.

Mieux vaut une question qu'une régression silencieuse dans un modèle
scientifique en production.
