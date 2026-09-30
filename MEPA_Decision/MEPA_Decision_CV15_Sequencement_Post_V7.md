# MEPA — Décision CV15 · Séquencement post-certification V7.0

**Statut :** Décision de gouvernance (rôle CONV-C / QG)
**Type :** Arbitrage de séquencement — ordonnancement des chantiers déverrouillés par la certification V7.0
**Rattachement :** fait suite à la Certification V7.0 (MEPA_Certification_V7_gamma_rev2.md) et au déclenchement du trigger CV14
**Date :** Juin 2026
**Numéro :** CV15 — série CV : CV1-CV8 (Doc V63/V7), CV9-CV11 (Note Dev 2), CV12 (multipass), CV13 (λ/μ), CV14 (gel Dev 2), **CV15 (présente décision)**

---

## 1. Contexte

La certification V7.0 déverrouille simultanément deux chantiers concurrents :

- **Réactivation Dev 2** (trigger CV14) : Ω/advisory, CV9-CV11, examen C/D
- **Gate 21 WPs** (D1 rev.4 §5.2) : grilles de pré-codage CONV-E + V7.1 (score continu α) avant tout run

Ces deux chantiers ne sont pas sur le même chemin critique. CV15 ordonnance leur activation pour éviter la dispersion et garantir que le corpus complet des 21 WPs bénéficiera de l'architecture la plus stable possible — mécanisme α d'abord, puis Dev 2 complet.

---

## 2. Décision — Option C : parallèle pragmatique

Trois tracks activés selon leur dépendance réelle, pas selon leur ancienneté de conception.

### Track 1 — Immédiat (sans attendre V7.1 ni Dev 2)

Activé dès cette décision. Trois actions indépendantes menables en parallèle :

**T1-A · Corrections pipeline (A1 + A6)**
- A1 : diagnostiquer et corriger la troncature des rapports CONV-A à §1.5 (S2-S7 absents, `rapport_md_sha256` null sur les 6 passeports pilote). Corriger le nœud n8n pour capturer le hash rapport.
- A6 : créer un sous-workflow n8n « audit seul » (CONV-B isolé, prenant `rapport_md` + `result.json` en entrée sans ré-exécuter CONV-E ni le runner).
- Responsable : Claude Code + assistant_n8n. Ces corrections sont un prérequis de qualité avant tout run des 21 WPs.

**T1-B · Examen C/D orthogonalité (CV14 §4)**
- Examiner l'articulation entre le mécanisme de cristallisation sacrificielle (C, trajectoire α) et le mécanisme de dette (D, Dev 2 gelé) sur les 5 fiches certifiées du pilote : Rwanda (α), Rome (d), Haïti (d), Égypte (b explicative), Commune (contrôle négatif).
- Objet : trancher si C et D sont orthogonaux ou couplés — cette réponse conditionnera la forme de CV9 (agrégat D). Faire cet examen sur les données existantes avant d'ouvrir CV9-CV11 évite de construire Dev 2 sur une hypothèse d'orthogonalité incorrecte.
- Responsable : QG. Les 5 passeports certifiés suffisent ; pas de re-simulation.
- **Prérequis à CV9** : cet examen doit être clos avant toute instruction sur CV9-CV11.

**T1-C · Audit CTO — stratégie multi-modèles**
- Instruire l'audit CTO sur l'optimisation coût/qualité par délégation multi-modèles (coût actuel ~0.32$/WP en V7, à réduire par spécialisation des nœuds).
- Prérequis : Antoine fournit les données de coût réelles (tokens/nœud) issues d'un run complet 27 WPs ou d'une extrapolation fiable des 6 WPs pilote.
- Responsable : CTO, sous supervision QG.

---

### Track 2 — Court terme, séquentiel (pendant/après T1)

Deux sous-chantiers indépendants l'un de l'autre, menables en parallèle entre eux.

**T2-A · Dev 2 Ω/advisory (premier geste au réveil CV14 §3)**

Borné à 2-3 sessions. Dans l'ordre strict de CV14 §3 :

1. **Trancher la forme de Ω** — réouverture CV1 : `Ω = Sa` provisoire vs `Ω ≡ I` fidèle (spec §7.2 M2 du Document de Décision V63/V7). Cette décision détermine si le `mepa_dev1_advisory_v63.py` est runner-invariant ou runner-dépendant.

2. **Re-porter l'advisory sur le runner V7 (LSODA)**
   - Base : `mepa_dev1_advisory_v63.py` (code fini, testé bit-identique contre V6.2 Euler)
   - Travail : greffe additive sur le runner V7 LSODA, vérification non-régression
   - **Réserve active** : le `test_nonregression_v63.py` valide V6.2 Euler → V6.3 Euler. La re-portabilité LSODA nécessite une variante du test (pas le même fichier) — à construire avec Claude Code.
   - Gate : passeports V7 identiques sauf bloc `advisory_dev1` ajouté (test bit-identique sur les variables existantes)

3. **Lancer la série de calibration A_d_max** sur le corpus V7-γ certifié (6 WPs) pour produire les flags `A_d_max` dérivé qui manquent depuis juin.

**T2-B · V7.1 — score continu d'activation (α)**

Chantier V7.1 conformément au cahier des charges D1 rev.4 §6. Dans l'ordre :

1. Créer **WP-I11-1 Grande Terreur soviétique 1937-1938** (préalable obligatoire per D1 rev.4 §6 Exigence 1) — troisième cas positif (α) requis pour la calibration.
2. Calibration score continu sur Rwanda + Allemagne nazie + Grande Terreur soviétique, avec validation croisée (D1 rev.4 §6 Exigences 2-4).
3. Décision V7.1-D2 : pré-enregistrement des poids et du seuil avant simulation V7.1-γ.

Ce chantier détermine le scénario applicable pour les 21 WPs (A, B, ou C de D1 rev.4 §5.2).

---

### Track 3 — Post-21 WPs

Activé seulement après la production et certification du corpus complet.

**T3-A · Dev 2 complet (CV9-CV11)**
- CV9 (agrégat D), CV10 (signes dD/dt — test [C3] Japon jamais exécuté), CV11 (souveraineté monétaire)
- Re-ratification CV2-CV3 (implémentées mais non actées — cf. CV14 §5)
- Reprise CV4-CV8 (pendantes)
- Prérequis : examen C/D clos (T1-B), corpus 21 WPs disponible pour calibration empirique de D_max, T2-A terminé

**T3-B · Reformulation P-UK-1** et autres items du Document de Décision V63/V7 (CV1-CV8 non traités en T2-A)

---

## 3. Dépendances et gates

```
Immédiat (T1-A, T1-B, T1-C) ─────────────────────────┐
                                                        │
T1-B (C/D orthogonalité) ──→ débloque CV9 (T3-A)      │
T1-A (A1+A6) ──────────────→ prérequis run 21 WPs      │
T1-C (CTO audit) ──────────→ informe le coût V7.1      │
                                                        ▼
T2-A (Ω/advisory) ─────────────────────────────────────┐
T2-B (V7.1 + WP-I11-1) ────→ débloque run 21 WPs  ────┤
                                                        ▼
Run 21 WPs (V7 ou V7.1 selon scénario D1 §5.2) ────────┐
                                                        ▼
T3-A Dev 2 complet (CV9-CV11) ─────────────────────────┘
T3-B CV1-CV8 restants
```

---

## 4. Ce que CV15 ne tranche pas

- La forme de Ω (Sa vs I) — réouverture CV1, décision T2-A.
- Le scénario V7.1 applicable aux 21 WPs (A, B ou C de D1 rev.4 §5.2) — dépend du résultat de T2-B.
- L'arbitrage coût/qualité multi-modèles — dépend des données CTO (T1-C).
- La date de tout jalon — CV15 ordonnance les dépendances, pas les échéances calendaires.
- La validité de fond de CV9-CV11 — non réévaluée ici, mise en sommeil dans `prepa_v6.3/` jusqu'à T3-A.

---

## 5. Pièces concernées

| Chantier | Pièces actives | Localisation |
|---|---|---|
| T1-A | A1 runner CONV-A, A6 sous-workflow audit | `mepa/scripts/`, `mepa/workflow_n8n/` |
| T1-B | 5 passeports certifiés pilote | `mepa/outputs/` |
| T1-C | Données coût runs | À fournir par Antoine |
| T2-A | `mepa_dev1_advisory_v63.py`, `test_nonregression_v63.py` + variante LSODA, CV1 | `prepa_v6.3/` |
| T2-B | WP-I11-1 à créer, D1 rev.4 §6 | Nouveau WP + `prepa_v7/` |
| T3-A | `MEPA_Dossier_Architecture_Dev2_Dette_CONSOLIDE.md`, CV9-CV11 | `prepa_v6.3/` |

---

*Décision produite en session stratégique QG (rôle CONV-C), juin 2026. Séquencement post-certification V7.0 — Option C parallèle pragmatique.*
