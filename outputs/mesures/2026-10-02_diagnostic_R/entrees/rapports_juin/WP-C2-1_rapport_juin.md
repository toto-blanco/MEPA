# Working Paper MEPA — WP-C2-1
## Égypte 2011 — Printemps arabe et contre-révolution militaire
### Période 2010–2014 | Cluster C2 | Schéma V7-α rev. 2.1

---

## S1 — Contexte historique et codage MEPA Full

### 1.1 Narration historique

L'Égypte de 2010 présente une configuration socio-institutionnelle caractéristique des régimes autoritaires arabes en fin de cycle : un appareil d'État militaro-sécuritaire profondément enraciné depuis 1952, une économie rentière partiellement diversifiée mais incapable d'absorber une démographie jeune et éduquée, et une crédibilité du régime Moubarak en effondrement accéléré depuis les élections législatives frauduleuses de novembre 2010. La fracture de l'élite est réelle mais asymétrique : elle oppose moins des factions rivales au sein du SCAF (Supreme Council of the Armed Forces) qu'une tension entre l'appareil militaire institutionnel et le clan Moubarak-Gamal, perçu comme cherchant à privatiser l'État au profit d'une bourgeoisie d'affaires liée au fils du président.

Le 25 janvier 2011, la mobilisation de la place Tahrir cristallise une coalition hétérogène — jeunesse des réseaux sociaux, Frères musulmans disciplinés, syndicalistes, libéraux — autour d'une revendication commune : la chute du régime Moubarak. La dynamique des dix-huit jours qui suivent est remarquable par sa rapidité : la loyauté des appareils s'effondre progressivement, l'armée refuse d'ouvrir le feu sur les manifestants, et Moubarak démissionne le 11 février 2011, remettant le pouvoir au SCAF.

Ce moment est souvent lu comme une révolution. Il est plus précisément une **substitution de tutelle** : le SCAF ne subit pas la pression populaire, il l'utilise pour éliminer le clan Moubarak et reprendre le contrôle direct de l'État. La période 2011–2013 est celle d'une transition contrôlée, ponctuée d'élections (législatives décembre 2011–janvier 2012, présidentielle juin 2012) qui portent Mohamed Morsi et les Frères musulmans au pouvoir — un résultat que le SCAF tolère temporairement, dans l'attente d'une légitimation populaire de l'intervention militaire.

Le 30 juin 2013, des manifestations massives (mouvement Tamarrod, dont l'ampleur réelle est contestée) fournissent au général Sissi le prétexte d'un coup d'État institutionnel le 3 juillet 2013. Le massacre de Rabaa al-Adawiya le 14 août 2013 — entre 800 et 2 600 morts selon les sources — marque la clôture violente de la parenthèse islamiste et la restauration d'un régime militaire désormais débarrassé de toute contrainte de légitimité électorale. En 2014, Sissi est élu président avec 96,9 % des voix dans un scrutin sans compétition réelle.

La trajectoire 2010–2014 est donc celle d'une **mobilisation populaire réelle, suivie d'une répression réussie** : la force transformatrice (F) monte significativement en 2011, mais ne franchit jamais le seuil de résistance institutionnelle (R) — le SCAF reconstituant sa capacité répressive et redistributive (aide du Golfe, 12 milliards de dollars en 2013) plus vite que la coalition révolutionnaire ne peut consolider son avantage.

**Séquence analytique** : la trajectoire (b) Répression réussie de ce cas est déterminée non par la seule force brute de l'appareil répressif classique (A_r_c = 0.62, modéré), mais par la reconstitution de R via un apport redistributif exogène massif (aide saoudienne et émiratie post-coup) combinée à la dissolution des mouvements de masse post-Rabaa. C'est le calcul institutionnel du SCAF — et non la décroissance endogène de F — qui produit la trajectoire (b).

---

### 1.2 Codage MEPA Full V6.2 — 9 variables

| Variable | Symbole | Valeur codée | Source principale | Justification |
|---|---|---|---|---|
| Fracture de l'élite | E_split | **0.65** | Kandil (S2) ; El-Ghobashy (S1) | Fracture réelle entre clan Moubarak-Gamal (privatisation de l'État) et SCAF institutionnel. Fracture naissante-forte [0.60–0.70] : le SCAF est uni en interne, mais la rupture avec le président est consommée dès janvier 2011. |
| Cohésion organisationnelle élite | **γ** | **0.48** | Kandil (S2) ; Brownlee (S5) | γ = 0.48 : cohésion élite globale modérée. Le SCAF est discipliné, mais l'élite politique au sens large (partis, FM, libéraux) est fragmentée. Valeur intermédiaire reflétant la coexistence d'un noyau militaire cohérent et d'une périphérie politique désorganisée. |
| Capacité redistributive effective | A_d_eff | **3.8** | Banque mondiale (S8) ; FMI (S9) | A_d_eff = 3.8 [trappe à dette] : économie sous pression (chômage jeunes > 25 %, inflation, déficit budgétaire). Les subventions alimentaires et énergétiques absorbent ~30 % du budget mais ne suffisent pas à résorber le mécontentement. EROI = 3.75 confirme la contrainte énergétique. |
| Répression classique | A_r_c | **0.62** | Amnesty International (S10) ; HRW (S11) | A_r_c = 0.62 : répression classique significative mais non maximale. La police (CSF) est déployée massivement en janvier 2011 puis retirée stratégiquement par le SCAF. Post-coup 2013, la répression monte (Rabaa), mais reste en dessous du seuil de saturation. |
| Répression numérique/non-étatique | A_r_ne | **0.35** | Freedom House (S7) ; V-DEM (S6) | A_r_ne = 0.35 : surveillance numérique active (coupure internet 27–28 janvier 2011, surveillance des réseaux sociaux) mais capacité non-étatique limitée. Les délateurs et milices pro-régime existent mais ne constituent pas un réseau systématique. |
| Crédibilité du régime | Cs | **0.18** | V-DEM (S6) ; Brownlee (S5) | Cs = 0.18 : crédibilité effondrée. Les élections de 2010 frauduleuses, la corruption visible du clan Moubarak et l'incapacité à offrir des perspectives économiques ont détruit la légitimité du régime. Valeur basse [0.10–0.25]. |
| Loyauté des appareils | L(t) | **0.28** | Kandil (S2) ; El-Ghobashy (S1) | L(t) = 0.28 : loyauté faible. La police se retire, l'armée refuse de tirer sur les manifestants en janvier 2011. La loyauté se reconstitue progressivement sous le SCAF post-Moubarak, mais reste fragile jusqu'en 2013. |
| Rendement énergétique net | EROI | **3.75** | BP Statistical Review (S12) ; IEA (S13) | EROI = 3.75 : rendement en déclin (pic pétrolier égyptien dépassé, dépendance croissante aux importations de gaz). Contrainte énergétique réelle pesant sur la capacité redistributive. |
| Structure anthropologique Todd | Sa | **6** | Todd 1990 (S4) | Sa = 6 : structure communautaire (famille élargie, endogamie, solidarités claniques). Cohérence avec la mobilisation par réseaux de proximité à Tahrir et la résistance institutionnelle des Frères musulmans. |

**Conversion des scores en paramètres p1–p13** (Euler dt=1, t_max=300) :

| Paramètre | Valeur | Dérivation |
|---|---|---|
| p1 (pression initiale S₀) | 1.05 | f(E_split=0.65, Cs=0.18) |
| p2 (chaleur latente L₀) | 0.28 | L(t) initial |
| p3 (chaleur collective C₀) | 0.08 | f(Cs=0.18, Sa=6) |
| p4 (complexité institutionnelle I₀) | 6.20 | f(A_d_eff=3.8, γ=0.48) |
| p5 (couplage S→L) | 0.38 | μ standard V6.2 |
| p6 (dissipation C) | 0.045 | f(A_r_c=0.62, A_r_ne=0.35) ; Sa=6 → modulateur ×1.0 (Sa≠7) |
| p7 (couplage L→C) | 0.12 | f(E_split=0.65) |
| p8 (amortissement I) | 0.008 | f(A_d_eff=3.8, EROI=3.75) |
| p9 (λ, couplage L dans F) | 0.55 | standard V6.2 |
| p10 (μ, couplage γ×E dans F) | 0.38 | standard V6.2 |
| p11 (ν, couplage répression dans R) | 0.72 | f(A_r_c=0.62, A_r_ne=0.35) |
| p12 (ℓ, loyauté dans R) | 0.28 | L(t) initial |
| p13 (ρ, résistance résiduelle) | 0.15 | standard V6.2 |

**Sanity checks V6.2** :
- EROI > 1 ✓ (3.75 — thermodynamiquement valide)
- Sa ∈ {2, 4, 6, 7} ✓ (6 — communautaire)
- A_r_c + A_r_ne < 2.0 ✓ (0.97)
- E_split ∈ [0,1] ✓ ; γ ∈ [0,1] ✓ ; Cs ∈ [0,1] ✓ ; L(t) ∈ [0,1] ✓

---

### 1.3 Codage MEPA Full V7 — 6 variables supplémentaires

| Variable | Symbole | Valeur codée | Source | Justification |
|---|---|---|---|---|
| Stade matrice religieuse | M_r | **1** | Todd 1990 (S4) | Stade 1 : religion active. L'islam structure le droit (référence constitutionnelle à la charia), les institutions et la morale publique en Égypte. Pratique et identité religieuses fortement actives. M_r ∈ {1, 2} satisfait pour la sous-condition anthropologique de C1. |
| Polarisation mimétique | **μ_m** | **0.50** | El-Ghobashy (S1) ; Kandil (S2) ; V-DEM (S6) | μ_m = 0.50, bande [0.40–0.60] : polarisation forte (Armée vs Frères musulmans, clivage structurant le discours public) mais sans désignation publique systématique d'un bouc émissaire démographique unique. Valeur conforme à l'ancre de la grille CONV-E.md §V7-2 (« Égypte 2011, Frères musulmans vs Armée »). μ_m = 0.50 < μ_m* = 0.60 : sous-condition mimétique de C1 non franchie. |
| Fragmentation symbolique | Φ | **0.55** | V-DEM (S6) ; Freedom House (S7) | Φ = 0.55, bande [0.40–0.60] : pluralisme symbolique partiel. En 2011, l'espace médiatique combine télévision d'État, chaînes satellitaires (Al Jazeera), presse indépendante et réseaux sociaux mobilisés à Tahrir — plusieurs récits coexistent sans monopole d'un noyau. Φ modéré → σ(Φ) modéré. |
| Proportion noyau engagé | Ψ_noyau | **0.03** | Kandil (S2) ; V-DEM (S6) | Ψ_noyau = 0.03, bande [0.01–0.05] : le noyau organisé pertinent (appareil militaire/sécuritaire, SCAF) est numériquement restreint rapporté à la population totale (~2.4 millions de personnels militaires et sécuritaires / ~82 millions d'habitants ≈ 0.03), même s'il est très discipliné. Engagement actif soutenu = encadrement militaire et sécuritaire, pas une avant-garde de masse. |
| Proportion cible désignée | Ψ_cible | **null** | El-Ghobashy (S1) ; Kandil (S2) ; Wickham (S3) ; V-DEM (S6) ; Freedom House (S7) | *Voir justification E3 rev. 2.1 ci-dessous* |
| Capacité organisationnelle noyau | **γ_local** | **0.75** | Kandil (S2) ; ancre corpus V7 (γ_local_max_programme) | γ_local = 0.75, bande [0.60–0.80] : organisation très disciplinée. Le SCAF / appareil militaire égyptien possède une discipline hiérarchique forte, une chaîne de commandement centralisée et une capacité d'action coordonnée à grande échelle. Valeur pré-enregistrée γ_local_max_programme (ancre corpus V7). **Divergence noyau/élite** : γ_local = 0.75 (discipline militaire du SCAF) >> γ = 0.48 (cohésion de l'élite globale, plus fragmentée). Cas de divergence légitime, analogue au Rwanda ; γ V6.2 laissé intact (décision QG). |

**Justification E3 rev. 2.1 — Ψ_cible = null (positif)** :

> Les sources historiques consultées [El-Ghobas