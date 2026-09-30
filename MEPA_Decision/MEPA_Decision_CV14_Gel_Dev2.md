# MEPA — Décision CV14 · Gel de Dev 2 (Dette) — suspension gated, non informelle

**Statut :** Décision de gouvernance (rôle CONV-C / QG)
**Type :** Suspension de chantier avec trigger de réactivation explicite (pas un report informel)
**Rattachement :** clôt provisoirement le Document de Décision Architecturale V6.3/V7 (02 juin 2026) et l'ensemble de ses suites Dev 2 (Note d'Architecture, Dossier consolidé, Instructions CV9/CV10/CV11)
**Date :** Juin 2026
**Numéro :** CV14 confirmé — CV13 (recalibration λ/μ) existe déjà (`MEPA_Decision_CV13_Recalibration.md`). Série : CV1-CV8 (Document de Décision V63/V7), CV9-CV11 (Note Dev 2), CV12 (codage multi-passes, workflow), CV13 (recalibration λ/μ), **CV14 (présente décision)**.

---

## 0. Portée de cette décision

CV14 **ordonnance** le chantier Dev 2 à un trigger de réactivation vérifiable. Elle ne tranche ni n'évalue la validité de fond des travaux gelés (§6), et elle ne résout pas l'articulation C/D (§4) — elle programme son instruction. Toute lecture de CV14 comme un règlement de Dev 2 serait erronée.

## 1. Constat

Le chantier Dev 2 (dette, variable d'état D) a été instruit à partir du Document de Décision Architecturale V6.3/V7 du 02 juin 2026, qui le désigne comme correcteur de la lacune **A1 — sévérité « Maximale »**, l'unique lacune qui fait changer le verdict de trajectoire sur des cas réels du périmètre contemporain. Ont suivi : Note d'Architecture, Dossier consolidé, Instructions CV9/CV10/CV11, et le gel advisory V6.3 (code testé, prêt à lancer).

Le projet a ensuite bifurqué vers V7 sur un axe — noyau sacrificiel, trajectoire α — absent des lacunes A1-A4 et des chantiers C0-C10 de cette feuille de route. La priorité n°1 qu'elle identifiait (la dette) n'a été ni intégrée ni formellement close.

**Vérification effectuée** (juin 2026, contre le dépôt `mepa/` réel) : `grep -rniE 'dev1|dev2|advisory|a_d_max|souv.?monetaire|D_max|dD.?dt'` sur l'ensemble des fichiers `.py`/`.js`/`.json` du dépôt — **aucune occurrence substantielle**. Confirmé en particulier sur `mepa_runner_v3_v7.py`, `mepa_node2_audit_v7.js`, `mepa_constants.json` : pas de bloc `advisory_dev1`, pas de `A_d_max` dérivé, pas de `souv_monétaire`. La branche V6.3/Dev (isolée dans `prepa_v6.3/`) n'a jamais fusionné avec le tronc V7.

C'est exactement le mode de défaillance déjà documenté pour la branche V6.3 : une pause sans trigger explicite se transforme en perte. Cette décision a pour seul objet d'éviter la récidive — sur ce qui est, selon le Document de Décision, la lacune la plus grave de V6.2. **Le gel n'est pas un enterrement : c'est la mise en attente, sous condition de réveil, de la priorité architecturale n°1.**

## 2. Décision

**Dev 2 est gelé** — Document de Décision V63/V7 (et ses CV pendantes, cf. §5), Instructions CV9/CV10/CV11, amendements C0/CV4/D_max, reformulation P-UK-1 : **statut « re-soumis, non acté »**. Aucune de ces décisions n'est validée ni invalidée par ce gel ; elles sont mises en sommeil dans l'état où les sessions stratégiques QG de juin 2026 les ont laissées — à l'exception de CV2/CV3, dont le statut est précisé au §5.

**Trigger de réactivation, explicite et unique :** certification de V7-γ rev. 2 sur le cluster pilote (les 6 WP — Rwanda, Allemagne nazie, Commune de Paris, Rome IIIe, Haïti, Égypte 2011 — en statut CERTIFIÉ ou CONDITIONNELLE_V7).

Tant que ce trigger n'est pas atteint, Dev 2 reste hors scope de toute session opérationnelle. Aucune session ne doit instruire C0, C1, C2, CV9, CV10 ou CV11 avant réactivation, sauf décision QG explicite contraire.

**Note de séquencement au trigger.** Le trigger CV14 est, à la date de rédaction, proche (5/6 WP validés, Égypte 2011 en attente de reconfirmation). À l'atteinte du trigger, la réactivation de Dev 2 entrera en concurrence directe avec un autre chantier également gaté sur la certification V7.0 : la production des grilles de pré-codage pour les 21 WP restants. CV14 ne tranche pas cet arbitrage de séquencement — il devra faire l'objet d'une décision QG dédiée au moment du trigger, et n'est mentionné ici que pour signalement.

## 3. Ce qui n'est PAS gelé — l'advisory Dev 1

Le module advisory (`mepa_dev1_advisory_v63.py`) est traité à part : dans sa forme **codée actuelle**, il pose `Ω = Sa/Sa_ref` (Sa constant) et ne lit donc que des commandes codées (`EROI`, `gamma`, `Pop`, `A_d_eff`/`R`) — il est de ce fait **invariant au runner** (V6.2 ou V7).

**Réserve importante (à trancher au réveil).** Cette invariance n'est pas une propriété de fond de Dev 1 : c'est le symptôme d'une **simplification provisoire**. Le Document de Décision V63/V7 spécifie (§7.2, M2) `C_maint = c_Ω × I(t)^θ` avec **Ω ≡ I** — la complexité institutionnelle, variable d'état dynamique — ce qui rend `A_d_max` *dépendant de la trajectoire*. Le code a substitué `Ω = Sa`, en le marquant explicitement « PROVISOIRE, à réviser ». Le choix n'est donc pas « facile vs difficile » mais :

- `Ω = Sa` (actuel) : détecteur grossier, hors boucle, runner-invariant, donnée identique sous V6.2 ou V7 ;
- `Ω ≡ I` (spec d'origine) : fidèle, lit la trajectoire, runner-**dépendant** → la donnée advisory reflète les trajectoires V7. **Probablement préférable si l'objectif est de calibrer Dev 2 pour V7**, pas pour V6.2.

Dans les deux cas le re-port reste **non-régressif** : l'advisory lit la trajectoire mais ne la modifie pas. Le test « passeports V7 identiques sauf bloc `advisory_dev1` ajouté » tient quelle que soit la forme de Ω retenue.

**Deux notions distinctes à ne pas confondre :**
- La **correction/non-régression** de l'advisory (re-port sur runner V7, test bit-identique hors bloc `advisory_dev1`) est **indépendante du trigger §2** — c'est un travail de plomberie qui ne préjuge d'aucune décision Dev 2 de fond, et qui pourrait en théorie être fait dès maintenant.
- Le **lancement effectif** d'une série de calibration sur le corpus V7-γ est en revanche **séquencé au réveil** (§2), pour une raison de propreté des entrées : à la date de rédaction, 5 des 6 fiches du cluster pilote V7-γ portent des échecs C14/C15 ouverts (`psi_cible`/`m_r` null sur plusieurs WP). Lancer l'advisory sur des entrées encore mouvantes produirait une série de calibration à refaire.

**Premier geste au réveil (avant toute reprise de CV9/CV10/CV11), dans l'ordre :**
1. **Trancher la forme de Ω** (`Sa` provisoire vs `I` fidèle) — c'est une réouverture de CV1, et elle détermine si la donnée est runner-invariante.
2. Re-porter l'advisory sur le runner V7 (greffe additive + test de non-régression V7), si pas déjà fait en amont au titre de la correction indépendante du trigger ci-dessus.
3. Lancer le corpus V7-γ certifié sous advisory pour fabriquer la série `A_d_max` dérivé / flags qui manque depuis juin.

## 4. Question à instruire pendant le gel — pas après

L'articulation entre le mécanisme de cristallisation sacrificielle (`C`, trajectoire α, déjà actif en V7) et le mécanisme de dette (`D`, Dev 2, gelé) n'est tranchée nulle part — et pour cause : la trajectoire α n'existait pas au 02 juin, le Document de Décision ne pouvait pas la prévoir. Les deux peuvent être deux canaux de compensation du même déficit de surplus net (`S*`) : un régime qui ne peut plus emprunter (D → D_max, non-souverain, mode défaut) est précisément un candidat à la bascule sacrificielle.

Cette question doit mûrir **pendant** le gel — et peut être instruite **dès maintenant** sur le pilote V7-γ existant, sans attendre la clôture complète du cluster ni rouvrir C0/C1/C2 : 5 des 6 fiches sont déjà certifiées ou conformes à l'attendu. Deux lectures concrètes, faisables sur les fiches disponibles :
- **Rwanda** ((α), CERTIFIÉ, CCI 0.78) : le cas montre-t-il une saturation préalable du canal informel de la dette (au sens large — capacité d'emprunt, soutenabilité externe) en précondition de la bascule sacrificielle, ou les deux mécanismes apparaissent-ils indépendants dans la trajectoire ?
- **Allemagne nazie** (échec C2 conforme à l'attendu, conditionnel) : la relation D → D_max est-elle lisible dans ce cas comme corrélée à la bascule, ou orthogonale ?

Cet examen reste qualitatif et hors gel formel (aucune fiche n'est rouverte, aucune équation Dev 2 n'est instruite) ; il vise seulement à nourrir la décision de fond — D comme variable indépendante, vs D et C couplés — qui conditionnera potentiellement la forme même de C1 au réveil. Aucune réponse n'est imposée par cette décision.

## 5. Registre des pièces gelées (archivage)

| Pièce | Nature | Statut au gel |
|---|---|---|
| `MEPA_Decision_V63_V7_ConvQG.md` | **Document de Décision parent** — diagnostic A1-A4, feuille de route C0-C10, jalons J1-J5, séries de décisions CV1-CV8 | re-soumis, non acté (statut des CV ci-dessous) |
| ↳ CV1 (forme de η_D) | Décision collégiale | tranchée **provisoirement** dans le code (η_D=γ, Ω=Sa) — à réviser |
| ↳ CV2 (Mode B advisory) · CV3 (M5 non bloquant) | Décisions collégiales | **implémentées dans le code** du gel V6.3 — statut de gouvernance non acté, à re-ratifier explicitement au réveil. L'implémentation ne vaut pas validation de la décision. |
| ↳ CV4-CV8 (ancre Sa=4, stochastique/P1, `D_seuil.sa4=null`→NC, commit atomique labels, séquencement C1<C6) | Décisions collégiales | pendantes |
| `MEPA_Note_Architecture_QG_Dev2_Dette.md` | Note d'architecture (3 prérequis : CV9, CV10, CV11 ; risques R7-R10) | re-soumise, non actée |
| `MEPA_Dossier_Architecture_Dev2_Dette_CONSOLIDE.md` | Référence consolidée | re-soumise, non actée |
| `MEPA_Instruction_CV9_Agregat_Dette.md` | Choix de l'agrégat de D | re-soumise, non actée |
| `MEPA_Instruction_CV10_Equation_dDdt.md` | Re-spécification des signes `dD/dt` | re-soumise, non actée — test [C3] Japon jamais exécuté |
| `MEPA_Instruction_CV11_Souverainete_Monetaire.md` | Souveraineté monétaire comme déterminant de D_max | re-soumise, non actée |
| `MEPA_Gel_V63_Specification.md` + code associé (`mepa_runner_v2_gamma_v63.py`, `mepa_dev1_advisory_v63.py`, `mepa_passeport_schema_v63.py`, `mepa_constants_v63.json`, `mepa_whitelist_keys_v63.json`, `CONV-E_Addendum_V63.md`, `test_nonregression_v63.py`) | Gel advisory V6.2→V6.3 — **code fini, testé bit-identique** | non lancé — relance de calibration séquencée au réveil (§3) ; la correction/re-port technique est indépendante du trigger |

*Toutes les pièces ci-dessus sont réunies dans `prepa_v6.3/`, distinct des dépôts actifs `mepa/` et `prepa_v7/`.*

## 6. Ce que CV14 ne tranche pas

- La validité de fond des CV1-CV11 — non réévaluée ici, simplement mise en sommeil.
- La forme de Ω dans l'advisory (`Sa` vs `I`) — réouverture de CV1, listée comme premier geste au réveil (§3).
- L'articulation C/D (§4) — volontairement laissée ouverte, à instruire pendant le gel sur le pilote disponible.
- L'arbitrage de séquencement entre réactivation Dev 2 et lancement des grilles de pré-codage 21 WP au trigger (§2) — décision QG distincte, à prendre au moment venu.
- La date du trigger — dépend de l'avancement réel de la certification V7-γ, non fixée a priori.

---

*Décision produite en session stratégique QG (rôle CONV-C), juin 2026. Suspension gated — réactivation conditionnée à la certification V7-γ rev. 2, non à une échéance calendaire.*
