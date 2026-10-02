# Working Paper MEPA — WP-F1-1
## Rome — Crise du IIIe siècle (235–284 apr. J.-C.)

**Cluster :** C1 | **Sa :** 4 (nucléaire égalitaire) | **Version moteur :** mepa_runner_v3_v7 v3.0 | **Cadre :** MEPA V4-alpha (V7-α rev. 2.1)

---

## S1 — Contexte historique et codage MEPA Full

### 1.1 Narration historique

La période 235–284 apr. J.-C. constitue l'une des crises systémiques les plus documentées de l'Antiquité. Elle s'ouvre avec l'assassinat d'Alexandre Sévère par ses propres troupes et se clôt avec l'avènement de Dioclétien, qui entreprend une reconstruction institutionnelle d'envergure. Entre ces deux bornes, l'Empire romain traverse ce que les historiens nomment l'« anarchie militaire » : cinquante ans durant lesquels se succèdent plus de vingt empereurs légitimes, auxquels s'ajoutent de nombreux usurpateurs régionaux.

La crise est fondamentalement **systémique et multi-causale**. Elle ne résulte pas d'une rupture politique ponctuelle ni d'une mobilisation populaire organisée, mais d'une accumulation de défaillances structurelles qui se renforcent mutuellement. Sur le plan militaire, la pression simultanée des Alamans et des Francs sur le Rhin, des Goths sur le Danube et des Sassanides en Orient contraint l'Empire à maintenir des armées permanentes sur plusieurs fronts, ce qui exige une fiscalité croissante. Sur le plan fiscal, la débasement monétaire — la teneur en argent du denier passe d'environ 50 % sous Septime Sévère à moins de 5 % sous Gallien — génère une inflation structurelle qui érode les revenus réels de l'État et la confiance dans la monnaie. Sur le plan institutionnel, la complexité administrative croissante (multiplication des bureaux, des légions, des provinces) consomme des ressources sans produire de rendements proportionnels, illustrant le mécanisme de « surcharge de complexité » décrit par Tainter (1988).

L'EROI énergétique de l'Empire, estimé à 3,15 pour la période, reflète une économie agricole en tension : les terres marginales sont de plus en plus sollicitées, les rendements agricoles stagnent, et les flux d'esclaves — moteur énergétique de l'économie romaine — se tarissent avec la fin des grandes conquêtes. Ward-Perkins (2005) documente le recul de la production céramique, de la construction et des échanges commerciaux comme indicateurs matériels de cette contraction énergétique.

La structure anthropologique Todd de type **nucléaire égalitaire** (Sa = 4) caractérise une société où les individus sont formellement égaux en droits mais où les liens familiaux étendus sont faibles. Cette structure favorise une certaine fluidité sociale mais aussi une faible capacité de résistance collective organisée face à la désintégration institutionnelle — ce qui est cohérent avec l'absence de mobilisation populaire structurée pendant la crise.

La fracture de l'élite (E_split = 0,20) est remarquablement basse pour une période d'instabilité aussi intense. Cette valeur reflète un paradoxe romain : les élites sénatoriales et équestres ne sont pas fondamentalement divisées sur un projet politique alternatif — elles sont toutes également dépassées par la crise militaire et fiscale. Les usurpations impériales sont des compétitions pour le contrôle d'un appareil en déclin, non des projets de transformation sociale. La capacité organisationnelle de l'élite (γ = 0,25) est basse, reflétant la désintégration progressive des réseaux clientélaires et des institutions sénatoriales.

La crédibilité du régime (Cs = 0,35) est faible mais non nulle : l'idéologie impériale conserve une légitimité résiduelle, comme en témoigne le fait que les usurpateurs cherchent systématiquement à se faire reconnaître comme empereurs légitimes plutôt qu'à abolir l'institution impériale. La loyauté des appareils (L = 0,55) est modérée : les armées restent fonctionnelles mais leur loyauté est conditionnelle et vénale.

Aucun mécanisme sacrificiel girardien organisé n'est documenté pour cette période. Les persécutions chrétiennes (édit de Dèce, 250 ; édit de Valérien, 257) sont ponctuelles, instrumentales et non érigées en polarisation mimétique structurante. La crise est impersonnelle : elle n'a pas de bouc émissaire démographique désigné, pas de noyau organisé porteur d'un projet de purge, pas de désignation publique d'un « eux » coupable de la décadence.

### 1.2 Tableau de codage MEPA Full V6.2 — 9 variables

| Variable | Symbole | Valeur | Justification synthétique | Source principale |
|---|---|---|---|---|
| Fracture de l'élite | E_split | 0,20 | Élites sénatoriales/équestres non divisées sur un projet alternatif ; compétitions pour le contrôle d'un appareil en déclin, pas de fracture idéologique structurante | Gibbon (S1) ; Wickham (S2) |
| Capacité organisationnelle élite | γ | 0,25 | Désintégration progressive des réseaux clientélaires et des institutions sénatoriales ; γ bas mais non nul (structures formelles subsistent) | Tainter 1988 (S5) |
| Capacité redistributive effective | A_d_eff | 4,5 | Trappe à dette fiscale : débasement monétaire, inflation structurelle, fiscalité croissante sans rendements proportionnels | Tainter 1988 (S5) ; Ward-Perkins 2005 (S6) |
| Répression classique | A_r_c | 0,50 | Armées fonctionnelles mais loyauté conditionnelle ; capacité répressive réelle mais fragmentée entre prétendants | Gibbon (S1) |
| Répression numérique | A_r_ne | 0,00 | Période pré-numérique ; aucun réseau de surveillance non-étatique organisé au sens V7 | — |
| Crédibilité du régime | Cs | 0,35 | Légitimité impériale résiduelle (les usurpateurs cherchent la reconnaissance) mais érodée par l'instabilité et l'inflation | Gibbon (S1) ; Wickham (S2) |
| Loyauté des appareils | L(t) | 0,55 | Armées fonctionnelles, loyauté conditionnelle et vénale ; bureaucratie civile maintenue | Gibbon (S1) |
| Rendement énergétique net | EROI | 3,15 | Économie agricole en tension, terres marginales sollicitées, flux d'esclaves taris, recul de la production matérielle documenté | Ward-Perkins 2005 (S6) ; Tainter 1988 (S5) |
| Structure anthropologique Todd | Sa | 4 | Nucléaire égalitaire : fluidité sociale, faibles liens familiaux étendus, faible capacité de résistance collective organisée | Todd 1990 (S4) |

**Sanity checks V6.2 :**
- E_split = 0,20 (borne inférieure programme) : cohérent avec l'absence de rupture (a) malgré T = 0,80 — la pression transformatrice est forte mais la fracture de l'élite est insuffisante pour produire une coalition de rupture.
- γ = 0,25 : cohérent avec E_split bas — une élite peu fracturée mais peu organisée produit une résistance diffuse, pas une répression ciblée.
- A_d_eff = 4,5 : zone de trappe à dette (bande [4–6]) — ni faillite technique immédiate ni surplus, mais dégradation progressive.
- A_r_c = 0,50 : répression classique modérée — insuffisante pour déclencher la branche (b) répression réussie (seuil Rc + Rn > 0,6 non atteint).
- EROI = 3,15 : valeur basse pour une économie impériale, cohérente avec la contraction matérielle documentée par Ward-Perkins.

### 1.3 Tableau de codage MEPA Full V7 — 6 variables

| Variable | Symbole | Valeur | Justification synthétique | Source |
|---|---|---|---|---|
| Stade matrice religieuse Todd | M_r | 1 | Religion civique active : culte impérial, sacrifices publics, collèges sacerdotaux structurent les institutions. L'édit de Dèce (250) imposant le sacrifice universel atteste le caractère institutionnellement contraignant de la matrice religieuse. **Réserve source** : grille Todd calibrée sur le christianisme européen ; mapping au polythéisme romain approximatif. Sans incidence sur C1 (échec par μ_m). | Todd 1990 (S4) |
| Polarisation mimétique girardienne | μ_m | 0,25 | Bande [0,20–0,40] : polarisation modérée. Crise multi-causale et diffuse ; aucun discours public ne désigne un « eux » coupable unique. Persécutions chrétiennes ponctuelles et non érigées en polarisation mimétique structurante. μ_m = 0,25 < μ_m* = 0,60 : sous-condition mimétique de C1 non franchie. | Gibbon (S1) ; Tainter 1988 (S5) |
| Fragmentation symbolique | Φ | 0,50 | Bande [0,40–0,60] : pluralisme symbolique partiel. Juxtaposition du culte civique d'État, de cultes orientaux et à mystères, d'écoles philosophiques et d'un christianisme montant — aucun monopole d'un noyau organisé. **Réserve source** : mesure du pluralisme symbolique pour une société pré-moderne approximative. Non décisif : C2 échoue largement par Ψ_noyau et γ_local quasi-nuls. | Brown (contexte) ; Tainter 1988 (S5) |
| Proportion population engagée noyau | Ψ_noyau | 0,02 | Bande [0,01–0,05] basse : aucun noyau organisé porteur d'un mécanisme sacrificiel. L'effondrement est systémique et impersonnel (surcharge de complexité, défaillance fiscale et militaire), non l'œuvre d'une avant-garde mobilisée autour d'une purge. Valeur quasi-nulle reflétant l'absence de noyau. | Tainter 1988 (S5) ; Ward-Perkins 2005 (S6) |
| Proportion population cible désignée | Ψ_cible | **null** | Voir justification E3 rev. 2.1 ci-dessous (§1.4). | Gibbon (S1) ; Wickham (S2) ; Tainter 1988 (S5) ; Ward-Perkins 2005 (S6) |
| Capacité organisationnelle noyau | γ_local | 0,10 | Bande [0,00–0,20] : aucun noyau organisé, donc pas de discipline doctrinale ni de commandement central porteur d'un mécanisme sacrificiel. Corollaire de Ψ_noyau quasi-nul. γ_local ≈ γ (V6.2 = 0,25) — convergence basse, pas de divergence noyau/élite (il n'y a pas de noyau au sens V7). | Tainter 1988 (S5) ; Gibbon (S1) |

### 1.4 Justification E3 rev. 2.1 — Ψ_cible = null (positif)

> Les sources historiques consultées [Gibbon (S1), Wickham (S2), Tainter 1988 (S5), Ward-Perkins 2005 (S6)] ne mentionnent aucune désignation publique de cible démographique unique au sens de la trajectoire (α). La crise du IIIe siècle est une désintégration systémique impersonnelle : la surcharge de complexité administrative, la contraction fiscale et la pression militaire multi-frontières ne sont attribuées publiquement à aucun groupe démographique désigné comme bouc émissaire structurant. Les persécutions chrétiennes (Dèce 250, Valérien 257) sont ponctuelles, instrumentales et non érigées en polarisation mimétique démographique durable. La fracture principale du cas est codée dans E_split = 0,20 comme compétition intra-élitaire pour le contrôle d'un appareil en déclin, non comme mobilisation contre un groupe cible. L'absence de ��_cible est donc une propriété positive du cas, pas une omission.

### 1.5 Précheck V7 — Conditions C1–C4 de la branche (α)

```
C1 = (M_r = 1 ∈ {1, 2}) AND (μ_m = 0.25 > 0.60)
   = TRUE AND FALSE
   = FALSE

C2_sigma = 0.018 × (1 + 1.7 × 0.50) = 0.018 × 1.85 = 0.0333
C2 = (Ψ_noyau × γ_local > C2_sigma)
   = (0.02 × 0.10 > 0.0333)
   = (0.002 > 0.0333)
   = FALSE

C3 = (Ψ_cible ≠ null)
   = (null ≠ null)
   = FALSE

A_r_c = 0.50 ≤ 0.70 → clause de repli V7-C1 :
A_r_c_eff = A_r_c + 0.5 × A_r_ne = 0.50 + 0.5 × 0.00 = 0.50
C4 = (A_r_c_eff > 0.70)
   = (0.50 > 0.70)
   = FALSE

alpha_precheck = C1 AND C2 AND C3 AND C4
              = FALSE AND FALSE AND FALSE AND FALSE
              = FALSE
```

**Résultat précheck V7 :** La branche (α) Cristallisation sacrificielle d'État est **exclue avant simulation**. Les quatre conditions C1, C2, C3 et C4 échouent simultanément. La rampe mod_mimétique n'est **pas activée**. La simulation tourne en mode V6.2 standard avec modulateur Sa =