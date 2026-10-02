# WP-F10-1 — Commune de Paris (1871)
## Working Paper MEPA V7-α rev. 2.1 | Cluster C2 | Sa = 4

---

## S1 — Contexte historique et codage MEPA Full

### 1.1 Narration historique

La Commune de Paris (18 mars – 28 mai 1871) constitue l'épisode révolutionnaire le plus bref et le plus intense du cycle républicain français du XIXe siècle. Elle naît dans le contexte immédiat de la défaite franco-prussienne, de la capitulation de Napoléon III à Sedan (2 septembre 1870), de l'armistice humiliant du 28 janvier 1871 et de l'élection d'une Assemblée nationale à majorité monarchiste et rurale, perçue par Paris comme une trahison. La tentative du gouvernement de Thiers de désarmer la Garde nationale parisienne le 18 mars 1871 — en récupérant les canons de Montmartre — déclenche l'insurrection : les soldats fraternisent avec la foule, les généraux Lecomte et Thomas sont fusillés, et le gouvernement se replie à Versailles.

La Commune s'installe au pouvoir pendant 72 jours. Elle adopte une série de mesures sociales et politiques radicales : séparation de l'Église et de l'État (décret du 2 avril 1871), remise des loyers, moratoire sur les dettes, gratuité de l'enseignement, autogestion de certaines usines abandonnées par leurs propriétaires. Mais elle est traversée dès l'origine par des courants idéologiques profondément antagonistes — Jacobins centralisateurs, Blanquistes insurrectionnels, Proudhoniens fédéralistes, Internationalistes — qui paralysent la prise de décision et empêchent toute doctrine unifiée. Le Comité de salut public, créé le 1er mai, est immédiatement contesté par la minorité fédéraliste.

Sur le plan militaire, la Commune ne parvient pas à briser le siège versaillais. L'armée de Versailles, reconstituée grâce à la libération anticipée des prisonniers de guerre par Bismarck, entre dans Paris le 21 mai 1871. La Semaine sanglante (21-28 mai) voit l'écrasement systématique des fédérés barricade par barricade. Le bilan humain est catastrophique : entre 10 000 et 30 000 Communards tués (les estimations varient selon les sources), 38 000 arrestations, 7 500 déportations en Nouvelle-Calédonie. La répression versaillaise est d'une brutalité sans précédent dans l'histoire révolutionnaire française du XIXe siècle.

**Fracture de l'élite (E_split = 0.63)** : La fracture est réelle et profonde — entre une élite républicaine modérée ralliée à Versailles (Thiers, Favre, Simon) et une élite radicale parisienne engagée dans la Commune (Delescluze, Vallès, Courbet). Mais cette fracture reste incomplète : une fraction significative de la bourgeoisie républicaine, hostile à la fois à la Commune et à la restauration monarchiste, reste attentiste. E_split = 0.63 reflète une fracture naissante-avancée sans atteindre la rupture totale.

**Capacité organisationnelle de l'élite (γ = 0.15)** : La valeur la plus discriminante du cas. L'élite communarde est numériquement présente mais organisationnellement défaillante. Absence de commandement militaire unifié, rivalités entre comités, improvisation tactique permanente, incapacité à coordonner une sortie offensive avant que le siège ne soit bouclé. γ = 0.15 est la valeur caractéristique d'une *V_col sans doctrine* — une coalition de volontés sans architecture institutionnelle.

**Capacité redistributive effective (A_d_eff = 3.5)** : La Commune hérite d'une économie parisienne dévastée par le siège prussien. Les caisses de la Banque de France sont intactes mais la Commune, par scrupule légaliste, n'y touche pas (décision qui sera rétrospectivement jugée fatale). Les mesures redistributives adoptées (remise des loyers, moratoire sur dettes) sont réelles mais leur portée pratique est limitée par la durée de l'épisode et l'état de guerre permanent. A_d_eff = 3.5 reflète une capacité redistributive faible, en zone de trappe à dette basse.

**Répression classique (A_r_c = 0.8)** : La répression versaillaise est massive et organisée. L'armée régulière reconstituée dispose d'une supériorité numérique et logistique écrasante. A_r_c = 0.8 reflète la capacité répressive effective de l'État versaillais, pas de la Commune elle-même.

**Répression numérique/non-étatique (A_r_ne = 0)** : Cas pré-numérique. Aucune infrastructure de surveillance électronique. Les réseaux de délation existent mais sont informels et non systématisés. A_r_ne = 0 par convention V6.2.

**Crédibilité du régime (Cs = 0.22)** : La crédibilité du gouvernement de Versailles est faible à Paris — il est perçu comme capitulard, monarchiste et anti-parisien. La crédibilité de la Commune elle-même est forte dans les quartiers populaires mais inexistante dans les quartiers bourgeois. Cs = 0.22 reflète la crédibilité du régime *en place* (Versailles) vue depuis la population mobilisée.

**Loyauté des appareils (L(t) = 0.32)** : La Garde nationale est loyale à la Commune dans les premiers jours, mais cette loyauté se fragmente rapidement. Les unités de l'armée régulière restent loyales à Versailles. L(t) = 0.32 reflète une loyauté institutionnelle faible et instable.

**EROI = 7** : La France de 1871 est en phase d'industrialisation avancée, avec un EROI charbon-vapeur estimé à 7. Ce niveau est suffisant pour soutenir une mobilisation industrielle mais insuffisant pour compenser les destructions de la guerre franco-prussienne.

**Sa = 4 (nucléaire égalitaire)** : La structure anthropologique Todd pour la France est nucléaire égalitaire — héritage égalitaire, individualisme fort, faible autorité parentale. Sa = 4 est la valeur standard pour la France du XIXe siècle.

---

### 1.2 Tableau de codage MEPA Full V6.2 — 9 variables

| Variable | Symbole | Valeur | Source principale | Justification synthétique |
|---|---|---|---|---|
| Fracture élite | E_split | 0.63 | Tombs 1981 (S3) | Fracture Versailles/Commune réelle mais incomplète ; bourgeoisie républicaine attentiste |
| Cohésion élite | γ | 0.15 | Rougerie 1971 (S5) ; Lissagaray 1876 (S1) | V_col sans doctrine : rivalités Jacobins/Blanquistes/Proudhoniens, absence commandement unifié |
| Capacité redistributive | A_d_eff | 3.5 | Merriman 2014 (S7) | Économie dévastée post-siège ; mesures redistributives réelles mais portée limitée |
| Répression classique | A_r_c | 0.8 | Tombs 1981 (S3) | Armée versaillaise reconstituée, supériorité numérique et logistique écrasante |
| Répression numérique | A_r_ne | 0 | Convention V6.2 | Cas pré-numérique |
| Crédibilité régime | Cs | 0.22 | Ross 2015 (S2) | Versailles perçu comme capitulard et anti-parisien dans les quartiers populaires |
| Loyauté appareils | L(t) | 0.32 | Lissagaray 1876 (S1) | Garde nationale loyale initialement, fragmentation rapide ; armée régulière loyale à Versailles |
| Rendement énergétique | EROI | 7 | Wrigley 1988 (S6) | France industrialisation avancée, charbon-vapeur ; destructions guerre franco-prussienne |
| Structure anthropologique | Sa | 4 | Todd 1990 (S4) | Nucléaire égalitaire — valeur standard France XIXe siècle |

---

### 1.3 Tableau de codage MEPA Full V7 — 6 variables

| Variable | Symbole | Valeur | Source principale | Justification synthétique |
|---|---|---|---|---|
| Stade matrice religieuse | M_r | 2 | Todd 1990 (S4) | Catholicisme en transition zombie : anticléricalisme républicain structurant, décret séparation 2 avril 1871, exécution otages ecclésiastiques — résidus culturels sans centralité institutionnelle |
| Polarisation mimétique | μ_m | 0.50 | Tombs 1981 (S3) ; Rougerie 1971 (S5) | Polarisation forte Versaillais/Communards, guerre civile, Semaine sanglante — MAIS antagonisme politique et de classe, sans désignation d'une cible démographique homogène ; μ_m = 0.50 < μ_m* = 0.60 |
| Fragmentation symbolique | Φ | 0.65 | Ross 2015 (S2) ; Rougerie 1971 (S5) | Pluralisme interne fort : Jacobins, Blanquistes, Proudhoniens, Anarchistes, presse libre, débats ouverts au Conseil — antithèse du monopole symbolique sacrificiel |
| Proportion noyau engagé | Ψ_noyau | 0.10 | Rougerie 1971 (S5) ; Lissagaray 1876 (S1) ; Merriman 2014 (S7) | Membres actifs comités de section + fédérés Garde nationale / population parisienne ≈ 2M ; engagement réel et soutenu sur 72 jours |
| Cible démographique désignée | Ψ_cible | **null** | Tombs 1981 (S3) ; Rougerie 1971 (S5) ; Lissagaray 1876 (S1) ; Merriman 2014 (S7) | Voir règle E3 rev. 2.1 — justification positive obligatoire ci-dessous |
| Capacité organisationnelle noyau | γ_local | 0.18 | Tombs 1981 (S3) ; Rougerie 1971 (S5) ; Lissagaray 1876 (S1) | Désorganisation interne marquée : comités multiples en compétition, absence doctrine unifiée, commandement central ineffectif sur 72 jours |

**Justification E3 rev. 2.1 — Ψ_cible = null (justification positive obligatoire)** :

> Les sources historiques consultées [Tombs 1981 (S3), Rougerie 1971 (S5), Lissagaray 1876 (S1), Merriman 2014 (S7)] ne mentionnent aucune désignation publique de cible démographique unique au sens de la trajectoire (α). La Commune de Paris organise son antagonisme selon des lignes politiques et de classe — Versaillais contre Communards, bourgeoisie contre prolétariat parisien — mais ne désigne jamais un groupe démographique homogène (défini par l'origine, la religion ou l'ethnicité) comme cible sacrificielle. Les exécutions d'otages (dont l'archevêque Darboy, 24 mai 1871) sont des représailles politiques contre des individus représentant une institution, non l'extermination d'un groupe démographique. La fracture principale du cas est codée dans E_split = 0.63 comme fracture politique et de classe entre deux gouvernements rivaux. L'absence de Ψ_cible est donc une propriété positive du cas, pas une omission : la Commune de Paris est structurellement incompatible avec la trajectoire (α) Cristallisation sacrificielle d'État.

---

### 1.4 Conversion des scores en paramètres p1–p13

| Paramètre | Formule de conversion | Valeur |
|---|---|---|
| p1 (pression sociale) | S₀ = 0.5 + 0.5 × E_split | 0.815 |
| p2 (chaleur latente) | L₀ = L_t | 0.32 |
| p3 (chaleur collective) | C₀ = (1 − Cs) × 0.15 | 0.117 |
| p4 (complexité institutionnelle) | I₀ = A_d_eff + 2 | 5.5 |
| p5 (mobilisation) | T = 0.95 (fiche) | 0.95 |
| p6 (dissipation) | R_param = 0.20 (fiche) | 0.20 |
| p7 (répression classique) | Rc = A_r_c | 0.80 |
| p8 (répression numérique) | Rn = A_r_ne | 0.00 |
| p9 (cohésion élite) | γ = 0.15 | 0.15 |
| p10 (fracture élite) | E = E_split | 0.63 |
| p11 (EROI) | EROI = 7 | 7.00 |
| p12 (structure anthropologique) | Sa = 4 | 4 |
| p13 (loyauté) | L_param = L_t | 0.32 |

**Modulateur Sa** : Sa = 4 (nucléaire égalitaire) → pas de modulation p6 (modulateur Sa = 7 uniquement). p6 nominal = 0.20.

---

### 1.5 Précheck V7 — Conditions C1–C4 de la branche (α)

```
C1 = (M_r = 2 ∈ {1, 2}) AND (μ_m = 0.50 > μ_m* = 0.60)
   = TRUE AND FALSE
   = FALSE ← échec sur la sous-condition mimétique

C2_sigma = 0.018 × (1 + 1.7 × Φ) = 0.018 × (1 + 1.7 × 0.65)
         = 0.018 × (1 + 1.105) = 0.018 × 2.105 = 0.03789
C2 = Ψ_noyau

### 1.6 Anomalie documentée


B.3.1 — Énoncé neutre de la divergence
Le modèle V7 a produit la trajectoire (b) Répression réussie alors que la trajectoire attendue était (a) Rupture transformatrice. Cette divergence est robuste sur 11 passes (base + 2 passes N1 optimiste/pessimiste + 8 combinaisons N2), toutes diagnostiquées (b).

B.3.2 — Signature numérique observée

FR_max = 0.2908 · FR_final = 0.2404
t_bascule = null (branche α exclue avant simulation ; F < R sur toute la simulation)
I_min_sim = 3 · I_final = 3
C_max = 0.1639 · C_final = 0.1368
S_final = 0.857 · L_final = 0.3427
Robustesse N1 = ROBUSTE · N2 = ROBUSTE (8/8 combinaisons en (b))
Précheck (α) : C1 = faux (μ_m = 0.50 < μ_m* = 0.60), C2 = faux (Ψ_noyau × γ_local = 0.10 × 0.18 = 0.018 < σ(Φ=0.65) = 0.03789), C3 = faux (Ψ_cible = null), C4 = vrai


B.3.3 — Renvoi à CONV-C pour chantier V8
Cette anomalie est renvoyée à CONV-C pour traitement dans le chantier V8 de révision théorique. Elle ne peut pas être interprétée dans le cadre actuel du modèle.

B.3.4 — Interdiction explicite d'interprétation alternative
Le présent rapport n'interprète pas le diagnostic divergent comme un résultat empirique valide. Toute interprétation théorique du diagnostic divergent est explicitement interdite par le protocole anti-rationalisation V7-C3.

### 1.7 Hypothèse théorique sous contrainte

La divergence (a) Rupture transformatrice → (b) Répression réussie résulte d'une configuration paramétrique spécifique : A_r_c = 0.80 (capacité répressive institutionnelle forte) combinée à γ_local = 0.18 (noyau désorganisé), maintenant F < R sur toute la simulation. Cette configuration suggère que le modèle V7 capture la résolution militaire à court terme de l'épisode, mais ne dispose pas à ce stade d'un mécanisme pour distinguer les cas où une répression forte coexiste avec une potentielle capacité transformatrice de l'acteur insurgé. La direction de résolution candidate est l'introduction d'une variable d'asymétrie temporelle distinguant la résolution de court terme (issue militaire immédiate) de la transformation institutionnelle de moyen terme. La prédiction structurelle de l'hypothèse est la suivante : lorsque A_r_c > 0.70, le modèle V7-α rev. 2.1 produit systématiquement (b), indépendamment de γ_local et de la trajectoire historique effective.

**Prédiction falsifiable sur WP-F8-1 France Révolutionnaire 1789-1799 (cas non encore simulé en V7)** : WP-F8-1 France Révolutionnaire présente une trajectoire attendue (a), un appareil répressif institutionnel initialement plus faible (A_r_c attendu < 0.55 — l'Ancien Régime s'effondre avant que l'armée révolutionnaire ne soit constituée) et une capacité organisationnelle du Comité de Salut Public structurellement supérieure à la Commune (γ_local attendu > 0.35 — doctrine jacobine unifiée, commandement militaire centralisé, hiérarchie fonctionnelle). Si le modèle V7 produit (a) pour WP-F8-1 avec ces paramètres, l'hypothèse est supportée : la capacité répressive de l'État adversaire est bien le déterminant dominant de la bascule (b) vs (a), et la Commune échoue à (a) structurellement en raison de A_r_c = 0.80. Si le modèle produit (b) pour WP-F8-1 malgré un A_r_c < 0.55, l'hypothèse est réfutée et une variable de capacité transformatrice distincte de γ_local devra être introduite en V7.1.

*Cette hypothèse est spéculative. Elle n'interprète pas le diagnostic (b) Répression réussie comme un résultat empirique valide pour le cas Commune de Paris. Elle relève du chantier V7.1 et ne sera testable qu'après codage V7 complet de WP-F8-1 France Révolutionnaire.*

---

## Récapitulatif des insertions

| WP | Fichier cible | Position d'insertion | Titre exact |
|---|---|---|---|
| WP-I4-1 Allemagne | `WP-I4-1_rapport.md` | Après `### 1.6 Anomalie documentée` | `### 1.7 Hypothèse théorique sous contrainte` |
| WP-F10-1 Commune | `WP-F10-1_rapport.md` | Après `### 1.6 Anomalie documentée` | `### 1.7 Hypothèse théorique sous contrainte` |

## Suite opérationnelle après insertion

1. Relancer CONV-B sur **WP-F10-1** (Commune) — fichiers requis : `WP-F10-1_rapport.md` (version avec §1.6 + §1.7) + `WP-F10-1_result.json`
2. Relancer CONV-B sur **WP-I4-1** (Allemagne) — fichiers requis : `WP-I4-1_rapport.md` (version avec §1.6 + §1.7) + `WP-I4-1_result.json`
3. Critère de clôture : les deux `audit_b.json` doivent afficher `CERTIFIE` ou `CONDITIONNELLE_V7` (pour Allemagne)
4. Transmettre les deux `audit_b.json` à QG → décision de certification V7.0 formelle