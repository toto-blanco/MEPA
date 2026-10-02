# WORKING PAPER MEPA V7-α rev. 2.1
## WP-C1-1 — Haïti : Crise post-séisme et dissolution institutionnelle (2010–2024)

**Cluster C1 | Sa = 4 | Trajectoire attendue : (d) Effondrement progressif**
**Schéma : V7-α rev. 2.1 | Runner : mepa_runner_v3_v7 v3.0**
**Date de production : avril 2026**

---

## S1 — Contexte historique et codage MEPA Full

### 1.1 Narration historique

Le 12 janvier 2010, un séisme de magnitude 7,0 frappe la région métropolitaine de Port-au-Prince. Le bilan humain dépasse 200 000 morts selon les estimations gouvernementales haïtiennes, et plus d'un million de personnes se retrouvent déplacées. L'événement ne crée pas la fragilité institutionnelle haïtienne — il l'amplifie et l'accélère. Haïti entre dans la période 2010–2024 avec un appareil d'État déjà structurellement défaillant, une économie dépendante de l'aide internationale et des transferts de la diaspora, et une élite politique fragmentée incapable de produire une coalition gouvernante stable.

La reconstruction post-séisme est marquée par une double dynamique contradictoire. D'un côté, un afflux massif d'aide internationale — estimé à plus de 13 milliards de dollars sur la décennie — qui contourne systématiquement les institutions étatiques haïtiennes au profit d'ONG et d'organisations internationales. De l'autre, une incapacité structurelle de l'État à absorber, redistribuer ou capitaliser sur ces ressources. La Banque mondiale documente dès 2012 un EROI effectif de l'économie haïtienne inférieur à 2, reflétant une agriculture de subsistance à rendement déclinant, une déforestation quasi-totale (moins de 2 % de couverture forestière), et une dépendance aux importations alimentaires pour plus de 50 % de la consommation nationale.

La période 2011–2016 est dominée par la présidence de Michel Martelly, caractérisée par une gouvernance patrimoniale, une suspension prolongée du Parlement (2015–2016), et une incapacité à organiser des élections crédibles. La fracture de l'élite (E_split = 0,72) reflète l'absence de tout consensus entre les factions politiques, les oligarchies économiques de la capitale et les réseaux régionaux. La capacité organisationnelle de l'élite (γ = 0,22) est correspondamment basse : aucune coalition n'est capable de produire une politique publique cohérente sur plus de quelques mois.

L'assassinat du président Jovenel Moïse le 7 juillet 2021 marque un point de basculement symbolique. L'État haïtien perd sa dernière figure d'autorité nominale. Dans le vide institutionnel qui suit, les gangs — fédérés sous l'alliance G9 an Fanmi e Alye dirigée par Jimmy Chérizier dit « Barbecue » — étendent leur contrôle territorial à plus de 80 % de Port-au-Prince selon les estimations de l'ONU en 2023. La capacité redistributive effective (A_d_eff = 1,4) reflète cet effondrement : l'État ne peut plus assurer les fonctions minimales de sécurité, de justice ou de services publics.

La loyauté des appareils (L(t) = 0,18) est au plancher : la Police Nationale d'Haïti est infiltrée, sous-équipée et partiellement corrompue. La crédibilité du régime (Cs = 0,22) est quasi-nulle dans la population. La répression classique (A_r_c = 0,58) est insuffisante pour rétablir l'ordre, et la répression numérique/non-étatique (A_r_ne = 0) est inexistante au sens institutionnel — les gangs exercent une violence territoriale mais sans mécanisme de surveillance systématique.

La structure anthropologique Todd (Sa = 4, famille nucléaire égalitaire) est cohérente avec le profil haïtien : héritage de la révolution de 1804, égalitarisme de principe, mais faiblesse des structures de solidarité horizontale au-delà du cercle familial immédiat. Cette structure ne génère pas de prime organisationnelle (pas de modulateur Sa = 7).

Sur le plan énergétique, l'EROI de 1,5 est critique. Il se situe en dessous du seuil de subsistance agricole historique (généralement estimé à EROI ≈ 3–5 pour une économie pré-industrielle viable). Cette valeur reflète la combinaison d'une déforestation extrême, d'une érosion des sols irréversible à court terme, et d'une dépendance aux importations d'hydrocarbures pour les fonctions urbaines minimales. L'EROI < 2 est un marqueur de la trajectoire (d) : la base matérielle de l'État s'érode avant que toute mobilisation collective puisse s'organiser.

La période 2022–2024 voit l'installation d'un Conseil Présidentiel de Transition (CPT) sous pression internationale, et le déploiement d'une Mission Multinationale de Soutien à la Sécurité (MMSS) dirigée par le Kenya. Ces interventions extérieures ne modifient pas structurellement les paramètres MEPA : elles constituent des tentatives de stabilisation exogène d'un système dont la dynamique interne reste celle de l'effondrement progressif.

### 1.2 Tableau de codage MEPA Full V6.2 — 9 variables

| Variable | Symbole | Valeur | Source principale | Justification synthétique |
|---|---|---|---|---|
| Fracture de l'élite | E_split | 0,72 | Schuller & Morales (S3) ; V-DEM (S5) | Fragmentation extrême des factions politiques, oligarchies économiques et réseaux régionaux. Aucune coalition gouvernante stable sur 2010–2024. |
| Capacité organisationnelle élite | γ | 0,22 | V-DEM (S5) ; Freedom House (S6) | Élite incapable de produire une politique cohérente. Suspension du Parlement 2015–2016. Gouvernance patrimoniale. |
| Capacité redistributive effective | A_d_eff | 1,4 | Banque mondiale (S1) ; PNUD (S2) | Faillite technique de l'État redistributif. Aide internationale contournant les institutions. Contrôle territorial des gangs. |
| Répression classique | A_r_c | 0,58 | Schuller & Morales (S3) ; ONU (S7) | PNH infiltrée et sous-équipée. Incapacité à rétablir l'ordre face aux gangs. Sous le seuil d'efficacité. |
| Répression numérique | A_r_ne | 0,00 | V-DEM (S5) | Période pré-numérique au sens institutionnel. Aucun mécanisme de surveillance systématique étatique. |
| Crédibilité du régime | Cs | 0,22 | Freedom House (S6) ; V-DEM (S5) | Quasi-nulle. Assassinat de Moïse 2021. Absence d'élections crédibles. Perception de prédation étatique. |
| Loyauté des appareils | L(t) | 0,18 | Schuller & Morales (S3) ; ONU (S7) | Plancher. PNH corrompue et infiltrée. Armée reconstituée symboliquement sans capacité opérationnelle. |
| Rendement énergétique net | EROI | 1,5 | Banque mondiale (S1) ; FAO (S8) | En dessous du seuil de subsistance agricole historique. Déforestation quasi-totale, érosion des sols, dépendance aux importations. |
| Structure anthropologique | Sa | 4 | Todd 1990 (S4) | Famille nucléaire égalitaire. Héritage révolutionnaire 1804. Pas de prime organisationnelle (Sa ≠ 7). |

**Sanity checks V6.2** :
- E_split = 0,72 > 0,70 → fracture critique confirmée ✓
- γ = 0,22 → capacité organisationnelle très basse, cohérente avec E_split élevé ✓
- A_d_eff = 1,4 → bande [0–2] faillite technique ✓
- EROI = 1,5 → valeur réelle > 1 (thermodynamiquement obligatoire) ✓
- L(t) = 0,18 → plancher, cohérent avec Cs = 0,22 ✓
- Sa = 4 → pas de modulateur p6 × 1,5 ✓

### 1.3 Tableau de codage MEPA Full V7 — 6 variables

| Variable | Symbole | Valeur | Source | Justification synthétique |
|---|---|---|---|---|
| Stade matrice religieuse | M_r | 1 | Todd 1990 (S4) | Stade 1 : religion active. Catholicisme, protestantisme évangélique en expansion et Vodou structurent fortement la vie quotidienne, l'identité et la morale publique. Matrice religieuse socialement active. |
| Polarisation mimétique | μ_m | 0,30 | V-DEM (S5) ; Freedom House (S6) | Bande [0,20–0,40] : polarisation modérée. Conflits politiques et prédation des gangs, mais aucune désignation publique d'un ennemi démographique unique. Conflictualité fragmentée sans « nous/eux » mimétique structurant. μ_m = 0,30 < μ_m* = 0,60. |
| Fragmentation symbolique | Φ | 0,65 | V-DEM (S5) ; Freedom House (S6) ; ancre corpus V7 | Bande [0,60–0,80] : pluralisme médiatique élevé. Paysage radiophonique et médiatique haïtien dense et fragmenté, multiples voix concurrentes, aucun monopole symbolique. Valeur pré-enregistrée Φ_max_programme (ancre corpus V7). |
| Proportion noyau engagé | Ψ_noyau | 0,04 | Schuller & Morales (S3) ; Farmer 2011 (S4) | Bande [0,01–0,05] : pas de noyau idéologique organisé porteur d'un mécanisme sacrificiel. Les gangs sont des acteurs criminels fragmentés et concurrents (motivation prédatrice/territoriale), pas une avant-garde unifiée portant une purge démographique. |
| Proportion cible désignée | Ψ_cible | **null** | Banque mondiale (S1) ; Schuller & Morales (S3) ; Farmer 2011 (S4) ; V-DEM (S5) ; Freedom House (S6) | *Voir justification E3 rev. 2.1 ci-dessous* |
| Capacité organisationnelle noyau | γ_local | 0,15 | Schuller & Morales (S3) ; V-DEM (S5) | Bande [0,00–0,20] : aucun noyau organisé discipliné porteur d'un mécanisme sacrificiel. Les gangs ont une organisation interne locale mais sont mutuellement concurrents, sans doctrine commune ni commandement central unifié. |

**Justification E3 rev. 2.1 — Ψ_cible = null (justification positive obligatoire)** :

> Les sources historiques consultées [Banque mondiale (S1), Schuller & Morales (S3), Farmer 2011 (S4), V-DEM (S5), Freedom House (S6)] ne mentionnent aucune désignation publique de cible démographique unique au sens de la trajectoire (α). La violence haïtienne sur la période 2010–2024 est de nature prédatrice et territoriale : les gangs s'affrontent entre eux et rançonnent les populations civiles sans désigner un groupe ethnique, religieux ou démographique comme ennemi sacrificiel. La conflictualité est fragmentée entre factions rivales (G9, GPEP, etc.) sans convergence vers un bouc émissaire démographique commun. La fracture principale du cas est codée dans E_split comme fragmentation politique et prédatrice de l'élite, non comme clivage démographique. L'absence de Ψ_cible est donc une propriété positive du cas, pas une omission.

### 1.4 Précheck V7 — Conditions C1–C4 de la branche (α)

```
C1 = (M_r = 1 ∈ {1, 2}) AND (μ_m = 0.30 > 0.60)
   = TRUE AND FALSE
   = FALSE

C2_sigma = 0.018 × (1 + 1.7 × 0.65) = 0.018 × (1 + 1.105) = 0.018 × 2.105 = 0.03789
C2 = (Ψ_noyau × γ_local > C2_sigma)
   = (0.04 × 0.15 > 0.03789)
   = (0.006 > 0.03789)
   = FALSE

C3 = (Ψ_cible ≠ null)
   = (null ≠ null)
   = FALSE

A_r_c = 0.58 ≤ 0.70 → clause de repli activée
A_r_c_eff = A_r_c + 0.5 × A_r_ne = 0.58 + 0.5 × 0.00 = 0.58
C4 = (A_r_c_eff > 0.70)
   = (0.58 > 0.70)
   = FALSE

alpha_precheck = C1 AND C2 AND C3 AND C4
              = FALSE AND FALSE AND FALSE AND FALSE
              = FALSE
```

**Résultat précheck V7** : `alpha_precheck = FALSE`. Les conditions C1, C2, C3 et C4 sont toutes non satisfaites. La branche (α) Cristallisation sacrificielle d'État est **exclue avant simulation**. La rampe mod_mimétique n'est pas activée. La simulation tourne en mode V6.2 standard (modulateur Sa = 4, pas de prime organisationnelle).

**C5** : non évaluée (alpha_precheck = FALSE, condition C5 sans objet).

---

## S2 — Simulation MEPA Lite

### 2.1 Paramètres de simulation

**Intégrateur** : Euler explicite dt = 1 (V6.2 standard — rampe mod_mim