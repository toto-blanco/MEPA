# MEPA — Erratum à la Certification V7.0
## Protocole réellement exécuté · Provenance de la température · Réserve Rwanda (C4)

| Champ | Valeur |
|---|---|
| Statut | **Erratum et décision QG** — complète la Certification V7.0, ne la remplace pas |
| Objet | Certification V7.0 du cluster pilote V7-γ rev. 2 (`MEPA_Certification_V7_gamma_rev2.md`) |
| Rôle | QG / CONV-C (Architecte Scientifique) — décision prise par Antoine |
| Date | 2026-09-29 |
| Base factuelle | Traçage C-1 du CTO (`MEPA_C1_Tracage_E_Rc_gamma_L0.md`), recoupé par le QG sur les fiches V7, les 6 `result.json` de la session de certification (19-22 juin 2026) et `mepa_workflow_n8n_V7.json` |
| Références | Décision V7-D1 rev. 4 · Décision QG ARCH-AG-01 rev. 0 (C-1, C-2) · CV16 (non formalisée) |

---

## 1. Portée

Ce document corrige la description du protocole sous lequel les 6 WP pilotes ont été certifiés, et assortit la certification de WP-I10-1 Rwanda d'une réserve.

Il ne modifie **aucun** passeport, aucune empreinte d'intégrité, aucune trajectoire, aucun verdict ni aucun statut de certification. Les passeports certifiés sont des artefacts figés : les corrections sont portées ici, par référence, et non par réécriture.

---

## 2. Erratum 1 — Protocole réellement exécuté

### 2.1 Chaîne causale établie

Pour les 6 WP pilotes, les entrées simulées proviennent du **seul nœud CONV-E** :

1. La fiche V7 porte des valeurs pré-remplies dans `commandes` et `conditions_initiales`, et des variables V6.2 à coder (`variables.{E_split, A_r_c, gamma, L_t}.valeur = null`).
2. Le nœud CONV-E produit, dans un même appel, deux sorties : `variables_codees` et `commandes_mises_a_jour` (+ `L0_mis_a_jour`). La seconde écrase `commandes.{E, gamma, Rc, Rn}` et `conditions_initiales.L0`.
3. Aucun nœud en aval ne modifie ces valeurs. Le runner simule les commandes issues de CONV-E.
4. Le Nœud 8d (injection des valeurs résolues) est inerte : `scores_resolus` est toujours vide, par discordance des noms de champs entre 8a et `mepa_kappa_calculator.py`.
5. CONV-B (8a, 6b) a donc joué un rôle d'**audit de fiabilité** (CCI, verdict) **sans rétroaction** sur les entrées simulées.

### 2.2 Écarts fiche → entrées simulées (vérifiés)

| WP | Variables modifiées par CONV-E (fiche → simulé) |
|---|---|
| WP-I10-1 Rwanda | E 0.80 → 0.82 · Rc 0.60 → **0.90** · L0 0.10 → 0.12 |
| WP-I4-1 Allemagne | Rc 0.65 → 0.35 |
| WP-F10-1 Commune | E 0.60 → 0.63 · Rc 0.70 → 0.80 · L0 0.30 → 0.32 |
| WP-F1-1 Rome IIIe | Rc 0.45 → 0.50 |
| WP-C1-1 Haïti | E 0.70 → 0.72 · γ 0.25 → 0.22 · Rc 0.60 → 0.58 · L0 0.20 → 0.18 |
| WP-C2-1 Égypte | E 0.60 → 0.65 · γ 0.50 → 0.48 · Rc 0.55 → 0.62 · L0 0.25 → 0.28 |

Aucune variable hors du périmètre autorisé au nœud CONV-E (`E, gamma, Rc, Rn, L0`) n'a été modifiée. `T, Mob, R, Ref, EROI, Pop, S0, C0, I0` sont intactes sur 6/6.

### 2.3 Explication retirée

L'explication donnée en juin 2026 de la variance inter-run (« la résolution CONV-B se propage via 8a → 8d vers `y0` / `cmd_base` ») est **retirée**. La variance observée entre les runs de juin et de juillet provient du recodage par CONV-E à chaque exécution. La décision de geler les entrées (CV16) reste fondée, et l'est davantage : la variance naît au niveau du codeur lui-même.

### 2.4 Traçabilité incomplète

La sortie brute de CONV-E (`conv_e_raw`) n'est archivée dans aucun artefact. Le CCI (8a) porte sur `variables_codees` ; le runner simule `commandes_mises_a_jour`. Rien dans le pipeline ne garantit leur égalité.

Leur concordance sur les pilotes est établie **indirectement** : les tableaux S1 des rapports CONV-A, alimentés par `mepa_full_vars` (variables codées), concordent avec les `cmd_base` simulés sur E_split/E, γ, A_r_c/Rc, A_r_ne/Rn et L_t/L0 pour Rwanda, Allemagne, Rome, Haïti et Égypte (vérification QG) ; pour la Commune, la concordance a été vérifiée par CONV-B (contrôle C3 du Temps 2). Aucune divergence détectée. Cette preuve reste indirecte.

---

## 3. Erratum 2 — Provenance de la température

Les nœuds suivants n'ont transmis **aucun paramètre `temperature`** à l'API ; la valeur par défaut de l'API s'est donc appliquée :

| Nœud | Rôle | Température réellement transmise |
|---|---|---|
| CONV-E | Codage historique | non transmise (défaut API) |
| 8a | CONV-B, codage indépendant + CCI | non transmise (défaut API) |
| 6b | CONV-B, audit final | non transmise (défaut API) |
| 13 | Prédiction Popper | non transmise (défaut API) |
| 6 | CONV-A, rédaction | 0 |

La mention `provenance_ia.temperature: 0` figurant dans les 6 passeports pilotes est écrite en dur par `mepa_passeport_schema.py` : elle est **inexacte** pour les quatre premiers nœuds. Les codages, CCI et verdicts CONV-B des pilotes doivent être lus comme produits à la température par défaut de l'API.

Cette correction ne modifie aucun gate : les seuils de certification ont été appliqués aux valeurs effectivement produites.

---

## 4. Réserve sur la certification de WP-I10-1 Rwanda

### 4.1 Constat

La condition C4 du précheck (α) s'écrit `A_r_c_eff = A_r_c + 0.5 × A_r_ne > 0.70`. Avec `A_r_ne = 0.10` (valeur pré-remplie, non modifiée), la trajectoire (α) exige un **`A_r_c` codé strictement supérieur à 0.65**.

- Valeur pré-remplie dans la fiche (héritée de la V6.2) : **0.60** → `A_r_c_eff = 0.65` → C4 non satisfaite → (α) exclue.
- Valeur codée par CONV-E et simulée : **0.90** → `A_r_c_eff = 0.90` → C4 satisfaite.
- Valeur observée à l'identique sur deux exécutions indépendantes (juin et juillet 2026).
- Le stress N2 fait varier Rc de ±0.10 autour de 0.90 (plage 0.80–1.00) : il n'éprouve pas la zone du seuil.

La valeur 0.90 est historiquement défendable (appareil répressif d'État pleinement mobilisé en 1994) et a été auditée par CONV-B. Mais la trajectoire (α) du seul cas positif du corpus repose sur une variable codée à température non fixée, sans sortie brute archivée.

### 4.2 Décision

- La certification de WP-I10-1 Rwanda est **maintenue**.
- Elle est assortie de la réserve suivante : **« Trajectoire (α) conditionnelle à un `A_r_c` codé > 0.65 ; valeur codée 0.90, observée à l'identique sur deux tirages. »**
- La note antérieure du QG qualifiant d'« artefact de constantes de repli » le résultat sandbox du CTO (`A_r_c_eff = 0.65`) est **retirée** : ce run exécutait la fiche telle qu'écrite.

### 4.3 Critère de levée — pré-enregistré

Mesure : au moins **3 recodages indépendants** de WP-I10-1 par CONV-E, sous le protocole corrigé (température 0 transmise et enregistrée, sortie brute archivée), hors certification.

- **Levée** de la réserve si tous les recodages produisent `A_r_c > 0.65`.
- Si au moins un recodage produit `A_r_c ≤ 0.65` : la réserve devient une **instabilité documentée** et le statut de Rwanda est réexaminé par décision CV.

Cette mesure est la première à exécuter au titre de la mesure de variance prévue par ARCH-AG-01 §8.

### 4.4 Cas voisin — Allemagne

Pour WP-I4-1, C4 dépend aussi du recodage (Rc 0.65 → 0.35, `A_r_c_eff` 1.00 → 0.70). Le verdict n'en dépend pas : C2 échoue indépendamment (0.0055 < 0.0272) sur des valeurs pré-enregistrées par D1 rev. 4 §5. Aucune réserve.

---

## 5. Mesures pour les 21 WP restants

### 5.1 Actées par le présent document

| Mesure | Porteur |
|---|---|
| Transmettre `temperature: 0` sur les nœuds CONV-E, 8a, 6b et 13 | CTO |
| Enregistrer dans le passeport la température **effectivement transmise**, par nœud ; supprimer la valeur écrite en dur | CTO |
| Archiver la sortie brute de chaque appel CONV-E (`conv_e_raw`) | CTO |
| Porter la version de protocole dans chaque passeport | CTO |

Conséquence assumée : à température 0, une partie de la dispersion entre codeurs disparaît. Le CCI des 21 WP n'est pas directement comparable à celui des pilotes. La mesure Q-4 (troisième codeur d'une autre famille, hors certification) en devient plus nécessaire.

### 5.2 Renvoyées à CV16

- **Source unique audit / simulation** : dériver les `commandes` de façon déterministe à partir des `variables_codees`, au lieu de les demander une seconde fois au LLM. Condition pour que le gate `cci_global` porte sur les valeurs effectivement simulées.
- **Suppression des valeurs pré-remplies** dans `commandes` pour toute variable à coder (valeur `null`, ou valeur gelée après H1). Une fiche exécutée directement ne doit pas pouvoir produire une trajectoire différente de celle certifiée.
- **Verrouillage des valeurs pré-enregistrées** (ex. `A_r_ne`) : elles ne transitent plus par la sortie du codeur (cf. Décision QG ARCH-AG-01, C-2).
- **Sort du Nœud 8d** : suppression ou refonte. Il n'est pas corrigé en l'état, son activation modifierait le protocole sous lequel les pilotes ont été certifiés.

---

## 6. Ce que ce document ne change pas

- Les trajectoires diagnostiquées, verdicts et statuts des 6 WP pilotes.
- Les passeports archivés et leurs empreintes `hash_integrite.*`.
- Le gate de certification (`cci_global ≥ 0.75`) et les conditions de D1 rev. 4 §4.
- Le prononcé de la Certification V7.0 (6/6 conditions satisfaites).

---

*Erratum QG (CONV-C) — MEPA V7.0 — 2026-09-29*
