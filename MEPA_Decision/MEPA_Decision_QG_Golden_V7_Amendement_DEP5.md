# MEPA — Décision QG : golden V7, sort du runner V6.2, amendement de la reconstitution DEP5

| Champ | Valeur |
|---|---|
| Statut | **Décision QG** |
| Rôle | QG / CONV-C (Architecte Scientifique) — décision prise par Antoine |
| Date | 2026-10-04 |
| Base factuelle | Retour CTO du 2026-10-04 ; `tests/test_golden_v7.py` ; `tests/test_t6_rampe_segmentation.py` v1.2 ; `MEPA_Correspondance_Depot_Pi_et_Rangement.md` |
| Références | `MEPA_Decision_QG_DEP5_Registre.md` · ARCH-AG-01 (invariant I-1) · `MEPA_Decision_QG_Diagnostic_R.md` |

---

## 1. Test T6 — v1.2 acceptée

- La règle T1 est alignée sur le runner : un seul `t_bascule` défini fait échouer le test.
- L'écart d'empreinte du `result.json` Rwanda est expliqué : le fichier écrit par le runner (`b47bb3c5…`, inscrit au passeport) et la copie conservée sur le poste (`877b9471…`) ne diffèrent que par la mise en forme de sept nombres (`1` au lieu de `1.0`). L'empreinte canonique distingue entier et flottant et ne résout pas l'écart.

**Constat de méthode :** les copies des `result.json` conservées sur le poste ne sont pas les fichiers tels que produits ; elles ont été réécrites en cours de circuit. Seul un fichier dont l'empreinte est égale à celle du passeport fait foi comme artefact.

---

## 2. Suite de tests et golden V7

**Constat :** la réorganisation de `config/` avait cassé 18 tests et, plus gravement, supprimé sans signal la collecte de 56 tests (29 golden et 27 de sensibilité V6.2). La suite est réparée : 89 réussis, 1 ignoré avec sa raison, 1 échec attendu. Une collecte vide fait désormais échouer la suite.

**Golden V7 :** `tests/test_golden_v7.py` relance les six runs certifiés V7.0-P1 et exige l'égalité au bit près avec l'empreinte inscrite dans chaque passeport (invariant I-1). Vérifié 6/6 dans le conteneur de production et sur deux jeux de versions de NumPy et SciPy, à la précision des résultats archivés.

**Décisions :**
- Le golden V7 est le garde-fou de non-régression du runner de production pour les 21 WP.
- **Les références golden ne sont modifiées que par décision QG explicite.** Toute recalibration d'un hyperparamètre, même à l'intérieur de son intervalle pré-enregistré au §5.3 de D1 rev. 4, fait échouer le golden (vérifié : p6 phase 2 de 2.50 à 2.51) ; elle exige une décision qui la justifie et qui autorise la mise à jour des références.
- La Sentinelle CI peut devenir bloquante.

---

## 3. Emplacement des références golden

Les six `result.json` certifiés sont versionnés dans le dépôt public sous `tests/golden_v7/`, comme références de test.

**Décision :** ils y restent.
- Ce sont des données de simulation déjà rendues publiques par ailleurs (`outputs/mesures/`, décision DEP5 §2.6), sans passeport, rapport ni sortie brute de LLM.
- Une Sentinelle dépendante du dépôt privé exigerait de lui confier un accès à `mepa-registre` : complexité et surface d'exposition sans bénéfice.
- `mepa-registre` reste le registre de référence des artefacts ; les références golden en sont des copies de test, rattachées aux passeports par leur empreinte.

---

## 4. Sort du runner V6.2 et de ses tests

Le runner V7 ne dépend pas du runner V6.2 : il embarque sa propre intégration Euler pour la comparaison T1–T5.

**Décision :** le runner V6.2 et ses tests sont **conservés** jusqu'à la certification des 21 WP en V7. Ils restent la référence de ce que produit le modèle V6.2 sur les fiches dont dériveront les 21 WP, et leur maintien ne coûte que quelques secondes de suite. Leur archivage fera l'objet d'une décision après cette certification.

---

## 5. Amendement de la reconstitution DEP5 (§2.2)

L'inventaire de la corbeille prévu au §2.2 a été remplacé, à l'initiative d'Antoine, par une comparaison entre le dépôt local de référence et le Pi.

**Décision :** l'amendement est acté. Les deux buts de l'inventaire sont couverts :
- les `result.json` certifiés sont reconstruits au bit près (golden V7) ;
- l'historique est conservé dans `sauvegarde_outputs/` sur le Pi et sur le poste ; il sera versé dans `mepa-registre/archives/`.

**Résultats acquis :**
- les éléments exécutés par le pipeline sont sains (20 scripts identiques au dépôt, constantes v1.4.0, six fiches de référence `config/v7/` identiques, séquenceur lisant `config/v7/`) ;
- la table de correspondance des chemins entre le dépôt et le Pi est établie (`MEPA_Correspondance_Depot_Pi_et_Rangement.md`) ;
- 49 fichiers restaurés par erreur, listés avec leur empreinte et validés par Antoine, ont été rangés : 42 en `quarantaine_2026-10-03/`, 7 dans la corbeille Nextcloud.

**Réserve sur les 7 fichiers en corbeille :** la corbeille n'est pas un support de conservation (elle peut être vidée automatiquement). Ces fichiers ne posent pas de risque, leurs originaux étant intacts ou versionnés, mais la règle reste : un rangement se fait vers `quarantaine_*`, jamais vers la corbeille.

**Constat sans effet :** le diagnostic R du 2026-10-02 a été exécuté avec les constantes v1.3.0 (`154ed376…`). Sans incidence sur ses conclusions : la reproduction au bit près des six runs d'origine y a été vérifiée.

---

## 6. Whitelist — configuration désignée

Le Nœud 2 cherche la whitelist dans `scripts/`, ne la trouve pas et utilise sans signal sa copie embarquée ; la v3.0.0 déployée dans `config/` n'est lue par personne. Les deux versions exécutées produisent les mêmes plages et contraintes : aucun contrôle n'a été faussé.

**Décision :** correction incluse dans le lot de déploiement, conformément à DEP5 §2.3 — whitelist déployée et suivie par DEP3, échec du Nœud 2 si le fichier désigné manque.

---

## 7. État du gate DEP5 (critères du §3 de la décision DEP5)

| Critère | État |
|---|---|
| 1. Artefacts certifiés de juin versionnés dans `mepa-registre` | en cours |
| 2. Règle de validation des opérations destructives | en vigueur (appliquée au rangement) |
| 3. Synchronisation sans propagation des suppressions | non confirmé |
| 4. Commit automatique en fin d'exécution, contrôle de secrets | en cours |
| 5. DEP3 étendu aux fichiers agissant par présence | prévu dans le lot de déploiement |

Le gate DEP5 n'est pas levé.

---

*Décision QG (CONV-C) — MEPA V7.0 — 2026-10-04*
