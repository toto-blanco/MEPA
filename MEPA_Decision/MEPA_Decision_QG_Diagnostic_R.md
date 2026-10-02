# MEPA — Décision QG : diagnostic de sensibilité des pilotes à R

| Champ | Valeur |
|---|---|
| Statut | **Décision QG** |
| Rôle | QG / CONV-C (Architecte Scientifique) — décision prise par Antoine |
| Date | 2026-10-02 |
| Base factuelle | Diagnostic R du CTO (`outputs/mesures/2026-10-02_diagnostic_R/`) ; vérification QG des annotations de branche et des critères V7-C4 dans les 18 sorties complètes |
| Références | `MEPA_Decision_QG_Cloture_L0_D3_A_d_eff.md` (§3, §5) · `MEPA_Decision_V7_D1_rev4.md` (§4, §5.3) · Certification V7.0 · CV16 (à rédiger) |

---

## 1. Rappel

Le Nœud CONV-E code `A_d_eff`, que l'audit CCI contrôle, mais le `R` simulé est la valeur pré-remplie de la fiche (décision du 2026-09-30, §3). Le diagnostic pré-enregistré (même décision, §5) mesure la sensibilité des trajectoires certifiées à un `R` dérivé de `A_d_eff`, sans conséquence automatique.

**Méthode :** runner seul, constantes réelles, entrées des `result.json` de juin. Reproduction au bit près vérifiée à `R` d'origine sur les 6 WP (vérifiée aussi par le QG sur les blocs simulation, stress, verdict, précheck, entrées). Une seule variation : `R = A_d_eff / 10`, conversion provisoire.
- **Série A** : `A_d_eff` relevé dans les rapports de juin (provenance indirecte).
- **Série B** : `A_d_eff` relevé dans les rapports du 3 juillet (authentifiés par empreinte).

Les séries ne diffèrent que sur l'Égypte (3.8 en juin, 3.5 en juillet).

---

## 2. Résultats

| WP | R origine → A / B | Trajectoire (orig. / A / B) | Annotation (orig. → A, B) | `C_max` (orig. / A / B) | Robustesse N1 (orig. → A, B) |
|---|---|---|---|---|---|
| WP-I10-1 Rwanda | 0.15 → 0.15 / 0.15 | (α) / (α) / (α) | EXPLICATIVE, inchangée | 1.6587 ×3 | ROBUSTE, inchangée |
| WP-I4-1 Allemagne | 0.30 → 0.25 / 0.25 | (b) / (b) / (b) | **CATCHALL → EXPLICATIVE** | 0.1145 / 0.1218 / 0.1218 | ROBUSTE, inchangée |
| WP-F10-1 Commune | 0.20 → 0.35 / 0.35 | (b) / (b) / (b) | **CATCHALL → EXPLICATIVE** | 0.1639 / 0.1338 / 0.1338 | ROBUSTE, inchangée |
| WP-F1-1 Rome IIIe | 0.30 → 0.45 / 0.45 | (d) / (d) / (d) | EXPLICATIVE, inchangée | 0.1100 / 0.1051 / 0.1051 | **MÉTASTABLE → ROBUSTE** |
| WP-C1-1 Haïti | 0.15 → 0.14 / 0.14 | (d) / (d) / (d) | EXPLICATIVE, inchangée | 0.2842 / 0.2875 / 0.2875 | ROBUSTE, inchangée |
| WP-C2-1 Égypte | 0.25 → 0.38 / 0.35 | (b) / (b) / (b) | EXPLICATIVE, inchangée | 0.1460 / **0.1213** / 0.1262 | MÉTASTABLE, inchangée (stress redistribués) |

Pour l'Égypte, les perturbations qui produisent (d) changent : en séries A et B, N1 optimiste, N2 E−0.1, N2 R+0.08 et N2 Rc+0.1 passent de (b) à (d) ; N1 pessimiste et N2 R−0.08 passent de (d) à (b).

Les séries A et B aboutissent aux mêmes conclusions sur les six WP. La question de provenance des valeurs de juin est sans objet pour ce diagnostic.

---

## 3. Lecture au regard des conditions de certification (D1 rev. 4 §4)

| Condition | WP | Origine | Série A | Série B |
|---|---|---|---|---|
| 1 — (α) via V7-C1 | Rwanda | satisfaite | satisfaite | satisfaite |
| 2 — échec C2 pré-enregistré | Allemagne | satisfaite | satisfaite | satisfaite |
| 3 — non-(α), contrôle négatif | Commune | satisfaite | satisfaite | satisfaite |
| 4 — (d) via V7-C2 | Rome | satisfaite | satisfaite | satisfaite |
| 5 — (d) via V7-C2 | Haïti | satisfaite | satisfaite | satisfaite |
| 6 — (b) explicative via V7-C4 | Égypte | satisfaite (`C_max` 0.146) | satisfaite (`C_max` **0.1213**) | satisfaite (`C_max` 0.1262) |

Les six conditions restent satisfaites avec un `R` dérivé de `A_d_eff`. La condition 6 tient avec une marge de **0.0013** au-dessus du seuil `C_max > 0.12` en série A, contre 0.026 à l'origine. Le §5.3 autorise ce seuil dans l'intervalle [0.10, 0.18] : toute valeur supérieure à 0.1213 ferait échouer la condition 6 en série A.

---

## 4. Décisions

1. **Statuts de certification inchangés.** Les 6 pilotes sont certifiés sur leurs entrées V7.0-P1, archivées et figées. Le diagnostic était pré-enregistré sans conséquence automatique.
2. **Pour les 21 WP restants, `R` doit dériver de `A_d_eff`.** Conserver la valeur pré-remplie de la fiche n'est pas acceptable : elle détermine l'annotation de branche de deux cas sur six (Allemagne, Commune). La règle de conversion est arrêtée dans CV16 ; la division par 10 n'est retenue que pour ce diagnostic.
3. **Fragilité de l'annotation V7-C4.** Sous `R` codé, trois cas sur six ont un `C_max` compris entre 0.12 et 0.14. Le seuil, pré-enregistré au §5.3, n'est pas modifié. Ce constat est versé comme intrant au chantier V7.1.
4. **Marge au seuil dans le passeport.** CV16 examinera l'inscription au passeport de la marge entre chaque grandeur décisive d'annotation (`C_max`, `chute_C`) et son seuil, afin qu'une annotation à la limite soit visible à la lecture.
5. **Lecture des cas divergents.** Les rapports de l'Allemagne et de la Commune documentent un (b) CATCHALL. Sous `R` codé, ce (b) serait annoté EXPLICATIVE par V7-C4. Ce point n'invalide pas les §1.6–§1.7 de ces rapports, établis sur les entrées certifiées ; il sera repris lors du traitement de ces cas sous protocole V7.0-P2.

---

## 5. Rectification de la décision du 2026-09-30 (§3.1)

- WP-F10-1 Commune : `A_d_eff` codé = **3.5** (la cellule portait « à relever »).
- Les valeurs de juin de la colonne « `A_d_eff` codé » sont de **provenance indirecte** : les rapports de juin ne peuvent pas être authentifiés par empreinte (`rapport_md_sha256 = null`). Leur provenance repose sur la concordance de leurs tableaux S1 avec les `result.json` de juin ; elle est sans objet pour le diagnostic, les séries A et B concluant de même.

---

## 6. Note de méthode

La demande QG au CTO ne listait pas l'annotation de branche parmi les grandeurs à relever. Les changements d'annotation ont été identifiés par le QG dans les sorties complètes de l'archive. Toute demande de diagnostic portant sur des cas certifiés doit désormais inclure l'annotation de branche et les grandeurs des critères V7 correspondants.

---

*Décision QG (CONV-C) — MEPA V7.0 — 2026-10-02*
