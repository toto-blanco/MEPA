# MEPA V7 — Modèle Énergétique du Potentiel Adaptatif

> Simulation des transitions socio-institutionnelles sur 27 cas historiques via équations différentielles couplées, pipeline n8n automatisé, audit inter-codeurs (κ de Cohen / CCI), et modélisation conditionnelle du mécanisme sacrificiel (extension Todd-Girard).

**Statut : cluster pilote V7-γ rev. 2 certifié (6 WP). Pipeline V7 opérationnel. Extension au corpus complet (21 WP restants) en préparation.**

---

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [État du projet](#état-du-projet)
3. [Architecture du projet](#architecture-du-projet)
4. [Corpus historique (27 WP)](#corpus-historique-27-wp)
5. [Cadre théorique](#cadre-théorique)
6. [Pipeline technique](#pipeline-technique)
7. [Structure des fichiers](#structure-des-fichiers)
8. [Installation et utilisation](#installation-et-utilisation)
9. [Format d'entrée — Fiche WP](#format-dentrée--fiche-wp)
10. [Trajectoires diagnostiquées](#trajectoires-diagnostiquées)
11. [Contrôle qualité et gouvernance](#contrôle-qualité-et-gouvernance)
12. [Feuille de route](#feuille-de-route)
13. [Références](#références)
14. [Licence](#licence)

---

## Vue d'ensemble

**MEPA** (Modèle Énergétique du Potentiel Adaptatif) est un cadre de modélisation quantitatif-qualitatif conçu pour analyser les **transitions socio-institutionnelles** à travers l'histoire. Le modèle postule que tout système socio-politique bascule lorsque la force transformatrice `F(t)` dépasse la résistance du système `R(t)`.

Le projet couvre **27 Working Papers (WP)** répartis sur cinq clusters thématiques, de la Rome du IIIe siècle au Rwanda contemporain, en passant par la Révolution française, la montée du nazisme ou l'effondrement de l'URSS.

Depuis la version V7 (extension Todd-Girard, cadre V7-α rev. 2.1), le modèle intègre en plus un mécanisme conditionnel de **cristallisation sacrificielle d'État** — la trajectoire où l'État organise une partie de la société contre une autre partie publiquement désignée, distincte analytiquement de la répression classique.

### Deux composantes complémentaires

| Composante | Rôle | Outils |
|---|---|---|
| **MEPA Full** | Codage qualitatif de 9 variables historiques (V6.2) + 6 variables V7 (Todd-Girard) sur sources documentées | Fiches JSON, audit inter-codeurs |
| **MEPA Lite** | Simulation numérique de 4 équations différentielles couplées | `mepa_runner_v3_v7.py` (LSODA), n8n |

---

## État du projet

La **certification V7.0 du cluster pilote V7-γ rev. 2** a été prononcée sur 6 WP (Rwanda, Allemagne nazie, Commune de Paris, Rome IIIe siècle, Haïti, Égypte 2011), contre les 6 conditions de la Décision de gouvernance V7-D1 rev. 4 §4 :

| Cas | Trajectoire diagnostiquée | Concordance | Statut |
|---|---|---|---|
| WP-I10-1 Rwanda | (α) Cristallisation sacrificielle | ✓ | CERTIFIÉ |
| WP-I4-1 Allemagne nazie | (b) Répression réussie | Divergence attendue* | CONDITIONNELLE_V7 |
| WP-F10-1 Commune de Paris | (b) Répression réussie | Contrôle négatif ✓ | CERTIFIÉ |
| WP-F1-1 Rome IIIe s. | (d) Effondrement progressif | ✓ | CERTIFIÉ_MÉTASTABLE |
| WP-C1-1 Haïti | (d) Effondrement progressif | ✓ | CERTIFIÉ |
| WP-C2-1 Égypte 2011 | (b) Répression réussie | ✓ | CERTIFIÉ_MÉTASTABLE |

\* *Allemagne nazie n'atteint pas la trajectoire (α) attendue — échec pré-enregistré de la condition C2 du précheck sacrificiel (masse critique du noyau formel insuffisante), documenté comme limite assumée du cadre V7-α et traité selon le protocole anti-rationalisation V7-C3 (Réserves 1 et 2 du §4bis de la Décision V7-D1 rev. 4).*

Ce résultat déverrouille l'extension du pipeline aux 21 WP restants du corpus, sous réserve de garde-fous de fiabilité mis en place lors de l'audit technique post-certification (voir [Contrôle qualité et gouvernance](#contrôle-qualité-et-gouvernance)).

---

## Architecture du projet

```
┌───────────────────────────────────────────────────────────────────────┐
│  Fiche WP (JSON)  →  Audit conformité (C1–C15)  →  Runner (ODE LSODA) │
│                                              →  CONV-B Temps 1 (CCI)   │
│                                              →  Rédaction LLM (S1→S7)  │
│                                              →  CONV-B Temps 2 (audit) │
│                                              →  Certification (cci_global)│
│                                              →  Passeport WP archivé   │
│                                              →  Export / Méta-analyse  │
└───────────────────────────────────────────────────────────────────────┘
```

Le pipeline est orchestré via **n8n**. Deux workflows coexistent :

- `mepa_workflow_n8n_V7.json` — pipeline complet (codage → simulation → audit → certification → archivage)
- `mepa_workflow_n8n_V7_audit_seul.json` — sous-workflow isolé permettant de relancer l'audit CONV-B sur un rapport corrigé, sans ré-exécuter la simulation ni le codage

Le runner V6.2 (`mepa_runner_v2_gamma.py`, intégration Euler dt=1) reste disponible pour comparaison de non-régression avec le runner V7 (`mepa_runner_v3_v7.py`, intégration LSODA adaptative).

---

## Corpus historique (27 WP)

### Cluster C1 — Crises contemporaines (6 WP)
| WP | Cas | Période | Trajectoire attendue | Fiche V7 |
|---|---|---|---|---|
| WP-C1-1 | Haïti | 2010–2024 | (d) Effondrement progressif | ✓ certifié |
| WP-C2-1 | Égypte 2011 | 2010–2014 | (b) Répression réussie | ✓ certifié |
| WP-C3-1 | Argentine | 1998–2003 | (a) Rupture transformatrice | — |
| WP-C4-1 | Liban | 2019–2023 | (d) Effondrement progressif | — |
| WP-C5-1 | Iran | 2009–2022 | (b) Répression réussie | — |
| WP-C6-1 | Chine (Xi) | 2012–2023 | (b) Répression réussie | — |

### Cluster C2 — Fondements / Effondrements historiques (10 WP)
| WP | Cas | Trajectoire attendue | Fiche V7 |
|---|---|---|---|
| WP-F1-1 | Rome IIIe s. | (d) Effondrement progressif | ✓ certifié |
| WP-F2-1 | Rome tardive | (d) Effondrement progressif | — |
| WP-F3-1 | Maya classique | (d) Effondrement progressif | — |
| WP-F4-1 | Égypte ancienne | (c) Stase / ambigu | — |
| WP-F5-1 | Venise déclin | (d) Effondrement progressif | — |
| WP-F6-1 | Empire ottoman | (d) Effondrement progressif | — |
| WP-F7-1 | Révolution haïtienne | (a) Rupture transformatrice | — |
| WP-F8-1 | France révolutionnaire | (a) Rupture transformatrice | — |
| WP-F9-1 | Angleterre stabilité | (h) Stabilité | — |
| WP-F10-1 | Commune de Paris | (a) attendue / (b) diagnostiquée — contrôle négatif α | ✓ certifié |

### Cluster C3 — Industrialisation & Ruptures (10 WP)
| WP | Cas | Trajectoire attendue | Fiche V7 |
|---|---|---|---|
| WP-I1-1 | Angleterre industrielle | (h) Stabilité | — |
| WP-I2-1 | Russie 1917 | (a) Rupture transformatrice | — |
| WP-I3-1 | Japon Meiji-Guerre *(Sa=7)* | (a)→(e)→(h)→(d) | — |
| WP-I4-1 | Allemagne nazie *(Sa=7)* | (α) attendue / (b) diagnostiquée — divergence assumée | ✓ certifié conditionnel |
| WP-I5-1 | Espagne Guerre civile | (a) Rupture transformatrice | — |
| WP-I6-1 | Tiananmen | (b) Répression réussie | — |
| WP-I7-1 | URSS | (d) Effondrement progressif | — |
| WP-I8-1 | Chine Deng | (e)→(h) | — |
| WP-I9-1 | Singapour *(Sa=7)* | (h) Stabilité | — |
| WP-I10-1 | Rwanda | (α) Cristallisation sacrificielle d'État | ✓ certifié |

### Cluster C4 — Transitions (1 WP)
| WP | Cas | Trajectoire attendue |
|---|---|---|
| WP-T1-1 | Guerre de Sécession | (a) Rupture transformatrice |

### Étalon (hors corpus principal)
| WP | Cas | Note |
|---|---|---|
| WP-EXT-5 | Islande 2008–2013 | Ancre MAX EROI=35.0 |

### Cas prévu — chantier V7.1
| WP | Cas | Rôle |
|---|---|---|
| WP-I11-1 *(à créer)* | Grande Terreur soviétique 1937-1938 | Troisième cas positif (α), requis pour la calibration du score continu d'activation sacrificielle (Décision V7-D1 rev. 4 §6) |

---

## Cadre théorique

### Variables d'état (MEPA Lite)

| Variable | Signification |
|---|---|
| `S` | Pression sociale |
| `L` | Chaleur latente (légitimité) |
| `C` | Chaleur collective (capital social) |
| `I` | Complexité institutionnelle |

### Équations différentielles

```
dS = p1·T − p2·(R + Ref + Mob) − p2b·S
dL = p4·S − L − p3·L·Θ
dC = p5·M − p6·C − p7·(Rc + Rn)·ℓ·gC
dI = p8·(EROI − 1)·Pop − p9·I

F(t) = C + λ·L·(1 + μ·γ·E)
R(t) = I^(1/3) + ν·(Rc + Rn)·ℓ + ρ

Condition de bascule : F(t) ≥ R(t)
```

Runner V7 : intégration LSODA (`scipy.solve_ivp`, rtol=1e-6, atol=1e-9). Runner V6.2 conservé pour non-régression : intégration Euler explicite dt=1.

### Variables de commande — socle V6.2 (9 variables)

| Symbole | Clé JSON | Échelle | Description |
|---|---|---|---|
| E_split | `E` (cmd) | [0,1] | Part des élites marginalisées |
| **γ** | `gamma` | [0,1] | Capacité organisationnelle de l'élite (globale) |
| A_d_eff | `R` (cmd) | [0,10] | Capacité redistributive effective |
| A_r_c | `Rc` | [0,1] | Répression classique |
| A_r_ne | `Rn` | [0,1] | Répression numérique / non-étatique |
| Cs | — | [0,1] | Crédibilité du régime |
| L(t) | `L` (y0) | [0,1] | Loyauté des appareils |
| EROI | `EROI` | >1 | Rendement énergétique net |
| Sa | `sa` | {2,4,6,7} | Structure anthropologique Todd |

> **Règle de nomenclature absolue :** `gamma` est la clé JSON/Python exclusive du paramètre γ. La lettre `g` isolée est interdite dans tout contexte MEPA.

### Extension V7 — variables Todd-Girard (6 variables supplémentaires)

| Symbole | Clé JSON | Échelle | Description |
|---|---|---|---|
| M_r | `m_r` | {1,2,3} | Stade de la matrice religieuse Todd (1 = active, 2 = zombie, 3 = zéro) |
| μ_m | `mu_m` | [0,1] | Polarisation mimétique girardienne |
| Φ | `phi` | [0,1] | Fragmentation symbolique de l'espace médiatique |
| Ψ_noyau | `psi_noyau` | [0,1] | Proportion de population engagée dans le noyau de croyance cohérent |
| Ψ_cible | `psi_cible` | [0,1] ou `null` | Proportion de population désignée comme cible démographique |
| γ_local | `gamma_local` | [0,1] | Capacité organisationnelle propre du noyau (distincte de γ, capacité moyenne de l'élite globale) |

> **Distinction impérative** : `gamma` (γ, cohésion de l'élite globale, V6.2) et `gamma_local` (γ_local, discipline du seul noyau organisé, V7) mesurent des objets différents et peuvent diverger fortement pour un même cas (ex. Rwanda : γ ≈ 0.55, γ_local ≈ 0.55 par coïncidence numérique documentée ; Allemagne : γ_local = γ = 0.55 également, distinction conceptuelle maintenue). De même, `mu` (μ, amplification γ-élite dans F(t)) est distincte de `mu_m` (μ_m, polarisation mimétique).

### Précheck de la branche sacrificielle (α)

Quatre conditions doivent être simultanément satisfaites pour que la trajectoire (α) soit évaluable :

```
C1 = (M_r ∈ {1,2}) AND (μ_m > μ_m* = 0.60)
C2 = (Ψ_noyau × γ_local > σ(Φ))         où σ(Φ) = σ_base × (1 + α × Φ), σ_base = 0.018, α = 1.7
C3 = (Ψ_cible ≠ null)
C4 = (A_r_c_eff > 0.70)                  où A_r_c_eff = A_r_c + 0.5 × A_r_ne (clause de repli si A_r_c ≤ 0.70)
```

Si `alpha_precheck = C1 AND C2 AND C3 AND C4` est faux, la branche (α) est exclue avant simulation et le système retombe sur l'arbre de décision V6.2 standard.

> **Statut épistémologique** : les valeurs numériques du mécanisme sacrificiel (σ_base, α, seuil μ_m*, modulateurs de la rampe en trois phases) sont calibrées sur un nombre restreint de cas actifs (Rwanda, Égypte) et explicitement documentées comme hyperparamètres V7-α à confirmer — non comme constantes établies. Voir cadre théorique V7-α rev. 2.1 pour le détail des intervalles plausibles et le plan de validation.

### Modulateur Todd (Sa)

| Sa | Type familial | Effet sur le modèle |
|---|---|---|
| 2 | Nucléaire absolu (monde anglo-saxon) | Instabilité haute |
| 4 | Nucléaire égalitaire (France, Amérique latine) | Instabilité chronique |
| 6 | Communautaire (Russie, Chine, Iran) | Résilience autoritaire |
| **7** | **Souche (Allemagne, Japon, Corée)** | **p6 × 1.5 obligatoire** |

---

## Pipeline technique

### Flux V7 (résumé des nœuds n8n clés)

```
Nœud 1   → Audit & Conformité structurelle       [mepa_node2_audit_v7.js]
Nœud 4   → Execute Runner                        [mepa_runner_v3_v7.py]
Nœud 6   → Rédaction LLM CONV-A (S1→S7)
Nœud 6b  → CONV-B Temps 2 — Audit final C1–C6    [mepa_node2_audit_v7.js]
Nœud 8a  → CONV-B Temps 1 — CCI pré-simulation    [mepa_kappa_calculator.py]
Nœud 14  → Certification (gate cci_global)
Nœud 15  → Archivage passeport WP                [mepa_passeport_schema.py]
```

Sous-workflow indépendant : `mepa_workflow_n8n_V7_audit_seul.json`, pour ré-audit CONV-B isolé sur rapport révisé.

### Scripts

| Script | Rôle | Notes |
|---|---|---|
| `mepa_runner_v3_v7.py` | Simulation ODE (LSODA) + précheck α + stress-tests N1/N2 + non-régression T1-T5 vs Euler | v3.0.0 |
| `mepa_runner_v2_gamma.py` | Runner V6.2 (Euler dt=1) — conservé pour non-régression et corpus non migré | v2.1.1 |
| `mepa_dev1_advisory_v7.py` | Module advisory diagnostique — plafond redistributif dérivé de l'EROI (Ω ≡ I(t)) — NON CALIBRÉ, non bloquant | Dev 2 gelé |
| `mepa_kappa_calculator.py` | CCI (ICC 3,1) et κ de Cohen inter-codeurs | v3.0 |
| `mepa_passeport_schema.py` | Construction et validation du Passeport WP archivé | v3.0.2 |
| `mepa_node2_audit_v7.js` | Audit conformité structurelle fiche (contrôles C1–C15, incl. C14/C15 spécifiques V7) | v3.0.0 |
| `mepa_consistency_check.py` | Vérifie la cohérence des seuils de certification répliqués contre `mepa_constants.json` — bloquant en préflight | v1.0.0 |
| `mepa_deploy_check.py` | Garde-fou d'intégrité de déploiement — compare le sha256 des scripts déployés à un manifeste de référence | v1.0.0 |

---

## Structure des fichiers

```
mepa/
│
├── prompt_projet_MEPA_V4_alpha.md           ← Prompt système LLM (moteur MEPA V7)
├── mepa_pipeline_architecture_V62.md        ← Documentation technique pipeline (socle)
├── INSTRUCTIONS_WORKFLOW_N8N_V7.md          ← Modifications V7 du workflow n8n
│
├── scripts/
│   ├── mepa_runner_v3_v7.py
│   ├── mepa_runner_v2_gamma.py
│   ├── mepa_dev1_advisory_v7.py
│   ├── mepa_sensitivity_n1.py
│   ├── mepa_kappa_calculator.py
│   ├── mepa_passeport_schema.py
│   ├── mepa_node2_audit_v7.js
│   ├── mepa_node2_audit_v62.js
│   ├── mepa_consistency_check.py
│   ├── mepa_deploy_check.py
│   └── correctif_V5_compteur_CCI.js         ← reliquat V5, archivage prévu
│
├── config/
│   ├── mepa_constants.json                  ← Source unique de vérité (paramètres, seuils)
│   ├── mepa_whitelist_keys.json
│   ├── mepa_friction_profile.json
│   ├── mepa_deploy_manifest.json
│   └── v7/                                  ← Fiches V7 (6 pilotes certifiées)
│
├── workflow_n8n/
│   ├── mepa_workflow_n8n_V7.json
│   ├── mepa_workflow_n8n_V7_audit_seul.json
│   ├── mepa_workflow_n8n_V7_sequencer.json
│   └── mepa_workflow_n8n_V62*.json          ← workflows V6.2 (référence, non migrés)
│
├── WP-F*/  WP-I*/  WP-C*/  WP-T*/           ← 27 fiches, V6.2 + V7 selon migration
│
├── MEPA_Decision/                           ← Série des décisions de gouvernance (CV-series)
│   ├── MEPA_Decision_V7_D1_rev4.md
│   ├── MEPA_Certification_V7_gamma_rev2.md
│   ├── MEPA_Decision_CV14_Gel_Dev2.md
│   ├── MEPA_Decision_CV15_Sequencement_Post_V7.md
│   └── ...
│
├── Docs/
│   ├── MEPA_cadre_theorique_V7_alpha_rev2_1.docx
│   ├── MEPA_cadre_theorique_V6_2.docx
│   ├── MEPA_Addendum_Theorique_V6_2.docx
│   └── ...
│
└── Conversations/
    ├── CONV-A.md   (rédaction rapport)
    ├── CONV-B.md   (audit inter-codeurs, Temps 1 et 2)
    ├── CONV-E.md   (codage MEPA Full)
    └── CONV-D.md   (synthèse cumulative de cluster)
```

---

## Installation et utilisation

### Prérequis

```bash
Python >= 3.9
Node.js >= 18
n8n (self-hosted ou cloud)
```

### Dépendances Python

```bash
pip install numpy scipy
```

### Lancer une simulation V7

```bash
python mepa_runner_v3_v7.py WP-C2-1_Egypte2011_v7.json
```

### Lancer une simulation V6.2 (référence / non-régression)

```bash
python mepa_runner_v2_gamma.py WP-C2-1_Egypte2011_v62.json
```

### Calculer le CCI / κ inter-codeurs

```bash
python mepa_kappa_calculator.py fiche_CONV-E.json fiche_CONV-B.json
```

### Vérifier la cohérence des seuils de certification

```bash
python mepa_consistency_check.py
```

### Pipeline complet via n8n

Importer `mepa_workflow_n8n_V7.json` dans votre instance n8n, puis déclencher le workflow avec une fiche WP V7 en entrée. Pour ré-auditer un rapport révisé sans relancer toute la chaîne, utiliser `mepa_workflow_n8n_V7_audit_seul.json`.

---

## Format d'entrée — Fiche WP

```json
{
  "wp_id": "WP-C2-1",
  "cas": "Égypte 2011",
  "cluster": "C2",
  "trajectoire_attendue": "(b) Répression réussie",
  "sa": 6,
  "fiche_v7": true,
  "y0": [1.2, 0.28, 0.1, 3],
  "cmd_base": {
    "T": 0.9, "Mob": 0.2, "R": 0.25, "Ref": 0.1,
    "Rc": 0.62, "Rn": 0.35, "E": 0.65,
    "gamma": 0.48,
    "EROI": 3.75, "Pop": 1.0
  },
  "variables_v7": {
    "m_r": 1, "mu_m": 0.5, "phi": 0.55,
    "psi_noyau": 0.03, "psi_cible": null, "gamma_local": 0.75
  },
  "t_max": 300,
  "theta_C": 0.30,
  "theta_I": 0.22
}
```

> ⚠️ La clé `gamma` est la seule forme acceptée pour γ. Les clés `g` ou `Gamma` sont rejetées par l'audit de conformité. `psi_cible: null` requiert une justification positive explicite dans le codage (règle E3 rev. 2.1).

---

## Trajectoires diagnostiquées

Dix trajectoires possibles, dont une nouvelle en V7 :

| Label | Code | Condition principale |
|---|---|---|
| Rupture transformatrice | `(a)` | F≥R, ΔC_rel élevé, dC/dt>0 à t_b |
| **Cristallisation sacrificielle d'État** | **`(α)`** | **V7 — précheck C1-C4 satisfait, rampe mod_mimétique activée** |
| Répression réussie | `(b)` | F<R sur tout t_max, Rc+Rn>0.6 |
| Stase / ambigu | `(c)` | Bascule sans dominance nette |
| Effondrement progressif | `(d)` | ΔI_rel élevé, ΔC_rel faible |
| Réforme institutionnelle | `(e)` | Bascule avec Ref>0.35, Rc+Rn<0.35 |
| Stabilité | `(h)` | F<R, répression faible |
| Stabilité ou réforme lente | `(h)/(e)` | Sortie runner si F<R sur tout t_max |
| Transformation forcée | `(γ)` | Cas extrêmes à override documenté |
| Dissolution | `(d)` var. | Variante effondrement (Manuel Gouvernance Annexe A) |

Chaque passeport porte une **annotation de branche** (`branche_annotation`) : `EXPLICATIVE` (le mécanisme identifié rend compte de la trajectoire) ou `CATCHALL` (trajectoire par défaut du modèle V6.2, hors mécanisme V7 spécifique).

---

## Contrôle qualité et gouvernance

### Seuils de validation inter-codeurs

| Métrique | Certifié | Révision | Rejet |
|---|---|---|---|
| CCI (variables continues) | ≥ 0.70 | 0.50–0.69 | < 0.50 |
| κ de Cohen (Sa catégorielle) | ≥ 0.70 | 0.50–0.69 | < 0.50 |
| **cci_global (gate de certification)** | **≥ 0.75** | **0.55–0.74** | **< 0.55** |

Le gate de certification est **`cci_global` seul**. `kappa_sa` et `kappa_m_r` sont des champs de traçabilité de l'accord inter-codeurs archivés dans le passeport — jamais des critères bloquants.

### Garde-fous de fiabilité (issus de l'audit technique post-certification V7.0)

- **Sauvegarde du registre scientifique** : chaque passeport certifié doit exister simultanément sur au moins deux supports indépendants, sans fenêtre où il n'existe qu'à un seul endroit.
- **Intégrité de déploiement** : `mepa_deploy_check.py` compare le sha256 des scripts en production à un manifeste de référence versionné — bloque tout run si un script diverge silencieusement de sa version committée.
- **Cohérence des seuils** : `mepa_consistency_check.py` vérifie que les seuils de certification (répliqués dans plusieurs scripts pour robustesse) restent identiques à la source unique de vérité `mepa_constants.json`.
- **Traçabilité de la résolution inter-codeurs** : chaque passeport archive, par variable, la valeur CONV-E, la valeur CONV-B, l'action de résolution appliquée et la valeur finale retenue — condition requise avant l'extension aux 21 WP restants.
- **Gel des entrées résolues à la certification** : une fois un WP certifié, ses entrées numériques résolues (`y0`, `cmd_base`) sont figées comme partie intégrante de l'artefact certifié. Tout re-run ultérieur réutilise cette configuration gelée plutôt que de repasser par un nouveau tirage d'audit inter-codeurs — condition de reproductibilité stricte du corpus.

### Protocole anti-rationalisation (V7-C3)

Pour tout WP dont la trajectoire diagnostiquée diverge de la trajectoire attendue dans le cluster pilote, le rapport doit contenir deux sections obligatoires :
- **Anomalie documentée** — énoncé neutre de la divergence, signature numérique brute, sans interprétation justificative.
- **Hypothèse théorique sous contrainte** — hypothèse falsifiable sur un cas futur distinct, avec critères d'acceptation et de réfutation explicites, disclaimer anti-rationalisation.

---

## Feuille de route

### Court terme
- [ ] Extension du pipeline aux 21 WP restants du corpus (gatée sur le chantier V7.1, voir ci-dessous)
- [ ] Création de WP-I11-1 (Grande Terreur soviétique 1937-1938) — troisième cas de calibration positive (α)
- [ ] V7.1 — score continu d'activation sacrificielle (remplace le seuil binaire du précheck C2)

### Moyen terme
- [ ] Réintégration du mécanisme de dette institutionnelle (Dev 2 — actuellement gelé, réactivation conditionnée à la certification V7.0)
- [ ] Calibration bayésienne complète post-27 WP
- [ ] Plancher de complexité I_min dynamique

### Suivi théorique ouvert
- [ ] Limite documentée sur WP-I4-1 (Allemagne nazie) : le critère de masse critique du noyau (Ψ_noyau formel) exclut les mécanismes de mobilisation par adhésion tacite de masse — piste de révision en V7.1/V8

---

## Références

- Turchin, P. — Cliodynamique et régularités mathématiques dans l'histoire longue.
- Tainter, J. (1988). *The Collapse of Complex Societies* — mécanique de la surcharge de complexité.
- Todd, E. — Typologies anthropologiques familiales (Sa ∈ {2, 4, 6, 7}) et stades de la matrice religieuse (M_r ∈ {1, 2, 3}).
- Girard, R. (1972). *La Violence et le Sacré* — mécanisme mimétique et bouc émissaire (base de l'extension V7).
- Chenoweth, E. — seuil empirique de mobilisation active (~3,5 % de population), utilisé comme point d'ancrage (non causal) pour la calibration du seuil sacrificiel.
- Shrout & Fleiss (1979). Intraclass correlations: uses in assessing rater reliability. *Psychological Bulletin* 86(2).
- McGraw & Wong (1996). Forming inferences about some intraclass correlation coefficients. *Psychological Methods* 1(1).
- Gellately, R. (2001) ; Mallmann & Paul (1994) — répression non-étatique auto-entretenue (délation volontaire).
- BP Statistical Review / Our World in Data — données EROI.
- V-DEM, Freedom House, Polity V — indicateurs E_split / Cs.
- IMF / World Bank — A_d_eff (dette/PIB, inflation, GFCF).

---

## Licence

Ce projet est distribué sous **double licence** :

- **Documentation, fiches WP et cadre théorique** (fichiers `.md`, `.docx`, `.odt`, `.json` de codage)
  → [CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/) — Attribution obligatoire, pas de version modifiée redistribuable.

- **Scripts de simulation et d'audit** (`mepa_runner_v3_v7.py`, `mepa_runner_v2_gamma.py`, `mepa_dev1_advisory_v7.py`, `mepa_sensitivity_n1.py`, `mepa_kappa_calculator.py`, `mepa_passeport_schema.py`, `mepa_node2_audit_v7.js`, `mepa_node2_audit_v62.js`, `mepa_consistency_check.py`, `mepa_deploy_check.py`)
  → [MIT License](https://opensource.org/licenses/MIT) — Libre utilisation, modification et redistribution avec attribution.

© 2026 — [toto-blanco](https://github.com/toto-blanco)

*MEPA V7 — Juin 2026*
