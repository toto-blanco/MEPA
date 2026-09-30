# MEPA — Décision QG sur la proposition ARCH-AG-01 rev. 0

| Champ | Valeur |
|---|---|
| Statut | **Décision QG** — adoption partielle, rev. 1 demandée |
| Objet | Proposition d'architecture agentique `MEPA_ARCH-AG-01_Architecture_Agentique_rev0.md` |
| Rôle | QG / CONV-C (Architecte Scientifique) — décision prise par Antoine |
| Date | 2026-09-29 |
| Références | Décision V7-D1 rev. 4 · CV15 Option C · CV16 (non formalisée) · Certification V7.0 cluster pilote V7-γ rev. 2 · audit technique CTO post-certification |

---

## 1. Verdict

ARCH-AG-01 identifie le bon goulot (relais manuel entre conversations) et reprend fidèlement les décisions en vigueur : déterminisme au centre, Hermes limité à la couche opérationnelle, `resolution_detail` explicite, gel des entrées résolues.

Le document n'est **pas adopté en bloc**. Il contient une contradiction interne, deux changements de protocole présentés comme des évolutions techniques, et un oubli sur le chemin critique. Les phases 0 et 1 sont engagées ; les phases 2 à 4 attendent une rev. 1.

---

## 2. Éléments retenus

- **`context_manifest`** : la pré-registration devient prouvable et non plus seulement déclarée. Retenu comme principe.
- **Schéma `resolution_detail`** à règles fermées, avec validation bloquante contre `mepa_whitelist_keys.json`. Retenu.
- **Vérificateur numérique** du rapport S1–S7, rapprochement déterministe, toute valeur non rapprochée bloquante. Retenu.
- **Gel en porte H1, avant simulation.** Cette formulation améliore celle envisagée jusqu'ici pour CV16 (gel à la certification) : figer les entrées avant d'observer la trajectoire est une garantie anti-rationalisation par construction. Retenu pour CV16.
- **Contradicteur** (red team systématique avant décision). Retenu pour la phase 4.

---

## 3. Corrections exigées pour la rev. 1

### C-1 — Contradiction D-2 / D-3

D-2 constate que le Nœud 8d est inerte (`scores_resolus` toujours vide). D-3 affirme que la résolution CONV-B se propage via 8d vers `y0` / `cmd_base`. Les deux ne peuvent pas être vrais simultanément. L'origine réelle des écarts fiche → passeport sur E / Rc / γ / L0 est donc **inconnue**.

**Exigence :** tracer le point exact où ces quatre variables sont modifiées entre la fiche CONV-E et le passeport. Ce traçage devient **prérequis bloquant de la phase 2**. On ne remplace pas un mécanisme dont le comportement réel n'est pas établi.

### C-2 — Pare-feu et pré-registration QG

MEPA pratique deux formes de pré-registration distinctes :
- le **codage aveugle** : le codeur ignore la trajectoire attendue ;
- la **fixation préalable de valeurs par le QG** : D1 rev. 4 §5 fixe Ψ_noyau = 0.01 et Φ = 0.30 pour WP-I4-1 avant tout test.

Le pare-feu tel que rédigé (§7) interdirait les secondes. Or elles sont aujourd'hui transmises au codeur, et la fiche V7 Allemagne mentionne explicitement l'échec attendu sur C2.

**Exigence :** distinguer dans les schémas deux catégories.
- **Valeurs codées** : produites en aveugle, soumises au pare-feu, incluses dans le κ / CCI.
- **Valeurs pré-enregistrées QG** : injectées après le codage par l'orchestrateur, marquées comme telles dans la fiche et le passeport, exclues du κ / CCI, référencées à la décision qui les fixe.

### C-3 — Le Documentaliste est un changement de protocole

Si les Codeurs E et B travaillent sur un même `dossier_sources`, le κ mesure la fiabilité du codage **à sources données**, et non plus la fiabilité du jugement historique complet, sélection des sources comprise. C'est un construit légitime mais différent de celui sous lequel le cluster pilote a été certifié : la comparabilité est rompue.

Deux conséquences supplémentaires :
- une entrée commune **corrèle** les codeurs, ce qui aggrave D-7 au lieu de le traiter ;
- la **sélection** des extraits par un agent qui connaît l'issue historique est le point d'entrée principal de la rationalisation. La nuance du §5.1 couvre les faits, pas le choix des faits.

**Exigence :** requalifier le Documentaliste comme changement de protocole soumis à décision CV. Si retenu : contrôle de la sélection (audit ou contradiction du dossier) et re-baseline explicite.

### C-4 — Critère d'acceptation de la phase 2

Rejouer WP-C1-1 avec la fiche gelée produit nécessairement des blocs bit-identiques, le runner étant déterministe. Ce critère valide le mécanisme de gel, pas la nouvelle chaîne Codeurs → Arbitre.

**Exigence :** ajouter un critère portant sur la chaîne complète — nouvelle exécution depuis le codage sur au moins un WP pilote, comparaison de la fiche résolue obtenue avec la fiche certifiée, et **seuil d'écart acceptable déclaré avant l'essai**.

### C-5 — Gate V7.1 omis

La phase 4 enchaîne sur les 21 WP restants sans mentionner que D1 rev. 4 §5.2 conditionne leur simulation à V7.1 (score continu d'activation α, création de WP-I11-1 Grande Terreur soviétique), gate repris par CV15 en T2-B.

**Exigence :** intégrer ce gate à la feuille de route.

---

## 4. Décisions sur Q-1 à Q-6

| # | Décision | Conditions |
|---|---|---|
| **Q-1** | **Adopté avec amendements** — principes P-1 à P-5 retenus, phases 0 et 1 engagées | La Sentinelle s'exécute là où les commits sont faits (poste local ou CI GitHub), pas sur le Pi. Elle réutilise les Contrôles A (`mepa_deploy_check.py`) et B (`mepa_consistency_check.py`) sans les dupliquer. |
| **Q-2** | **Option A amendée** — `resolution_detail` et gel en H1 relèvent d'une décision CV16 unique | (i) C-1 résolu au préalable. (ii) Arbitrage **déterministe par défaut** (`accord`, `moyenne` sous les seuils de `mepa_constants.json`). L'Arbitre LLM n'intervient que pour proposer une justification sur les cas `escalade_humain`, tranchés par Antoine en H1. (iii) Toute modification après H1 ouvre une nouvelle passe tracée ; aucune réécriture d'un artefact gelé. |
| **Q-3** | **Option B d'abord, A ensuite** | Après réécriture selon C-2. Les 6 pilotes restent certifiés sous le protocole en vigueur à leur certification ; le passeport porte désormais la version de protocole. |
| **Q-4** | **Option C adoptée** | Troisième codeur d'une autre famille, hors certification, pour mesurer le biais corrélé. Décision A/B ultérieure sur données. Provenance du modèle enregistrée **par nœud** dans le passeport. |
| **Q-5** | **Non tranché par le QG — renvoyé au CTO** | Le choix de l'outil d'orchestration relève du CTO, déjà mandaté pour la proposition d'architecture finale. ARCH-AG-01 lui est transmis comme intrant. Le QG fixe les contraintes (invariants I-1 à I-6, trois portes humaines, pare-feu selon C-2) ; le CTO choisit et chiffre le risque de régression d'une éventuelle réécriture du workflow V7. |
| **Q-6** | **Option C — reporté** | Subordonné à la décision sur le Documentaliste (C-3). En cas de reprise : vérifier la présence de variables d'issue des campagnes dans NAVCO et imposer une liste blanche de champs excluant toute variable d'issue. |

---

## 5. Mises à jour de l'Annexe A

1. **Libellé du Nœud 2** — clos. Le CTO a vérifié que le code embarqué est `mepa_node2_audit_v7.js` v3.0.0 (C14/C15 actifs) et a corrigé le libellé.
2. **Contrat 8c → 8d** — élargi et rendu bloquant : voir C-1.
3. **T6** (`mepa_test_rampe_segmentation.py`) — à confirmer sur `main`.
4. **CV16** — non formalisée à ce jour. Sera rédigée après résolution de C-1, en intégrant le gel en H1 et `resolution_detail` (Q-2).

---

## 6. Suites

| Action | Porteur | Condition |
|---|---|---|
| Phase 0 (bus, schémas, tableau généré) | CTO | Engagée |
| Phase 1 (Sentinelle CI) | CTO | Engagée, conditions Q-1 |
| Traçage des écarts E / Rc / γ / L0 (C-1) | CTO | Prérequis phase 2 |
| Intégration d'ARCH-AG-01 dans la proposition d'architecture finale | CTO | Contraintes Q-5 |
| Rev. 1 d'ARCH-AG-01 intégrant C-1 à C-5 | Auteur du document | Avant toute décision sur les phases 2–4 |
| Rédaction de CV16 | QG | Après C-1 |

---

*Décision QG (CONV-C) — MEPA V7.0 — 2026-09-29*
