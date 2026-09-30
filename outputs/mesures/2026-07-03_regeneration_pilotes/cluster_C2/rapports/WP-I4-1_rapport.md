# WP-I4-1 — Allemagne nazie (1919–1945)
## Working Paper MEPA V7-α rev. 2.1 | Cluster C2 | Sa = 7

---

## S1 — Contexte historique et codage MEPA Full

### 1.1 Narration historique

La République de Weimar (1919–1933) naît dans la défaite militaire et la délégitimation immédiate : le « coup de poignard dans le dos » (*Dolchstoßlegende*) impute la capitulation à une trahison intérieure — Juifs, socialistes, défaitistes — et non à l'épuisement militaire réel. Ce récit fondateur n'est pas anecdotique : il structure la grammaire politique de la droite radicale pendant quatorze ans et préfigure le mécanisme sacrificiel ultérieur. La crise économique de 1929–1932 effondre la crédibilité des partis du centre (Cs chute), radicalise les électorats et produit une fracture de l'élite entre conservateurs-nationalistes (Hindenburg, Papen, Hugenberg) qui croient pouvoir instrumentaliser Hitler, et le noyau NSDAP qui dispose d'une doctrine raciale cohérente et d'un appareil organisé.

La nomination de Hitler comme chancelier le 30 janvier 1933 est le produit de cette fracture : l'élite conservatrice cède le pouvoir exécutif à un mouvement de masse en croyant le contrôler. La *Machtergreifung* (prise du pouvoir) est suivie d'une *Gleichschaltung* (mise au pas) accélérée : incendie du Reichstag (27 février 1933), décret d'urgence, loi des pleins pouvoirs (23 mars 1933), interdiction des partis (juillet 1933), dissolution des syndicats, alignement de la presse. L'espace symbolique pluraliste se referme en moins de six mois.

Le régime nazi présente trois mécanismes analytiquement distincts que ce WP doit traiter séparément :

**Mécanisme 1 — E_split désigné vs E_split réel.** La fracture de l'élite codée en MEPA (E_split = 0.75) est la fracture *réelle* entre factions de l'élite allemande (conservateurs vs noyau NSDAP, Wehrmacht vs SS, industriels vs planificateurs d'État). Elle est analytiquement distincte du « E_split désigné » propagandiste : la rhétorique nazie construit une *élite fictive* (les Juifs comme « ploutocratie internationale », « bolchevisme juif ») qui n'a aucune correspondance avec la structure réelle du pouvoir. Ce E_split désigné est un artefact de la propagande girardienne — il alimente μ_m et Ψ_cible, pas E_split. Confondre les deux serait une erreur de codage majeure : E_split = 0.75 mesure la fracture réelle de l'élite allemande non-juive, pas la désignation propagandiste.

**Mécanisme 2 — A_r_ne auto-entretenue par délateurs volontaires.** La Gestapo compte environ 7 000 agents pour 66 millions d'Allemands en 1933 (ratio 1/9 400), soit un appareil répressif classique structurellement sous-dimensionné (A_r_c = 0.45). Ce paradoxe apparent est résolu par A_r_ne = 0.70 : environ 80 % des dossiers Gestapo sont ouverts sur délation spontanée de la population (Gellately 1990, Johnson 1999). La répression numérique/non-étatique n'est pas imposée d'en haut — elle est auto-entretenue par la participation volontaire de la société civile. La clause de repli V7-C1 (A_r_c_eff = A_r_c + 0.5 × A_r_ne = 0.45 + 0.35 = 0.80) capture précisément cette amplification.

**Mécanisme 3 — Sa = 7 (structure souche) vs E_split désigné amplificateur.** La structure anthropologique souche (Sa = 7, Todd 1990) produit deux effets antagonistes : (a) le modulateur p6 × 1.5 amortit la dissipation de la chaleur collective C (la structure souche favorise la cohésion hiérarchique et ralentit la désintégration institutionnelle), mais (b) la désignation d'un ennemi intérieur par le noyau NSDAP amplifie μ_m et la pression sociale S. Ces effets sont quantifiés en S3.

La trajectoire historique réelle suit une logique en deux temps : (a) cristallisation sacrificielle d'État (1933–1944), avec construction progressive de l'appareil d'exclusion et d'extermination, puis (d) effondrement exogène imposé par la défaite militaire (1944–1945). La phase (d) n'est pas produite endogènement par le modèle — elle est imposée par un choc exogène (la coalition alliée), ce qui distingue ce cas de WP-T1 où le choc exogène impose γ. Ici, le choc exogène impose (d) après une phase (a) prolongée.

### 1.2 Codage MEPA Full V6.2 — 9 variables

| Variable | Valeur | Source | Justification |
|---|---|---|---|
| E_split | 0.75 | Evans 2003 (S1) ; Kershaw 1998 (S3) | Fracture réelle de l'élite : conservateurs-nationalistes vs noyau NSDAP, Wehrmacht vs SS, industriels vs planificateurs. Fracture naissante à critique (bande 0.6–0.8). Distinct du E_split désigné propagandiste (voir §1.1). |
| **γ** | 0.55 | Kershaw 1998 (S3) ; Evans 2003 (S1) | Capacité organisationnelle de l'élite globale : NSDAP discipliné, doctrine unifiée, chaîne de commandement. Bande [0.40–0.60] organisation structurée. Conceptuellement distinct de γ_local (voir §1.3). |
| A_d_eff | 2.5 | Overy 1994 (S5) ; Tooze 2006 (S6) | Capacité redistributive effective faible : économie de guerre sous contrainte, réarmement financé par déficit (Mefo-Wechsel), pillage des territoires occupés. Bande [2–4] faillite technique à trappe à dette. |
| A_r_c | 0.45 | Gellately 1990 (S2) ; Johnson 1999 (S9) | Répression classique modérée : Gestapo ~7 000 agents / 66 M d'Allemands. Appareil d'État classique sous-dimensionné. Compensé par A_r_ne élevé (voir clause de repli V7-C1). |
| A_r_ne | 0.70 | Gellately 1990 (S2) ; Johnson 1999 (S9) | Répression non-étatique très élevée : ~80 % des dossiers Gestapo ouverts sur délation spontanée. Réseau de surveillance auto-entretenu par la société civile. |
| Cs | 0.15 | Kershaw 1998 (S3) ; Evans 2003 (S1) | Crédibilité du régime très faible à l'onset 1933 : légitimité contestée, gouvernement de coalition instable, mémoire de la défaite 1918. La crédibilité nazie se construit *après* la prise du pouvoir, pas avant. |
| L(t) | 0.20 | Kershaw 1998 (S3) | Loyauté des appareils initiale faible : Wehrmacht non alignée, bureaucratie d'État héritée de Weimar, résistances internes. L(t) croît après 1934 (Nuit des longs couteaux, serment à Hitler). |
| EROI | 13 | Overy 1994 (S5) ; Tooze 2006 (S6) | Rendement énergétique net : Allemagne 1930s dispose d'un accès au charbon de la Ruhr (EROI charbon ~13), base industrielle solide. Valeur > 1 thermodynamiquement obligatoire. |
| Sa | 7 | Todd 1990 (S4) ; Todd 2017 (S7) | Structure anthropologique souche (*Stammfamilie*) : héritage unique, cohabitation intergénérationnelle, autorité paternelle forte, inégalité acceptée. Modulateur p6 × 1.5 activé. |

**Sanity checks V6.2** :
- EROI = 13 > 1 ✓ (thermodynamiquement obligatoire)
- A_r_c + A_r_ne = 0.45 + 0.70 = 1.15 (valeurs indépendantes, pas additionnées dans R(t)) ✓
- E_split = 0.75 ∈ [0,1] ✓ ; γ = 0.55 ∈ [0,1] ✓
- Sa = 7 ∈ {2, 4, 6, 7} ✓

### 1.3 Codage MEPA V7 — 6 variables supplémentaires

| Variable | Valeur | Source | Justification |
|---|---|---|---|
| M_r | 2 | Todd 1990 (S4) ; Todd 2017 (S7) | Stade 2 — religion en transition zombie. Protestantisme et catholicisme ont perdu leur fonction institutionnelle structurante mais conservent des effets sociaux résiduels (identité confessionnelle, antijudaïsme chrétien sédimenté). La matrice religieuse n'est plus active (≠ Stade 1) mais pas encore dissoute (≠ Stade 3). C'est sur ce substrat zombie que se greffe le mécanisme sacrificiel racialisé séculier. M_r ∈ {1, 2} requis pour C1 : **satisfait**. |
| μ_m | 0.85 | Evans 2003 (S1) ; Kershaw 1998 (S3) | Bande [0.80–1.00] : polarisation mimétique maximale avec désignation d'un ennemi démographique. Les Juifs sont désignés publiquement comme ennemi racial absolu (lois de Nuremberg 1935, *Der Stürmer*, propagande d'État systématique). Valeur au plafond programme (μ_m_max = 0.85, partagé avec Rwanda 1994). μ_m > μ_m* = 0.60 requis pour C1 : **satisfait**. (Distinct du paramètre dynamique μ ≈ 0.38 de F(t).) |
| Φ | 0.30 | Evans 2003 (S1) ; Décision V7-D1 rev. 4 §5.1 | Bande [0.20–0.40] : monopole dominant avec résidus pluralistes en cours de répression. Valeur codée à l'*onset* 1933 : la *Gleichschaltung* est en cours mais des poches symboliques subsistent (presse confessionnelle, partis en voie d'interdiction, Églises). Valeur pré-enregistrée par la Décision V7-D1 rev. 4 §5.1. Note : la grille CONV-E.md cite « Allemagne 1935–1945 » en bande [0.00–0.20] — cet exemple décrit la phase consolidée, pas l'onset 1933 codé ici. Distinction onset/consolidation à harmoniser en V7.1. Sans incidence sur C2 : l'échec est robuste même à Φ = 0.15. |
| Ψ_noyau | 0.01 | NSDAP *Parteistatistik* 1933 (S8) ; Recensement 1933 (S8) | Codée ≈ 0.01 conformément à la règle pré-enregistrée par la Décision V7-D1 rev. 4 §5 : NSDAP ≈ 800 000 membres formels / 66 M d'Allemands = 1.2 %. **Exclus** du comptage : votants NSDAP de mars 1933 (~43 % — le vote n'est pas un engagement actif soutenu), sympathisants passifs, population sous contrôle après 1934 (la contrainte n'est pas l'adhésion). Cette valeur entraîne un **échec attendu** sur C2 : Ψ_noyau × γ_local = 0.01 × 0.55 = 0.0055 < σ(Φ = 0.30) ≈ 0.0275. |
| Ψ_cible | 0.008 | Recensement allemand juin 1933 (S8) ; Evans 2003 (S1) | Juifs désignés publiquement par le noyau NSDAP comme cible démographique unique : désignation raciale (critère d'appartenance biologique), publique (lois de Nuremberg, presse d'État), dominante. Proportion ≈ 525 000 Juifs / 66 M d'Allemands = 0.008. Valeur non-null : condition C3 **satisfaite**. Cohérent avec μ_m = 0.85 (règle de cohérence : Ψ_cible non-null si μ_m > 0.80). |
| γ_local | 0.55 | Kershaw 1998 (S3) ; Evans 2003 (S1) | Bande [0.40–0.60] : organisation structurée du noyau NSDAP — parti discipliné doté d'une doctrine raciale unifiée, SA structurée, hiérarchie fonctionnelle, chaîne de commandement opérationnelle. γ_local mesure la discipline du **seul noyau** Ψ_noyau, distincte de γ (cohésion de l'élite globale V6.2 = 0.55, conceptuellement séparée). Le noyau est très discipliné (γ_local élevé) mais sa base est extrêmement restreinte (Ψ_noyau = 0.01) : la discipline ne compense pas la base — c'est précisément la limite illustrée par l'échec C2. |

### 1.4 Précheck V7 — Conditions C1–C4 (pré-simulation)

```
C1 = (M_r = 2 ∈ {1, 2}) AND (μ_m = 0.85 > 0.60)
   = TRUE AND TRUE
   = TRUE ✓

C2 : σ(Φ = 0.30) = 0.018 × (1 + 1.7 × 0.30)
                  = 0.018 × (1 + 0.51)
                  = 0.018 × 1.51
                  = 0.0272
     Ψ_noyau × γ_local = 0.01 × 0.55 = 0.0055
     C2 = (0.0055 > 0.0272) = FALSE ✗

C3 = (Ψ_cible = 0.008 ≠ null) = TRUE ✓

Clause de repli V7-C1 (A_r_c = 0.45 ≤ 0.70) :
     A_r_c_eff = A_r_c + 0.5 × A_r_ne
               = 0.45 + 0.5 × 0.70
               = 0.45 + 0.35
               = 0.80
C4 = (A_r_c_eff = 0.80 > 0.70) = TRUE ✓

alpha_precheck = C1 AND C2 AND C3 AND C4
               = TRUE AND FALSE AND TRUE AND TRUE
               = FALSE

→ Branche (α) EXCLUE avant simulation (C2 non satisfaite).
→ Rampe mod_mimétique NON activée.
→ Simulation en mode V6.2 standard avec modulateur Sa = 7 (p6 × 1.5).
```

**Résumé précheck** : trois conditions sur quatre sont satisfaites (C1, C3, C4). La condition C2 échoue de manière robuste : Ψ_noyau × γ_local = 0.0055 est inférieur à σ(Φ = 0.30) = 0.0272 d'un facteur ~5. Cet échec est **attendu et pré-enregistré** par la Décision V7-D1 rev. 4 §5. La condition C5 n'est pas évaluée (alpha_precheck = FALSE). Le rapport doit contenir les Réserves 1 et 2 du §4bis (§S3bis et §S3ter ci-dessous).

---

## S2 — Simulation MEPA Lite

### 2.1 Paramètres de simulation

- Intégrateur : Euler explicite dt = 1 (V6.2 standard — rampe mod_mimétique non activée)
- Modulateur Sa = 7 : p6 × 1.5 activé avant la première itération
- Durée : t = 0 à t = 300
- Conditions initiales : S₀ = 1.0, L₀ = 0.20, C₀ = 0.05, I₀ = 6.0

### 2.2 Tableau F(t)/R(t) — valeurs exactes du runner

| t | F(t) | R(t) | FR = F/R |
|---|---|---|---|
| 0 | 0.2573 | 1.5598 | 0.1650 |
| 25 | 0.3615 | 1.7176 | 0.2104 |
| 50 | 0.3088 | 1.7925 | 0.1723 |
| 75 | 0.2968 | 1.8491 | 0.1605 |
| 100 | 0.2941 | 1.8995 | 0.1548 |
| 150 | 0.2934 | 1.9911 | 0.1473 |
| 200 | 0.2933 | 2.0740 | 0.1414 |
| 250 | 0.2933 | 2.1502 | 0.1364 |
| 300 | 0.2933 | 2.2208 | 0.1321 |

### 2.3 Indicateurs de simulation

| Indicateur | Valeur | Note |
|---|---|---|
| t_bascule | **null** | Aucune bascule F > R détectée — F reste inférieur à R sur toute la simulation |
| ΔC_rel | **null** | Non calculé (absence de bascule) |
| ΔI_rel | **null** | Non calculé (absence de bascule) |
| FR_max | **0.3** | Atteint vers t ≈ 25 (pic de mobilisation précoce) |
| FR_final | 0.1321 | Ratio décroissant — résistance institutionnelle croissante |
| C_max | 0.1097 | Chaleur collective maximale — inférieure au seuil C5 (θ_C = 0.30) |
| C_final | 0.0574 | Dissipation progressive de la chaleur collective |
| chute_C | (0.1097 − 0.0574) / 0.1097 = **0.477** | Chute relative de C : 47.7 % |
| S_final | 0.75 | Pression sociale résiduelle |
| L_final | 0.2999 | Loyauté des appareils en légère hausse |
| C5 | **FALSE** | C_max = 0.1097 < θ_C = 0.30 |
| A_r_c_eff | 0.80 | Clause de repli V7-C1 activée |
| Branche annotation | **CATCHALL** | Voir §2.4 |

### 2.4 Trajectoire diagnostiquée et divergence

**Trajectoire diagnostiquée par le runner : (b) Répression réussie — CATCHALL**

Vérification des conditions de la branche (b) explicative V7-C4 :
- C_max = 0.1097 > 0.12 ? → **FALSE** (0.1097 < 0.12)
- chute_C = 0.477 > 0.20 ? → TRUE
- Cs = 0.15 ∈ [0.10, 0.50] ? → TRUE
- Rc + Rn = 0.45 + 0.70 = 1.15 > 0.40 ? → TRUE

La condition C_max > 0.12 n'est pas satisfaite (0.1097 < 0.12). La branche (b) **explicative** V7-C4 n'est donc pas déclenchée. Le runner classe le cas en branche (b) **CATCHALL** (Rc + Rn > 0.6 → fallback V6.2).

**Divergence documentée — la simulation produit (b) Répression réussie au lieu de (α) Cristallisation sacrificielle d'État attendue.**

Condition technique non atteinte : F reste < R sur toute la simulation (t_bascule = null). La force transformatrice F(t) atteint un maximum de FR_max = 0.3 à t ≈ 25, soit un ratio F/R de 0.21 — très loin du seuil F = R (FR = 1.0). La résistance institutionnelle R(t) croît monotonement de 1.56 à 2.22 sur la période simulée, tandis que F(t) se stabilise autour de 0.29 après t = 50. La chaleur collective C_max = 0.1097 est inférieure au seuil θ_C = 0.30 requis pour la condition C5 de la branche (α). La condition C2 de la branche (α) échoue en précheck (Ψ_noyau × γ_local = 0.0055 < σ(Φ) = 0.0272).

Potentielle zone de réfutation [RF1 : EROI < 5 sans techno / RF2 : absence (a)/(d) malgré E_split > 0.7 / RF3 : complexité croissante avec EROI déclinant] si confirmée sur d'autres cas.

**Note sur la phase (d) exogène** : la trajectoire historique réelle inclut un effondrement (d) en 1944–1945, mais celui-ci est imposé par un choc exogène (défaite militaire alliée), non produit endogènement par la dynamique F/R. Le runner confirme que (d) n'est pas produit endogènement : R(t) croît continûment, aucune chute de I n'est observée dans la simulation. Ceci distingue ce cas de WP-T1 : dans WP-T1, le choc exogène impose γ ; ici, il impose (d) après une phase (a) prolongée non capturée par le runner.

---

## S3 — Analyse MEPA Full et concordance

### 3.1 Tableau de concordance — 6 dimensions

| Dimension | Prédit par MEPA | Observé historiquement | Concordance |
|---|---|---|---|
| Trajectoire principale | (b) Répression réussie [CATCHALL] | (α) Cristallisation sacrificielle d'État | **NON** |
| Mécanisme répressif | Répression élevée (A_r_c_eff = 0.80) | Appareil répressif hybride État/société civile | Partielle |
| Dynamique F/R | F < R sur toute la période, R croissant | Résistance institutionnelle croissante 1933–1944 | Oui (partielle) |
| Chaleur collective C | C_max = 0.1097, dissipation progressive | Mobilisation de masse réelle mais canalisée par l'État | Partielle |
| Loyauté des appareils | L(t) croissant (0.20 → 0.30) | Alignement progressif Wehrmacht/bureaucratie 1933–1938 | Oui |
| Effondrement (d) | Non produit endogènement | Effondrement exogène 1944–1945 | Partielle (exogène) |

**Annotation branche** : (b) Répression réussie — **CATCHALL**. Cette concordance est **non-discriminante** : le cas tombe dans le fourre-tout par défaut (Rc + Rn > 0.6), la concordance sur cette dimension ne teste pas réellement le modèle.

### 3.2 Effets antagonistes Sa = 7 vs E_split désigné

Le modulateur Sa = 7 (p6 × 1.5) produit un amortissement de la dissipation de C : la structure souche favorise la cohésion hiérarchique et ralentit la désintégration institutionnelle, ce qui se traduit par une R(t) croissante et une F(t) qui ne perce jamais le seuil. Simultanément, E_split = 0.75 (fracture réelle de l'élite) devrait amplifier C via le terme μ × γ × E dans F(t). Ces deux effets sont antagonistes :

- **Effet Sa = 7** : p6 × 1.5 → amortissement de la dissipation de C → R(t) croissant → F/R décroissant après t = 25
- **Effet E_split = 0.75** : terme μ × γ × E = 0.38 × 0.55 × 0.75 ≈ 0.157 → amplification de F(t) via L(t)

Le résultat net est une F(t) qui culmine à 0.36 à t = 25 puis décroît vers 0.29 : l'amortissement Sa domine l'amplification E_split sur le long terme. Le E_split désigné propagandiste (construction fictive de l'élite juive) n'est pas capturé par E_split = 0.75 — il est encodé dans μ_m = 0.85 et Ψ_cible = 0.008, variables V7 qui n'entrent pas dans les équations différentielles V6.2.

### 3.3 §S3bis — Anomalie documentée (Réserve 1 §4bis, Décision V7-D1 rev. 4)

**Divergence nominée** : trajectoire attendue (α) Cristallisation sacrificielle d'État vs trajectoire diagnostiquée (b) Répression réussie [CATCHALL].

**Explication causale par le modèle** : la divergence est entièrement imputable à l'échec de la condition C2 de la branche (α). Le calcul est le suivant :

- Ψ_noyau × γ_local = 0.01 × 0.55 = **0.0055**
- σ(Φ = 0.30) = 0.018 × (1 + 1.7 × 0.30) = **0.0272**
- Ratio : 0.0055 / 0.0272 ≈ **0.20** — le produit Ψ_noyau × γ_local est cinq fois inférieur au seuil σ(Φ)

La condition C2 échoue parce que Ψ_noyau est codée à 0.01 (membres formels NSDAP en janvier 1933, règle pré-enregistrée par la Décision V7-D1 rev. 4 §5). Cette valeur est correcte au sens de la définition stricte de l'engagement actif soutenu : les 43 % de votants NSDAP de mars 1933 ne constituent pas un noyau organisé au sens de la trajectoire (α). La discipline organisationnelle élev��e du noyau (γ_local = 0.55) ne compense pas sa base démographique extrêmement restreinte.

**Statut de zone de réfutation** : cet échec est **attendu et pré-enregistré** par la Décision V7-D1 rev. 4 §5. Il ne constitue pas une réfutation empirique du cadre V7-α rev. 2.1 mais une **limite assumée** : le cadre ne parvient pas à capturer la trajectoire (α) pour le cas paradigmatique de la cristallisation sacrificielle d'État nazie, précisément parce que la définition stricte de Ψ_noyau exclut la mobilisation de masse post-prise du pouvoir. Cette limite est documentée comme zone de réfutation potentielle si elle se confirme sur d'autres cas du corpus (voir RF3 en S7).

Référence : Décision V7-D1 rev. 4 §4bis (Réserve 1) et Annexe B §B.1 du cadre rev. 2.1.

### 3.4 §S3ter — Hypothèse théorique sous contrainte (Réserve 2 §4bis, Décision V7-D1 rev. 4)

**Isolation textuelle** : cette sous-section est séparée et identifiée conformément au protocole V7-C3. Elle ne constitue pas une justification a posteriori du cas WP-I4-1 mais une direction de résolution pour le chantier V7.1.

**Hypothèse** : la condition C2 dans sa formulation actuelle (Ψ_noyau × γ_local > σ(Φ)) capture la masse critique d'un noyau *pré-existant* à la prise du pouvoir. Elle ne capture pas les cas où le noyau organisé *utilise l'appareil d'État* comme multiplicateur de sa capacité après la prise du pouvoir. Dans ces cas, la variable pertinente n'est pas Ψ_noyau × γ_local mais une variable composite intégrant l'alignement institutionnel macro (Wehrmacht, bureaucratie, police) — appelons-la provisoirement Ψ_eff = Ψ_noyau × γ_local × f(A_r_c_eff, L(t)). Si cette hypothèse est correcte, les cas où un noyau restreint mais discipliné s'empare d'un appareil d'État et l'utilise comme vecteur du mécanisme sacrificiel devraient déclencher la branche (α) avec une formulation étendue de C2.

**Prédiction falsifiable sur un cas non encore simulé** : cette hypothèse sera testée sur **WP-RU1-1 (Russie 1917–1924, bolchevisme)**, cas où un noyau bolchevik restreint (~10 000 membres en février 1917, Ψ_noyau ≈ 0.006) s'empare de l'appareil d'État et organise un mécanisme sacrificiel (Terreur rouge, dékoulakisation). Si WP-RU1-1 produit également un échec C2 avec Ψ_noyau × γ_local < σ(Φ) malgré un mécanisme sacrificiel historiquement documenté, l'hypothèse est **confirmée** (la limite est structurelle, pas spécifique à WP-I4-1). Si WP-RU1-1 déclenche la branche (α) avec les paramètres actuels, l'hypothèse est **réfutée** (la limite est spécifique à WP-I4-1 et la formulation actuelle de C2 est suffisante).

**Statut spéculatif** : cette hypothèse est spéculative et relève du chantier V7.1. Elle ne modifie pas le cadre V7-α rev. 2.1 figé jusqu'à la certification V7.0 post-test V7-γ rev. 2.

---

## S4 — Stress-test de robustesse

### 4.1 Stress-test N1 (optimiste/pessimiste)

| Scénario | Modification | Trajectoire |
|---|---|---|
| Nominal | — | (b) Répression réussie |
| N1 Optimiste | E − 0.08 / R + 0.08 | (b) Répression réussie |
| N1 Pessimiste | E + 0.08 / R − 0.08 | (b) Répression réussie |

**Verdict N1 : ROBUSTE** — la trajectoire (b) Répression réussie est stable sous les perturbations N1 standard.

### 4.2 Stress-test N2 (8 combinaisons)

```
Stress N2 (8 combinaisons) :
  E+0.1    : (b) Répression réussie
  E-0.1    : (b) Répression réussie
  R+0.08   : (b) Répression réussie
  R-0.08   : (b) Répression réussie
  EROI+0.5 : (b) Répression réussie
  EROI-0.5 : (b) Répression réussie
  Rc+0.1   : (b) Répression réussie
  Rc-0.1   : (b) Répression réussie
```

**Sensibilité N1** : NON_CALCULÉ (non fourni par le runner).

### 4.3 Conclusion robustesse N1 + N2

La trajectoire (b) Répression réussie est **invariante** sur l'ensemble des 10 scénarios testés (nominal + 2 N1 + 8 N2). Cette robustesse extrême reflète la structure du cas : FR_max = 0.3 est très éloigné du seuil FR = 1.0, et R(t) croît monotonement sur toute la simulation. Aucune perturbation paramétrique raisonnable ne suffit à produire une bascule F > R. La robustesse est ici un indicateur de la **profondeur de la divergence** avec la trajectoire attendue (α) : le modèle est très loin de capturer le mécanisme sacrificiel, et les stress-tests confirment que cette distance n'est pas un artefact de paramétrage marginal.

---

## S5 — Fiche standardisée V7

| Champ | Valeur |
|---|---|
| **WP-ID** | WP-I4-1 |
| **Cas** | Allemagne nazie |
| **Période** | 1919–1945 |
| **Cluster** | C2 |
| **Version cadre** | V7-α rev. 2.1 |
| **E_split** | 0.75 (fracture réelle de l'élite — distinct du E_split désigné propagandiste) |
| **γ** | 0.55 (capacité organisationnelle élite globale) |
| **A_d_eff** | 2.5 (faillite redistributive, économie de guerre sous contrainte) |
| **A_r_c** | 0.45 (Gestapo sous-dimensionnée ~7 000 agents / 66 M) |
| **A_r_ne** | 0.70 (~80 % délations spontanées, réseau auto-entretenu) |
| **A_r_c_eff** | 0.80 (clause de repli V7-C1 : 0.45 + 0.5 × 0.70) |
| **Cs** | 0.15 (crédibilité très faible à l'onset 1933) |
| **L(t) initial** | 0.20 (loyauté faible, Wehrmacht non alignée) |
| **EROI** | 13 (charbon de la Ruhr, base industrielle solide) |
| **Sa** | 7 — structure souche (*Stammfamilie*), modulateur p6 × 1.5 activé |
| **M_r** | 2 — Stade 2, religion zombie (protestantisme/catholicisme en transition) |
| **μ_m** | 0.85 — polarisation mimétique maximale, désignation démographique (lois de Nuremberg, *Der Stürmer*) |
| **Φ** | 0.30 — monopole dominant avec résidus pluralistes (onset 1933, *Gleichschaltung* en cours) |
| **Ψ_noyau** | 0.01 — membres formels NSDAP jan. 1933 (≈ 800 000 / 66 M). Règle pré-enregistrée V7-D1 rev. 4 §5. Votants exclus. |
| **Ψ_cible** | 0.008 — Juifs désignés publiquement (≈ 525 000 / 66 M, recensement 1933). Condition C3 satisfaite. |
| **γ_local** | 0.55 — capacité organisationnelle du seul noyau NSDAP (distinct de γ global) |
| **Trajectoire attendue** | (α) Cristallisation sacrificielle d'État |
| **Trajectoire diagnostiquée** | (b) Répression réussie |
| **Branche annotation** | **CATCHALL** (fallback V6.2 : Rc + Rn > 0.6) |
| **Concordance** | **NON** — divergence pré-enregistrée (Décision V7-D1 rev. 4 §5) |
| **alpha_precheck** | FALSE (C2 échoue : 0.0055 < 0.0272) |
| **C5** | FALSE (C_max = 0.1097 < θ_C = 0.30) |
| **Robustesse N1** | ROBUSTE — trajectoire stable sur 10 scénarios |
| **FR_max** | 0.3 (t ≈ 25) |
| **C_max** | 0.1097 |

---

## S6 — Prédictions Popper

### P1 — Bascule F > R (prédiction de base MEPA)

**Prédiction** : si E_split > 0.6 et Cs < 0.3, une bascule F > R doit être observable dans la simulation.

**Résultat** : **INFIRMÉE sur ce cas**. E_split = 0.75 et Cs = 0.15 satisfont les conditions, mais t_bascule = null — aucune bascule détectée. FR_max = 0.3, très loin du seuil FR = 1.0. La résistance institutionnelle R(t) croît continûment, portée par la complexité institutionnelle I(t) croissante et le niveau élevé de répression (A_r_c_eff = 0.80). L'infirmation est robuste sur 10 scénarios de stress-test.

**Interprétation** : P1 est infirmée parce que le régime nazi n'est pas un régime en voie de transformation — c'est un régime qui *consolide* sa résistance institutionnelle après la prise du pouvoir. La logique MEPA de bascule F > R capture les transitions depuis un régime établi vers un challenger, pas la consolidation d'un régime nouveau.

### P2 — Loyauté des appareils (prédiction dynamique)

**Prédiction** : L(t) doit croître si le régime survit à la phase initiale de fragilité (Cs faible).

**Résultat** : **CONFIRMÉE partiellement**. L_final = 0.2999 vs L_initial = 0.20 — hausse de 50 % sur la période simulée. Cohérent avec l'alignement progressif de la Wehrmacht (serment à Hitler 1934), de la bureaucratie et des appareils judiciaires.

### P3 — Répression et dissipation de C (prédiction mécanistique)

**Prédiction** : si A_r_c_eff > 0.7, la chaleur collective C doit être dissipée sans atteindre le seuil de bascule.

**Résultat** : **CONFIRMÉE**. C_max = 0.1097 < θ_C = 0.30, chute_C = 47.7 %. La répression effective (A_r_c_eff = 0.80) dissipe C avant qu'elle n'atteigne le seuil critique. Mécanisme cohérent avec la répression précoce des opposants (KPD, SPD, syndicats) en 1933.

### P4 — Structure souche et amortissement (prédiction anthropologique)

**Prédiction** : Sa = 7 doit produire un amortissement de la dissipation institutionnelle (R(t) croissant, I(t) stable ou croissant).

**Résultat** : **CONFIRMÉE**. R(t) croît de 1.56 à 2.22 sur la simulation. Le modulateur p6 × 1.5 ralentit la dissipation de C et contribue à la croissance de R(t). La structure souche allemande (hiérarchie acceptée, autorité paternelle) est cohérente avec l'alignement progressif des appareils.

### P5 — EROI et base énergétique (prédiction biophysique)

**Prédiction** : EROI = 13 doit permettre une résistance institutionnelle soutenue (R(t) > 1 sur toute la période).

**Résultat** : **CONFIRMÉE**. R(t) reste supérieur à 1.55 sur toute la simulation et croît jusqu'à 2.22. La base énergétique charbon de la Ruhr soutient la résistance institutionnelle. Les stress-tests EROI ± 0.5 ne modifient pas la trajectoire.

### P6 — Cristallisation sacrificielle (prédiction V7)

**Prédiction** : le mécanisme sacrificiel girardien ne se déclenche que si les 5 conditions C1–C5 de la branche (α) sont simultanément satisfaites.

**Résultat** : **FORMELLEMENT INFIRMÉE sur ce cas**. Les conditions C1 (TRUE), C3 (TRUE) et C4 (TRUE) sont satisfaites, mais C2 échoue (Ψ_noyau × γ_local = 0.0055 < σ(Φ) = 0.0272) et C5 n'est pas évaluée (alpha_precheck = FALSE). Le cadre V7-α rev. 2.1 ne parvient pas à diagnostiquer la trajectoire (α) pour le cas paradigmatique de la cristallisation sacrificielle d'État nazie.

**Statut de cette infirmation** : **pré-enregistrée et assumée** (Décision V7-D1 rev. 4 §5). Elle n'est pas considérée comme une réfutation empirique du cadre mais comme une **limite assumée** de la formulation actuelle de C2. La définition stricte de Ψ_noyau (engagement actif soutenu pré-prise du pouvoir) exclut structurellement les cas où un noyau restreint s'empare de l'appareil d'État et l'utilise comme multiplicateur. Cette limite est documentée et oriente le chantier V7.1 (voir §S7bis).

---

## S7 — Bornes de réfutation et synthèse comparative cluster C2

### 7.1 Bornes de réfutation

**RF1 — Seuil EROI et base énergétique** : si un cas du corpus présente EROI < 5 sans substitution technologique documentée et produit néanmoins une trajectoire (α) ou (a), la prédiction biophysique de MEPA est réfutée. Pour WP-I4-1, EROI = 13 est robuste — la base charbon de la Ruhr n'est pas en question sur la période 1919–1945. Horizon de test : WP-SY1-1 (Syrie 2011, EROI pétrolier déclinant).

**RF2 — E_split élevé sans trajectoire (a) ou (d)** : si E_split > 0.7 produit systématiquement une trajectoire (b) CATCHALL sans jamais déclencher (a) ou (d), la variable E_split perd son pouvoir discriminant. WP-I4-1 est un premier cas de ce type (E_split = 0.75, trajectoire (b) CATCHALL). Si WP-RU1-1 (Russie 1917) et WP-CN1-1 (Chine 1949) produisent également (b) CATCHALL malgré E_split > 0.7, RF2 est activée. Horizon de test : cluster C2 complet.

**RF3 — Complexité institutionnelle croissante avec EROI déclinant** : si I(t) croît continûment pendant qu'EROI décline, le modèle prédit une résistance institutionnelle croissante indéfiniment — ce qui est thermodynamiquement impossible. Pour WP-I4-1, I(t) croît et EROI = 13 est stable : pas de contradiction. Mais si un cas futur montre I(t) croissant avec EROI < 5, RF3 est activée. Horizon de test : WP-VE1-1 (Venezuela 2013–2019).

### 7.2 §S7bis — Direction de résolution V7.1

*(Obligatoire — §S3bis rédigée, divergence sur cas pilote V7-γ rev. 2)*

**Chantier V7.1 engagé par la divergence WP-I4-1** : la divergence identifie une limite structurelle de la condition C2 dans sa formulation actuelle. Trois directions de résolution sont envisagées pour le chantier V7.1 :

**Direction A — Score continu de Ψ_noyau** : remplacer la définition binaire (membres formels / non-membres) par un score continu pondéré par le niveau d'engagement (membres formels × 1.0 + cadres actifs × 0.7 + sympathisants organisés × 0.3). Cette direction permettrait de capturer les cas où la base formelle est restreinte mais l'engagement effectif est plus large. Risque : introduire une subjectivité dans le codage qui affaiblit la reproductibilité.

**Direction B — Variable d'alignement macro (Configuration B)** : introduire une variable Ψ_eff = Ψ_noyau × γ_local × f(A_r_c_eff, L(t)) qui capture l'amplification du noyau par l'appareil d'État après la prise du pouvoir. Cette direction est cohérente avec l'hypothèse théorique de §S3ter. Risque : complexifier le modèle et réduire sa parcimonie.

**Direction C — Reset inter-phases** : distinguer deux phases temporelles dans la condition C2 — une phase pré-prise du pouvoir (Ψ_noyau strict) et une phase post-prise du pouvoir (Ψ_noyau élargi à l'appareil d'État aligné). Cette direction permettrait de capturer la dynamique temporelle de la cristallisation sacrificielle nazie. Risque : introduire une discontinuité temporelle difficile à opérationnaliser.

**Cas futur de test** : **WP-RU1-1 (Russie 1917–1924)**. Prédiction falsifiable : si WP-RU1-1 produit un échec C2 avec Ψ_noyau × γ_local < σ(Φ) malgré un mécanisme sacrificiel documenté (Terreur rouge), la Direction B est confirmée comme nécessaire. Si WP-RU1-1 déclenche la branche (α) avec les paramètres actuels, la Direction B est inutile et la limite est spécifique à WP-I4-1.

**Temporalité** : selon la Décision V7-D1 rev. 4 §6, le chantier V7.1 est conditionné à la complétion du cluster pilote V7-γ rev. 2 (WP-I4-1, WP-F10-1, WP-RW1-1). La direction de résolution sera arbitrée après analyse comparative des trois cas.

### 7.3 Synthèse comparative cluster C2

Le cluster C2 regroupe les cas de cristallisation sacrificielle d'État et de répression organisée. WP-I4-1 est le seul WP fasciste du corpus et présente trois caractéristiques uniques :

1. **E_split désigné vs réel** : seul cas du corpus où la propagande construit une fracture fictive de l'élite (Juifs comme « ploutocratie ») analytiquement distincte de la fracture réelle (conservateurs vs NSDAP). Cette dualité n'est pas capturée par les équations V6.2.

2. **A_r_ne auto-entretenue** : seul cas du corpus (avec Rwanda 1994) où la répression non-étatique est majoritairement auto-entretenue par délation volontaire. La clause de repli V7-C1 (A_r_c_eff = 0.80) est nécessaire pour capturer ce mécanisme.

3. **Divergence pré-enregistrée** : seul cas du corpus où la divergence trajectoire attendue / diagnostiquée est anticipée et documentée avant la simulation. Cette pré-enregistrement est une propriété positive du protocole V7-C3 — il distingue les limites assumées des réfutations empiriques.

Par rapport à WP-T1 (cas de référence cluster C2 avec choc exogène imposant γ) : dans WP-T1, le choc exogène modifie la capacité organisationnelle de l'élite ; dans WP-I4-1, le choc exogène (défaite 1945) impose la phase (d) après une phase (a) prolongée non capturée endogènement. Les deux cas illustrent la limite du runner face aux chocs exogènes majeurs, mais par des mécanismes distincts.

**Implication pour le corpus MEPA** : WP-I4-1 établit que la branche (α) dans sa formulation V7-α rev. 2.1 ne capture pas les cas de cristallisation sacrificielle d'État opérée par un noyau restreint s'appuyant sur l'appareil d'État comme multiplicateur. Cette limite est documentée, assumée, et oriente le chantier V7.1 vers la Direction B (variable d'alignement macro). Elle ne remet pas en cause la validité du cadre pour les cas où le noyau organisé est démographiquement significatif (Rwanda 1994, WP-RW1-1 attendu).

---

*WP-I4-1 — Rapport complet S1→S7 | MEPA V7-α rev. 2.1 | CONV-A Rédacteur*
*Divergence pré-enregistrée — Décision V7-D1 rev. 4 §5 | Réserves 1 et 2 §4bis documentées*