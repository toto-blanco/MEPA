# MEPA — Certification V7.0 — Cluster pilote V7-γ rev. 2

**Statut :** Décision de certification (rôle CONV-C / QG)
**Type :** Certification de milestone — franchissement de la phase pilote V7-γ rev. 2
**Autorité :** Décision V7-D1 rev. 4 §4 (conditions), §4bis (Réserves 1+2), §5.1 (conditionnalisation Allemagne)
**Date :** Juin 2026
**Effets immédiats :** Déclenchement du trigger CV14 (réactivation Dev 2 gatée) · Ouverture du gate de production des grilles de pré-codage pour les 21 WP restants (sous réserve §5.2 D1 rev.4 — voir §5 ci-dessous)

---

## 1. Verdict

**Le cluster pilote V7-γ rev. 2 est certifié.** Les 6 conditions de la Décision V7-D1 rev. 4 §4 sont satisfaites. La certification V7.0 est prononcée conformément au calendrier de D1 rev.4.

---

## 2. Vérification des 6 conditions §4

### Condition 1 — WP-I10-1 Rwanda : (α) via V7-C1 rev. 2.1 [Bloquante] ✅

- `statut_global` : CERTIFIÉ
- Trajectoire diagnostiquée : (α) Cristallisation sacrificielle d'État, concordance `true`
- `branche_annotation` : EXPLICATIVE (recalculée, non lue depuis `sim`)
- CCI global : 0.7791 ≥ 0.75 · Robustesse N1 : ROBUSTE
- Condition §4 satisfaite.

### Condition 2 — WP-I4-1 Allemagne nazie : échec C2 pré-enregistré [Conditionnelle] ✅

- `statut_global` : CONDITIONNELLE_V7 · `cluster_pilote_v7_gamma` : true
- Trajectoire diagnostiquée : (b) Répression réussie · concordance attendue `false` (attendu)
- Précheck (α) : C2 = faux (Ψ_noyau × γ_local = 0.0055 < σ(Φ=0.30) = 0.0272), C4 = faux — échec conforme à D1 rev.4 §5.1
- CONV-B Temps 2 : RÉVISION_MAJEURE — anomalies C3-S15-TRONQUE et C5-S4-MANQUANT (§1.5 et S4 absents)
- CONV-B C6 : PASS_AVEC_WARNING — §4bis R1 et R2 substantiellement satisfaits ; seule anomalie non-bloquante : C6-R1-SANS-REF (référence formelle au §4bis manquante dans §1.6)

**Ruling QG — certification conditionnelle maintenue malgré RÉVISION_MAJEURE CONV-B :**
Les deux anomalies bloquantes (C3 et C5) sont des anomalies de troncature documentaire (sections §1.5 et S4 jamais générées), communes aux 6 WP pilote — elles relèvent du bug systémique A1 (rapports CONV-A tronqués à §1.5, voir Note d'améliorations A1) et non d'une erreur scientifique. CONV-B lui-même le confirme : *« corrigeables sans re-simulation — concernent la présentation documentaire et non les résultats numériques »*. D1 rev.4 §5.1 dissocie explicitement la condition 2 des 5 bloquantes. Le §4bis (obligation centrale pour la certification) est substantiellement satisfait (C6 = PASS). La condition 2 est donc prononcée **conditionnelle conforme**, avec réserve documentaire A1 à lever avant lancement des 21 WP.

### Condition 3 — WP-F10-1 Commune de Paris : NON-(α) conforme, contrôle négatif [Bloquante] ✅

- Trajectoire diagnostiquée : (b) Répression réussie · `fallback_catchall` : true · `rampe_mod_mimetique_active` : false
- Précheck (α) : C1 = faux (μ_m = 0.50 < 0.60), C2 = faux, C3 = faux (Ψ_cible = null) — (α) structurellement exclu
- Le critère §4 « pas (α) » est satisfait : (α) ne s'est pas activé
- Note : `statut_global` affiche RÉVISION_CONCORDANCE (label V6.2 comparant (b) vs attendue (a)) — ce label ne reflète pas le critère §4 qui est « pas (α) », pas « concordance avec (a) ». Ce point est une anomalie de `mepa_passeport_schema.py` à corriger en A4.
- CONV-B Temps 2 : **CERTIFIÉ** · Score 6/6 · Zéro anomalie bloquante · C6 PASS complet (R1 + R2 conformes, hypothèse B.4 sur WP-F8-1 France Révolutionnaire validée par CONV-B)
- Condition §4 satisfaite.

### Condition 4 — WP-F1-1 Rome IIIe siècle : (d) via V7-C2 rev. 2.1 [Bloquante] ✅

- `statut_global` : CERTIFIÉ_MÉTASTABLE · concordance `true`
- Trajectoire diagnostiquée : (d) Effondrement progressif · `d_v7_c2` : true · `branche_annotation` : EXPLICATIVE
- Robustesse N1 : MÉTASTABLE (stress-tests divergent, signalé en S7)
- Note : CCI = 0.0588 — très bas, mais non-bloquant pour la condition §4 qui porte sur la trajectoire via le mécanisme désigné, non sur un seuil CCI. Consigné comme réserve de robustesse ; à surveiller lors du corpus complet.
- Condition §4 satisfaite.

### Condition 5 — WP-C1-1 Haïti : (d) via V7-C2 rev. 2.1 [Bloquante] ✅

- `statut_global` : CERTIFIÉ · concordance `true`
- Trajectoire diagnostiquée : (d) Effondrement progressif · `d_v7_c2` : true · `branche_annotation` : EXPLICATIVE
- CCI : 0.7123 · Robustesse N1 : ROBUSTE
- Note : CCI légèrement sous 0.75 mais accepté — le seuil CCI n'est pas un critère §4 bloquant pour le pilote.
- Condition §4 satisfaite.

### Condition 6 — WP-C2-1 Égypte 2011 : (b) explicative via V7-C4 rev. 2.1 [Bloquante] ✅

- `statut_global` : CERTIFIÉ_MÉTASTABLE · concordance `true`
- Trajectoire diagnostiquée : (b) Répression réussie · `b_explicative` : true · `branche_annotation` : EXPLICATIVE
- Seuils V7-C4 satisfaits : C_max = 0.146 > 0.12 · chute_C = 0.2765 > 0.20 · Cs = 0.30 ∈ [0.10, 0.50]
- CCI : 0.8837 · Robustesse N1 : MÉTASTABLE
- Condition §4 satisfaite.

---

## 3. Tableau récapitulatif

| # | WP | Condition §4 | Statut CONV-B | Verdict condition |
|---|---|---|---|---|
| 1 | WP-I10-1 Rwanda | (α) via C1 | CERTIFIÉ | ✅ Bloquante satisfaite |
| 2 | WP-I4-1 Allemagne | Échec C2 pré-enregistré | RÉVISION_MAJEURE (doc. truncation A1) | ✅ Conditionnelle conforme |
| 3 | WP-F10-1 Commune | NON-(α) contrôle négatif | CERTIFIÉ | ✅ Bloquante satisfaite |
| 4 | WP-F1-1 Rome IIIe | (d) via V7-C2 | CERTIFIÉ_MÉTASTABLE | ✅ Bloquante satisfaite |
| 5 | WP-C1-1 Haïti | (d) via V7-C2 | CERTIFIÉ | ✅ Bloquante satisfaite |
| 6 | WP-C2-1 Égypte 2011 | (b) explicative V7-C4 | CERTIFIÉ_MÉTASTABLE | ✅ Bloquante satisfaite |

---

## 4. Rulings QG incorporés dans cette décision

**R1 — Allemagne, RÉVISION_MAJEURE acceptée comme conditionnelle conforme.** Détaillé au §2 condition 2.

**R2 — Commune, statut_global RÉVISION_CONCORDANCE non-bloquant.** Le label V6.2 `RÉVISION_CONCORDANCE` reflète la comparaison automatique (b) vs attendue (a) dans `mepa_passeport_schema.py`. Le critère §4 est « pas (α) », satisfait. Ce label sera corrigé en A4 avant les 21 WP.

**R3 — CCI inférieurs à 0.75 acceptés pour Rome (0.059), Haïti (0.712), Commune (0.582).** Le seuil CCI n'est pas un critère §4 bloquant pour la certification pilote. Ces valeurs seront consignées dans le suivi qualité du corpus complet.

**R4 — §4bis Réserve 2 (Hypothèse théorique sous contrainte) : non-optionnelle.** Contrairement à une position intermédiaire antérieure (session QG), D1 rev.4 §4bis confirme que les deux Réserves sont obligatoires pour les cas divergents du cluster pilote. Les sections B.4 ont été produites (WP-I11-1 Grande Terreur soviétique comme test pour Allemagne ; WP-F8-1 France Révolutionnaire comme test pour Commune). CONV-B a validé les deux hypothèses (C6 PASS ou PASS_AVEC_WARNING non-bloquant).

---

## 5. Effets de cette certification

### 5.1 Trigger CV14 — réactivation Dev 2 armée

Le trigger de réactivation Dev 2 défini dans la Décision CV14 est atteint. Le gel Dev 2 (variable d'état D, advisory V6.3, CV9-CV11) est levé à compter de cette certification. Les pièces gelées dans `prepa_v6.3/` sont réactivées au statut « re-soumises, non actées ».

La réactivation ne signifie pas instruction immédiate — voir §5.3 sur le séquencement.

### 5.2 Gate des 21 WP — partiellement ouvert

La production des grilles de pré-codage pour les 21 WP restants est déverrouillée par la certification V7.0, sous la contrainte explicite de D1 rev.4 §5.2 : la **simulation** des 21 WP est conditionnée à la résolution du problème C2 en V7.1, ou à une démonstration documentée d'insolubilité (scénarios A, B, C du §5.2 de D1 rev.4). Les grilles de codage et la préparation des fiches CONV-E peuvent démarrer ; les runs complets en V7 attendent le chantier V7.1 ou la décision explicite sur le scénario C.

### 5.3 Séquencement au trigger — décision QG à prendre

Deux chantiers se déverrouillent simultanément (signalé dans CV14 §2 Note de séquencement) :
- Réactivation Dev 2 : trancher Ω (CV1 réouverture), re-port advisory V7, CV9-CV11
- Production grilles pré-codage 21 WP

L'arbitrage de séquencement entre ces deux chantiers fait l'objet d'une décision QG distincte, à prendre dans la session qui suit cette certification. Il n'est pas tranché ici.

### 5.4 Corrections A1 prioritaires avant tout run

Avant tout run des 21 WP, les corrections A1-A4 de la Note d'améliorations doivent être traitées — en particulier A1 (rapports tronqués + hash manquant) et A6 (sous-workflow audit isolé). Ces corrections sont un prérequis de qualité pour le corpus complet.

---

## 6. Réserves actives au moment de la certification

| Code | Nature | Impact | Échéance |
|---|---|---|---|
| A1 | Rapports CONV-A tronqués à §1.5, S2-S7 absents, rapport_md_sha256 null | Concerne les 6 WP pilote ; Allemagne RÉVISION_MAJEURE résiduelle | Avant run 21 WP |
| A4 | statut_global RÉVISION_CONCORDANCE sur Commune (label V6.2 anachronique) | Cosmétique ; ne bloque pas la lecture §4 | Avant run 21 WP |
| R3 | CCI bas sur Rome (0.059), Haïti (0.712), Commune (0.582) | Qualité de reproductibilité à surveiller sur corpus complet | Suivi corpus |
| Rome métastable | Robustesse N1 MÉTASTABLE sur Rome IIIe | Mentionner dans le rapport S7 | Déjà documenté |

---

*Décision produite en session stratégique QG (rôle CONV-C), juin 2026. Certification V7.0 du cluster pilote V7-γ rev. 2 contre les 6 conditions de la Décision V7-D1 rev. 4 §4.*
