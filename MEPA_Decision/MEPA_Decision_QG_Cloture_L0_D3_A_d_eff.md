# MEPA — Décision QG : contrôle L0 Rwanda · fin de D3 · A_d_eff non simulé

| Champ | Valeur |
|---|---|
| Statut | **Décision QG** |
| Rôle | QG / CONV-C (Architecte Scientifique) — décision prise par Antoine |
| Date | 2026-09-30 |
| Base factuelle | Retour CTO du 2026-09-30 (contrôle L0, recensement D3) ; vérification QG sur les fiches V7, les 6 `result.json` de juin 2026 et `mepa_node2_audit_v7.js` |
| Références | `MEPA_Decision_QG_Levee_Reserve_Rwanda_Accord.md` (§2.5) · Erratum Certification V7.0 · Décision D3 · CV15 (T2-A) · CV16 (à rédiger) |

---

## 1. Contrôle résiduel L0 sur Rwanda — réussi

**Critère pré-enregistré (§2.5 de la décision précédente) :** runner seul, entrées certifiées du 19 juin, `y0[1] = 0.10` ; réussi si la trajectoire reste (α) et si `C_max > 0.30`.

**Vérification préalable :** à `L0 = 0.12`, l'exécution reproduit au bit près le run certifié sur les 9 blocs de sortie.

| | L0 = 0.12 (certifié) | L0 = 0.10 |
|---|---|---|
| Trajectoire | (α) | (α) |
| `C_max` | 1.6587 | 1.6572 |
| `t_bascule` | 7 | 7 |
| `FR_max` | 1.7601 | 1.7588 |
| Précheck α | satisfait | satisfait |
| Stress N1 / N2 | tout en (α) | tout en (α) |

**Décision :** contrôle réussi. La certification (α) de WP-I10-1 Rwanda est confirmée sur C4 (décision précédente) et sur L0 (présente décision).

---

## 2. Fin de la décision D3 — retrait des derniers champs `kappa`

Deux résidus relèvent de la règle posée en D3 (aucun champ ne porte le nom de kappa s'il ne s'agit pas d'un κ de Cohen) :
- le calculateur émet un champ `kappa`, alias du CCI ;
- le Nœud 7 propage un champ `kappa` qu'aucun nœud ne produit.

**Décision :** option A. Retrait de l'alias dans `mepa_kappa_calculator.py`, de la ligne de repli correspondante dans `mepa_passeport_schema.py` et de la ligne du Nœud 7, **dans le même déploiement** que le renommage `accord_sa` / `accord_m_r`, avec un seul run de validation. D3 est clos après ce déploiement.

---

## 3. `A_d_eff` est audité mais pas simulé

### 3.1 Constat

| WP | `A_d_eff` codé (juin, rapport S1) | `R` simulé (juin) | `R` pré-rempli dans la fiche |
|---|---|---|---|
| WP-I10-1 Rwanda | 1.5 | 0.15 | 0.15 |
| WP-I4-1 Allemagne | 2.5 | 0.30 | 0.30 |
| WP-F10-1 Commune | à relever | 0.20 | 0.20 |
| WP-F1-1 Rome IIIe | 4.5 | 0.30 | 0.30 |
| WP-C1-1 Haïti | 1.4 | 0.15 | 0.15 |
| WP-C2-1 Égypte | 3.8 | 0.25 | 0.25 |

- La fiche V7 laisse `variables.A_d_eff` à `null` ; CONV-E le code au run.
- `mepa_node2_audit_v7.js` transmet `A_d_eff` à l'audit CCI (l. 901) et documente le mapping « `A_d_eff` → R » (contrôle C9b).
- Mais `R` est exclu des commandes que CONV-E peut réécrire (`CMD_MAPPING_LIBRE`). Le `R` simulé est, sur 6/6 pilotes, la valeur pré-remplie de la fiche.
- Le LLM propose la conversion (Égypte : R = 0.38, soit 3.8 / 10) ; le pipeline ne l'applique pas.

Le mapping « `A_d_eff` → R » annoncé par le contrôle C9b n'a jamais été implémenté. La variable `A_d_eff` entre dans le CCI, donc dans le gate de certification, sans entrer dans la simulation.

### 3.2 Portée

- Aucune trajectoire, aucun verdict ni aucun statut des pilotes n'est modifié par ce constat. Le gate a été appliqué aux valeurs réellement produites.
- Le constat s'ajoute au point 2.4 de l'erratum (concordance audit / simulation non garantie), sous une forme plus nette : sur `A_d_eff`, la variable auditée n'est pas la variable simulée.

---

## 4. Retrait de la série advisory de T2-A

Le module `mepa_dev1_advisory_v7.py` compare au plafond `A_d_max` dérivé une valeur qu'il nomme `R_code_A_d_eff`, lue dans `cmd.R` et supposée exprimée sur l'échelle [0, 10]. Il lit en réalité la valeur pré-remplie de la fiche, qui n'est ni le codage de `A_d_eff` ni exprimée sur cette échelle.

**Décision :**
- La **série de calibration advisory produite en T2-A** (6 WP pilotes) est **retirée**. Aucun de ses drapeaux n'est exploitable, y compris le drapeau Allemagne à `t_max` signalé pour CV9.
- L'affirmation du QG selon laquelle T2-A était complet est corrigée : la greffe technique (Ω ≡ I(t), non-régression, capture dans le passeport) reste acquise ; la série de données ne l'est pas.
- Avec les valeurs de `A_d_eff` réellement codées, les drapeaux de Haïti, Rome et Égypte basculeraient : l'écart n'est pas marginal.
- Aucun effet sur la certification : l'advisory est non calibré et non bloquant.
- L'advisory lira la valeur codée de `A_d_eff` une fois la source unique audit / simulation en place (CV16). D'ici là, aucune série advisory n'est exploitable pour CV9.

---

## 5. Diagnostic pré-enregistré — sensibilité des pilotes à R

**Objet :** mesurer si les trajectoires certifiées dépendent de la valeur pré-remplie de `R` plutôt que du codage de `A_d_eff`.

**Mesure :**
- runner seul (`mepa_runner_v3_v7.py`), sans LLM ni passeport, vraies constantes ;
- entrées : `result.json` de juin de chacun des 6 WP pilotes ;
- vérification préalable : à `R` d'origine, reproduction au bit près du run certifié ;
- variation unique : `R = A_d_eff / 10`, avec `A_d_eff` relevé dans le tableau S1 du rapport de juin de chaque WP. La division par 10 est une **conversion provisoire**, retenue pour ce diagnostic seulement ; la règle définitive relève de CV16.

**Relevé :** trajectoire, robustesse N1, stress N1 et N2, `C_max`, `FR_max`, `t_bascule`, pour chaque WP.

**Critère :** diagnostic sans conséquence automatique. Toute trajectoire qui change est documentée et examinée dans CV16. Aucun statut de certification n'est modifié par ce diagnostic.

**Cas à surveiller :** WP-F1-1 Rome (R 0.30 → 0.45) et WP-C2-1 Égypte (R 0.25 → 0.38). Tous deux sont MÉTASTABLES, et l'écart dépasse la plage des stress-tests existants (±0.08).

---

## 6. Intrants versés au dossier CV16

- **Conversion `A_d_eff` → R** : règle de conversion à proposer par le CTO dans la spécification de la source unique, à trancher par le QG.
- **Désaccord sur Sa impliquant la valeur 7** : Sa = 7 est la seule valeur qui modifie la simulation (p6 × 1.5). Un désaccord entre codeurs portant sur cette valeur change l'entrée simulée ; son traitement (signal, blocage ou résolution) est à définir.
- **README public** : la ligne présentant `A_d_eff` sous la clé `R (cmd)` sera corrigée avec CV16, pour éviter plusieurs révisions successives.

---

## 7. Suites

| Action | Porteur |
|---|---|
| Déploiement groupé : renommage `accord_sa` / `accord_m_r`, retrait de `SEUIL_KAPPA_SA`, retrait des résidus `kappa` (option A) | CTO |
| Diagnostic de sensibilité à R sur les 6 pilotes (§5) — sortie brute | CTO |
| Spécification de la source unique, incluant la conversion `A_d_eff` → R | CTO |
| Rédaction de CV16 | QG — après réception de la spécification et du diagnostic |

---

*Décision QG (CONV-C) — MEPA V7.0 — 2026-09-30*
