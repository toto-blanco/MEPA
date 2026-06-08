# MEPA V6.2 — Modèle Énergétique du Potentiel Adaptatif

> Simulation des transitions socio-institutionnelles sur 27 cas historiques via équations différentielles couplées, pipeline n8n automatisé, audit inter-codeurs (CCI / κ de Cohen) et analyse de sensibilité bayésienne.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![Node.js](https://img.shields.io/badge/Node.js-18+-339933?logo=nodedotjs&logoColor=white)](https://nodejs.org)
[![n8n](https://img.shields.io/badge/Orchestration-n8n-EA4B71)](https://n8n.io)
[![Claude](https://img.shields.io/badge/Claude-Anthropic-D4A017)](https://www.anthropic.com)
[![Raspberry Pi](https://img.shields.io/badge/Infra-Raspberry_Pi_5-A22846?logo=raspberrypi&logoColor=white)](https://www.raspberrypi.com)
[![License](https://img.shields.io/badge/License-CC_BY--ND_4.0-lightgrey)](https://creativecommons.org/licenses/by-nd/4.0/)

---

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Rôle de Claude dans MEPA](#rôle-de-claude-dans-mepa)
3. [Architecture du projet](#architecture-du-projet)
4. [Corpus historique (27 WP)](#corpus-historique-27-wp)
5. [Cadre théorique](#cadre-théorique)
6. [Pipeline technique](#pipeline-technique)
7. [Structure des fichiers](#structure-des-fichiers)
8. [Installation et utilisation](#installation-et-utilisation)
9. [Format d'entrée — Fiche WP](#format-dentrée--fiche-wp)
10. [Trajectoires diagnostiquées](#trajectoires-diagnostiquées)
11. [Contrôle qualité](#contrôle-qualité)
12. [Feuille de route V7](#feuille-de-route-v7)
13. [Références](#références)

---

## Vue d'ensemble

**MEPA** (Modèle Énergétique du Potentiel Adaptatif) est un cadre de modélisation quantitatif-qualitatif conçu pour analyser les **transitions socio-institutionnelles** à travers l'histoire. Le modèle postule que tout système socio-politique bascule lorsque la force transformatrice `F(t)` dépasse la résistance du système `R(t)`.

Le projet V6.2 couvre **27 Working Papers (WP)** répartis sur cinq clusters thématiques (C1–C5), de la Rome du IIIe siècle au Rwanda contemporain, en passant par la Révolution française, la montée du nazisme ou l'effondrement de l'URSS.

### Deux composantes complémentaires

| Composante | Rôle | Outils |
|---|---|---|
| **MEPA Full** | Codage qualitatif de 9 variables sur sources historiques, audit inter-codeurs, rédaction des WP | Fiches JSON · CCI · **Claude** (CONV-A, CONV-B, CONV-E) |
| **MEPA Lite** | Simulation numérique de 4 équations différentielles couplées | `mepa_runner_v2_gamma.py` · n8n |

---

## Rôle de Claude dans MEPA

Claude (API Anthropic) n'est pas un outil parmi d'autres dans MEPA : il est l'**opérateur central de la chaîne qualitative** et le **partenaire de développement du cadre théorique**. Il intervient sous quatre rôles distincts, chacun isolé par le protocole double aveugle du pipeline.

### Les quatre rôles CONV

| Rôle | Conv | Mission | Modèle |
|---|---|---|---|
| **Historien-Codeur** | CONV-E | Coder les 9 variables MEPA sur sources historiques primaires, produire les fiches JSON conformes au schéma `mepa-fiche-codage-v6.2` | claude-sonnet-4-6 (T=0) |
| **Auditeur scientifique** | CONV-B | Codage indépendant (double aveugle), calcul du CCI / κ de Cohen, audit des 7 sections du WP final | claude-sonnet-4-6 (T=0) |
| **Rédacteur** | CONV-A | Rédiger les sections S1–S7 du Working Paper depuis les résultats de simulation, sans accès aux scores du codeur | claude-sonnet-4-6 (T=0) |
| **Architecte scientifique / QG** | CONV-C | Co-développement du cadre théorique et de l'architecture du modèle : critique épistémique, décisions d'architecture (équations, paramètres, protocoles), préparation des chantiers V7 | claude-sonnet-4-6 |

> **Note sur CONV-C.** Le rôle QG va au-delà de l'usage API classique. Il s'agit d'une collaboration stratégique sur la théorie du modèle — vérification des équations différentielles, cohérence des paramètres, définition des prédictions falsifiables, feuille de route V7. C'est dans ce rôle que l'architecture V6.2 a été fortifiée, que les chantiers Dev 1–Dev 3 ont été instruits, et que les décisions collégiales CV1–CV11 ont été formalisées.

### Étanchéité informationnelle

Le protocole garantit que CONV-E (codeur) et CONV-B (auditeur) opèrent **sans accès aux résultats l'un de l'autre** jusqu'au calcul du CCI. La mesure de reproductibilité est conditionnelle au modèle LLM utilisé — non une indépendance absolue inter-codeurs humains. Ce point est documenté dans l'Addendum Théorique V6.2 (Pilier 4) et tracé dans chaque passeport via le champ `provenance_ia`.

### Traçabilité

Chaque résultat de simulation embarque dans son passeport de certification le modèle exact utilisé :

```json
"provenance_ia": {
  "modele": "claude-sonnet-4-6",
  "famille": "Claude 4",
  "fournisseur": "Anthropic",
  "temperature": 0.0,
  "protocole": "Double aveugle n8n — étanchéité informationnelle garantie par le workflow"
}
```

---

## Architecture du projet

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Fiche WP (JSON)                                                        │
│     ↓                                                                   │
│  [Nœud 2] Audit C1–C13     →  INVALIDE : recodage CONV-E (Claude)      │
│                             →  DONNÉES_INSUFFISANTES : escalade Archi.  │
│     ↓ VALIDE                                                            │
│  [Nœud 8a] CONV-B (Claude) — CCI pré-simulation (double aveugle)       │
│     ↓ valeurs résolues injectées                                        │
│  [Nœud 4] Runner Python (ODE Euler dt=1) + [Nœud 4b] Sensibilité N1   │
│     ↓                                                                   │
│  [Nœud 6] CONV-A (Claude) — Rédaction WP S1→S7 (T=0)                  │
│     ↓                                                                   │
│  [Nœud 7] CONV-B (Claude) — Audit WP complet C1–C5                    │
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

> **Rappel de nomenclature :** Les clusters **C1–C5** ci-dessous sont les clusters **MEPA** (déterminés par la dynamique du modèle), non des catégories éditoriales.

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
>
> **Note mapping Cs → Mob :** La variable Cs (crédibilité du régime) est mappée vers la commande runner `Mob` — approximation connue, à résoudre en V7 (chantier C0).

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
     ├─ INVALIDE     → Alerte recodage CONV-E (Claude)
     └─ DONNÉES_INSUFFISANTES → Alerte escalade Architecte
     ↓ VALIDE
N8a  CONV-B (Claude) — codage indépendant + CCI pré-simulation [double aveugle, T=0]
N8b  Router CCI — AUTO / WAIT_HUMAIN
     ├─ WAIT → N8c Validation humaine
     └─ AUTO →
N8d  Injection valeurs résolues dans runner_config
N3   Write runner_config.json [/tmp/]
N4   Execute Runner [mepa_runner_v2_gamma.py v2.1.1]  ←─ parallèle
N4b  Execute Sensibilité N1 [mepa_sensitivity_n1.py]  ←─ parallèle
N5   Parse Runner Result
N5b  Parse Sensibilité N1
N6   CONV-A (Claude) — Rédaction WP S1→S7 [T=0, sans accès scores codeur]
NC   Nettoyage /tmp/ [Anti-Contamination]
N7   CONV-B (Claude) — Audit WP complet C1–C5
     Router CONV-B → CERTIFIÉ / RÉVISION_MINEURE / RÉVISION_MAJEURE / REJET
N12  Stress-test N2 [combinaisons critiques optimiste/pessimiste]
N13  Prédiction Popper [RF1/RF2/RF3 + horizon temporel]
N14  Certification [WP_CERTIFIÉ / WP_EXPLORATOIRE]
N15  Archivage Final [/data/mepa/outputs/ + Passeport compact CONV-D]
```

### Scripts et nœuds associés

| Script | Nœud | Rôle | Claude | Seuil bloquant |
|---|---|---|---|---|
| `mepa_node2_audit_v62.js` | N2 | Validation structurelle C1–C13, normalisation `gamma`, détection NC | — | INVALIDE ou DONNÉES_INSUFFISANTES |
| `mepa_runner_v2_gamma.py` | N4 | Simulation ODE Euler dt=1 + stress N1 interne | — | RuntimeError NC bloquant |
| `mepa_sensitivity_n1.py` | N4b | Sensibilité ±20% (9 cmd + 16 params) | — | flag verdict_n1 |
| `mepa_kappa_calculator.py` | N8a | CCI / κ de Cohen CONV-E / CONV-B | Post-codage Claude | CCI < 0.50 → REJET |
| `mepa_passeport_schema.py` | N15 | Construction + validation Passeport WP | Trace `provenance_ia` Claude | toute erreur bloquante |
| `CONV-E.md` | — | Instructions codage historien | **CONV-E** (Claude, T=0) | — |
| `CONV-A.md` | N6 | Instructions rédaction WP | **CONV-A** (Claude, T=0) | — |
| `CONV-B.md` | N8a, N7 | Instructions audit scientifique | **CONV-B** (Claude, T=0) | — |
| `CONV-D.md` | N15 | Instructions observatoire résultats | **CONV-D** (Claude) | — |

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
│   ├── mepa_passeport_schema.py      ← Passeport WP (trace provenance_ia Claude)
│   ├── mepa_node2_audit_v62.js       ← Audit conformité (v2.1.0 référence doc.)
│   ├── correctif_V5_compteur_CCI.js  ← Correctif compteur CCI V5
│   ├── mepa_pipeline_architecture_V62.md
│   ├── prompt_projet_MEPA_V3_gamma.md ← Prompt système Claude CONV-E
│   ├── CONV-A.md                     ← Instructions Claude — rédaction WP
│   ├── CONV-B.md                     ← Instructions Claude — audit scientifique
│   ├── CONV-D.md                     ← Instructions Claude — observatoire résultats
│   ├── CONV-E.md                     ← Instructions Claude — codage MEPA Full
│   └── mepa_whitelist_keys.json
│
├── config/
│   ├── mepa_constants.json           ← Source unique de vérité (v1.2.3)
│   ├── mepa_friction_profile.json
│   ├── MEPA_V62_Ordre_de_Marche_1_WP-C1-1.json
│   ├── mepa_fiches_WP-F10-1_WP-I10-1.json
│   ├── fiche_etalon_WP-C1-1_Haiti_v62.json   ← Étalon ancre EROI min
│   ├── fiche_etalon_WP-EXT-5_Islande_v62.json ← Étalon ancre EROI max
│   └── WP-*.json                     ← 27 fiches WP
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

```
Python >= 3.9
Node.js >= 18
n8n (self-hosted — testé sur Raspberry Pi 5 / CasaOS / Docker)
Compte API Anthropic (Claude — pour CONV-A, CONV-B, CONV-E)
```

### Dépendances Python

```bash
pip install numpy scipy --break-system-packages
```

### Variables d'environnement n8n (obligatoires)

```bash
ANTHROPIC_API_KEY=sk-ant-...      # Clé API Claude (Anthropic) — CONV-A, CONV-B, CONV-E
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

Importer `mepa_workflow_n8n_V62.json` dans votre instance n8n, configurer les variables d'environnement (dont `ANTHROPIC_API_KEY`), puis déclencher manuellement en pointant `MEPA_FICHE_PATH` vers la fiche WP souhaitée.

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

**9 labels D4 officiels** (source : `mepa_constants.json` v1.2.3) :

| Label complet | Code | Condition principale | Produit par l'arbre auto |
|---|---|---|---|
| `(a) Rupture transformatrice` | (a) | F≥R, ΔC_rel > θ_C, dC/dt > 0 à t_b | ✓ |
| `(b) Répression réussie` | (b) | F < R sur tout t_max, Rc+Rn > 0.6 | ✓ |
| `(c) Stase / ambigu` | (c) | Bascule sans dominance nette | ✓ |
| `(d) Effondrement progressif` | (d) | ΔI_rel > θ_I ET ΔC_rel < θ_C | ✓ |
| `(d) Dissolution` | (d) var. | F≥R, Ref>0.35, Rc+Rn<0.35 | ✗ — LOI PHYSIQUE |
| `(e) Réforme institutionnelle` | (e) | Bascule avec Ref>0.35 et Rc+Rn<0.35 | ✓ |
| `(h) Stabilité` | (h) | F < R, répression faible | ✓ |
| `(h)/(e) Stabilité ou réforme lente` | (h)/(e) | F < R sur tout t_max, Rc+Rn ≤ 0.6 | ✓ |
| `(γ) Transformation forcée` | (γ) | Cas extrêmes (WP-I5-1 Espagne, WP-T1-1 Sécession) | ✗ — `trajectoire_forcee` |

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
- CONV-B (Claude) verdict = CERTIFIÉ

Sinon : `WP_EXPLORATOIRE` (résultats disponibles mais non certifiables sans révision).

---

## Feuille de route V7

- [ ] Intégration Dev 1 — chaîne biophysique EROI→S\*→A_d_max (en advisory depuis V6.3)
- [ ] Intégration Dev 2 — dette D(t) comme variable d'état (découplage temporaire surplus)
- [ ] Intégration Dev 3 — technologie T(t) comme modificateur endogène de l'EROI
- [ ] Implémentation θ_C adaptatif (0.15 si C0 ≥ 0.4)
- [ ] Nouveaux WP : Portugal 1974, New Deal 1933, Espagne démocratique 2010
- [ ] Calibration bayésienne complète post-27 WP (après Cluster C1 complet)
- [ ] Résolution mapping Cs → Mob (chantier C0 — variable intermédiaire dédiée)
- [ ] Extension cluster C6 (réservé)
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

---

## 🤖 Collaboration avec Claude (Anthropic)

Ce projet a été développé en collaboration active avec **Claude Sonnet** et **Claude Opus** (Anthropic).

**Ce que Claude a fait :**
La rédaction du code a été intégralement déléguée à Claude : scripts Python du pipeline de simulation (`mepa_runner_v2_gamma.py`, `mepa_kappa_calculator.py`, `mepa_sensitivity_n1.py`, `mepa_passeport_schema.py`), nœuds JavaScript des 26 étapes du workflow n8n (`mepa_node2_audit_v62.js`, correctifs A1–A6), et débogage itératif en conditions réelles (race conditions, correctifs architecture, gestion des edge cases statistiques).

**Ce que j'ai fait :**
La conception de l'architecture complète — séparation des rôles entre agents (CONV-E codeur historique, CONV-A rédacteur à T=0, CONV-B auditeur, CONV-D observatoire), protocole de double aveugle inter-codeurs (CCI / κ de Cohen), checklist C1–C13 de validation des données, checklist C1–C5 de détection du narrative smoothing, système de certification WP_CERTIFIÉ / WP_EXPLORATOIRE. Les 27 cas historiques du corpus, les hypothèses théoriques du modèle (équations F/R, 13 paramètres dynamiques), et la validation de chaque output produit par le pipeline.

**Pourquoi cette transparence ?**
L'IA agentique est un outil de production — pas un substitut à la conception. Architecturer un système multi-agents avec des contraintes méthodologiques explicites, déléguer l'implémentation, auditer les résultats : c'est la posture d'un chef de projet IA, pas d'un développeur.
