# MEPA — Décision QG : version canonique de V7-D1 rev. 4 · vérification a posteriori du §5.3

| Champ | Valeur |
|---|---|
| Statut | **Décision QG** — complète la Certification V7.0 |
| Rôle | QG / CONV-C (Architecte Scientifique) — décision prise par Antoine |
| Date | 2026-09-30 |
| Base factuelle | Comparaison des deux versions de V7-D1 rev. 4 ; relevé des hyperparamètres dans `config/mepa_constants.json` et `scripts/mepa_runner_v3_v7.py` (constat Claude Code du 2026-09-30) |
| Références | `MEPA_Decision_V7_D1_rev4.md` (version canonique) · `MEPA_Certification_V7_gamma_rev2.md` · Erratum Certification V7.0 |

---

## 1. Version canonique de V7-D1 rev. 4

Deux versions du texte circulaient :

| | Version canonique | Export aplati (retiré) |
|---|---|---|
| Origine | Dépôt `prepa_v7`, commit `680ed31` du 2026-06-11 | Copie de la base de connaissance du projet (`Décision_de_Décertification_V7-D1_rev__4.docx`, en réalité du markdown) |
| sha256 | `6e27b2ba7a5b3dd5dd546e0b11603e98c32ae5ab240a3c89696137c0e67b3b89` | `406bafd5…` |
| §2 — tableau des 15 rapports décertifiés | présent | absent (le texte y renvoie pourtant) |
| §5.3 — intervalles de tolérance pré-enregistrés | présent | absent |

Les seuls éléments propres à l'export aplati sont éditoriaux (un sous-titre, l'attribution « V7-R3 §2 et §3 », la mention « à venir » au §8). Aucun ne modifie une règle.

**Décision :**
- La version canonique de V7-D1 rev. 4 est celle du dépôt `prepa_v7`. Elle remplace mot pour mot, dans `MEPA_Decision/`, l'export aplati versionné par erreur (commit `dedda61`, remplaçant `4485c35`). Aucune fusion n'est faite.
- La copie de la base de connaissance du projet est remplacée par la version canonique, pour que toutes les sessions (QG, CTO, CONV-B) travaillent sur le texte complet.

**Constat de méthode :** la certification V7.0 et les audits CONV-B ont été conduits sur l'export aplati, donc sans le §5.3. C'est une nouvelle illustration de la règle selon laquelle une copie de la base de connaissance ne fait pas foi : seule la version tracée dans git est de référence.

---

## 2. Vérification a posteriori du §5.3

Le §5.3 de V7-D1 rev. 4 pré-enregistre un intervalle de tolérance pour dix hyperparamètres V7-α rev. 2.1, et dispose qu'un hyperparamètre dont la valeur sort de son intervalle lors du test V7-γ est considéré comme réfuté. La Certification V7.0 ne contient pas cette vérification ; elle est faite ici.

| Hyperparamètre | Intervalle §5.3 | Valeur utilisée | Source | Résultat |
|---|---|---|---|---|
| θ_C (C_max, condition C5 de α) | [0.30, 0.50] | 0.30 | `config/mepa_constants.json:493` | sur la borne basse |
| σ_base | [0.015, 0.025] | 0.018 | `config/mepa_constants.json:483` | dans l'intervalle |
| α (facteur σ-Φ) | [1.2, 2.5] | 1.7 | `config/mepa_constants.json:488` | dans l'intervalle |
| μ_m* | [0.55, 0.65] | 0.60 | `config/mepa_constants.json:478` | dans l'intervalle |
| Modulateur p6, phase 1 | [0.40, 0.60] | 0.50 | `config/mepa_constants.json:510` | dans l'intervalle |
| Modulateur p6, phase 2 | [2.00, 3.00] | 2.50 | `config/mepa_constants.json:517` | dans l'intervalle |
| Modulateur p6, phase 3 | [1.05, 1.25] | 1.15 | `config/mepa_constants.json:524` | dans l'intervalle |
| Coefficient de A_r_c_eff (clause de repli) | [0.3, 0.7] | 0.5 | `config/mepa_constants.json:499` | dans l'intervalle |
| Seuil chute_C (branche b explicative) | [0.15, 0.30] | 0.20 | `config/mepa_constants.json:537` | dans l'intervalle |
| Seuil C_max (branche b explicative) | [0.10, 0.18] | 0.12 | `config/mepa_constants.json:532` | dans l'intervalle |

Les valeurs de repli codées dans `mepa_runner_v3_v7.py` sont identiques aux constantes pour les dix hyperparamètres.

**θ_C sur la borne :** la condition C5 est codée en inégalité stricte (`C_max > theta_C_alpha`, `mepa_runner_v3_v7.py:516`), ce qui correspond à la notation « > 0.30 » du §5.3. Seul WP-I10-1 Rwanda est concerné par C5 ; son `C_max` certifié (1.6587) est très au-dessus du seuil.

**Décision :**
- Aucun hyperparamètre n'est réfuté au sens du §5.3. La Certification V7.0 est conforme au §5.3.
- **Portée :** la vérification porte sur les valeurs codées. Aucun hyperparamètre n'a été recalibré pendant le test V7-γ : les valeurs utilisées sont celles qui avaient été pré-enregistrées.

---

## 3. Constat technique transmis au CTO

Le runner charge `mepa_constants.json` depuis `MEPA_SCRIPTS_DIR` (par défaut `/data/mepa/scripts`), alors que dans le dépôt le fichier se trouve dans `config/`. Sans effet aujourd'hui, puisque les valeurs de repli sont identiques. Mais l'emplacement de la source unique de vérité diffère entre le dépôt et la production.

**Demandé au CTO :** confirmer que la copie déployée est identique à `config/mepa_constants.json`, vérifier que le contrôle DEP3 la couvre, et documenter la correspondance des chemins entre le dépôt et le Pi.

---

*Décision QG (CONV-C) — MEPA V7.0 — 2026-09-30*
