# MEPA — C-1 : traçage des écarts E / Rc / γ / L0 entre fiche CONV-E et passeport
**De :** CTO · **À :** QG · **Date :** 2026-09-29
**Objet :** prérequis bloquant de la phase 2 (Décision QG ARCH-AG-01, C-1)
**Base :** code du workflow `mepa_workflow_n8n_V7.json` + fiches V7/V6.2 du projet + 6 `result.json` de juin (session de certification, 19-22 juin)

---

## 1. Réponse

Les quatre variables sont modifiées **à un seul endroit : le nœud CONV-E** (nœud LLM de codage), lignes 179-204 de son code. Aucun autre nœud ne les modifie. Le Nœud 8d n'y est pour rien.

Le runner ne simule pas les `commandes` de la fiche : il simule une **seconde sortie du LLM CONV-E**, `commandes_mises_a_jour`, produite dans le même appel que les variables codées.

Ceci corrige et remplace l'explication « propagation CONV-B via 8a → 8d » de ma note sur la reproductibilité, qui était fausse.

---

## 2. Chaîne causale, nœud par nœud

| # | Nœud | Effet sur E / Rc / γ / L0 | Preuve |
|---|---|---|---|
| 0 | Fiche V7 (entrée) | `commandes.{E,Rc,gamma}` et `conditions_initiales.L0` = valeurs normatives. `variables.{E_split,A_r_c,gamma,L_t}.valeur` = **null** (à coder au run). `A_r_ne` pré-rempli. | Fiches V7 et V6.2 identiques sur ces champs (6/6) |
| 1 | **CONV-E [LLM]** | **ÉCRIT.** Le prompt exige deux blocs : `variables_codees` et `commandes_mises_a_jour` + `L0_mis_a_jour`. Le code écrase `commandes.{E, gamma, Rc, Rn}` (liste `CMD_MAPPING_LIBRE`) et `conditions_initiales.L0`. `R` et `Mob` explicitement préservés. | l. 95-113 (format demandé), l. 179-204 (écriture) |
| 2 | Nœud 2 (audit C1-C15) | Relais pur : `cmd = fiche.commandes`, `y0` depuis `conditions_initiales`, conversion numérique, aucun bornage. Construit aussi `mepa_full_vars` depuis `fiche.variables`. | l. 811-831, l. 893-900 |
| 3 | 8a (CONV-B, CCI) | Ne modifie rien. Audite `mepa_full_vars`, c'est-à-dire les `variables` codées, pas les `commandes`. | — |
| 4 | 8d | **Inerte.** `scores_resolus` toujours `{}` (8a lit `cci_result.resolution` / `"MOYENNE"` / `valeur_retenue` ; le calculateur produit `instructions_resolution` / `"MOYENNE_AUTO"` / `valeurs_finales_provisoires`). `cmd_brut` n'est assigné nulle part. Défaut supplémentaire : le bloc de correction L0 modifie une copie locale jamais réinjectée. | code 8d intégral ; `mepa_kappa_calculator.py` l. 585, 657-658 |
| 5 | P, 3 | Aucune écriture sur ces valeurs. | recherche d'affectations : 0 |
| 6 | Runner v3 | Simule `cmd` reçu. Lit `A_r_c` depuis `cmd.Rc` pour le précheck α. | `mepa_runner_v3_v7.py` l. 767 |

---

## 3. Vérification sur fichiers réels (6 pilotes, juin)

Si CONV-E est le seul point de modification, l'ensemble des variables qui diffèrent entre la fiche et le `result.json` doit être inclus dans le périmètre que son code autorise (`E, gamma, Rc, Rn, L0`), et tout le reste (`T, Mob, R, Ref, EROI, Pop, S0, C0, I0`) doit être intact.

| WP | Variables modifiées | Hors périmètre CONV-E |
|---|---|---|
| Rwanda | E, Rc, L0 | aucune |
| Allemagne | Rc | aucune |
| Commune | E, Rc, L0 | aucune |
| Rome | Rc | aucune |
| Haïti | E, Rc, γ, L0 | aucune |
| Égypte | E, Rc, γ, L0 | aucune |

**0 violation.** Le mécanisme était donc actif pendant la session de certification, même si le code lu est la version courante du workflow (les correctifs de juillet ne touchent pas le nœud CONV-E).

Amplitudes observées : Rwanda Rc 0.60 → 0.90, Allemagne Rc 0.65 → 0.35, Égypte Rc 0.55 → 0.62. Ce ne sont pas des arrondis : ce sont des recodages.

La divergence juin / juillet sur Commune et Haïti s'explique par la même cause : chaque run rappelle le LLM CONV-E, qui recode. Égypte est restée identique entre les deux runs.

---

## 4. Trois constats qui dépassent la question posée

### 4.1 Température non fixée sur quatre nœuds LLM — provenance déclarée inexacte
Le payload d'appel ne contient **aucun paramètre `temperature`** sur CONV-E, 8a (CONV-B CCI), 6b (CONV-B audit final) et 13 (Popper). L'API applique alors sa valeur par défaut, soit 1.0. Seul le Nœud 6 (CONV-A) fixe `temperature: 0`.
Or chaque passeport déclare `provenance_ia.temperature: 0` : cette valeur est écrite en dur par le schéma, pas mesurée. **La provenance archivée des 6 pilotes est inexacte sur ce point.** C'est aussi la cause probable de l'essentiel de la variance inter-run observée (CCI 0.86-0.93 sur Égypte, recodages Commune/Haïti).

### 4.2 L'audit et la simulation ne portent pas sur la même valeur
Le CCI (8a) est calculé sur `variables_codees` (E_split, A_r_c, γ, L_t). Le runner simule `commandes_mises_a_jour` (E, Rc, γ, L0). Ce sont **deux sorties distinctes du même appel LLM**, sans lien programmatique : rien ne garantit que `commandes.Rc == variables.A_r_c.valeur`. La concordance visible dans le précheck α est tautologique, puisque le runner relit `cmd.Rc`.
Je n'ai trouvé la sortie brute CONV-E (`conv_e_raw`) dans aucun artefact archivé en ma possession : je ne peux donc pas vérifier si les deux sorties concordaient pour les 6 pilotes.

### 4.3 CONV-B n'a eu aucun effet sur les entrées simulées
8d étant inerte, les 6 pilotes ont été simulés sur les valeurs de CONV-E seul. CONV-B a joué un rôle d'audit de fiabilité (CCI, verdict), sans rétroaction sur la simulation. C'est un fait sur le protocole réellement exécuté lors de la certification, que je transmets sans l'interpréter.

---

## 5. Conséquences pour la suite (propositions, rien n'est modifié)

- **CV16 / gel en H1** : l'objet à geler est identifié avec précision : `commandes.{E, gamma, Rc, Rn}` et `conditions_initiales.L0` après CONV-E, plus le vecteur de variables codées. Le gel en H1 garde tout son sens, et il est plus nécessaire encore puisque la variance vient du codeur lui-même.
- **Une seule source pour l'audit et la simulation** : dériver les `commandes` de façon déterministe à partir des `variables_codees` (mapping fixe E_split → E, A_r_c → Rc, γ → γ, L_t → L0) au lieu de les demander une seconde fois au LLM. C'est ce qui rend le κ opposable à la simulation. Modification de pipeline : à décider avec la rev. 1 et CV16.
- **Température** : fixer `temperature: 0` sur CONV-E, 8a, 6b, 13 ; enregistrer la valeur **effectivement transmise** par nœud dans le passeport (cohérent avec Q-4). Correction technique, mais elle change la distribution des sorties par rapport à la certification : je la propose pour les 21 WP, pas en rétroactif.
- **Nœud 8d / 8a** : ne pas corriger en l'état. Activer 8d changerait le protocole par rapport à celui sous lequel les pilotes ont été certifiés. Suppression ou refonte à trancher dans CV16.
- **Pare-feu C-2** : la valeur `A_r_ne` pré-remplie (Rn) transite par la sortie LLM (`"Rn": <float A_r_ne hardcodé>`), puis réécrit `commandes.Rn`. Elle est restée intacte sur 6/6, mais une valeur fixée hors codage ne devrait pas pouvoir être réécrite par le codeur. C'est un cas concret de la catégorie « valeurs pré-enregistrées » de C-2.

---

## 6. Décisions demandées au QG

1. Prendre acte que la chaîne est CONV-E → runner, sans intervention de CONV-B sur les entrées, pour les 6 pilotes certifiés.
2. Statuer sur la mention `temperature: 0` des passeports pilotes : correction par note de provenance (sans toucher aux valeurs scientifiques), ou maintien avec mention en annexe.
3. Valider la fixation de `temperature: 0` sur les quatre nœuds pour les 21 WP.
4. Intégrer la « source unique audit/simulation » dans le périmètre de CV16.

*CTO — MEPA V7.0 — 2026-09-29*
