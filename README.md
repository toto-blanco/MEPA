# MEPA V6.2 — Modèle Énergétique du Potentiel Adaptatif

> Simulation des transitions socio-institutionnelles sur 27 cas historiques via équations différentielles couplées, pipeline n8n automatisé, audit inter-codeurs (κ de Cohen) et analyse de sensibilité bayésienne.

---

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture du projet](#architecture-du-projet)
3. [Corpus historique (27 WP)](#corpus-historique-27-wp)
4. [Cadre théorique](#cadre-théorique)
5. [Pipeline technique](#pipeline-technique)
6. [Structure des fichiers](#structure-des-fichiers)
7. [Installation et utilisation](#installation-et-utilisation)
8. [Format d'entrée — Fiche WP](#format-dentrée--fiche-wp)
9. [Trajectoires diagnostiquées](#trajectoires-diagnostiquées)
10. [Contrôle qualité](#contrôle-qualité)
11. [Feuille de route V7](#feuille-de-route-v7)
12. [Références](#références)

---

## Vue d'ensemble

**MEPA** (Modèle Énergétique du Potentiel Adaptatif) est un cadre de modélisation quantitatif-qualitatif conçu pour analyser les **transitions socio-institutionnelles** à travers l'histoire. Le modèle postule que tout système socio-politique bascule lorsque la force transformatrice `F(t)` dépasse la résistance du système `R(t)`.

Le projet V6.2 couvre **27 Working Papers (WP)** répartis sur cinq clusters thématiques, de la Rome du IIIe siècle au Rwanda contemporain, en passant par la Révolution française, la montée du nazisme ou l'effondrement de l'URSS.

### Deux composantes complémentaires

| Composante | Rôle | Outils |
|---|---|---|
| **MEPA Full** | Codage qualitatif de 9 variables sur sources historiques | Fiches JSON, audit inter-codeurs |
| **MEPA Lite** | Simulation numérique de 4 équations différentielles couplées | `mepa_runner_v2_gamma.py`, n8n |

---

## Architecture du projet

```
┌──────────────────────────────────────────────────────────────┐
│  Fiche WP (JSON)  →  Nœud 1 Audit  →  Runner Python (ODE)   │
│                                    →  LLM Rédaction WP       │
│                                    →  Porte Kappa (κ ≥ 0.70) │
│                                    →  Passeport WP           │
│                                    →  Export / Méta-Analyse  │
└──────────────────────────────────────────────────────────────┘
```

Le pipeline complet est orchestré via **n8n** (workflow `mepa_workflow_n8n_V62.json`) et enchaîne 9 nœuds : validation structurelle, simulation ODE, analyse de sensibilité N1, rédaction LLM (7 sections), audit inter-codeurs, construction du Passeport WP et méta-analyse de cluster.

---

## Corpus historique (27 WP)

### Cluster C1 — Crises contemporaines (6 WP)
| WP | Cas | Période | Trajectoire attendue |
|---|---|---|---|
| WP-C1-1 | Haïti | 2010–2021 | (d) Effondrement progressif |
| WP-C2-1 | Égypte 2011 | 2008–2013 | (a) Rupture transformatrice |
| WP-C3-1 | Argentine | 1998–2003 | (a) Rupture transformatrice |
| WP-C4-1 | Liban | 2019–2023 | (d) Effondrement progressif |
| WP-C5-1 | Iran | 2009–2022 | (b) Répression réussie |
| WP-C6-1 | Chine (Xi) | 2012–2023 | (b) Répression réussie |

### Cluster C2 — Fondements / Effondrements historiques (10 WP)
| WP | Cas | Trajectoire attendue |
|---|---|---|
| WP-F1-1 | Rome IIIe s. | (c) → (d) |
| WP-F2-1 | Rome tardive | (d) Effondrement progressif |
| WP-F3-1 | Maya classique | (d) Effondrement progressif |
| WP-F4-1 | Égypte ancienne | (c) Stase / ambigu |
| WP-F5-1 | Venise déclin | (d) Effondrement progressif |
| WP-F6-1 | Empire ottoman | (d) Effondrement progressif |
| WP-F7-1 | Révolution haïtienne | (a) Rupture transformatrice |
| WP-F8-1 | France révolutionnaire | (a) Rupture transformatrice |
| WP-F9-1 | Angleterre stabilité | (h) Stabilité |
| WP-F10-1 | Commune de Paris | (a) Rupture transformatrice |

### Cluster C3 — Industrialisation & Ruptures (10 WP)
| WP | Cas | Trajectoire attendue |
|---|---|---|
| WP-I1-1 | Angleterre industrielle | (h) Stabilité |
| WP-I2-1 | Russie 1917 | (a) Rupture transformatrice |
| WP-I3-1 | Japon Meiji-Guerre *(Sa=7)* | (a)→(e)→(h)→(d) |
| WP-I4-1 | Allemagne nazie *(Sa=7)* | (b) Répression réussie |
| WP-I5-1 | Espagne Guerre civile | (a) Rupture transformatrice |
| WP-I6-1 | Tiananmen | (b) Répression réussie |
| WP-I7-1 | URSS | (d) Effondrement progressif |
| WP-I8-1 | Chine Deng | (e)→(h) |
| WP-I9-1 | Singapour *(Sa=7)* | (h) Stabilité |
| WP-I10-1 | Rwanda | (a)→(e) reconstruction |

### Cluster C4 — Transitions (1 WP)
| WP | Cas | Trajectoire attendue |
|---|---|---|
| WP-T1-1 | Guerre de Sécession | (a) Rupture transformatrice |

### Étalon (hors corpus principal)
| WP | Cas | Note |
|---|---|---|
| WP-EXT-5 | Islande 2008–2013 | Ancre MAX EROI=35.0 — candidat V7 |

---

## Cadre théorique

### Variables d'état (MEPA Lite)

| Variable | Signification |
|---|---|
| `S` | Pression sociale |
| `L` | Chaleur latente (légitimité) |
| `C` | Chaleur collective (capital social) |
| `I` | Complexité institutionnelle |

### Équations différentielles (intégration Euler explicite, dt=1)

```
dS = p1·T − p2·(R + Ref + Mob) − p2b·S
dL = p4·S − L − p3·L·Θ
dC = p5·M − p6·C − p7·(Rc + Rn)·ℓ·gC
dI = p8·(EROI − 1)·Pop − p9·I

F(t) = C + λ·L·(1 + μ·γ·E)
R(t) = I^(1/3) + ν·(Rc + Rn)·ℓ + ρ

Condition de bascule : F(t) ≥ R(t)
```

### Variables de commande (9 variables MEPA Full)

| Symbole | Clé JSON | Échelle | Description |
|---|---|---|---|
| E_split | `E` | [0,1] | Fracture de l'élite |
| **γ** | `gamma` | [0,1] | Capacité organisationnelle de l'élite |
| A_d_eff | `R` | [0,10] | Capacité redistributive effective |
| A_r_c | `Rc` | [0,1] | Répression classique |
| A_r_ne | `Rn` | [0,1] | Répression numérique |
| Cs | — | [0,1] | Crédibilité du régime |
| L(t) | `L` | [0,1] | Loyauté des appareils |
| EROI | `EROI` | >1 | Rendement énergétique net |
| Sa | `sa` | {2,4,6,7} | Structure anthropologique Todd |

> **Règle de nomenclature absolue V6.2 :** `gamma` est la clé JSON/Python exclusive. **γ** est le symbole dans les équations et le texte rédigé. La lettre `g` isolée est interdite dans tout contexte MEPA.

### Modulateur Todd (Sa)

| Sa | Type familial | Effet sur le modèle |
|---|---|---|
| 2 | Nucléaire absolu (monde anglo-saxon) | Instabilité haute |
| 4 | Nucléaire égalitaire (France, Amérique latine) | Instabilité chronique |
| 6 | Communautaire (Russie, Chine, Iran) | Résilience autoritaire |
| **7** | **Souche (Allemagne, Japon, Corée)** | **p6 × 1.5 obligatoire** |

---

## Pipeline technique

### Nœuds n8n (9 étapes)

```
Nœud 1  → Audit & Conformité          [mepa_node2_audit_v62.js]
Nœud 3  → Write Config File
Nœud 4  → Execute Runner              [mepa_runner_v2_gamma.py]
Nœud 5  → Parse Runner Result
Nœud 5b → Sensibilité N1              [mepa_sensitivity_n1.py]        ★
Nœud 6  → Rédaction LLM WP (7 sections S1→S7)
Nœud 6b → Porte Kappa inter-codeurs   [mepa_kappa_calculator.py]      ★
Nœud 6c → Construction Passeport WP   [mepa_passeport_schema.py]      ★
Nœud 7  → Export WP (Drive / Notion / PDF)
Nœud 8  → Merge Cluster (après 5 WP du cluster)
Nœud 9  → Méta-Analyse cluster
```

### Scripts

| Script | Nœud | Rôle | Seuil bloquant |
|---|---|---|---|
| `mepa_runner_v2_gamma.py` | 4 | Simulation ODE + stress N1 partiel | divergence p6 > 0.001 |
| `mepa_sensitivity_n1.py` | 5b | Sensibilité ±20% (9 cmd + 16 params) | flag verdict_n1 |
| `mepa_kappa_calculator.py` | 6b | κ de Cohen CONV-E / CONV-B | κ < 0.50 → REJET |
| `mepa_passeport_schema.py` | 6c | Construction + validation Passeport WP | toute erreur bloquante |
| `mepa_node2_audit_v62.js` | 1 | Validation structurelle + normalisation `gamma` | status=ERROR |

---

## Structure des fichiers

```
mepa-v62/
│
├── prompt_projet_MEPA_V3_gamma.md        ← Prompt système LLM (moteur MEPA)
├── mepa_pipeline_architecture_V62.md     ← Documentation technique pipeline
│
├── Scripts/
│   ├── mepa_runner_v2_gamma.py
│   ├── mepa_sensitivity_n1.py
│   ├── mepa_kappa_calculator.py
│   ├── mepa_passeport_schema.py
│   ├── mepa_node2_audit_v62.js
│   └── correctif_V5_compteur_CCI.js
│
├── Config/
│   ├── mepa_constants.json               ← Source unique de vérité (paramètres)
│   ├── mepa_whitelist_keys.json
│   ├── mepa_friction_profile.json
│   └── mepa_workflow_n8n_V62.json
│
├── WP-F*/                                ← Cluster Fondements (10 fiches)
├── WP-I*/                                ← Cluster Industrialisation (10 fiches)
├── WP-C*/                                ← Cluster Crises contemporaines (6 fiches)
├── WP-T*/                                ← Cluster Transitions (1 fiche)
│
├── Fiches-Etalon/
│   ├── fiche_etalon_WP-C1-1_Haiti_v62.json
│   └── fiche_etalon_WP-EXT-5_Islande_v62.json
│
├── Docs/
│   ├── MEPA_cadre_theorique_V6_2.docx
│   ├── MEPA_V6_2_Schema_Directeur_Architecture.docx
│   ├── MEPA_Guide_Methodologique_27WP_V6_2.docx
│   ├── MEPA_Manuel_Gouvernance_Execution_V6_2.docx
│   ├── MEPA_Protocole_Experimental_V6_2.docx
│   ├── MEPA_Stratification_Priorite_V6_2.docx
│   └── MEPA_Instructions_27WP_V6_2.docx
│
└── Conversations/
    ├── CONV-A.md   (runner — simulation)
    ├── CONV-B.md   (audit inter-codeurs)
    ├── CONV-E.md   (codage MEPA Full)
    └── TABLEAU_DE_CONTRÔLE_GLOBAL___27_WP_V6_2.odt
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

### Lancer une simulation directe

```bash
python mepa_runner_v2_gamma.py WP-C2-1_Egypte2011_v62.json
```

### Lancer l'analyse de sensibilité N1

```bash
python mepa_sensitivity_n1.py WP-C2-1_Egypte2011_v62.json
```

### Calculer le κ inter-codeurs

```bash
python mepa_kappa_calculator.py fiche_CONV-E.json fiche_CONV-B.json
```

### Pipeline complet via n8n

Importer `mepa_workflow_n8n_V62.json` dans votre instance n8n, puis déclencher le workflow avec une fiche WP en entrée.

---

## Format d'entrée — Fiche WP

```json
{
  "wp_id": "WP-C2-1",
  "cas": "Égypte 2011",
  "periode": "2008-2013",
  "cluster": "C1",
  "trajectoire_attendue": "(a) Rupture transformatrice",
  "sa": 4,
  "y0": { "S": 1.1, "L": 0.4, "C": 0.10, "I": 6.0 },
  "cmd": {
    "T": 0.9, "Mob": 0.6, "R": 2.5, "Ref": 0.10,
    "Rc": 0.5, "Rn": 0.2, "E": 0.7,
    "gamma": 0.55,
    "EROI": 4.0, "Pop": 1.0
  },
  "t_max": 200,
  "theta_C": 0.30,
  "theta_I": 0.22
}
```

> ⚠️ La clé `gamma` est la seule forme acceptée. Les clés `g` ou `Gamma` sont rejetées par le Nœud 1 (Audit & Conformité).

---

## Trajectoires diagnostiquées

| Label | Code | Condition principale |
|---|---|---|
| Rupture transformatrice | `(a)` | F≥R, ΔC_rel élevé, dC/dt>0 à t_b |
| Répression réussie | `(b)` | F<R sur tout t_max, Rc+Rn>0.6 |
| Stase / ambigu | `(c)` | Bascule sans dominance nette |
| Effondrement progressif | `(d)` | ΔI_rel élevé, ΔC_rel faible |
| Dissolution | `(d)` | Variante effondrement (Manuel Gouvernance Annexe A) |
| Réforme institutionnelle | `(e)` | Bascule avec Ref>0.35, Rc+Rn<0.35 |
| Stabilité | `(h)` | F<R, répression faible |
| Stabilité ou réforme lente | `(h)/(e)` | Sortie runner si F<R sur tout t_max |
| Transformation forcée | `(γ)` | Cas extrêmes (Manuel Gouvernance Annexe A) |

---

## Contrôle qualité

### Seuils de validation inter-codeurs

| Métrique | Certifié | Révision | Rejet |
|---|---|---|---|
| CCI (variables continues) | ≥ 0.70 | 0.50–0.69 | < 0.50 |
| κ de Cohen (Sa catégorielle) | ≥ 0.70 | 0.50–0.69 | < 0.50 |
| CCI global agrégé | ≥ 0.75 | 0.55–0.74 | < 0.55 |

### Ordre de traitement recommandé (Stratification V6.2)

```
Phase 1 — Ancres LOI PHYSIQUE (à traiter en premier)
  WP-I10  Rwanda        → ancre EROI min
  WP-C1   Haïti         → ancre EROI min corpus
  WP-C2   Égypte 2011   → ancre C max

Phase 2 — Fondateurs calibration bayésienne
  WP-F1, WP-F2, WP-I7

Phase 3 — Cœur (11 WP)
Phase 4 — Zone de stress (10 WP)
  ⚠ WP-I3, WP-I4, WP-I9 : Sa=7 → vérifier p6×1.5 dans audit_log
```

---

## Feuille de route V7

- [ ] Implémentation θ_C adaptatif (0.15 si C0 ≥ 0.4)
- [ ] Nouveaux WP : Portugal 1974, New Deal 1933, Espagne 2010
- [ ] Calibration bayésienne complète post-27 WP
- [ ] Plancher de complexité I_min dynamique
- [ ] Extension cluster C6 (réservé)

---

## Références

- Turchin, P. et al. (2015). *Seshat Global History Databank* — méthodologie de codage.
- Shrout & Fleiss (1979). Intraclass correlations: uses in assessing rater reliability. *Psychological Bulletin* 86(2).
- McGraw & Wong (1996). Forming inferences about some intraclass correlation coefficients. *Psychological Methods* 1(1).
- Todd, E. — Typologies anthropologiques familiales (Sa ∈ {2, 4, 6, 7}).
- BP Statistical Review / Our World in Data — données EROI.
- V-DEM, Freedom House, Polity V — indicateurs E_split / Cs.
- IMF / World Bank — A_d_eff (dette/PIB, inflation, GFCF).

---

*MEPA V6.2 — Mars 2026*
