# CV13 — Rapport de test : recalibration λ/μ (Option A, volet partiel)

**Branche :** `test/cv13-recalibration` — non mergée, en attente de validation QG
**Origine :** `MEPA_Decision_CV13_Recalibration.md` (rôle CONV-C / QG)
**Statut :** Test exécuté. CV13 reste **instruite, pas tranchée** — ce rapport
fournit les données pour la décision QG (§6 de la décision CV13).

---

## 0. Limite actée avant le test (Blocage 2)

Le plancher `I_min = 0.30` visé par CV13 §3 (Option A) **n'existe pas dans
`mepa_constants.json`**. Il s'agit de la constante `I_MIN = 0.30` codée en dur
dans `scripts/mepa_runner_v2_gamma.py` (ligne 92, bloc « CONSTANTES FIXES »),
utilisée à l'intérieur de `_step()` (ligne 340 : `max(I_MIN, I + dI)`) —
fonction protégée par CLAUDE.md §2.

**Décision actée avec QG (avant test) :** ne pas toucher au runner. Le test
CV13 porte **uniquement sur λ et μ**. Le volet `I_min` est **suspendu** —
les résultats ci-dessous sont donc **partiels** sur la composante « plancher
de R ». Une observation empirique (§3) permet néanmoins d'éclairer la
pertinence probable de ce volet pour les 4 WP à codage fort.

---

## 1. Modification appliquée

Dans `config/mepa_constants.json`, section `bornes_parametres_dynamiques` :

| Paramètre | Avant | Après | Borne [min, max] |
|---|---|---|---|
| `lam` (λ) | 0.68 | **0.85** | [0.30, 0.90] — inchangées |
| `mu` (μ) | 0.38 | **0.55** | [0.10, 0.70] — inchangées |

Seuls les champs `defaut` ont été modifiés (+ note `[CV13-test]` ajoutée).
`I_min` non touché (cf. §0). `bornes_corpus_commandes` (section documentaire
distincte, non lue par le runner) non touchée.

WP-I10-1 Rwanda possède une surcharge `params_p.lam = 0.72` qui **n'est pas
affectée** par ce changement de défaut global (seul `mu` change pour ce WP).

---

## 2. Étape 3 — Harnais de non-régression

```
pytest tests/ -v  →  47 passed, 29 failed (golden), 1 xfailed
```

**Les 29 golden changent tous** — attendu : λ et μ sont des paramètres
globaux qui entrent dans `F(t)` pour les 27 WP + 2 étalons, donc toute
trajectoire numérique (`FR_max`, `tableau_S2`, etc.) change, même quand le
**label de trajectoire** et la **concordance** restent identiques.

**Contrainte dure CV13 (C2 Égypte, I6 Tiananmen ne doivent pas diverger) :**

| WP | FR_max avant | FR_max après | traj avant/après | concordance |
|---|---|---|---|---|
| WP-C2-1 Égypte | 0.3158 | 0.3830 | `(b) Répression réussie` → inchangé | **True → True** ✅ |
| WP-I6-1 Tiananmen | 0.2689 | 0.3358 | `(b) Répression réussie` → inchangé | **True → True** ✅ |

→ **Contrainte respectée.** Les golden « changent » au sens hash (valeurs
numériques), mais ni le label de trajectoire ni la concordance des 2 WP déjà
certifiés ne régressent. Les golden n'ont **pas été régénérés** sur cette
branche (décision de merge/régénération réservée à QG).

---

## 3. Étape 4 — Les 4 WP à codage fort (γ>0.60 ET E>0.60)

| WP | FR_max avant | FR_max après | Δ | Franchit F≥R ? | I_min_sim | I_MIN=0.30 actif ? |
|---|---|---|---|---|---|---|
| WP-I2-1 Russie 1917 | 0.6549 | 0.8004 | +0.145 | **Non** | 0.8022 | Non (loin du plancher) |
| WP-F7-1 Révolution haïtienne | 0.6056 | 0.7306 | +0.125 | **Non** | 1.25 | Non |
| WP-I4-1 Allemagne nazie | 0.3089 | 0.3924 | +0.084 | **Non** | 2.50 | Non |
| WP-I10-1 Rwanda | 1.2765 | 1.2986 | +0.022 | **Oui** (déjà avant, t=8→7) | 1.0 | Non |

**Résultat :** sur les 3 WP à codage fort qui ne franchissaient pas (I2, F7,
I4), **aucun ne franchit après recalibration λ/μ**, malgré un λ porté à
0.85 (proche du plafond corpus 0.90) et μ à 0.55. I10 Rwanda franchissait
déjà — mais via sa **propre surcharge `params_p.lam=0.72`**, indépendante
de ce test (le franchissement de I10 n'est pas un effet de la recalibration
globale).

**Observation sur le volet I_min suspendu (§0) :** pour ces 3 WP, `I_min_sim`
(valeur minimale atteinte par I durant la trajectoire) vaut 0.80 / 1.25 / 2.50
— **bien au-dessus du plancher I_MIN=0.30**. Le plancher `I_min` n'est donc
**jamais actif** pour I2, F7 ou I4 : le recalibrer (0.30→0.15, comme proposé
en §3.A de la décision CV13) **n'aurait aucun effet sur ces 3 WP**, qu'il
soit testé ou non. Le volet `I_min` semble pertinent uniquement pour les
trajectoires où I s'effondre vers le plancher (cf. WP-C1-1 ci-dessous), pas
pour les ruptures de type (a).

---

## 4. Étape 5 — Vue d'ensemble des 27 WP + 2 étalons

| wp_id | trajectoire attendue | traj golden (avant) | traj après | concordance avant→après |
|---|---|---|---|---|
| WP-C1-1 | (d) Dissolution | (h)/(e) Stabilité ou réforme lente | **(d) Effondrement progressif** | False → False (label différent mais même famille « d ») |
| WP-C2-1 | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | **True → True** |
| WP-C3-1 | (c) Stase / ambigu | (h)/(e) Stabilité ou réforme lente | (h)/(e) Stabilité ou réforme lente | False → False |
| WP-C4-1 | (d) Dissolution | (h)/(e) Stabilité ou réforme lente | (h)/(e) Stabilité ou réforme lente | False → False |
| WP-C5-1 | (h)/(e) Stabilité ou réforme lente | (b) Répression réussie | (b) Répression réussie | False → False |
| WP-C6-1 | (h) Stabilité | (b) Répression réussie | (b) Répression réussie | False → False |
| WP-F1-1 | (d) Effondrement progressif | (h)/(e) Stabilité ou réforme lente | (h)/(e) Stabilité ou réforme lente | False → False |
| WP-F10-1 | (a) Rupture transformatrice | (b) Répression réussie | (b) Répression réussie | False → False |
| WP-F2-1 | (d) Effondrement progressif | (h)/(e) Stabilité ou réforme lente | (h)/(e) Stabilité ou réforme lente | False → False |
| WP-F3-1 | (d) Effondrement progressif | (h)/(e) Stabilité ou réforme lente | (h)/(e) Stabilité ou réforme lente | False → False |
| WP-F4-1 | (c) Stase / ambigu | (h)/(e) Stabilité ou réforme lente | (h)/(e) Stabilité ou réforme lente | False → False |
| WP-F5-1 | (c) Stase / ambigu | (h)/(e) Stabilité ou réforme lente | (h)/(e) Stabilité ou réforme lente | False → False |
| WP-F6-1 | (d) Effondrement progressif | (h)/(e) Stabilité ou réforme lente | (h)/(e) Stabilité ou réforme lente | False → False |
| WP-F7-1 | (a) Rupture transformatrice | (h)/(e) Stabilité ou réforme lente | (h)/(e) Stabilité ou réforme lente | False → False |
| WP-F8-1 | (a) Rupture transformatrice | (h)/(e) Stabilité ou réforme lente | (h)/(e) Stabilité ou réforme lente | False → False |
| WP-F9-1 | (h) Stabilité | (h)/(e) Stabilité ou réforme lente | (h)/(e) Stabilité ou réforme lente | False → False |
| WP-I1-1 | (h) Stabilité | (h)/(e) Stabilité ou réforme lente | (h)/(e) Stabilité ou réforme lente | False → False |
| WP-I10-1 | (a) Rupture transformatrice | (a) Rupture transformatrice | (a) Rupture transformatrice | **True → True** |
| WP-I2-1 | (a) Rupture transformatrice | (h)/(e) Stabilité ou réforme lente | (h)/(e) Stabilité ou réforme lente | False → False |
| WP-I3-1 | (d) Effondrement progressif | (h)/(e) Stabilité ou réforme lente | (h)/(e) Stabilité ou réforme lente | False → False |
| WP-I4-1 | (a) Rupture transformatrice | (b) Répression réussie | (b) Répression réussie | False → False |
| WP-I5-1 | (γ) Transformation forcée | (b) Répression réussie | (b) Répression réussie | False → False |
| WP-I6-1 | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | **True → True** |
| WP-I7-1 | (d) Effondrement progressif | (b) Répression réussie | (b) Répression réussie | False → False |
| WP-I8-1 | (h) Stabilité | (b) Répression réussie | (b) Répression réussie | False → False |
| WP-I9-1 | (h) Stabilité | (b) Répression réussie | (b) Répression réussie | False → False |
| WP-T1-1 | (γ) Transformation forcée | (h)/(e) Stabilité ou réforme lente | (h)/(e) Stabilité ou réforme lente | False → False |
| WP-C1-1_etalon | (d) Dissolution | (h)/(e) Stabilité ou réforme lente | (d) Effondrement progressif | False → False |
| WP-EXT-5_etalon | (e) Réforme institutionnelle | (h)/(e) Stabilité ou réforme lente | (h)/(e) Stabilité ou réforme lente | False → False |

---

## 5. Synthèse (Étape 6)

- **Concordances honnêtes — avant : 3/27** (WP-C2-1, WP-I6-1, WP-I10-1).
  **Après : 3/27** (mêmes 3 WP — aucune nouvelle concordance, aucune perte).
- **Les 4 WP à codage fort franchissent-ils ?** I10 oui (préexistant, via
  surcharge propre). I2, F7, I4 : **non**, malgré λ porté quasiment au
  plafond corpus (0.85/0.90) et μ à 0.55/0.70.
- **Les 2 WP déjà concordants (C2, I6) le restent-ils ?** **Oui**, label et
  concordance inchangés, FR_max reste loin de 1 (0.38, 0.34).
- **Effets de bord non prévus :**
  - WP-C1-1 (Haïti) et son étalon `WP-C1-1_etalon` basculent de
    `(h)/(e) Stabilité ou réforme lente` vers `(d) Effondrement progressif`
    (FR_max 0.8857 → 1.0345, t_bascule=31). C'est un changement de **famille**
    de label vers la famille attendue « (d) » (attendu = `(d) Dissolution`),
    mais pas une concordance exacte (label différent). Pour ce WP,
    `I_min_sim = 0.30` **= I_MIN exactement**, dans les deux configurations :
    le plancher `I_min` est actif ici, contrairement aux 3 WP de rupture
    (§3). C'est cohérent avec le diagnostic CV13 §2.1 : le plancher I_min
    pèse sur les trajectoires d'effondrement (d), pas sur les ruptures (a).
  - Aucune autre des 24 WP non concordants ne change de label.

---

## 6. Conclusion pour QG (points CV13-C / CV13-D)

**CV13-C (seuil ≥ 8/27 concordances honnêtes) : non atteint.** 3/27 avant,
3/27 après — λ/μ seuls (même portés près de leurs bornes hautes corpus)
ne suffisent pas à faire émerger de nouvelles concordances sur ce corpus.

**Lecture du critère géométrique CV13-B (chevauchement F/R ≥20% sur WP à
codage fort) :** I2 et F7 se rapprochent nettement (FR_max 0.65→0.80 et
0.61→0.73, soit un déficit résiduel de 0.20 et 0.27 respectivement vs un
franchissement à FR_max=1.0), mais ni l'un ni l'autre ne franchit. I4 reste
loin (FR_max=0.39).

**Sur le volet I_min suspendu :** l'observation empirique (§3) suggère que
même si CV13-A (I_min 0.30→0.15) avait été testé, **il n'aurait pas changé
le résultat pour I2/F7/I4** — leur `I_min_sim` est loin du plancher actuel.
Il aurait en revanche probablement amplifié l'effet déjà observé sur
WP-C1-1 Haïti (le seul WP du corpus où `I_min_sim` touche exactement 0.30).

**Recommandation factuelle (pas une décision — à trancher en QG) :** sur la
base de ces données, le volet λ/μ d'Option A seul **n'atteint pas le seuil
CV13-C**. Le volet I_min, même s'il était instruit, ne semble pertinent que
pour la branche (d)/Haïti — pas pour les 3 WP de rupture (a) en échec. Ces
deux constats orientent vers l'instruction d'Option B (chemin architectural
pour (d), §3 décision CV13) en parallèle ou à la place d'une poursuite
d'Option A pour les ruptures (a).

---

## 7. État de la branche

- `git diff` : 1 fichier modifié (`config/mepa_constants.json`, defauts
  `lam`/`mu` uniquement, bornes inchangées) + ce rapport.
- `pytest tests/ -v` : 47 passed, **29 failed (golden, attendu — non
  régénérés)**, 1 xfailed.
- Aucun fichier de `config/WP-*.json`, aucune instruction CONV-*, aucun
  workflow n8n, aucun fichier du runner modifié.
- **Pas de merge.** Branche `test/cv13-recalibration` en attente de
  validation QG.
