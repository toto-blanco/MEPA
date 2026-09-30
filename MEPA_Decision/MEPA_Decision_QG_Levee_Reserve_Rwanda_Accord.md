# MEPA — Décision QG : levée de la réserve Rwanda · indicateurs d'accord · protocole V7.0-P2

| Champ | Valeur |
|---|---|
| Statut | **Décision QG** |
| Rôle | QG / CONV-C (Architecte Scientifique) — décision prise par Antoine |
| Date | 2026-09-30 |
| Base factuelle | Retour groupé CTO du 2026-09-30 (actions de l'erratum §5.1 et mesure pré-enregistrée §4.3) |
| Références | `MEPA_Erratum_Certification_V7_Provenance_Reserve_Rwanda.md` · Certification V7.0 · Décision QG ARCH-AG-01 rev. 0 · Décision D3 (nommage des indicateurs κ) |

---

## 1. Actions de l'erratum §5.1 — validées

| Action | Statut |
|---|---|
| `temperature: 0` transmis sur CONV-E, 8a, 6b et 13 | Fait |
| Provenance LLM enregistrée par nœud, lue sur la requête réellement sérialisée | Fait (`provenance_llm_par_noeud`) |
| Valeur de température écrite en dur supprimée du schéma passeport | Fait |
| Sortie brute CONV-E archivée, chemin et sha256 inscrits au passeport | Fait (`{wp_id}_conv_e_raw.json`) |
| Version de protocole inscrite au passeport | Fait |

Versions déployées : `mepa_passeport_schema.py` v3.0.4, `mepa_node2_audit_v7.js` v3.0.1 (aucun contrôle C1–C15 modifié), manifeste DEP3 régénéré, préflight bloquant passé.

**Libellés de protocole adoptés :**
- **V7.0-P1** : protocole sous lequel les 6 WP pilotes ont été certifiés (température non transmise sur quatre nœuds, sortie CONV-E non archivée).
- **V7.0-P2** : protocole en vigueur à compter du 2026-09-30.

---

## 2. Levée de la réserve sur WP-I10-1 Rwanda

### 2.1 Critère pré-enregistré (erratum §4.3)

Au moins 3 recodages indépendants de WP-I10-1 par CONV-E, sous protocole corrigé, hors certification. Levée si tous les recodages produisent `A_r_c > 0.65`.

### 2.2 Résultats

| | run 1 | run 2 | run 3 |
|---|---|---|---|
| `variables_codees.A_r_c` | 0.9 | 0.9 | 0.9 |
| `commandes_mises_a_jour.Rc` | 0.9 | 0.9 | 0.9 |
| `temperature_transmise` | 0 | 0 | 0 |
| Modèle servi | claude-sonnet-4-6 | claude-sonnet-4-6 | claude-sonnet-4-6 |

Conditions : sous-workflow isolé `mepa_workflow_n8n_V7_mesure_conv_e.json`, nœud CONV-E identique au workflow principal, fiche inchangée avant et après les 3 exécutions (sha256 vérifié), aucune écriture hors `outputs/mesures/`.

### 2.3 Décision

**Le critère est satisfait. La réserve est levée.** WP-I10-1 Rwanda est certifié (α) sans réserve.

### 2.4 Portée de la mesure

À température 0, les trois exécutions ne sont pas des tirages indépendants au sens statistique : elles établissent la **stabilité** du codage sous le protocole V7.0-P2, non sa robustesse face à un autre codeur. Deux éléments renforcent le résultat :
- les textes produits diffèrent d'un run à l'autre (8 846, 8 680 et 8 397 caractères) alors que `A_r_c` reste à 0.9 ;
- avec les exécutions de juin et de juillet, faites à la température par défaut de l'API, on dispose de **5 observations sur 5 à 0.9**, dont 2 issues d'un échantillonnage réellement aléatoire.

La robustesse face à un codeur d'une autre famille de modèles relève de la mesure Q-4 (Décision QG ARCH-AG-01).

### 2.5 Contrôle résiduel — L0 (pré-enregistré)

Au run 3, `L_t` = `L0` vaut 0.10 (0.12 aux runs 1 et 2 et au run de certification). L0 n'entre pas dans le précheck C1–C4, mais il agit sur F(t), donc sur C5 et sur la trajectoire simulée. Aucun stress-test ne le fait varier.

- **Mesure :** exécution du seul runner (`mepa_runner_v3_v7.py`), sans LLM ni passeport, sur les entrées certifiées de WP-I10-1 (`result.json` du 19 juin 2026) avec `y0[1] = 0.10`, toutes autres entrées identiques.
- **Critère :** contrôle réussi si la trajectoire reste (α) et si C5 est satisfaite (`C_max > 0.30`).
- **Si échec :** sensibilité à L0 documentée et statut de Rwanda réexaminé par décision CV.

Ce contrôle ne conditionne pas la levée de la réserve C4, qui porte sur une autre variable.

---

## 3. Fait établi pour CV16

La température 0 **ne rend pas** le codage CONV-E reproductible :
- les textes produits varient d'un run à l'autre ;
- `L_t` varie sur Rwanda (0.12 / 0.12 / 0.10) ;
- `Rc` Égypte vaut 0.55 dans la fiche, 0.62 aux runs de juin et du 3 juillet, 0.60 au run du 30 septembre.

La température 0 réduit la variance sans l'éliminer. **Le gel des entrées en porte H1 est donc indispensable**, et c'est désormais établi sur données archivées.

Deux autres faits versés au dossier CV16 :
- au run Égypte du 30 septembre, les deux sorties du codeur concordent (`A_r_c` = `Rc` = 0.60, `E_split` = `E` = 0.65, γ = 0.48, `L_t` = `L0` = 0.28) : c'est la première observation archivée des deux sorties côte à côte ;
- le prompt CONV-E demande des valeurs de R et Mob que le pipeline n'applique pas (`CMD_MAPPING_LIBRE`). Le périmètre de la source unique audit / simulation doit inclure la suppression de ces demandes.

---

## 4. Indicateurs d'accord `accord_sa` et `accord_m_r`

### 4.1 Constat

Les champs `kappa_sa` et `kappa_m_r` produits par `mepa_kappa_calculator.py` valent 1.0 si les deux codeurs ont retenu la même valeur sur le WP, 0.0 sinon. Un κ de Cohen n'est pas calculable sur un cas unique. Le seuil `SEUIL_KAPPA_SA` (0.70) n'intervient dans aucun verdict, alors que le contrôle de cohérence des seuils le vérifie.

### 4.2 Décision

- Les champs sont **renommés `accord_sa` et `accord_m_r`**, et documentés comme indicateurs d'accord binaires calculés sur un seul WP. Application de la règle posée en D3 : aucun champ ne porte le nom de kappa s'il ne s'agit pas d'un κ de Cohen.
- `SEUIL_KAPPA_SA` est **retiré** du calculateur, de `mepa_constants.json` et du contrôle de cohérence des seuils. Un contrôle portant sur un seuil sans effet donne une fausse assurance.
- Le **κ de Cohen** sur Sa et M_r sera calculé au niveau du corpus, comme diagnostic, lorsque le bus d'artefacts de la phase 0 sera en place. Son seuil éventuel sera décidé au vu de la série, pas avant.
- Les **passeports pilotes** ne sont pas concernés : ces champs y valaient `null`.
- Le constat Égypte reste valable sur le fond : les deux codeurs ont retenu des valeurs de Sa différentes. Seul le nom de l'indicateur était inexact.

---

## 5. Suites

| Action | Porteur |
|---|---|
| Contrôle résiduel L0 sur Rwanda (§2.5) | CTO |
| Renommage `accord_sa` / `accord_m_r` ; retrait de `SEUIL_KAPPA_SA` (calculateur, constantes, contrôle de cohérence) | CTO |
| Spécification technique de la source unique audit / simulation, intrant de CV16 | CTO |
| Phases 0 et 1 d'ARCH-AG-01 ; proposition d'architecture finale (Q-5, Option B) | CTO |
| Correction du README public (mentions κ, versions, provenance) | QG — livrée avec cette décision |
| Rédaction de CV16 | QG — après réception de la spécification |

---

*Décision QG (CONV-C) — MEPA V7.0 — 2026-09-30*
