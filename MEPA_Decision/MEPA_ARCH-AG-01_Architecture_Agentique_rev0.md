# MEPA — Proposition d'architecture agentique
## ARCH-AG-01 rev. 0 — Document soumis au QG pour décision

| Champ | Valeur |
|---|---|
| Statut | **PROPOSITION** — aucune décision prise, aucune modification engagée |
| Destinataire | QG / CONV-C (Architecte Scientifique) |
| Rédaction | Claude (session projet MEPA), sur demande d'Antoine |
| Date | 2026-09-29 |
| Base | Pipeline V7.0 — cluster pilote V7-γ rev. 2 certifié (6/6, Décision V7-D1 rev. 4 §4) |
| Références | `CLAUDE.md` · Décision V7-D1 rev. 4 · CV15 Option C · CV16 (en attente) · `mepa_pipeline_architecture_V62.md` · `mepa_workflow_n8n_V7.json` · `MEPA_Addendum_NoFS_Architecture.md` |
| Autorité | Claude propose et analyse ; **Antoine décide**. Aucune section de ce document ne vaut décision. |

> **Réserve de vérification.** La cartographie des nœuds (§4) a été établie à partir des copies présentes dans le contexte projet, pas depuis `main`. Conformément à la règle « vérification empirique sur fichiers Git-traçables », elle doit être confrontée au dépôt avant toute exécution (voir Annexe A).

---

## 0. Résumé exécutif

Le goulot actuel de MEPA n'est pas le calcul mais **le relais humain** : Antoine transmet manuellement les artefacts entre QG, CONV-A, CONV-B, CONV-D, CONV-E, CTO et assistant_n8n. Avec 21 WP restants et 3 à 10 passes par WP selon la stratification, ce mode de travail ne passe pas à l'échelle et multiplie les points de perte d'information (cf. Nœud 8d inerte, découvert tardivement).

La proposition tient en une phrase : **automatiser les transmissions et les contrôles, sans jamais confier à un agent le cœur scientifique ni une décision de gouvernance.**

Elle s'organise en trois couches :

1. **Couche QG (asynchrone)** — trois agents d'appui à la gouvernance : Greffier CV, Sentinelle CI, Contradicteur.
2. **Bus d'artefacts typés** — Postgres + schémas + SHA-256 ; remplace le relais manuel et rend chaque échange traçable.
3. **Usine WP** — un orchestrateur à états qui enchaîne agents LLM et outils déterministes existants, avec trois portes humaines.

Gains attendus : suppression du relais manuel, pré-registration **prouvable** (pare-feu épistémique), formalisation naturelle de CV16 via un `resolution_detail` explicite, détection immédiate des défauts de câblage de type Nœud 8d.

Six décisions sont demandées au QG (§11). Les phases 0 et 1 n'ont **aucun impact méthodologique** ; les phases 2 à 4 en ont et sont conditionnées à décision CV.

---

## 1. Diagnostic

| # | Constat | Conséquence |
|---|---|---|
| D-1 | Aucune communication directe entre conversations ; relais manuel par Antoine | Coût temporel élevé, risque de copie partielle ou de version erronée |
| D-2 | Nœud 8d effectivement inerte (`scores_resolus` toujours vide, noms de champs discordants) | Un défaut de contrat entre nœuds est passé inaperçu ; l'origine des divergences fiche→passeport (E / Rc / γ / L0) reste ouverte |
| D-3 | Variance inter-run identifiée : la résolution CONV-B se propage via 8d vers y0 / cmd_base | La résolution n'est ni explicite ni gelée → reproductibilité fragile ; CV16 non formalisé |
| D-4 | `resolution_detail` au Nœud 15 bloqué par D-2 | Porte bloquante avant les 21 WP |
| D-5 | Workflows n8n modifiés via l'interface graphique (cf. `INSTRUCTIONS_WORKFLOW_N8N_V7.md`) | Diffs git peu lisibles, dérive possible entre fichier JSON et instance exécutée |
| D-6 | Tableau de contrôle mis à jour par copier-coller dans un `.odt` | Source de vérité dupliquée, non vérifiable automatiquement |
| D-7 | CONV-E et CONV-B tournent sur le même modèle (`claude-sonnet-4-6`) | Le κ / CCI mesure en partie la cohérence du modèle avec lui-même (biais corrélés), pas uniquement une fiabilité inter-codeurs |

D-7 est un constat méthodologique, pas un défaut d'implémentation. Il est traité séparément (§5.2, décision Q-4).

---

## 2. Invariants et principes

### 2.1 Invariants hérités — non négociables

Ces invariants sont repris de `CLAUDE.md` et des décisions en vigueur. L'architecture proposée les **encapsule**, elle ne les modifie pas.

- **I-1 Bit-identité.** Les blocs `simulation`, `verdict`, `stress_n1`, `stress_n2` restent bit-identiques pour des entrées identiques. Toute phase se termine par la preuve de non-régression (T1–T5 runner + T6 segmentation).
- **I-2 Cœur scientifique intouchable.** `_step()`, `F_val()`, `R_val()`, `simulate()`, `apply_sa_modulator()`, `_build_result()`, `_tableau_s2()` : aucun agent ne les modifie ni ne raisonne à leur place.
- **I-3 Source unique de vérité.** `mepa_constants.json` ; aucun seuil recopié dans un prompt ou un agent.
- **I-4 Contraintes de domaine.** Clé `gamma` exclusive ; Sa=7 → `p6 × 1.5` (runner et N2 concordants à 0.001) ; protocole NC (γ, EROI bloquants) ; labels D4 officiels.
- **I-5 Pré-registration.** CONV-E code depuis les sources historiques, jamais à rebours de la trajectoire attendue.
- **I-6 Gouvernance.** Toute décision de certification ou de gouvernance scientifique est prise par Antoine.

### 2.2 Principes de conception proposés

- **P-1 Déterminisme au centre, LLM en périphérie.** Runner ODE, audit N2, κ / CCI, passeport, stress N2 restent des **outils** appelés par l'orchestrateur. Un agent LLM ne calcule jamais une trajectoire, un seuil ou un verdict.
- **P-2 Pare-feu épistémique.** Le contexte de chaque agent est construit par l'orchestrateur selon une liste blanche par rôle (§7), puis haché et archivé (`context_manifest`). La pré-registration devient **prouvable a posteriori**, et plus seulement déclarée.
- **P-3 Tout échange est un artefact typé et chaîné.** Enveloppe commune, schéma validé à chaque transition, SHA-256, références aux parents. Un contrat rompu échoue **bruyamment** (réponse directe à D-2).
- **P-4 Portes humaines explicites.** Trois portes seulement : gel de la fiche résolue, certification du WP, toute décision CV. Tout le reste est automatisé.
- **P-5 Reproductibilité LLM mesurée.** Modèle épinglé, T=0, prompts versionnés et hachés, requêtes et réponses archivées intégralement. La variance inter-run devient une métrique suivie.

---

## 3. Architecture cible

```
┌──────────────────────── COUCHE QG (asynchrone) ────────────────────────┐
│   Greffier CV          Sentinelle CI           Contradicteur           │
│   registre décisions   non-régression, SHA     red team théorique      │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌──────────────── BUS D'ARTEFACTS TYPÉS — Postgres, schémas, SHA-256 ─────┐
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌─────────────── USINE WP — orchestrateur à états (par WP × passe) ──────┐
│                                                                        │
│  [LLM] Documentaliste → [LLM] Codeurs E ∥ B → [DÉT] Porte κ / CCI      │
│                                                     │                  │
│                                              [LLM] Arbitre             │
│                                           (resolution_detail)          │
│                                                     │                  │
│                                   ══ PORTE H1 : gel fiche résolue ══   │
│                                                     │                  │
│  [DÉT] Passeport ← [LLM] Rédacteur ← [DÉT] Runner ← [DÉT] Audit N2+A/B │
│         │           + vérificateur    LSODA+N1/N2                      │
│  ══ PORTE H2 : certification (Antoine) ══                              │
└────────────────────────────────────────────────────────────────────────┘
        PORTE H3 : toute décision CV (Antoine, via QG)
```

**Machine à états d'un WP × passe :**

`INIT → SOURCES_PRÊTES → CODÉ_E ∥ CODÉ_B → κ_ÉVALUÉ → {AUTO | RÉVISION (max 2) | ARBITRAGE} → RÉSOLU → [H1] GELÉ → AUDITÉ → SIMULÉ → SENSIBILITÉ_OK → RÉDIGÉ → VÉRIFIÉ → AUDIT_FINAL → [H2] CERTIFIÉ | EXPLORATOIRE | REJETÉ → ARCHIVÉ`

Chaque transition écrit un artefact dans le bus. Une transition est **idempotente** : relancer un état déjà atteint avec les mêmes entrées gelées ne produit rien de nouveau.

---

## 4. Cartographie : existant → cible

L'architecture est une **évolution** du WF V7 (30 nœuds), pas un remplacement.

| Composant cible | Nœud(s) V7 existant(s) | Nature du changement |
|---|---|---|
| Préflight | Préflight — Contrôles d'intégrité | Inchangé ; résultat écrit comme artefact |
| Documentaliste | — | **Nouveau** |
| Codeur E | Nœud CONV-E — Codage historique [LLM] | Contexte restreint par pare-feu |
| Codeur B | Nœud 8a — CONV-B CCI (codage indépendant) | Contexte restreint ; diversité de modèle soumise à Q-4 |
| Porte κ / CCI | Nœud 8a (calcul) + Router CCI | Inchangé (`mepa_kappa_calculator.py`) |
| Arbitre + porte H1 | Nœud 8c WAIT Validation CCI + Nœud 8d Injection | **8d remplacé** par un artefact `resolution_detail` explicite et validé |
| Audit N2 | Nœud 2 — Audit C1→C15 + Router | Inchangé |
| Runner + N1 | Nœuds P, 3, 4, 4b, 5, 5b | Inchangés |
| Rédacteur | Nœud 6 — Rédaction CONV-A | Inchangé + **vérificateur numérique** ajouté |
| Audit final | Nœud 6b — CONV-B Audit Final C1-C5 + Router | Inchangé |
| Stress N2, Popper | Nœuds 12, 13 | Inchangés |
| Certification (H2) | Nœud 14 | Devient porte humaine formelle |
| Archivage | Nœuds 7, 15, 16, C | `resolution_detail` enfin alimenté au Nœud 15 |
| Séquenceur | `mepa_workflow_n8n_V7_sequencer.json` | Remplacé ou piloté par l'orchestrateur (Q-5) |
| Tableau de contrôle | `.odt` manuel | **Vue générée** depuis le bus |

---

## 5. Spécification des agents

Format commun : rôle · entrées autorisées · entrées interdites · sortie · outils · garde-fous.

### 5.1 Documentaliste (nouveau)

- **Rôle.** Constituer un dossier de sources par WP : extraits cités, références bibliographiques, données quantitatives externes (NAVCO pour les WP contemporains, sous réserve de Q-6).
- **Entrées autorisées.** WP-ID, intitulé du cas, bornes temporelles et géographiques, liste des variables de la whitelist (noms et définitions uniquement).
- **Entrées interdites.** Trajectoire attendue, Ψ_cible, statut V7, contenu du Tableau de contrôle, fiches et résultats antérieurs.
- **Sortie.** Artefact `dossier_sources` (§6.2).
- **Outils.** Recherche web, lecture de documents fournis par Antoine, index pgvector local.
- **Garde-fous.** Chaque extrait porte une référence vérifiable ; aucun extrait n'est paraphrasé sans source. Le dossier ne contient **aucune variable codée**.

> **Nuance importante.** L'issue historique d'un cas est connue et figurera dans les sources : ce n'est pas une contamination. Le pare-feu protège contre la connaissance du **label de trajectoire MEPA attendu** et des valeurs cibles du protocole, pas contre les faits historiques.

### 5.2 Codeurs E et B

- **Rôle.** Coder indépendamment les variables de la fiche à partir du seul dossier.
- **Entrées autorisées.** `dossier_sources`, `mepa_whitelist_keys.json`, bornes issues de `mepa_constants.json`, prompt codeur versionné (CONV-E / CONV-B).
- **Entrées interdites.** Tout ce qui est interdit au Documentaliste, plus : la fiche de l'autre codeur, les résultats du runner, les passeports antérieurs.
- **Sortie.** Artefact `fiche_codage` (schéma V7 existant + enveloppe).
- **Garde-fous.** Validation immédiate contre la whitelist et le contrôle C4 (`gamma`). Chaque valeur référence au moins un extrait du dossier.
- **Point méthodologique (D-7).** Deux instances d'un même modèle partagent leurs biais : le κ observé surestime probablement la fiabilité inter-codeurs réelle. Trois options sont présentées en Q-4. Toute modification du protocole de codage implique décision CV et re-baseline du cluster pilote.

### 5.3 Arbitre

- **Rôle.** Pour chaque variable divergente, produire une valeur résolue **explicite et justifiée**.
- **Entrées autorisées.** Les deux `fiche_codage`, le `dossier_sources`, le rapport κ / CCI.
- **Entrées interdites.** Trajectoire attendue, Ψ_cible, résultats du runner. L'arbitrage est aveugle au même titre que le codage.
- **Sortie.** Artefact `resolution_detail` (§6.3).
- **Garde-fous.** Règles d'arbitrage fermées (§6.3) ; toute règle `escalade_humain` bloque jusqu'à la porte H1. Aucune valeur hors bornes `mepa_constants.json`.
- **Effet attendu.** Remplace la mécanique implicite de 8d ; rend la source de variance D-3 observable et gelable ; fournit le contenu du champ `resolution_detail` au Nœud 15 ; opérationnalise CV16.

### 5.4 Rédacteur + vérificateur

- **Rôle.** Rédiger S1–S7 (CONV-A, inchangé) puis vérifier la conformité numérique du texte.
- **Vérificateur (nouveau).** Extraction de toute valeur numérique citée dans S1–S7 → rapprochement avec un chemin de `result.json`, `rapport_n1` ou la fiche gelée, à tolérance déclarée. Toute valeur non rapprochée est **BLOQUANTE**.
- **Implémentation.** Extraction par expression régulière et rapprochement déterministe ; le LLM n'intervient que pour associer une mention textuelle ambiguë à un chemin candidat, jamais pour valider.
- **Sortie.** Artefact `verification_rapport` (§6.4).

### 5.5 Greffier CV (couche QG)

- **Rôle.** Tenir le registre des décisions CV (état, décision parente, éléments touchés) ; signaler toute proposition qui toucherait un élément certifié ou gelé ; rédiger les brouillons de décision au format standard.
- **Garde-fou.** Il rédige, il ne décide pas ; aucun brouillon ne change d'état sans validation d'Antoine.

### 5.6 Sentinelle CI (couche QG)

- **Rôle.** À chaque commit sur `main` : exécution T1–T6, Contrôles A (manifest SHA-256) et B (cohérence des seuils), nomenclature `gamma`, labels D4, concordance Sa=7 runner / N2 ; puis résumé d'impact en français.
- **Implémentation.** Scripts existants (déterministes) + Claude Code headless pour le seul résumé d'impact.
- **Garde-fou.** Lecture seule sur le dépôt ; aucun commit, aucune correction automatique.

### 5.7 Contradicteur (couche QG)

- **Rôle.** Red team systématique de toute proposition théorique avant passage en décision : falsifiabilité (ex. P5, trajectoire *e* absente du corpus), confusions de variables (ex. Sa / souveraineté monétaire avant Dev 2), imports causaux indus (ex. seuil 3,5 %).
- **Entrées.** Accès complet (seul agent sans pare-feu).
- **Sortie.** Note contradictoire jointe au brouillon de décision.

---

## 6. Schémas d'artefacts

### 6.1 Enveloppe commune

```json
{
  "artefact_id": "uuid",
  "type": "dossier_sources | fiche_codage | kappa_rapport | resolution_detail | runner_result | verification_rapport | passeport | context_manifest | ...",
  "schema_version": "1.0.0",
  "wp_id": "WP-C1-1",
  "passe": 1,
  "produit_par": {
    "role": "codeur_E",
    "nature": "llm | deterministe | humain",
    "modele": "claude-sonnet-4-6",
    "temperature": 0,
    "prompt_sha256": "…",
    "script": null,
    "script_sha256": null
  },
  "parents": ["sha256:…", "sha256:…"],
  "context_manifest_sha256": "…",
  "created_at": "ISO-8601",
  "payload_sha256": "…",
  "payload": { }
}
```

Règle : `payload_sha256` est calculé sur la sérialisation canonique du payload (clés triées, séparateurs fixes). Un artefact n'est jamais modifié ; une correction produit un nouvel artefact dont le parent est l'ancien.

### 6.2 `dossier_sources` (payload)

```json
{
  "extraits": [
    {
      "id": "S-014",
      "reference": "Auteur, Titre, année, p. 123",
      "type_source": "primaire | secondaire | donnees",
      "texte": "extrait court",
      "variables_concernees": ["gamma", "EROI"]
    }
  ],
  "lacunes_declarees": ["Aucune source quantitative sur Rc avant 1995"]
}
```

### 6.3 `resolution_detail` (payload)

```json
{
  "kappa_global": 0.81,
  "cci_global": 0.78,
  "resolutions": [
    {
      "variable": "gamma",
      "valeur_E": 0.40,
      "valeur_B": 0.55,
      "valeur_resolue": 0.55,
      "regle": "choix_B",
      "justification": "≥ 50 caractères, référencée",
      "extraits": ["S-014", "S-022"]
    }
  ],
  "escalades": [],
  "gel": {
    "porte_H1": "en_attente | valide",
    "valide_par": null,
    "fiche_resolue_sha256": null
  }
}
```

- `regle` ∈ { `accord`, `moyenne`, `choix_E`, `choix_B`, `recodage`, `escalade_humain` } — ensemble fermé.
- `variable` doit appartenir à `mepa_whitelist_keys.json` : **validation bloquante** (réponse directe au défaut de 8d).
- À la validation H1, `fiche_resolue_sha256` est renseigné : c'est l'objet gelé que CV16 viserait.

### 6.4 `verification_rapport` (payload)

```json
{
  "mentions_extraites": 42,
  "rapprochees": 42,
  "non_rapprochees": [],
  "ecarts_hors_tolerance": [],
  "statut": "PASS | BLOQUANT"
}
```

### 6.5 `context_manifest` (payload)

```json
{
  "role": "codeur_B",
  "liste_blanche_version": "1.0.0",
  "elements_transmis": [
    { "nom": "dossier_sources", "sha256": "…" },
    { "nom": "mepa_whitelist_keys.json", "sha256": "…" }
  ],
  "elements_interdits_verifies_absents": ["trajectoire_attendue", "psi_cible_tableau", "fiche_codeur_E"],
  "requete_complete_sha256": "…"
}
```

### 6.6 Stockage (esquisse)

```sql
CREATE TABLE artefacts (
  artefact_id      UUID PRIMARY KEY,
  type             TEXT NOT NULL,
  schema_version   TEXT NOT NULL,
  wp_id            TEXT NOT NULL,
  passe            INTEGER,
  payload_sha256   TEXT NOT NULL UNIQUE,
  parents          TEXT[] NOT NULL DEFAULT '{}',
  produit_par      JSONB NOT NULL,
  payload          JSONB NOT NULL,
  created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE wp_etat (
  wp_id        TEXT,
  passe        INTEGER,
  etat         TEXT NOT NULL,
  artefact_courant UUID REFERENCES artefacts(artefact_id),
  maj          TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (wp_id, passe)
);
```

Les fichiers (`result.json`, rapports, passeports) restent écrits dans `/data/mepa/outputs/` et synchronisés par Nextcloud (DEP5) ; le bus en conserve le SHA-256 et le chemin. Le Tableau de contrôle devient une vue SQL sur `wp_etat` et `artefacts`.

---

## 7. Pare-feu épistémique — spécification

| Élément | Documentaliste | Codeurs E/B | Arbitre | Rédacteur | Contradicteur |
|---|:-:|:-:|:-:|:-:|:-:|
| Intitulé du cas, bornes | ✓ | ✓ | ✓ | ✓ | ✓ |
| Définitions whitelist | ✓ | ✓ | ✓ | ✓ | ✓ |
| `dossier_sources` | — | ✓ | ✓ | ✓ | ✓ |
| Fiche de l'autre codeur | ✗ | ✗ | ✓ | — | ✓ |
| Trajectoire attendue / Ψ_cible (Tableau) | ✗ | ✗ | ✗ | ✓ | ✓ |
| Résultats runner / N1 / N2 | ✗ | ✗ | ✗ | ✓ | ✓ |
| Passeports antérieurs | ✗ | ✗ | ✗ | ✓ | ✓ |

✓ transmis · ✗ interdit et vérifié absent · — non pertinent

**Mécanisme.** L'orchestrateur est le seul à assembler un contexte. Avant envoi, il vérifie l'absence des éléments interdits (recherche des identifiants, labels D4 et valeurs cibles du WP dans la requête sérialisée), puis écrit le `context_manifest`. Un contexte non conforme n'est pas envoyé.

**Portée probatoire.** Le manifest prouve ce qui a été transmis à l'agent. Il ne prouve pas l'absence de connaissance préalable du modèle sur le cas historique : cette limite est **documentée, pas masquée**.

---

## 8. Reproductibilité des appels LLM

- Modèle épinglé par identifiant exact ; température 0 ; `max_tokens` déclaré par rôle (cf. correctif T1-A CONV-A).
- Prompts système versionnés dans git ; leur SHA-256 figure dans `produit_par`.
- Requête et réponse complètes archivées (compressées) pour chaque appel.
- **Mesure de variance.** En phase 2, triple exécution des codeurs sur un WP du cluster pilote avec contexte identique : écart par variable publié comme métrique. Objectif : quantifier la part de variance due au LLM seul, distincte de la résolution (D-3).

---

## 9. Stack technique

| Fonction | Proposition | Remarque |
|---|---|---|
| Orchestration | Python versionné (machine à états explicite ; LangGraph envisageable pour les reprises sur erreur) | Décision Q-5 |
| Déclencheurs, alertes | n8n conservé | Rôle réduit à ce qu'il fait bien |
| Bus | PostgreSQL existant + pgvector | Pas de nouveau service |
| Validation | Pydantic (schémas §6) ; `mepa_passeport_schema.py` inchangé | |
| LLM | API Anthropic, modèle épinglé | Deuxième famille selon Q-4 |
| Sentinelle | Claude Code headless déclenché par hook git | Lecture seule |
| Local (Pi 5) | Modèles 7–8B quantifiés via Ollama : tri, extraction légère uniquement | Inadaptés au codage historique |
| Hermes Agent | Candidat à évaluer par le CTO | Critères : respect du pare-feu, archivage intégral des requêtes, orchestration versionnable |

---

## 10. Feuille de route et critères d'acceptation

Séquencement compatible CV15 Option C (pistes parallèles). Chaque phase se clôt par un verdict PASS / FAIL soumis à Antoine.

### Phase 0 — Bus, schémas, tableau généré
*Impact méthodologique : aucun. Aucun fichier de production modifié.*

| Critère | Seuil |
|---|---|
| Ingestion des 6 passeports V7 certifiés et des fiches V6.2 / V7 dans le bus | 100 %, sans perte de champ |
| Validation par schéma des fiches existantes | PASS sur l'ensemble, ou anomalies listées et qualifiées |
| Vue Tableau de contrôle générée | Identique au contenu manuel pour les 6 lignes pilotes |
| Sorties runner | Non touchées (aucun changement de code) |

### Phase 1 — Sentinelle CI

| Critère | Seuil |
|---|---|
| Défauts injectés détectés : constante modifiée, clé `g`, altération de `_step()`, label D4 hors liste | 4/4 |
| Faux positifs sur 10 commits légitimes | 0 |
| Temps d'exécution sur le Pi | Mesuré et jugé acceptable par Antoine |

### Phase 2 — Orchestrateur, pare-feu, Arbitre
*Impact méthodologique : oui (8d remplacé). Conditionnée à Q-2 et Q-3.*

| Critère | Seuil |
|---|---|
| Rejeu d'un WP pilote (proposition : WP-C1-1 Haïti) avec fiche résolue gelée | Blocs `simulation`, `verdict`, `stress_n1`, `stress_n2` bit-identiques au passeport certifié |
| `resolution_detail` | Non vide, valide, chaque variable dans la whitelist |
| `context_manifest` | Présent pour chaque appel LLM ; zéro élément interdit détecté |
| Mesure de variance LLM (§8) | Publiée |
| Tests T1–T6 | PASS |

### Phase 3 — Documentaliste, vérificateur, diversité des codeurs
*Conditionnée à Q-4 et Q-6.*

| Critère | Seuil |
|---|---|
| Vérificateur : erreurs numériques injectées dans un rapport | 0 faux négatif |
| Dossiers de sources sur les 6 WP pilotes | Chaque extrait référencé ; lacunes déclarées |
| Si Q-4 option C : κ Sonnet/Sonnet vs κ Sonnet/autre famille sur le cluster pilote | Écart publié et interprété par le QG |

### Phase 4 — Agents QG, puis montée en charge

- Greffier et Contradicteur opérationnels sur une décision réelle (proposition : CV16).
- Traitement des 21 WP restants selon la stratification (LOI PHYSIQUE → Fondateurs → Cœur → Stress), avec vérification systématique Sa=7 pour I3, I4, I9.

---

## 11. Décisions demandées au QG

| # | Objet | Options | Recommandation |
|---|---|---|---|
| **Q-1** | Adopter les principes P-1 à P-5 et engager les phases 0–1 | Oui / Non / Oui avec amendements | **Oui** — aucun impact méthodologique |
| **Q-2** | Remplacer la mécanique 8d par un `resolution_detail` explicite gelé en H1, comme opérationnalisation de CV16 | A. Oui, dans une décision CV16 unique · B. Oui, décision distincte de CV16 · C. Non | **A** — même objet, une seule décision |
| **Q-3** | Ériger le pare-feu épistémique (§7) en règle de protocole | A. Règle bloquante · B. Mesure consultative (manifest sans blocage) · C. Non | **A** après une passe en B sur la phase 2 |
| **Q-4** | Traiter le biais corrélé des codeurs (D-7) | A. Statu quo (Sonnet × 2) · B. Codeur B sur une autre famille de modèles (changement de protocole, re-baseline) · C. Mesure seule : troisième codeur d'une autre famille hors certification, pour quantifier le biais sans modifier le protocole | **C d'abord**, décision A/B sur données |
| **Q-5** | Lieu de l'orchestration | A. n8n conservé comme orchestrateur · B. Python versionné, n8n pour déclencheurs/alertes · C. Hermes Agent (après évaluation CTO) | **B**, C en évaluation parallèle |
| **Q-6** | Périmètre du Documentaliste | A. Sources textuelles seules · B. + NAVCO pour les WP contemporains · C. Reporter | **B** pour C2, C5, C6 et WP contemporains, sous réserve d'analyse de compatibilité de codage |

---

## 12. Risques et mesures

| Risque | Mesure |
|---|---|
| Complexité ajoutée pour un chercheur seul | Phases courtes, chacune utile seule ; les phases 0–1 livrent de la valeur sans engager la suite |
| Régression silencieuse du cœur | I-1 et I-2 ; Sentinelle CI ; rejeu bit-identique obligatoire en phase 2 |
| Coût API accru (triple codage, vérificateur, dossier) | Coût mesuré en phase 2 sur un WP avant extrapolation aux 21 |
| Dépendance à un fournisseur | Enveloppe d'artefact agnostique ; Q-4 introduit une seconde famille |
| Contamination via le dossier de sources | Nuance §5.1 ; manifest §7 ; limite documentée |
| Agent qui « corrige » au lieu de signaler | Sentinelle en lecture seule ; Arbitre à règles fermées ; aucun agent n'écrit dans `config/` ni `scripts/` |
| Charge du Pi 5 | Appels LLM distants ; modèles locaux limités au tri ; mesure en phase 1 |

---

## 13. Hors périmètre

- Toute modification des équations, constantes ou labels D4.
- Le chantier Dev 2 (variable D, CV9 / CV10 / CV11), qui suit son propre cycle.
- L'automatisation des opérations git, Docker et Nextcloud, qui restent exécutées par Antoine.

---

## Annexe A — Points à vérifier sur `main` avant exécution

1. **Libellé du Nœud 2 dans `mepa_workflow_n8n_V7.json`.** La copie du contexte projet affiche « Audit C1→C13 [mepa_node2_audit_v62.js v2.1] » alors que la V7 déploie `mepa_node2_audit_v7.js` v3.0.0 (C14, C15 actifs). Vérifier s'il s'agit d'un libellé non mis à jour ou d'un code embarqué V6.2.
2. **Contrat 8c → 8d.** Relever les noms de champs réellement émis et attendus, pour documenter précisément le défaut que `resolution_detail` corrige.
3. **Emplacement et nom canonique de T6** (`mepa_test_rampe_segmentation.py`) pour intégration dans la Sentinelle.
4. **État de la décision CV16.** Confirmer qu'elle n'a pas été formalisée depuis le 2026-09-09.

---

*ARCH-AG-01 rev. 0 — proposition non décisionnelle — MEPA V7.0 — 2026-09-29*
