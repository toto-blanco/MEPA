# MEPA V6.2 — Modèle Énergétique du Potentiel Adaptatif

> Simulation des transitions socio-institutionnelles sur 27 cas historiques via équations différentielles couplées, pipeline n8n automatisé, audit inter-codeurs (CCI / κ de Cohen) et analyse de sensibilité bayésienne.

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

Le projet V6.2 couvre **27 Working Papers (WP)** répartis sur cinq clusters thématiques (C1–C5), de la Rome du IIIe siècle au Rwanda contemporain, en passant par la Révolution française, la montée du nazisme ou l'effondrement de l'URSS.

### Deux composantes complémentaires

| Composante | Rôle | Outils |
|---|---|---|
| **MEPA Full** | Codage qualitatif de 9 variables sur sources historiques | Fiches JSON, audit inter-codeurs CCI |
| **MEPA Lite** | Simulation numérique de 4 équations différentielles couplées | `mepa_runner_v2_gamma.py`, n8n |

---

## Architecture du projet

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Fiche WP (JSON)                                                        │
│     ↓                                                                   │
│  [Nœud 2] Audit C1–C13     →  INVALIDE : recodage CONV-E               │
│                             →  DONNÉES_INSUFFISANTES : escalade Archi.  │
│     ↓ VALIDE                                                            │
│  [Nœud 8a] CONV-B CCI pré-simulation (double aveugle)                  │
│     ↓ valeurs résolues injectées                                        │
│  [Nœud 4] Runner Python (ODE Euler dt=1) + [Nœud 4b] Sensibilité N1   │
│     ↓                                                                   │
│  [Nœud 6] LLM Rédaction WP S1→S7 (CONV-A, T=0)                        │
│     ↓                                                                   │
│  [Nœud 7] CONV-B Audit WP complet C1–C5                                │
│     ↓ CERTIFIÉ                                                          │
│  [Nœud 12] Stress-test N2 + [Nœud 13] Prédiction Popper RF1/RF2/RF3   │
│     ↓                                                                   │
│  [Nœud 14] Certification (WP_CERTIFIÉ / WP_EXPLORATOIRE)               │
│     ↓                                                                   │
│  [Nœud 15] Archivage /data/mepa/outputs/ + Passeport compact CONV-D    │
└─────────────────────────────────────────────────────────────────────────┘
```

Le pipeline complet est orchestré via **n8n** (workflow `mepa_workflow_n8n_V62.json`, WF2 — 26 nœuds) et suit la séquence : `CONV-E → CONV-B CCI → Runner → CONV-A → CONV-B Audit → Certification`.

> **Note technique :** Le nœud 2 opérationnel est le code embarqué dans `mepa_workflow_n8n_V62.json` (version "V6.3 Fortifié", Correctif A6 — 2026-03-16). Le fichier `scripts/mepa_node2_audit_v62.js` est la version de référence documentaire (v2.1.0) — légèrement antérieure à la version embarquée mais fonctionnellement équivalente pour les 13 contrôles C1–C13.

---

## Corpus historique (27 WP)

> **Rappel de nomenclature :** Les clusters **C1–C5** ci-dessous sont les clusters **MEPA** (déterminés par la dynamique du modèle), non des catégories éditoriales. Chaque fiche JSON contient le cluster réel assigné à chaque WP.

### Cluster C1 — Effondrements et transitions longue durée (11 WP)

| WP | Cas | Période | Sa | Trajectoire attendue |
|---|---|---|---|---|
| WP-C1-1 | Haïti — Crise post-séisme | 2010–2024 | 4 | (d) Dissolution |
| WP-C4-1 | Liban — Effondrement institutionnel | 2019–2026 | 6 | (d) Dissolution |
| WP-F1-1 | Rome — Crise du IIIe siècle | 235–284 | 4 | (d) Effondrement progressif |
| WP-F2-1 | Rome tardive | IIIe–Ve s. | 4 | (d) Effondrement progressif |
| WP-F3-1 | Empire Maya classique | 800–950 | 6 | (d) Effondrement progressif |
| WP-F6-1 | Empire Ottoman | 1908–1922 | 6 | (d) Effondrement progressif |
| WP-F7-1 | Révolution haïtienne | 1791–1804 | 6 | (a) Rupture transformatrice |
| WP-I2-1 | Russie 1917 | 1905–1921 | 6 | (a) Rupture transformatrice |
| WP-I7-1 | URSS — Effondrement | 1970–1991 | 6 | (d) Effondrement progressif |
| WP-I10-1 | Rwanda — Génocide et reconstruction | 1990–2010 | 6 | (a) Rupture transformatrice |
| WP-T1-1 | Guerre de Sécession — États-Unis | 1860–1877 | 2 | (γ) Transformation forcée |

### Cluster C2 — Transitions oligarchiques et réformes bloquées (5 WP)

| WP | Cas | Période | Sa | Trajectoire attendue |
|---|---|---|---|---|
| WP-C2-1 | Égypte 2011 — Printemps arabe | 2010–2014 | 6 | (b) Répression réussie |
| WP-F5-1 | Venise — Déclin oligarchique | XVIIe–XVIIIe s. | 4 | (c) Stase / ambigu |
| WP-F8-1 | France révolutionnaire | 1787–1799 | 4 | (a) Rupture transformatrice |
| WP-F10-1 | Commune de Paris | 1871 | 4 | (a) Rupture transformatrice |
| WP-I4-1 | Allemagne nazie *(Sa=7)* | 1919–1945 | 7 | (a) Rupture transformatrice |

### Cluster C3 — Cas singuliers / instabilité structurelle (1 WP)

| WP | Cas | Période | Sa | Trajectoire attendue |
|---|---|---|---|---|
| WP-I5-1 | Espagne — Guerre civile | 1931–1939 | 4 | (γ) Transformation forcée |

### Cluster C4 — Crédibilité du système et résilience institutionnelle (6 WP)

| WP | Cas | Période | Sa | Trajectoire attendue |
|---|---|---|---|---|
| WP-C6-1 | Chine Xi Jinping | 2012–2026 | 6 | (h) Stabilité |
| WP-F9-1 | Angleterre — Stabilité sous pression | 1789–1815 | 2 | (h) Stabilité |
| WP-I1-1 | Angleterre industrielle | 1760–1840 | 2 | (h) Stabilité |
| WP-I6-1 | Chine — Tiananmen 1989 | 1989 | 6 | (b) Répression réussie |
| WP-I8-1 | Chine Deng | 1978–1997 | 6 | (h) Stabilité |
| WP-I9-1 | Singapour *(Sa=7)* | 1965–2024 | 7 | (h) Stabilité |

### Cluster C5 — Transitions complexes avec réorganisation partielle (4 WP)

| WP | Cas | Période | Sa | Trajectoire attendue |
|---|---|---|---|---|
| WP-C3-1 | Argentine — Cycles Turchin | 2001–2024 | 4 | (c) Stase / ambigu |
| WP-C5-1 | Iran 1979–2026 | 1979–2026 | 6 | (h)/(e) Stabilité ou réforme lente |
| WP-F4-1 | Égypte ancienne — Cycles dynastiques | 3000 av.–640 ap. | 6 | (c) Stase / ambigu |
| WP-I3-1 | Japon Meiji–Guerre–Reconstruction *(Sa=7)* | 1853–1945 | 7 | (d) Effondrement progressif |

### Étalon (hors corpus principal)

| WP | Cas | Note |
|---|---|---|
| WP-EXT-5 | Islande 2008–2013 | Ancre MAX EROI=35.0 — candidat V7 — (e) Réforme institutionnelle |

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
ℓ = R / (R + p13)
gC = C / (C + ε)              ← variable interne de saturation (≠ γ, ne pas renommer)
Θ = 1 / (1 + exp(-K_SIG × (C − Cc)))
M = p10 × (1 + a×E) × L / (1 + p11a×ℓ×Rc + p11b×ℓ×Rn×(1 − κ×C))

dS = p1×T − p2×(R + Ref + Mob) − p2b×S
dL = p4×S − L − p3×L×Θ
dC = p5×M − p6×C − p7×(Rc + Rn)×ℓ×gC
dI = p8×(EROI − 1)×Pop − p9×I

F(t) = C + λ×L×(1 + μ×γ×E)
R(t) = I^(1/3) + ν×(Rc + Rn)×ℓ + ρ

Condition de bascule : F(t) ≥ R(t)
```

### Variables de commande (9 variables MEPA Full → 10 commandes runner)

| Symbole MEPA Full | Clé JSON runner | Échelle | Description |
|---|---|---|---|
| E_split | `E` | [0,1] | Fracture de l'élite |
| **γ** | **`gamma`** | [0,1] | Capacité organisationnelle de l'élite |
| A_d_eff | `R` | [0,10] | Capacité redistributive effective |
| A_r_c | `Rc` | [0,1] | Répression classique |
| A_r_ne | `Rn` | [0,1] | Répression numérique (0.00 si pré-numérique) |
| Cs | `Mob` | [0,1] | Crédibilité du régime / mobilisation *(mapping approx.)* |
| L_t | `y0[L0]` | [0,1] | Loyauté des appareils (condition initiale L0) |
| EROI | `EROI` | >1 | Rendement énergétique net |
| Sa | `sa` | {2,4,6,7} | Structure anthropologique Todd |

> **Règle de nomenclature absolue V6.2 :** `gamma` est la clé JSON/Python exclusive. **γ** est le symbole dans les équations et le texte rédigé. La lettre `g` isolée est interdite dans tout contexte MEPA.

> **Note mapping Cs → Mob :** La variable Cs (crédibilité du régime) est mappée vers la commande runner `Mob` (mobilisation sociale) — ces deux grandeurs sont corrélées mais distinctes. Cette approximation est une limite connue de MEPA Lite (9 variables Full → 10 commandes runner). À documenter en S7 de chaque WP.

### Modulateur Todd (Sa)

| Sa | Type familial | Effet sur le modèle |
|---|---|---|
| 2 | Nucléaire absolu (monde anglo-saxon) | Instabilité haute — dissolution rapide des mobilisations |
| 4 | Nucléaire égalitaire (France, Amérique latine) | Instabilité chronique |
| 6 | Communautaire (Russie, Chine, Iran) | Résilience autoritaire |
| **7** | **Souche (Allemagne, Japon, Corée)** | **p6 × 1.5 obligatoire** — mobilisation maximale |

---

## Pipeline technique

### Séquence WF2 Protocole Complet (26 nœuds)

```
N0   ▶ Démarrage Manuel
NA   Lecture fiche WP JSON (binaire → décodage)
NB   Décode JSON [No-FS]
N2   Audit C1–C13 [mepa_node2_audit_v62.js v2.1 embarqué]
     ├─ INVALIDE     → Alerte recodage CONV-E
     └─ DONNÉES_INSUFFISANTES → Alerte escalade Architecte
     ↓ VALIDE
N8a  CONV-B codage indépendant + CCI pré-simulation [LLM double aveugle]
N8b  Router CCI — AUTO / WAIT_HUMAIN
     ├─ WAIT → N8c Validation humaine
     └─ AUTO →
N8d  Injection valeurs résolues dans runner_config
N3   Write runner_config.json [/tmp/]
N4   Execute Runner [mepa_runner_v2_gamma.py v2.1.1]  ←─ parallèle
N4b  Execute Sensibilité N1 [mepa_sensitivity_n1.py]  ←─ parallèle
N5   Parse Runner Result
N5b  Parse Sensibilité N1
N6   Rédaction LLM WP S1→S7 [CONV-A, T=0]
NC   Nettoyage /tmp/ [Anti-Contamination]
N7   CONV-B Audit WP complet C1–C5 [LLM]
     Router CONV-B → CERTIFIÉ / RÉVISION_MINEURE / RÉVISION_MAJEURE / REJET
N12  Stress-test N2 [combinaisons critiques optimiste/pessimiste]
N13  Prédiction Popper [RF1/RF2/RF3 + horizon temporel]
N14  Certification [WP_CERTIFIÉ / WP_EXPLORATOIRE]
N15  Archivage Final [/data/mepa/outputs/ + Passeport compact CONV-D]
```

### Scripts et nœuds associés

| Script | Nœud | Rôle | Seuil bloquant |
|---|---|---|---|
| `mepa_node2_audit_v62.js` | N2 | Validation structurelle C1–C13, normalisation `gamma`, détection NC | status=INVALIDE ou DONNÉES_INSUFFISANTES |
| `mepa_runner_v2_gamma.py` | N4 | Simulation ODE Euler dt=1 + stress N1 interne | RuntimeError NC bloquant |
| `mepa_sensitivity_n1.py` | N4b | Sensibilité ±20% (9 cmd + 16 params) | flag verdict_n1 |
| `mepa_kappa_calculator.py` | N8a | CCI / κ de Cohen CONV-E / CONV-B | CCI < 0.50 → REJET |
| `mepa_passeport_schema.py` | N15 | Construction + validation Passeport WP | toute erreur bloquante |

---

## Structure des fichiers

```
mepa-v62/
│
├── README.md
├── LICENSE
├── mepa_workflow_n8n_V62.json        ← Workflow WF2 Protocole Complet (26 nœuds)
│
├── scripts/
│   ├── mepa_runner_v2_gamma.py       ← Runner ODE (v2.1.1)
│   ├── mepa_sensitivity_n1.py        ← Analyse sensibilité N1
│   ├── mepa_kappa_calculator.py      ← CCI / κ inter-codeurs
│   ├── mepa_passeport_schema.py      ← Construction Passeport WP
│   ├── mepa_node2_audit_v62.js       ← Audit conformité (v2.1.0 référence doc.)
│   ├── correctif_V5_compteur_CCI.js  ← Correctif compteur CCI V5
│   ├── mepa_pipeline_architecture_V62.md
│   ├── prompt_projet_MEPA_V3_gamma.md ← Prompt système LLM CONV-E
│   ├── CONV-A.md                     ← Instructions rédaction WP
│   ├── CONV-B.md                     ← Instructions audit scientifique
│   ├── CONV-D.md                     ← Instructions observatoire résultats
│   ├── CONV-E.md                     ← Instructions codage MEPA Full
│   └── mepa_whitelist_keys.json
│
├── config/
│   ├── mepa_constants.json           ← Source unique de vérité (v1.2.3)
│   ├── mepa_friction_profile.json
│   ├── MEPA_V62_Ordre_de_Marche_1_WP-C1-1.json
│   ├── mepa_fiches_WP-F10-1_WP-I10-1.json
│   │
│   ├── fiche_etalon_WP-C1-1_Haiti_v62.json   ← Étalon ancre EROI min
│   ├── fiche_etalon_WP-EXT-5_Islande_v62.json ← Étalon ancre EROI max
│   │
│   ├── WP-C1-1_Haiti_v62.json        ← Cluster C1
│   ├── WP-C2-1_Egypte2011_v62.json   ← Cluster C2
│   ├── WP-C3-1_Argentine_v62.json    ← Cluster C5
│   ├── WP-C4-1_Liban_v62.json        ← Cluster C1
│   ├── WP-C5-1_Iran_v62.json         ← Cluster C5
│   ├── WP-C6-1_ChineXi_v62.json      ← Cluster C4
│   ├── WP-F1-1_RomeIIIe_v62.json     ← Cluster C1
│   ├── WP-F2-1_RomeTardive_v62.json  ← Cluster C1
│   ├── WP-F3-1_MayaClassique_v62.json ← Cluster C1
│   ├── WP-F4-1_EgypteAncienne_v62.json ← Cluster C5
│   ├── WP-F5-1_VeniseDéclin_v62.json  ← Cluster C2
│   ├── WP-F6-1_EmpireOttoman_v62.json ← Cluster C1
│   ├── WP-F7-1_RevolutionHaitienne_v62.json ← Cluster C1
│   ├── WP-F8-1_FranceRevolutionnaire_v62.json ← Cluster C2
│   ├── WP-F9-1_AngleterreStabilite_v62.json ← Cluster C4
│   ├── WP-F10-1_CommuneParis_v62.json ← Cluster C2
│   ├── WP-I1-1_AngleterreIndustrielle_v62.json ← Cluster C4
│   ├── WP-I2-1_Russie1917_v62.json   ← Cluster C1
│   ├── WP-I3-1_JaponMeijiGuerre_v62.json ← Cluster C5
│   ├── WP-I4-1_AllemagneNazie_v62.json ← Cluster C2
│   ├── WP-I5-1_EspagneGuerreCivile_v62.json ← Cluster C3
│   ├── WP-I6-1_Tiananmen_v62.json    ← Cluster C4
│   ├── WP-I7-1_URSS_v62.json         ← Cluster C1
│   ├── WP-I8-1_ChineDeng_v62.json    ← Cluster C4
│   ├── WP-I9-1_Singapour_v62.json    ← Cluster C4
│   ├── WP-I10-1_Rwanda_v62.json      ← Cluster C1
│   └── WP-T1-1_GuerreSecession_v62.json ← Cluster C1
│
├── documentation/                    ← Fichiers .docx, .odt, .md
│
└── outputs/                          ← Générés par le pipeline
    ├── cluster_C1/
    │   ├── results/
    │   └── rapports/
    ├── passeports/
    ├── sensitivity/
    └── certification/
```

---

## Installation et utilisation

### Prérequis

```bash
Python >= 3.9
Node.js >= 18
n8n (self-hosted — testé sur Raspberry Pi 5 / CasaOS / Docker)
```

### Dépendances Python

```bash
pip install numpy scipy --break-system-packages
```

### Variables d'environnement n8n (obligatoires)

```bash
ANTHROPIC_API_KEY=sk-ant-...
MEPA_SCRIPTS_DIR=/data/mepa/scripts
MEPA_OUTPUT_DIR=/data/mepa/outputs
MEPA_FICHE_PATH=/data/mepa/config/WP-C1-1_Haiti_v62.json
```

### Lancer une simulation directe

```bash
python3 scripts/mepa_runner_v2_gamma.py config/WP-C2-1_Egypte2011_v62.json
```

### Lancer l'analyse de sensibilité N1

```bash
python3 scripts/mepa_sensitivity_n1.py config/WP-C2-1_Egypte2011_v62.json /tmp/n1_result.json
```

### Calculer le CCI inter-codeurs

```bash
python3 scripts/mepa_kappa_calculator.py fiche_CONV-E.json fiche_CONV-B.json cci_result.json
```

### Pipeline complet via n8n

Importer `mepa_workflow_n8n_V62.json` dans votre instance n8n, configurer les variables d'environnement, puis déclencher manuellement en pointant `MEPA_FICHE_PATH` vers la fiche WP souhaitée.

**Ordre de traitement recommandé (Stratification V6.2) :**
```
Phase 1 — LOI PHYSIQUE (3 passes)    : WP-C1-1 Haïti, WP-C4-1 Liban
Phase 2 — Fondateurs calibration     : WP-I10-1 Rwanda, WP-F1-1 Rome IIIe, WP-F2-1 Rome tardive
Phase 3 — Cœur de modèle (11 WP)
Phase 4 — Zone de stress (10 WP)
  ⚠ WP-I3-1, WP-I4-1, WP-I9-1 : Sa=7 → vérifier p6×1.5 dans audit_log
```

---

## Format d'entrée — Fiche WP

```json
{
  "wp_id": "WP-C2-1",
  "cas": "Égypte 2011",
  "periode": "2010-2014",
  "cluster": "C2",
  "trajectoire_attendue": "(b) Répression réussie",
  "sa": 6,
  "sa_p6_modulation": false,
  "t_max": 300,
  "theta_C": 0.30,
  "theta_I": 0.22,
  "conditions_initiales": { "S0": 1.1, "L0": 0.4, "C0": 0.10, "I0": 6.0 },
  "commandes": {
    "T": 0.9, "Mob": 0.6, "R": 2.5, "Ref": 0.10,
    "Rc": 0.5, "Rn": 0.2, "E": 0.7,
    "gamma": 0.55,
    "EROI": 4.0, "Pop": 1.0
  }
}
```

> ⚠️ La clé `gamma` est la seule forme acceptée. Les clés `g` ou `Gamma` sont rejetées par C4 du Nœud 2.
>
> ⚠️ Pour Cluster C1 (EROI dynamique), `cmd_linear.EROI: { start, end }` est obligatoire (contrôle C11).

---

## Trajectoires diagnostiquées

**9 labels D4 officiels** (source : `mepa_constants.json` v1.2.3, `labels_trajectoire_d4.labels`) :

| Label complet | Code | Condition principale | Produit par l'arbre auto |
|---|---|---|---|
| `(a) Rupture transformatrice` | (a) | F≥R, ΔC_rel > θ_C, dC/dt > 0 à t_b | ✓ |
| `(b) Répression réussie` | (b) | F < R sur tout t_max, Rc+Rn > 0.6 | ✓ |
| `(c) Stase / ambigu` | (c) | Bascule sans dominance nette | ✓ |
| `(d) Effondrement progressif` | (d) | ΔI_rel > θ_I ET ΔC_rel < θ_C | ✓ |
| `(d) Dissolution` | (d) var. | F≥R, Ref>0.35, Rc+Rn<0.35 (Manuel Gouvernance Annexe A) | ✗ — LOI PHYSIQUE |
| `(e) Réforme institutionnelle` | (e) | Bascule avec Ref>0.35 et Rc+Rn<0.35 | ✓ |
| `(h) Stabilité` | (h) | F < R, répression faible | ✓ |
| `(h)/(e) Stabilité ou réforme lente` | (h)/(e) | F < R sur tout t_max, Rc+Rn ≤ 0.6 | ✓ |
| `(γ) Transformation forcée` | (γ) | Cas extrêmes (WP-I5-1 Espagne, WP-T1-1 Sécession) | ✗ — `trajectoire_forcee` |

> Les labels `(d) Dissolution` et `(γ) Transformation forcée` ne sont pas produits automatiquement par l'arbre de décision. Ils sont assignés via la clé `trajectoire_forcee` dans la fiche ou via le protocole LOI PHYSIQUE (3 passes).

---

## Contrôle qualité

### Seuils de validation inter-codeurs

| Métrique | Certifié | Révision | Rejet |
|---|---|---|---|
| CCI par variable (continues) | ≥ 0.70 | 0.50–0.69 | < 0.50 |
| κ de Cohen (Sa catégorielle) | ≥ 0.70 | 0.50–0.69 | < 0.50 |
| CCI global agrégé | ≥ 0.75 | 0.55–0.74 | < 0.55 |

### Critères de certification WP (Nœud 14)

Un WP est classé `WP_CERTIFIÉ` si et seulement si :
- CCI global ≥ 0.75
- Robustesse N1 = ROBUSTE ou MÉTASTABLE
- Concordance trajectoire = OUI
- CONV-B verdict = CERTIFIÉ

Sinon : `WP_EXPLORATOIRE` (résultats disponibles mais non certifiables sans révision).

---

## Feuille de route V7

- [ ] Implémentation θ_C adaptatif (0.15 si C0 ≥ 0.4)
- [ ] Nouveaux WP : Portugal 1974, New Deal 1933, Espagne démocratique 2010
- [ ] Calibration bayésienne complète post-27 WP (après Cluster C1 complet)
- [ ] Plancher de complexité I_min dynamique
- [ ] Extension cluster C6 (réservé)
- [ ] Résolution mapping Cs → Mob (variable intermédiaire dédiée)
- [ ] Analyse d'identifiabilité structurelle (Annexe Addendum Théorique)

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

## Licence

Ce projet est distribué sous **double licence** :

- **Documentation, fiches WP et cadre théorique** (fichiers `.md`, `.docx`, `.odt`, `.json` de codage)
  → [CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/) — Attribution obligatoire, pas de version modifiée redistribuable.

- **Scripts de simulation et d'audit** (`mepa_runner_v2_gamma.py`, `mepa_sensitivity_n1.py`, `mepa_kappa_calculator.py`, `mepa_passeport_schema.py`, `mepa_node2_audit_v62.js`, `correctif_V5_compteur_CCI.js`)
  → [MIT License](https://opensource.org/licenses/MIT) — Libre utilisation, modification et redistribution avec attribution.

© 2026 — [toto-blanco](https://github.com/toto-blanco)

*MEPA V6.2 — Mars 2026*
