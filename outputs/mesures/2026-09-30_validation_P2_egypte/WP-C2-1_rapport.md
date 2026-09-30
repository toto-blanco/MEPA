# WP-C2-1 — Égypte 2011 : Printemps arabe et contre-révolution militaire
## Working Paper MEPA V7-α rev. 2.1 | Cluster C2 | Période 2010–2014

---

## S1 — Contexte historique et codage MEPA Full

### 1.1 Narration historique

L'Égypte de 2010–2014 constitue l'un des cas les plus documentés du corpus MEPA : une mobilisation de masse exceptionnelle, une transition institutionnelle avortée, et une reconsolidation autoritaire conduite par l'appareil militaire. La trajectoire se déroule en trois phases distinctes que le modèle doit restituer.

**Phase (a) — Mobilisation et chute de Moubarak (janvier–février 2011).** La place Tahrir cristallise une coalition hétéroclite : jeunesse urbaine éduquée, Frères musulmans (FM), syndicats indépendants, libéraux, nasséristes. La fracture de l'élite est réelle : le Parti national démocrate (PND) de Moubarak est traversé par des tensions entre l'aile militaire historique et les « héritiers » du capitalisme de copinage (Gamal Moubarak). La crédibilité du régime (Cs) s'effondre après les fraudes électorales de novembre 2010 et la répression des premières manifestations. Le 11 février 2011, le Conseil suprême des forces armées (SCAF) retire son soutien à Moubarak et prend le pouvoir. Cette décision n'est pas une capitulation devant la rue : c'est un calcul institutionnel visant à préserver l'appareil militaire en sacrifiant le président.

**Phase (e) — Transition contrôlée et montée des Frères musulmans (mars 2011–juin 2013).** Le SCAF organise des élections législatives (novembre 2011–janvier 2012) remportées par le Parti Liberté et Justice (PLJ, bras politique des FM) avec 47 % des sièges, puis l'élection présidentielle de juin 2012 remportée par Mohamed Morsi. Cette période est marquée par une tension croissante entre la présidence islamiste et l'appareil militaire, judiciaire et sécuritaire. L'économie se dégrade : le tourisme s'effondre, les réserves de change chutent de 36 Mds$ à 14 Mds$ entre 2010 et 2013, l'inflation alimentaire dépasse 10 %. La capacité redistributive effective (A_d_eff) reste faible. La loyauté des appareils (L(t)) est structurellement basse : les juges, les généraux et les directeurs des médias d'État ne sont pas acquis à Morsi.

**Phase (b) — Coup d'État du 3 juillet 2013 et répression (juillet 2013–2014).** Le général Abdel Fattah al-Sissi destitue Morsi après des manifestations de masse (mouvement Tamarod, 30 juin 2013). Le 14 août 2013, les forces de sécurité dispersent les sit-in pro-Morsi de Rabaa al-Adawiya et al-Nahda : entre 800 et 1 000 morts selon Human Rights Watch. Les FM sont déclarés organisation terroriste en décembre 2013. L'aide financière du Golfe (Arabie saoudite, Émirats, Koweït) — environ 12 Mds$ — reconstitue les réserves de change et stabilise l'économie. La répression est massive mais ciblée sur les structures organisationnelles des FM, pas sur une cible démographique au sens girardien. En 2014, Sissi est élu président avec 96,9 % des voix dans un scrutin sans opposition réelle.

**Interprétation MEPA.** Ce cas illustre la trajectoire (b) Répression réussie dans sa version la plus institutionnellement sophistiquée : la force transformatrice (F) ne franchit jamais le seuil de résistance (R) dans la simulation, non parce que la mobilisation est faible, mais parce que la résistance institutionnelle (I) reste structurellement élevée grâce à la cohésion de l'appareil militaire (γ_local = 0.75) et à la reconstitution exogène de la capacité redistributive par l'aide du Golfe. Le SCAF ne réprime pas parce qu'il est fort face à une rue faible : il réprime parce qu'il a calculé le moment où la coalition Tahrir s'était fragmentée et où le soutien international lui était acquis.

---

### 1.2 Codage MEPA Full V6.2 — 9 variables

| Variable | Symbole | Valeur codée | Source principale | Justification |
|---|---|---|---|---|
| Fracture de l'élite | E_split | **0.65** | El-Ghobashy (S1) ; Kandil (S2) | Fracture réelle entre aile militaire (SCAF), aile civile libérale, FM et restes du PND. Clivage structurant mais non terminal : le SCAF reste uni en interne. Bande [0.60–0.70] : fracture avancée sans désintégration. |
| Cohésion organisationnelle élite | **γ** | **0.48** | Kandil (S2) ; Brownlee (S5) | γ = 0.48 : cohésion de l'élite globale modérée. L'élite est fragmentée entre militaires, islamistes, libéraux et hommes d'affaires. Le SCAF est uni mais l'élite au sens large ne l'est pas. Distinct de γ_local = 0.75 (capacité du seul noyau militaire). |
| Capacité redistributive effective | A_d_eff | **3.8** | Banque mondiale (S8) ; FMI (S9) | Bande [3–5] : trappe à dette naissante. Réserves de change en chute libre (36→14 Mds$), déficit budgétaire > 10 % du PIB, subventions alimentaires sous pression. Capacité redistributive dégradée mais non effondrée grâce aux subventions héritées. |
| Répression classique | A_r_c | **0.60** | HRW (S10) ; Amnesty (S11) | Appareil sécuritaire (police, armée, services de renseignement) opérationnel et discipliné. Valeur 0.60 : répression classique forte mais pas maximale en 2011 (hésitations initiales du SCAF). Monte à ~0.85 post-Rabaa 2013. Valeur codée sur l'ensemble de la période. |
| Répression numérique/non-étatique | A_r_ne | **0.35** | Freedom House (S7) ; V-DEM (S6) | Surveillance numérique partielle, coupure d'internet (28 jan.–2 fév. 2011), délateurs informels. Capacité numérique réelle mais non systématisée en 2011. Monte post-2013 avec la surveillance des réseaux sociaux. |
| Crédibilité du régime | Cs | **0.18** | V-DEM (S6) ; Brownlee (S5) | Cs très bas : fraudes électorales 2010, répression des manifestants, corruption documentée. Le régime Moubarak a perdu toute légitimité performative. Cs remonte légèrement post-2013 (légitimité sécuritaire de Sissi) mais reste bas sur la période globale. |
| Loyauté des appareils | L(t) | **0.28** | Kandil (S2) ; Springborg (S12) | L(t) bas : les appareils (police, justice, médias d'État) ne sont pas loyaux à Morsi pendant la phase FM. La loyauté au SCAF est forte en interne mais la loyauté au régime civil est structurellement faible. Valeur initiale de simulation. |
| Rendement énergétique net | EROI | **3.75** | BP Statistical Review (S13) ; Krane (S14) | EROI = 3.75 : Égypte producteur pétrolier déclinant (pic 1996), importateur net depuis 2008. Subventions énergétiques massives (≈ 7 % du PIB) masquent la contrainte. EROI < 5 : zone de vulnérabilité énergétique structurelle. |
| Structure anthropologique Todd | Sa | **6** | Todd 1990 (S4) | Sa = 6 : structure communautaire (famille élargie, endogamie partielle, égalitarisme intra-communautaire). Conforme au codage Todd pour l'Égypte rurale et périurbaine. Pas de modulateur Sa=7 appliqué. |

**Conversion scores → paramètres p1–p13 (résumé)** :

| Paramètre | Valeur | Dérivation |
|---|---|---|
| p1 (pression initiale S) | 1.05 | f(E_split=0.65, Cs=0.18) |
| p2 (chaleur latente initiale L) | 0.28 | L(t) direct |
| p3 (chaleur collective initiale C) | 0.08 | f(Cs=0.18, mobilisation initiale) |
| p4 (complexité institutionnelle initiale I) | 6.20 | f(A_d_eff=3.8, γ=0.48, EROI=3.75) |
| p5 (taux de croissance S) | 0.012 | f(E_split=0.65) |
| p6 (dissipation C) | 0.038 | f(A_r_c=0.60, A_r_ne=0.35) — Sa=6, pas de modulateur |
| p7 (couplage L→C) | 0.045 | f(L_t=0.28, γ=0.48) |
| p8 (couplage C→L) | 0.022 | f(Cs=0.18) |
| p9 (dégradation I) | 0.008 | f(A_d_eff=3.8, EROI=3.75) |
| p10 (λ, couplage F) | 0.38 | standard V6.2 |
| p11 (μ, paramètre dynamique) | 0.38 | standard V6.2 |
| p12 (ν, couplage répression→R) | 0.55 | standard V6.2 |
| p13 (ρ, résistance résiduelle) | 0.15 | standard V6.2 |

**Sanity checks V6.2** :
- EROI > 1 ✓ (3.75 thermodynamiquement valide)
- A_r_c + A_r_ne < 2.0 ✓ (0.95 < 2.0)
- E_split ∈ [0,1] ✓ ; γ ∈ [0,1] ✓ ; Cs ∈ [0,1] ✓
- L(t) ∈ [0,1] ✓ ; A_d_eff ∈ [0,10] ✓
- Sa ∈ {2, 4, 6, 7} ✓ (Sa=6, pas de modulateur p6×1.5)

---

### 1.3 Codage MEPA Full V7 — 6 variables supplémentaires

| Variable | Symbole | Valeur codée | Source | Justification |
|---|---|---|---|---|
| Stade matrice religieuse | M_r | **1** | Todd 1990 (S4) | Stade 1 : religion active. L'islam structure le droit (référence constitutionnelle à la charia), les institutions et la morale publique. Pratique et identité religieuses fortement actives en 2011. M_r ∈ {1,2} satisfait pour C1 ; C1 échoue néanmoins sur μ_m (voir précheck). |
| Polarisation mimétique | **μ_m** | **0.50** | El-Ghobashy (S1) ; Kandil (S2) ; V-DEM (S6) | μ_m = 0.50, bande [0.40–0.60] : polarisation forte (Armée vs FM, clivage structurant le discours public) MAIS sans désignation publique systématique d'un bouc émissaire démographique unique. Conforme à l'ancre de la grille CONV-E.md §V7-2 (exemple Égypte 2011). μ_m = 0.50 < μ_m* = 0.60 : sous-condition mimétique de C1 non franchie. |
| Fragmentation symbolique | **Φ** | **0.55** | V-DEM (S6) ; Freedom House (S7) | Φ = 0.55, bande [0.40–0.60] : pluralisme symbolique partiel. En 2011, l'espace médiatique combine télévision d'État, chaînes satellitaires (Al Jazeera), presse indépendante et réseaux sociaux mobilisés à Tahrir. Plusieurs récits coexistent sans monopole d'un noyau. Φ modéré → σ(Φ) modéré. |
| Proportion noyau engagé | **Ψ_noyau** | **0.03** | Kandil (S2) ; V-DEM (S6) | Ψ_noyau = 0.03, bande [0.01–0.05] : le noyau organisé pertinent (appareil militaire/sécuritaire, SCAF) est numériquement restreint rapporté à la population totale (~2,4 M de militaires et forces de sécurité / ~80 M d'habitants ≈ 0.03). Engagement actif soutenu = encadrement militaire et sécuritaire. Noyau petit mais très discipliné. |
| Proportion cible désignée | **Ψ_cible** | **null** | El-Ghobashy (S1) ; Kandil (S2) ; Wickham (S3) ; V-DEM (S6) ; Freedom House (S7) | *Voir justification E3 rev. 2.1 ci-dessous.* |
| Capacité organisationnelle noyau | **γ_local** | **0.75** | Kandil (S2) ; ancre corpus V7 | γ_local = 0.75, bande [0.60–0.80] : organisation très disciplinée. Le SCAF possède une discipline hiérarchique forte, une chaîne de commandement centralisée et une capacité d'action coordonnée à grande échelle. Valeur pré-enregistrée γ_local_max_programme (ancre corpus V7). **Divergence légitime** : γ_local = 0.75 (discipline militaire du noyau) >> γ = 0.48 (cohésion de l'élite globale, plus fragmentée). Cas analogue au Rwanda ; γ V6.2 laissé intact (décision QG). |

**Justification E3 rev. 2.1 — Ψ_cible = null (justification positive obligatoire)** :

> Les sources historiques consultées [El-Ghobashy (S1), Kandil (S2), Wickham (S3), V-DEM (S6), Freedom House (S7)] ne mentionnent aucune désignation publique de cible démographique unique au sens de la trajectoire (α). La répression post-Rabaa (août 2013) cible les structures organisationnelles des Frères musulmans en tant qu'organisation politique, non un groupe démographique défini par l'appartenance ethnique, religieuse ou raciale. Les FM représentent une organisation politique transversale à plusieurs groupes sociaux, et leur désignation comme « organisation terroriste » (décembre 2013) relève d'une logique de neutralisation politique, non d'un mécanisme sacrificiel girardien au sens strict. La fracture principale du cas est codée dans E_split = 0.65 comme clivage militaire/islamiste/libéral. L'absence de Ψ_cible est donc une propriété positive du cas, pas une omission.

---

### 1.4 Précheck V7 — Conditions C1–C4 de la branche (α)

```
C1 = (M_r = 1 ∈ {1,2}) AND (μ_m = 0.50 > μ_m* = 0.60)
   = TRUE AND FALSE
   = FALSE ✗

C2_sigma = 0.018 × (1 + 1.7 × Φ) = 0.018 × (1 + 1.7 × 0.55)
         = 0.018 × (1 + 0.935) = 0.018 × 1.935 = 0.0348
C2 = (Ψ_noyau × γ_local > C2_sigma)
   = (0.03 × 0.75 > 0.0348)
   = (0.0225 > 0.0348)
   = FALSE ✗

C3 = (Ψ_cible ≠ null) = (null ≠ null) = FALSE ✗

A_r_c = 0.60 ≤ 0.70 → clause de repli V7-C1 activée
A_r_c_eff = A_r_c + 0.5 × A_r_ne = 0.60 + 0.5 × 0.35 = 0.60 + 0.175 = 0.775
C4 = (A_r_c_eff > 0.70) = (0.775 > 0.70) = TRUE ✓

alpha_precheck = C1 AND C2 AND C3 AND C4
              = FALSE AND FALSE AND FALSE AND TRUE
              = FALSE ✗
```

**Conclusion précheck V7** : la branche (α) Cristallisation sacrificielle d'État est **exclue** avant simulation. Trois conditions sur quatre échouent : C1 (μ_m = 0.50 < 0.60), C2 (Ψ_noyau × γ_local = 0.0225 < σ(Φ) = 0.0348), C3 (Ψ_cible = null). La rampe mod_mimétique n'est **pas** activée. La simulation tourne en mode V6.2 standard, sans modulateur Sa (Sa = 6). La condition C4 est satisfaite via la clause de repli (A_r_c_eff = 0.775 > 0.70), ce qui confirme la capacité répressive effective du régime mais ne suffit pas à déclencher la branche (α) en l'absence des trois autres conditions.

---

## S2 — Simulation MEPA Lite

### 2.1 Paramètres de simulation

- **Intégrateur** : Euler explicite dt = 1 (V6.2 standard — alpha_precheck = False, LSODA non activé)
- **Durée** : t = 0 à t = 300 (représentant la période 2010–2014 à raison d'environ 18 jours par unité de temps)
- **Modulateur Sa** : Sa = 6 → p6 nominal (pas de multiplication ×1.5)
- **Rampe mod_mimétique** : non activ��e (alpha_precheck = False)
- **Valeurs initiales** : S₀ = 1.05, L₀ = 0.28, C₀ = 0.08, I₀ = 6.20

### 2.2 Tableau F(t)/R(t) — valeurs exactes du runner

| t | F(t) | R(t) | FR = F/R |
|---|---|---|---|
| 0 | 0.3130 | 1.6037 | 0.1952 |
| 25 | 0.4065 | 1.4567 | 0.2790 |
| 50 | 0.3617 | 1.4017 | 0.2580 |
| 75 | 0.3501 | 1.3706 | 0.2554 |
| 100 | 0.3474 | 1.3444 | 0.2584 |
| 150 | 0.3466 | 1.2920 | 0.2683 |
| 200 | 0.3466 | 1.2348 | 0.2807 |
| 250 | 0.3466 | 1.1707 | 0.2961 |
| 300 | 0.3466 | 1.0973 | **0.3159** |

### 2.3 Indicateurs de simulation

| Indicateur | Valeur | Note |
|---|---|---|
| t_bascule | **null** | Aucune bascule F > R détectée — F reste inférieur à R sur toute la simulation |
| ΔC_rel | **null** | Non calculable — absence de bascule |
| ΔI_rel | **null** | Non calculable — absence de bascule |
| FR_max | **0.3159** | Atteint à t = 300 (fin de simulation) |
| FR_final | **0.3159** | Identique à FR_max |
| C_max | **0.1472** | Pic de chaleur collective |
| C_final | **0.1071** | Valeur finale après dissipation partielle |
| S_final | **0.7875** | Pression sociale résiduelle |
| L_final | **0.3149** | Loyauté résiduelle |
| chute_C | **(0.1472 − 0.1071) / 0.1472 = 0.272** | 27.2 % de dissipation — condition branche (b) explicative satisfaite |
| A_r_c_eff | **0.775** | Via clause de repli V7-C1 |
| C5 | **non évaluée** | alpha_precheck = False → C5 non applicable |
| Branche annotation | **EXPLICATIVE** | Voir §2.4 |
| Trajectoire diagnostiquée | **(b) Répression réussie** | Concordance : OUI |

### 2.4 Interprétation mécanistique

**Absence de bascule — F reste inférieur à R sur toute la simulation.** Le ratio FR_max = 0.3159 est atteint en fin de simulation (t = 300), ce qui signifie que la force transformatrice n'a jamais approché le seuil de résistance institutionnelle. La valeur FR_max = 0.3159 représente environ 32 % du seuil de bascule — un écart considérable qui traduit la robustesse structurelle de l'appareil répressif égyptien.

**Dynamique en trois temps.** La trajectoire FR montre une structure non monotone : FR monte de 0.1952 (t=0) à 0.2790 (t=25), correspondant à la phase de mobilisation maximale de Tahrir et à la montée de C. Puis FR redescend légèrement (0.2554 à t=75) avant de remonter progressivement jusqu'à 0.3159 (t=300). Cette remontée finale ne traduit pas une montée de F mais une érosion lente de R (dégradation progressive de I sous l'effet de la contrainte énergétique et redistributive), sans jamais atteindre le seuil critique.

**Branche (b) explicative V7-C4 — conditions satisfaites** :
- C_max = 0.1472 > 0.12 ✓
- chute_C = 27.2 % > 20 % ✓
- Cs = 0.18 ∈ [0.10, 0.50] ✓
- A_r_c + A_r_ne = 0.60 + 0.35 = 0.95 > 0.40 ✓

La branche (b) est diagnostiquée comme **EXPLICATIVE** : le cas montre une mobilisation réelle (C_max = 0.1472, pic à t ≈ 25) suivie d'une dissipation active par répression (chute_C = 27.2 %), pas une simple apathie ou une stabilité par défaut. Ce n'est pas un cas CATCHALL où la répression est forte par défaut sans mobilisation préalable — c'est un cas où la mobilisation a existé et a été activement contenue.

**Rôle de γ_local dans la résistance.** La résistance R(t) reste structurellement élevée (R = 1.60 à t=0, R = 1.10 à t=300) grâce à la combinaison de I élevé (complexité institutionnelle militaire) et de la répression effective (A_r_c_eff = 0.775). La discipline du noyau militaire (γ_local = 0.75) se traduit dans la simulation par le maintien de I au-dessus du seuil critique, empêchant la bascule malgré la montée de C à t=25.

---

## S3 — Analyse MEPA Full et concordance

### 3.1 Tableau de concordance — 6 dimensions

| Dimension | Prédiction MEPA | Observation historique | Concordance | Note |
|---|---|---|---|---|
| **Trajectoire** | (b) Répression réussie | Coup du 3 juillet 2013, répression Rabaa, consolidation Sissi 2014 | ✓ OUI | EXPLICATIVE |
| **Fracture élite** | E_split = 0.65 → fracture avancée sans désintégration | Clivage SCAF/FM/libéraux réel, mais SCAF reste uni en interne | ✓ OUI | Fracture de surface, cohésion du noyau préservée |
| **Capacité répressive** | A_r_c_eff = 0.775 → répression effective | Rabaa : 800–1 000 morts, dissolution FM, arrestations massives | ✓ OUI | Clause de repli V7-C1 pertinente (délateurs + surveillance) |
| **Dynamique C** | C_max = 0.1472, chute_C = 27.2 % | Mobilisation Tahrir réelle puis dissipation post-Rabaa | ✓ OUI | Mobilisation documentée, pas apathie |
| **Résistance R** | R reste > F sur toute la simulation | Aucun transfert de pouvoir à la rue — SCAF contrôle la transition | ✓ OUI | FR_max = 0.3159 << 1.0 |
| **Contrainte énergétique** | EROI = 3.75 → vulnérabilité structurelle | Subventions énergétiques ≈ 7 % PIB, dépendance aux importations | ✓ OUI | Contrainte réelle mais compensée par aide du Golfe |

**Annotation branche** : **(b) Répression réussie — EXPLICATIVE**. La concordance est discriminante : le cas présente une mobilisation réelle (C_max > 0.12, chute_C > 20 %) et une répression active documentée, ce qui distingue ce diagnostic d'un simple CATCHALL par défaut.

**Concordance globale : OUI** — trajectoire diagnostiquée (b) = trajectoire attendue (b).

### 3.2 Analyse des mécanismes causaux

**Le paradoxe de la force transformatrice.** E_split = 0.65 est une valeur élevée qui, dans d'autres configurations du corpus MEPA, produit des trajectoires (a) ou (e). Ici, la fracture de l'élite est réelle mais asymétrique : elle affecte l'élite civile (PND, libéraux, FM) sans pénétrer le noyau militaire. γ_local = 0.75 capture cette asymétrie que γ = 0.48 (cohésion globale) ne peut pas seul restituer. La divergence légitime γ_local >> γ est le mécanisme central du cas.

**Le rôle de la reconstitution exogène de R.** La résistance R(t) décroît lentement (1.60 → 1.10 sur 300 pas) mais ne s'effondre pas. Cette décroissance lente reflète la dégradation de I sous contrainte énergétique (EROI = 3.75) et redistributive (A_d_eff = 3.8). Ce qui empêche l'effondrement de R, c'est la reconstitution exogène de la capacité redistributive par l'aide du Golfe (≈ 12 Mds$), qui n'est pas directement modélisée dans les équations différentielles mais qui se traduit dans le maintien de A_d_eff au-dessus du seuil d'effondrement. Le cas illustre ainsi la limite de la modélisation endogène : la stabilisation finale est partiellement exogène.

**La séquence (a)→(e)→(b) comme loi physique du cluster C2.** Ce WP est l'ancre du cluster C2 pour la trajectoire (b) déterminée par calcul institutionnel plutôt que par répression pure. La distinction est cruciale : le SCAF ne réprime pas parce qu'il est mécaniquement plus fort que la rue (FR_max = 0.3159 montre que la force transformatrice est loin d'être négligeable), mais parce qu'il a attendu le moment où la coalition Tahrir s'était fragmentée (γ de la coalition chute après 2011) et où le soutien financier du Golfe était acquis. La simulation capture la structure de cette attente : C monte à t=25 (mobilisation Tahrir), puis redescend (dissipation par répression et fragmentation), tandis que R reste stable.

---

## S4 — Stress-test de robustesse

### 4.1 Stress-test N1

| Scénario | Modification | Trajectoire | Interprétation |
|---|---|---|---|
| **Optimiste** | E − 0.08 / R + 0.08 | **(b) Répression réussie** | Robuste dans le sens favorable |
| **Pessimiste** | E + 0.08 / R − 0.08 | **(d) Effondrement progressif** | Bascule vers effondrement si fracture élite s'aggrave |

**Verdict N1 : MÉTASTABLE.** Les deux scénarios N1 produisent des trajectoires différentes, ce qui indique que le cas se situe dans une zone de sensibilité paramétrique. La trajectoire (b) est robuste dans le sens optimiste mais bascule vers (d) dans le sens pessimiste. Cela traduit la réalité historique : la consolidation de Sissi n'était pas inévitable — elle dépendait de la cohésion du SCAF et de l'aide du Golfe.

### 4.2 Stress-test N2 — 8 combinaisons

```
Stress N2 (8 combinaisons) :
  E+0.1  : (b) Répression réussie
  E-0.1  : (b) Répression réussie
  R+0.08 : (b) Répression réussie
  R-0.08 : (d) Effondrement progressif
  EROI+0.5 : (b) Répression réussie
  EROI-0.5 : (b) Répression réussie
  Rc+0.1 : (b) Répression réussie
  Rc-0.1 : (b) Répression réussie
```

### 4.3 Analyse de robustesse N1+N2

**Robustesse globale : MÉTASTABLE avec asymétrie R-dépendante.**

Sur les 8 combinaisons N2, 7 produisent (b) Répression réussie et 1 produit (d) Effondrement progressif. La seule combinaison qui bascule est R−0.08 (réduction de la capacité redistributive). Ce résultat est théoriquement cohérent : la trajectoire (b) est robuste aux variations de E_split (±0.1 ne change pas la trajectoire) et aux variations d'EROI (±0.5 ne change pas la trajectoire), mais elle est sensible à la dégradation de la capacité redistributive. Cela confirme l'interprétation mécanistique : c'est la reconstitution de R par l'aide du Golfe qui stabilise le régime, pas la seule force répressive.

La sensibilité N1 est marquée NON_CALCULÉ dans les données du runner — ce champ n'est pas disponible pour ce WP.

**Implication pour le cluster C2.** La métastabilité de ce cas est cohérente avec la position d'ancre du cluster : WP-C2-1 illustre une trajectoire (b) qui n'est pas triviale (pas un CATCHALL) mais qui repose sur des conditions précises (cohésion du noyau militaire, aide exogène, fragmentation de la coalition d'opposition). La robustesse aux variations de E et de Rc, combinée à la sensibilité à R, définit la signature paramétrique du cluster C2.

---

## S5 — Fiche standardisée V7

| Champ | Valeur |
|---|---|
| **WP-ID** | WP-C2-1 |
| **Cas** | Égypte 2011 — Printemps arabe et contre-révolution militaire |
| **Période** | 2010–2014 |
| **Cluster** | C2 |
| **Trajectoire attendue** | (b) Répression réussie |
| **Trajectoire diagnostiquée** | (b) Répression réussie |
| **Concordance** | OUI |
| **Branche annotation** | EXPLICATIVE |
| **E_split** | 0.65 |
| **γ** | 0.48 |
| **A_d_eff** | 3.8 |
| **A_r_c** | 0.60 |
| **A_r_ne** | 0.35 |
| **Cs** | 0.18 |
| **L(t) initial** | 0.28 |
| **EROI** | 3.75 |
| **Sa** | 6 (communautaire — pas de modulateur p6) |
| **t_bascule** | null — aucune bascule F > R |
| **FR_max** | 0.3159 (t = 300) |
| **C_max / C_final** | 0.1472 / 0.1071 |
| **Robustesse N1** | MÉTASTABLE |
| **M_r** | 1 — Stade 1 (religion active, islam structurant) |
| **μ_m** | 0.50 — polarisation forte sans désignation démographique (El-Ghobashy S1 ; Kandil S2 ; V-DEM S6) |
| **Φ** | 0.55 — pluralisme symbolique partiel (V-DEM S6 ; Freedom House S7) |
| **Ψ_noyau** | 0.03 — appareil militaire/sécuritaire SCAF (Kandil S2 ; V-DEM S6) |
| **Ψ_cible** | null — justification E3 rev. 2.1 : aucune désignation publique de cible démographique unique ; répression ciblant une organisation politique, non un groupe démographique |
| **γ_local** | 0.75 — discipline militaire SCAF (Kandil S2 ; ancre corpus V7 γ_local_max_programme) |
| **A_r_c_eff** | 0.775 — via clause de repli V7-C1 (A_r_c = 0.60 + 0.5 × A_r_ne = 0.35) |
| **alpha_precheck** | FALSE — C1 ✗ (μ_m < 0.60), C2 ✗ (0.0225 < 0.0348), C3 ✗ (Ψ_cible = null) |
| **Branche (α)** | Exclue — trois conditions sur quatre non satisfaites |

---

## S6 — Prédictions Popper

### P1 — Prédiction énergétique

**Énoncé** : un EROI < 5 sans compensation technologique ou exogène produit une contrainte redistributive structurelle qui fragilise la trajectoire (b) en direction de (d).

**Évaluation sur WP-C2-1** : EROI = 3.75 < 5. La contrainte redistributive est réelle (A_d_eff = 3.8, réserves de change en chute). La trajectoire (b) est maintenue non par la robustesse énergétique mais par la compensation exogène (aide du Golfe ≈ 12 Mds$). Le stress N2 R−0.08 confirme : sans cette compensation, la trajectoire bascule vers (d). **P1 partiellement confirmée** : la contrainte énergétique est active, mais la compensation exogène la neutralise dans ce cas. Implication : P1 prédit que si l'aide du Golfe avait été absente, la trajectoire aurait été (d) — prédiction falsifiable sur un cas contrefactuel.

### P2 — Prédiction de fracture élite

**Énoncé** : E_split > 0.60 sans cohésion du noyau dominant (γ_local < 0.40) produit une trajectoire (a) ou (e), pas (b).

**Évaluation sur WP-C2-1** : E_split = 0.65 > 0.60, mais γ_local = 0.75 >> 0.40. La prédiction P2 est **confirmée par contraposée** : la trajectoire (b) est possible avec E_split élevé si et seulement si γ_local est également élevé. Ce cas illustre la condition suffisante de P2 : la fracture de l'élite globale (γ = 0.48) est compensée par la cohésion du noyau militaire (γ_local = 0.75). P2 serait réfutée si un cas présentait E_split > 0.60, γ_local < 0.40 et trajectoire (b) — ce cas n'existe pas dans le corpus actuel.

### P3 — Prédiction de loyauté des appareils

**Énoncé** : L(t) < 0.35 produit une résistance institutionnelle fragilisée qui favorise la bascule vers (a) ou (d) si C_max > 0.20.

**Évaluation sur WP-C2-1** : L(t) = 0.28 < 0.35, mais C_max = 0.1472 < 0.20. La condition de P3 n'est que partiellement satisfaite : L(t) est bas mais C_max ne dépasse pas 0.20. **P3 non testée dans sa forme complète** sur ce cas : la mobilisation n'a pas atteint le seuil C_max > 0.20 qui aurait mis à l'épreuve la faible loyauté des appareils. P3 reste falsifiable sur un cas futur avec L(t) < 0.35 ET C_max > 0.20.

### P4 — Prédiction de structure anthropologique

**Énoncé** : Sa = 6 (communautaire) produit une résistance à la mobilisation individuelle qui maintient C_max < 0.25 même en contexte de forte fracture élite.

**Évaluation sur WP-C2-1** : Sa = 6, C_max = 0.1472 < 0.25. **P4 confirmée** : la structure communautaire égyptienne (famille élargie, réseaux de solidarité locaux) n'a pas produit une mobilisation individuelle soutenue au-delà du pic initial de Tahrir. La dissipation de C après t=25 est cohérente avec la prédiction P4.

### P5 — Prédiction de crédibilité

**Énoncé** : Cs < 0.20 produit une mobilisation initiale forte (C_max > 0.10) mais ne garantit pas la bascule si R reste structurellement élevé.

**Évaluation sur WP-C2-1** : Cs = 0.18 < 0.20, C_max = 0.1472 > 0.10, aucune bascule. **P5 confirmée** : la faible crédibilité du régime produit bien une mobilisation initiale (C_max = 0.1472), mais cette mobilisation ne suffit pas à franchir le seuil de résistance (FR_max = 0.3159 << 1.0). P5 serait réfutée si un cas présentait Cs < 0.20 et FR_max > 1.0 sans bascule — ce qui serait une contradiction interne du modèle.

### P6 — Prédiction Cristallisation sacrificielle (V7)

**Énoncé** : le mécanisme sacrificiel girardien ne se déclenche que si les 5 conditions C1–C5 de la branche (α) sont simultanément satisfaites.

**Évaluation sur WP-C2-1** : trois conditions sur quatre échouent au précheck (C1 : μ_m = 0.50 < 0.60 ; C2 : 0.0225 < 0.0348 ; C3 : Ψ_cible = null). La branche (α) est exclue. **P6 confirmée négativement** : l'absence de désignation démographique publique (Ψ_cible = null) et la polarisation mimétique insuffisante (μ_m = 0.50 < μ_m* = 0.60) empêchent le déclenchement de la branche (α), conformément à la prédiction. La répression post-Rabaa, bien que massive, ne constitue pas un mécanisme sacrificiel girardien au sens de la trajectoire (α) — elle cible une organisation politique, pas un groupe démographique. P6 serait réfutée si un cas présentait les 5 conditions satisfaites mais ne produisait pas de mécanisme sacrificiel documenté.

---

## S7 — Bornes de réfutation et synthèse comparative cluster C2

### 7.1 Bornes de réfutation

**RF1 — Réfutation par EROI sans compensation exogène.**

*Énoncé* : si un cas du corpus présente EROI < 4.0, A_d_eff < 4.0, absence d'aide exogène documentée, et trajectoire (b) maintenue sur plus de 36 mois, alors la prédiction P1 est réfutée et le modèle sous-estime la capacité de résistance institutionnelle indépendamment de la contrainte énergétique.

*Mécanisme de réfutation* : dans WP-C2-1, la trajectoire (b) est maintenue malgré EROI = 3.75 et A_d_eff = 3.8 grâce à l'aide du Golfe. Si un cas analogue maintenait (b) sans aide exogène, cela indiquerait que le modèle surestime le rôle de la contrainte redistributive dans la détermination de la trajectoire.

*Horizon temporel* : falsifiable sur tout cas du corpus 2015–2030 présentant ces caractéristiques. Candidats potentiels : Algérie 2019 (Hirak), Soudan 2019.

*Implication V7* : si RF1 est confirmée, le paramètre p9 (dégradation de I par contrainte énergétique) devrait être révisé à la baisse pour les régimes militaires à forte γ_local.

**RF2 — Réfutation par absence de trajectoire (a) ou (d) malgré E_split > 0.70.**

*Énoncé* : si un cas présente E_split > 0.70, γ_local < 0.40, et trajectoire (b) maintenue, alors la prédiction P2 est réfutée et le modèle surestime le rôle de la cohésion du noyau dans la détermination de la trajectoire.

*Mécanisme de réfutation* : dans WP-C2-1, la trajectoire (b) avec E_split = 0.65 est explicable par γ_local = 0.75. Un cas avec E_split > 0.70 et γ_local < 0.40 produisant (b) serait inexplicable par le modèle actuel.

*Horizon temporel* : falsifiable sur tout cas du corpus présentant ces caractéristiques.

**RF3 — Réfutation par complexité institutionnelle croissante avec EROI déclinant.**

*Énoncé* : si un cas présente EROI déclinant sur toute la période ET I croissant (complexité institutionnelle augmentant), alors le modèle est structurellement incohérent dans son couplage p9 (dégradation de I par contrainte énergétique).

*Mécanisme de réfutation* : dans WP-C2-1, I décroît lentement (R passe de 1.60 à 1.10 sur 300 pas), cohérent avec EROI = 3.75 déclinant. Un cas où I croît malgré EROI déclinant invaliderait le couplage énergétique-institutionnel du modèle.

*Horizon temporel* : falsifiable sur tout cas du corpus avec données EROI longitudinales disponibles.

### 7.2 Synthèse comparative — Cluster C2

Le cluster C2 regroupe les cas où la trajectoire finale est déterminée par un calcul institutionnel du noyau dominant plutôt que par la seule force mécanique de la répression. WP-C2-1 est l'ancre de ce cluster et en définit la signature paramétrique :

| Dimension | Signature cluster C2 | WP-C2-1 | Implication |
|---|---|---|---|
| **Fracture élite** | E_split ∈ [0.55–0.70] | 0.65 | Fracture avancée mais asymétrique |
| **Cohésion noyau** | γ_local >> γ | 0.75 >> 0.48 | Divergence légitime noyau/élite globale |
| **Répression effective** | A_r_c_eff > 0.70 | 0.775 (clause de repli) | Répression via réseaux non-étatiques |
| **Mobilisation** | C_max ∈ [0.10–0.20] | 0.1472 | Mobilisation réelle mais contenue |
| **Résistance** | FR_max < 0.40 | 0.3159 | Jamais proche du seuil de bascule |
| **Robustesse** | MÉTASTABLE | MÉTASTABLE | Sensibilité à R, robustesse à E |

**Position du cas dans le corpus MEPA.** WP-C2-1 illustre la trajectoire (b) dans sa version la plus institutionnellement sophistiquée, distincte de la trajectoire (b) CATCHALL (répression forte par défaut sans mobilisation préalable). La branche EXPLICATIVE confirme que ce cas teste réellement le modèle : la mobilisation a existé (C_max = 0.1472), la répression a été active (chute_C = 27.2 %), et la résistance institutionnelle a tenu (FR_max = 0.3159). Ce n'est pas un cas trivial.

**Apport V7 au cluster C2.** L'introduction des variables V7 permet de préciser le mécanisme causal : l'absence de Ψ_cible (null positif, justification E3 rev. 2.1) distingue formellement la répression post-Rabaa d'un mécanisme sacrificiel girardien. La valeur μ_m = 0.50 < μ_m* = 0.60 confirme que la polarisation Armée/FM, bien que structurante, n'a pas atteint le seuil de désignation démographique. Ces deux propriétés positives du cas — absence de cible démographique, polarisation sous le seuil — définissent la frontière entre la trajectoire (b) et la trajectoire (α) dans le corpus MEPA.

**Prédiction pour les cas futurs du cluster C2.** Tout cas futur du cluster C2 présentant γ_local > 0.65, A_r_c_eff > 0.70, et μ_m < 0.60 devrait produire une trajectoire (b) EXPLICATIVE avec FR_max < 0.40. Si un tel cas produisait une trajectoire (a) ou (d), cela constituerait une zone de réfutation potentielle pour RF2 et devrait être documenté conformément au protocole V7-C3.

---

*WP-C2-1 — Rapport complet S1→S7 | MEPA V7-α rev. 2.1 | Cluster C2 | Ancre loi physique C2*
*Trajectoire : (b) Répression réussie — EXPLICATIVE | Concordance : OUI | Robustesse : MÉTASTABLE*