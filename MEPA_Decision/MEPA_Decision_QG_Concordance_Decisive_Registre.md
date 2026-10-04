# MEPA — Décision QG : concordance décisive inter-codeurs · mesure CONV-B · registre des exécutions

| Champ | Valeur |
|---|---|
| Statut | **Décision QG** — inclut une mesure pré-enregistrée |
| Rôle | QG / CONV-C (Architecte Scientifique) — décision prise par Antoine |
| Date | 2026-10-03 |
| Base factuelle | Retour CTO du 2026-10-03 ; run de validation WP-C2-1 du 2026-10-03 (`WP-C2-1_passeport.json`, `WP-C2-1_cci.json`, protocole V7.0-P2) |
| Références | Décision D3 · `MEPA_Decision_QG_Diagnostic_R.md` · Erratum Certification V7.0 (DEP5 et règle de non-suppression) · `MEPA_Decision_V7_D1_rev4.md` (§4) · CV16 (à rédiger) |

---

## 1. D3 clos

Le run WP-C2-1 du 2026-10-03 ne comporte plus aucune clé `kappa`, ni dans le passeport ni dans le rapport CCI. `accord_sa` = 0, `accord_m_r` = 1, CCI = 0.832. **D3 est clos.**

---

## 2. Constat — désaccord inter-codeurs sur les variables décisives de branche

Au run du 2026-10-03, les deux codeurs divergent sur les variables qui déterminent le précheck (α) :

| Variable | CONV-E (simulé) | CONV-B | Statut au rapport CCI |
|---|---|---|---|
| μ_m | 0.50 | 0.85 | désaccord, `friction_outlier` |
| Ψ_noyau | 0.03 | 0.18 | désaccord, `friction_outlier` |
| Ψ_cible | null | 0.32 | non scorable ; retiré des désaccords (défaut corrigé en v3.1.1) |
| Φ | 0.55 | 0.35 | désaccord |
| γ_local | 0.75 | 0.78 | accord |
| A_r_c / A_r_ne | 0.60 / 0.35 | 0.72 / 0.55 | accord / désaccord |
| Sa | 6 | 4 | désaccord (constant sur trois runs) |

Précheck (α) évalué sur chaque codage (σ(Φ) = 0.018 × (1 + 1.7 × Φ)) :

| Condition | Codage CONV-E | Codage CONV-B |
|---|---|---|
| C1 — M_r ∈ {1,2} et μ_m > 0.60 | non (0.50) | **oui** (0.85) |
| C2 — Ψ_noyau × γ_local > σ(Φ) | non (0.0225 < 0.0348) | **oui** (0.1404 > 0.0287) |
| C3 — Ψ_cible non nul | non | **oui** (0.32) |
| C4 — A_r_c_eff > 0.70 | oui (0.775) | **oui** (0.72) |
| **Précheck (α)** | **non** | **oui** |

Le codage indépendant de CONV-B conduit à la branche (α) ; le codage simulé conduit à (b) explicative. Le gate `cci_global` (0.832 ≥ 0.75) est satisfait : le CCI agrège quinze variables et ne signale pas qu'un désaccord porte sur une décision de branche.

**Portée :**
- La certification de WP-C2-1 (juin 2026, V7.0-P1) n'est pas modifiée : les codages CONV-B de juin ne sont pas archivés et les règles en vigueur ne retiennent que `cci_global`.
- Le constat est versé à CV16 sous la forme suivante : un contrôle de **concordance décisive** évaluant, sur chacun des deux codages, les décisions qui déterminent la branche (précheck α, et Sa lorsque la valeur 7 est en jeu), avec escalade lorsque les deux codages conduisent à des branches différentes. Ce contrôle complète `cci_global` ; il ne le remplace pas.

---

## 3. Mesure pré-enregistrée — stabilité du codage CONV-B sur WP-C2-1

**Objet :** caractériser la variance du codage indépendant de CONV-B à T=0, symétriquement à la mesure faite sur CONV-E (erratum §4.3), et vérifier si le passage en branche (α) observé le 2026-10-03 est stable.

**Mesure :**
- 3 exécutions isolées du Nœud 8a sur WP-C2-1, protocole V7.0-P2 (température 0 transmise et enregistrée) ;
- nœud 8a identique au workflow principal (empreinte relevée) ; fiche inchangée avant et après (empreinte vérifiée) ;
- sorties brutes archivées, avec `message_id` et horodatage ;
- aucune simulation, aucun passeport.

**Relevé, pour chaque exécution :** les 15 valeurs codées par CONV-B ; le CCI calculé contre le codage CONV-E du run du 2026-10-03 ; le précheck (α) C1–C4 évalué sur le codage CONV-B.

**Critère, fixé avant exécution :**
- Si le précheck (α) est satisfait sur le codage CONV-B dans **au moins 2 exécutions sur 3** : le cas WP-C2-1 est placé sous **réserve de concordance décisive**, levée ou confirmée par la règle de CV16. Le statut de certification n'est pas modifié par la mesure elle-même.
- Dans le cas contraire : le passage en (α) du 2026-10-03 est consigné comme variance du codeur, sans réserve.
- Dans tous les cas, les valeurs sont versées au dossier CV16.

---

## 4. Calculateur v3.1.1

Déploiement autorisé :
- note méthodologique corrigée (Sa et m_r : indicateurs d'accord binaires, plus de mention « κ de Cohen ») ;
- tout cas où un codeur retient `null` et l'autre une valeur est **listé dans les désaccords et escaladé** dans `instructions_resolution`, au lieu d'être retiré sans trace.

CCI, verdict, `n_desaccords` et valeurs finales restent inchangés (vérifié par le CTO sur trois paires).

---

## 5. Registre des exécutions

### 5.1 Une exécution, un répertoire

Constat : le Nœud 7 écrit sous des noms fixes, sans contrôle d'existence ; une nouvelle exécution remplace silencieusement le passeport précédent, et la synchronisation propage l'écrasement. C'est contraire à la règle selon laquelle un passeport certifié ne peut être supprimé ni remplacé.

**Décision :**
- chaque exécution écrit dans un répertoire propre `{wp_id}/{run_id}/` ; aucune écriture sur un fichier existant ;
- à la porte de certification (H2), une copie immuable est déposée dans `certifies/` ; ce répertoire est en ajout seul ;
- la synchronisation de sauvegarde suit cette organisation.

### 5.2 Reprise d'exécution

**Décision :**
- **interdite pour les exécutions de certification** : toute interruption impose une nouvelle exécution complète ;
- **autorisée pour les exécutions de validation et de diagnostic**, à condition d'être déclarée au passeport (identifiant de run, identifiant de chaque exécution, nœud de reprise).

Le run de validation WP-C2-1 du 2026-10-03, repris au Nœud 7, relève de ce second cas.

### 5.3 Suppression du dossier `outputs/` — DEP5

La suppression du dossier `outputs/` sur le Pi, probablement par la synchronisation, est la réalisation du risque visé par DEP5. Le gate DEP5 (sauvegarde continue, sans fenêtre et sans propagation des suppressions) reste une condition préalable aux 21 WP et n'est pas confirmé à ce jour.

**Demandé au CTO :**
- l'inventaire de ce que contenait `outputs/` et de ce qui a été perdu ou restauré ;
- la confirmation que la synchronisation en place ne propage pas les suppressions, ou sa reconfiguration en ce sens ;
- le remplacement des droits 777 par une permission de groupe.

---

## 6. Intrants versés au dossier CV16

- Contrôle de concordance décisive (§2).
- Résultats de la mesure CONV-B (§3).
- Le calculateur produit déjà des `instructions_resolution` (moyenne automatique, confrontation des sources) et des `valeurs_finales_provisoires`, jamais appliquées. Au 2026-10-03, `E_split` provisoire vaut 0.735 alors que la valeur simulée est 0.65. La règle d'arbitrage déterministe de CV16 doit partir de ce mécanisme existant.

---

*Décision QG (CONV-C) — MEPA V7.0 — 2026-10-03*
