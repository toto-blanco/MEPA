# Décision de Décertification V7-D1 rev. 4

**MEPA V7 — Document de gouvernance scientifique**

| Champ | Valeur |
|---|---|
| Référence | Décision V7-D1 rev. 4 |
| Date | Avril 2026 |
| Statut | Acte de gouvernance scientifique — applicable immédiatement |
| Remplace | Décision V7-D1 rev. 3 |
| Autorité | Architecte Système MEPA V7 |
| Document théorique de référence | `MEPA_cadre_theorique_V7_alpha_rev2_1.docx` |
| Document technique associé | `MEPA_Addendum_V7_beta_ING.md` |

---

## 1. Motivation de la révision rev. 3 → rev. 4

La version rev. 4 de la Décision V7-D1 est produite en réponse à l'arbitrage du critique externe sur la proposition de rev. 2.2 (adoption du score continu d'activation de (α)). Le critique a validé l'Option C — abandon de la rev. 2.2 et conservation de la rev. 2.1 comme base de la V7-α — sur la base d'un test de robustesse qui a révélé que le score continu était structurellement fragile sur l'Allemagne nazie sous variation combinée −5% des poids.

Cette décision rev. 4 intègre quatre modifications par rapport à la rev. 3.

**Première modification** — confirmation de l'abandon de la rev. 2.2 et maintien de la rev. 2.1 comme base finale de la V7-α. Aucune trace du score continu n'est introduite dans le cadre théorique V7-α. Le score continu devient exclusivement un chantier V7.1 dont le cahier des charges est fixé en §6 ci-dessous.

**Deuxième modification** — intégration des deux réserves originelles du critique sur la condition de certification 2 (Allemagne nazie), avec généralisation à l'ensemble du cluster pilote. Voir §4bis ci-dessous.

**Troisième modification** — clarification de la conditionnalisation : la certification V7.0 n'est pas bloquée par l'échec attendu sur Allemagne nazie, mais la production des 21 WP restants du corpus est explicitement conditionnée à la résolution V7.1 du problème C2 ou à une démonstration documentée que le problème est insoluble dans le cadre actuel. Voir §5 ci-dessous.

**Quatrième modification** — ajout du §6 nouveau « Cahier des charges du chantier V7.1 — score continu d'activation de (α) » qui formalise les quatre exigences que le critique a posées pour une adoption ultérieure rigoureuse du score continu : calibration sur trois cas positifs minimum, validation croisée, pré-enregistrement des poids et du seuil avec intervalles serrés, analyse de sensibilité globale par méthode de Sobol.

---

## 2. Constat empirique et liste des rapports décertifiés — inchangés

Les 15 rapports décertifiés par les rev. 1, 2 et 3 restent décertifiés par la rev. 4. Les quatre causes architecturales (A, B, C, D) et les quatre corrections V7-C1 à V7-C4 rev. 2.1 sont également inchangés. La liste détaillée et les motifs individuels sont conservés depuis la rev. 1 et restent opérationnels.

| WP | Cluster | N | Motif | Statut |
|---|---|---|---|---|
| WP-F1-1 Rome IIIe | C1 | 5 | Divergence architecturale | 5 rapports décertifiés |
| WP-C1-1 Haïti | C1 | 3 | Divergence architecturale | 3 rapports décertifiés |
| WP-I10-1 Rwanda | C1 | 3 | Divergence catégorielle | 3 rapports décertifiés, dont 1 en décertification renforcée |
| WP-C2-1 Égypte 2011 | C2 | 4 | Concordance non-discriminante | 4 rapports décertifiés |

**Total : 15 rapports décertifiés sur 15 lus.** Taux de décertification : 100%.

---

## 3. Corrections architecturales V7-C1 à V7-C4 rev. 2.1 — inchangées

Les quatre corrections architecturales restent dans leur formulation rev. 2.1, telle que documentée dans le cadre théorique `MEPA_cadre_theorique_V7_alpha_rev2_1.docx` :

**V7-C1 rev. 2.1** — Trajectoire (α) Cristallisation sacrificielle d'État avec branche binaire (cinq conditions C1-C5) incluant la clause de repli A_r_c_eff = A_r_c + 0.5 × A_r_ne. Spécification en §2ter.5 et Annexe D du cadre théorique.

**V7-C2 rev. 2.1** — Branche (d) sans bascule avec renvoi à la branche (b) explicative. Spécification en §5.3 et Annexe C.

**V7-C3 rev. 2** — Protocole anti-rationalisation avec hypothèses théoriques sous contrainte sous trois contraintes strictes. Spécification en §B.4 de l'Annexe B.

**V7-C4 rev. 2.1** — Test de discrimination par annotation explicative/catchall, avec branche (b) explicative ajustée aux seuils empiriques V6.2 (C_max > 0.12, chute_C > 0.20, Cs ∈ [0.10, 0.50]). Spécification en Annexe E.

---

## 4. Conditions de validation V7-γ rev. 2 — inchangées dans leur structure

Les six conditions de validation pré-enregistrées en rev. 3 sont maintenues sans modification de leur structure. La condition 2 reste conditionnelle, conformément à la rev. 3, avec les ajouts du §4bis ci-dessous.

| # | Cas | Trajectoire attendue | Statut |
|---|---|---|---|
| 1 | WP-I10-1 Rwanda | (α) via V7-C1 rev. 2.1 | Bloquante |
| 2 | WP-I4-1 Allemagne nazie | (α) attendue mais échec prévisible sur C2 | **Conditionnelle — voir §4bis et §5** |
| 3 | WP-F10-1 Commune de Paris | (a) — pas (α) (contrôle négatif) | Bloquante |
| 4 | WP-F1-1 Rome IIIe | (d) via V7-C2 rev. 2.1 | Bloquante |
| 5 | WP-C1-1 Haïti | (d) via V7-C2 rev. 2.1 | Bloquante |
| 6 | WP-C2-1 Égypte 2011 | (b) explicative via V7-C4 rev. 2.1 | Bloquante |

---

## 4bis. Réserves intégrées sur la documentation des anomalies — généralisation au cluster pilote

Suite à l'arbitrage du critique externe et conformément à sa demande explicite de généralisation, les deux réserves suivantes sont intégrées dans la Décision V7-D1 rev. 4 et s'appliquent à **tous les cas du cluster pilote V7-γ rev. 2**, pas seulement à Allemagne nazie. Elles complètent et précisent le protocole V7-C3 sans le contredire.

**Réserve 1 — Documentation obligatoire d'anomalie pour toute divergence.** Si le test V7-γ produit, sur n'importe lequel des six cas du cluster pilote, une trajectoire diagnostiquée différente de la trajectoire attendue spécifiée au §4 de la présente décision, le rapport CONV-A correspondant doit contenir une section obligatoire intitulée « Anomalie documentée » dont la structure est celle de l'Annexe B §B.1 du cadre théorique V7-α rev. 2.1. Cette obligation s'applique également au cas Allemagne nazie même si l'échec est attendu — l'anticipation théorique d'une divergence ne dispense pas de son traitement par le protocole V7-C3.

**Réserve 2 — Hypothèse théorique sous contrainte obligatoire pour toute anomalie documentée.** La section « Anomalie documentée » d'un rapport CONV-A doit obligatoirement être suivie d'une sous-section « Hypothèse théorique sous contrainte » qui respecte les trois contraintes du protocole §B.4 rev. 2 du cadre : isolation textuelle, prédiction falsifiable sur un cas non encore simulé, et reconnaissance explicite du statut spéculatif. L'hypothèse formulée doit proposer une direction de résolution pour V7.1, par exemple le score continu calibré (chantier V7.1 §6 ci-dessous), une variable d'alignement institutionnel macro, un mécanisme de reset d'état inter-phases (V7.2), ou toute autre piste théorique défendable.

**Justification de la généralisation.** La rev. 3 limitait ces deux réserves au cas Allemagne nazie seul, parce qu'il était identifié comme le cas-test critique de la conditionnalisation. La rev. 4 généralise les réserves à tous les cas divergents du cluster pilote sur recommandation explicite du critique externe. La motivation est la suivante : transformer chaque divergence — anticipée ou non — en contribution théorique pour le cycle suivant. Cette généralisation préserve l'intégrité du protocole anti-rationalisation tout en valorisant les divergences comme moteurs de progrès plutôt que comme échecs à minimiser. Elle est cohérente avec l'esprit Type B de l'Addendum V6.2 qui revendique la subordination du cadre à la critique empirique.

---

## 5. Conditionnalisation de la condition 2 — clarification rev. 4

La condition de certification 2 (WP-I4-1 Allemagne nazie produit (α)) reste **conditionnelle** dans le sens suivant, précisé par rapport à la rev. 3 :

### 5.1 Statut pour la certification V7.0

L'échec attendu sur Allemagne nazie ne bloque **pas** la certification V7.0 si les cinq autres conditions sont satisfaites. Le runner V7-γ classera prévisiblement Allemagne nazie en non-(α) à cause de l'échec structurel sur la condition C2 (Ψ_noyau × γ_local = 0.0055 < σ(Φ=0.30) ≈ 0.0275, voir §2ter.7 du cadre rev. 2.1). Cet échec est documenté comme résultat empirique attendu et traité par le rapport CONV-A correspondant selon les Réserves 1 et 2 du §4bis ci-dessus.

### 5.2 Statut pour la production des 21 WP restants

La production des 21 WP restants du corpus V6.2 (au-delà du cluster pilote) **est conditionnée** à la résolution du problème C2 en V7.1, ou à une démonstration documentée que le problème est insoluble dans le cadre théorique actuel. Cette conditionnalisation est plus forte que dans la rev. 3 : la rev. 3 laissait implicite la possibilité de lancer la production avec le problème C2 non résolu, la rev. 4 l'interdit explicitement.

Trois scénarios sont possibles à l'issue du test V7-γ et du chantier V7.1 :

**Scénario A — résolution V7.1 réussie.** Le score continu (ou une variable d'alignement macro, ou une autre formulation théorique) est validé en V7.1 sur trois cas positifs minimum. La condition 2 devient bloquante normale et le runner V7.1 produit (α) sur Allemagne nazie. La production des 21 WP restants est lancée.

**Scénario B — résolution V7.1 partielle.** Le score continu est validé en V7.1 mais avec des limitations explicitement documentées (par exemple impossibilité de calibrer sur la Grande Terreur soviétique faute de codage). La production des 21 WP restants est lancée mais les rapports CONV-A doivent inclure une note de réserve méthodologique sur les cas similaires structurellement à Allemagne nazie.

**Scénario C — démonstration d'insolubilité.** Le chantier V7.1 conclut que le problème C2 est insoluble dans le cadre théorique V7 actuel et exige une refonte structurelle pour V8. La production des 21 WP restants est suspendue jusqu'à V8 ou exécutée avec une note de réserve générale sur l'incomplétude du modèle pour les cas de cristallisation par petit noyau aligné sur grand appareil d'État.

Le scénario qui se réalisera n'est pas pré-enregistrable parce qu'il dépend du résultat empirique du chantier V7.1. La présente décision rev. 4 pré-enregistre simplement les trois scénarios possibles et leur traitement opérationnel, pour empêcher une dérive ad hoc au moment de la décision V7.1.

### 5.3 Intervalles de tolérance pré-enregistrés (rev. 3 maintenus en rev. 4)

Le présent §5.3 reprend les intervalles de tolérance pré-enregistrés introduits en rev. 3, sans modification. Les intervalles sont volontairement serrés pour éviter la tautologie du pré-enregistrement.

| Hyperparamètre | Valeur V7-α rev. 2.1 | Intervalle pré-enregistré V7-γ |
|---|---|---|
| θ_C (C_max Rwanda, cond. C5 α) | > 0.30 | [0.30, 0.50] |
| σ_base | 0.018 | [0.015, 0.025] |
| α (facteur σ-Φ) | 1.7 | [1.2, 2.5] |
| μ_m* | 0.60 | [0.55, 0.65] |
| Modulateur p6 Phase 1 | × 0.50 | [0.40, 0.60] |
| Modulateur p6 Phase 2 | × 2.50 | [2.00, 3.00] |
| Modulateur p6 Phase 3 | × 1.15 | [1.05, 1.25] |
| Coefficient A_r_c_eff (clause repli) | 0.5 | [0.3, 0.7] |
| Seuil chute_C (branche b expl) | > 0.20 | [0.15, 0.30] |
| Seuil C_max (branche b expl) | > 0.12 | [0.10, 0.18] |

Si le test V7-γ produit une valeur en dehors d'un intervalle pré-enregistré, l'hyperparamètre est considéré comme réfuté dans sa formulation V7-α et déclenche une révision rev. 3 avant certification V7.0.

---

## 6. Cahier des charges du chantier V7.1 — score continu d'activation de (α)

Conformément à la §4 de la lettre d'arbitrage du critique externe, la présente décision rev. 4 formalise le cahier des charges du chantier V7.1 sur le score continu d'activation de (α). Ce cahier des charges est engageant pour le projet et toute déviation devra être explicitement justifiée et documentée.

**Exigence 1 — Calibration sur trois cas positifs minimum.** Le score continu V7.1 ne peut être calibré qu'après création d'un troisième cas positif de cristallisation sacrificielle d'État dans le corpus MEPA, en complément de Rwanda et Allemagne nazie. Le cas privilégié est la Grande Terreur soviétique 1937-1938, qui présente l'avantage théorique d'être un cas de matrice idéologique séculière (M_r en transition vers Stade 3 selon Todd) plutôt que religieuse, et qui testerait l'extensibilité du mécanisme sacrificiel au-delà des matrices religieuses actives. La création de ce WP est un préalable au chantier V7.1.

**Exigence 2 — Validation croisée.** La calibration des poids et du seuil doit être effectuée par optimisation avec validation croisée sur les trois cas positifs : par exemple, calibrer les poids sur Rwanda + Allemagne nazie, puis tester sur Grande Terreur soviétique sans réajustement, et inversement pour les autres combinaisons. La validation croisée garantit que les poids ne sont pas surcalibrés sur deux cas particuliers mais capturent une régularité empirique sur les trois.

**Exigence 3 — Pré-enregistrement des poids et du seuil avec intervalles serrés.** Les poids (w1, w2, w3, w5 et la condition éliminatoire sur Ψ_cible) ainsi que le seuil d'activation doivent être pré-enregistrés dans une Décision V7.1-D2 avant toute simulation V7.1-γ, avec intervalles de tolérance volontairement serrés (typiquement ±10% sur chaque poids et ±0.15 sur le seuil). Les intervalles larges sont explicitement interdits parce qu'ils rendraient le pré-enregistrement tautologique.

**Exigence 4 — Analyse de sensibilité globale par méthode de Sobol.** Avant adoption définitive du score continu en V7.1, une analyse de sensibilité globale par méthode de Sobol doit être exécutée sur l'ensemble des hyperparamètres V7.1 (poids du score, seuil, paramètres de la rampe mod_mimétique, σ_base, α facteur Φ). Cette analyse doit identifier les hyperparamètres dont la variation produit le plus de variance dans les diagnostics, et permettre une réduction éventuelle de la paramétrisation. L'analyse de Sobol est l'outil méthodologique recommandé par l'analyse d'ingénierie système du critique externe.

Ces quatre exigences sont engageantes pour le projet MEPA. Toute adoption du score continu en V7.1 sans satisfaction de ces quatre exigences constituerait une rationalisation post-hoc et serait contraire au protocole V7-C3.

---

## 7. Justification épistémologique de la rev. 4

Le cycle complet de critique externe sur la V7-α rev. 1 → rev. 2.1 a produit une découverte méthodologique qui dépasse le cas particulier d'Allemagne nazie et qui mérite d'être nommée explicitement dans la présente décision.

Le critique externe a écrit dans son arbitrage final : « la conditionnalisation rev. 2.1 est plus honnête que l'adoption d'un score fragile en le documentant comme tel ». Cette formulation contient une vérité méthodologique générale qui guidera désormais le projet MEPA dans ses choix d'architecture théorique : **assumer ouvertement une limite vaut mieux que masquer une fragilité par une formulation continue**. Une condition binaire non satisfaite est une limite visible qui appelle une résolution explicite. Une formulation continue qui passe le seuil avec une marge nominale étroite est une fragilité masquée qui appelle des ajustements de poids dans des intervalles de tolérance — c'est-à-dire exactement la tentation post-hoc que le protocole V7-C3 condamne.

Le projet MEPA choisit donc, à partir de la rev. 4, **la limite assumée plutôt que la fragilité masquée**. Cette préférence n'est pas un dogme : elle pourra être révisée en V7.1 ou V8 si une formulation continue plus robuste émerge. Mais en l'état, sur la V7-α, elle est la règle. Toute proposition future de remplacer une condition binaire par une formulation continue devra démontrer empiriquement (par test de robustesse de type ±5%) qu'elle ne crée pas de fragilité supérieure à celle qu'elle prétend résoudre.

Cette règle est une contribution directe du dialogue avec le critique externe au cadre méthodologique du projet. Elle est attribuée explicitement à son arbitrage du présent cycle.

---

## 8. Calendrier d'application rev. 4

| Échéance | Action |
|---|---|
| **Immédiat** | Adoption de la présente Décision V7-D1 rev. 4 et clôture du cycle de critique théorique sur la V7-α |
| **Immédiat** | Marquage des 15 rapports décertifiés avec mention "DÉCERTIFIÉ V7-D1 rev. 1 + rev. 2 + rev. 3 + rev. 4" |
| **Avant V7-γ rev. 2** | Production des grilles de pré-codage V7 pour WP-I4-1 Allemagne nazie et WP-F10-1 Commune de Paris |
| **Avant V7-γ rev. 2** | Codage CONV-E des variables V7 sur ces deux WP additionnels |
| **V7-β rev. 2.1** | Implémentation technique du runner V7-α rev. 2.1 avec adoption de l'intégrateur LSODA (cf. addendum V7-β-ING) |
| **V7-γ rev. 2** | Re-simulation des 6 cas-tests avec runner V7-β ; certification subordonnée aux 5 conditions bloquantes ; condition 2 traitée comme conditionnelle avec application des Réserves 1 et 2 du §4bis |
| **V7.0** | Publication de la V7-α rev. 2.1 stable avec référence explicite à la présente décision V7-D1 rev. 4 |
| **Préalable V7.1** | Création du WP Grande Terreur soviétique 1937-1938 dans le corpus MEPA |
| **V7.1** | Chantier score continu d'activation de (α) selon le cahier des charges §6 |
| **V7.2** | Mécanisme de reset d'état inter-phases (chantier autonome déjà identifié) |

---

## 9. Clôture du cycle de critique externe

Le cycle de critique externe sur la V7-α, ouvert par la première lettre du critique sur la V7-α rev. 1 et clos par son arbitrage sur l'Option C, est officiellement **clos** par la présente Décision V7-D1 rev. 4.

Six lettres ont été échangées dans le cycle : V7-R1 (réponse à la critique initiale), V7-R2 (réponse à la contre-analyse sur la rev. 2), V7-R3 (réponse à la double contre-analyse sur la rev. 2.1), V7-R3-bis (test de robustesse et demande d'arbitrage), arbitrage du critique sur l'Option C, et V7-R3-ter (acceptation de l'arbitrage et clôture). Quatre cycles de correction ont été exécutés : V6.2 → V7-α rev. 1 → rev. 2 → rev. 2.1, plus une rev. 2.2 envisagée et abandonnée.

Toute critique ultérieure sur la V7-α rev. 2.1 sera bienvenue mais relèvera d'un nouveau cycle, post-V7-γ. Le présent cycle est clos pour permettre au projet de passer à la phase empirique (production des grilles de pré-codage, codage CONV-E sur les deux WP additionnels, lancement du test V7-γ rev. 2).

---

*Décision V7-D1 rev. 4 — Architecte Système MEPA V7 — Avril 2026*

*Cette décision révise et remplace la Décision V7-D1 rev. 3. Elle est applicable immédiatement et inséparable du cadre théorique V7-α rev. 2.1. Elle clôt le cycle de critique externe sur la V7-α et autorise le passage à la phase empirique du test V7-γ.*
