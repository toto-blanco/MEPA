# WP-I4-1 — Allemagne nazie (1919–1945)
## Working Paper MEPA V7-α rev. 2.1 | Cluster C2 | Sa = 7

---

## S1 — Contexte historique et codage MEPA Full

### 1.1 Narration historique

La République de Weimar (1919–1933) naît dans la défaite militaire et la honte nationale. Le traité de Versailles (1919) impose des réparations écrasantes, ampute le territoire allemand et interdit à l'Allemagne de se doter d'une armée significative. Cette humiliation fondatrice structure l'espace politique weimarien : la légitimité du régime républicain est contestée dès sa naissance par les nationalistes qui l'associent au « coup de poignard dans le dos » (*Dolchstoßlegende*) et par les communistes qui y voient un instrument de la bourgeoisie. La fracture de l'élite est donc précoce et profonde.

L'hyperinflation de 1923 détruit l'épargne de la classe moyenne et érode la crédibilité des institutions financières. La stabilisation Stresemann (1924–1929) offre un répit fragile, mais le krach de 1929 et la Grande Dépression qui s'ensuit précipitent une crise économique sans précédent : le chômage atteint 30 % en 1932, les faillites bancaires se multiplient, la capacité redistributive de l'État s'effondre. C'est dans ce contexte de triple crise — économique, institutionnelle, identitaire — que le NSDAP passe de 2,6 % des voix en 1928 à 37,4 % en juillet 1932.

La nomination d'Adolf Hitler comme chancelier le 30 janvier 1933 marque le début de la *Machtergreifung*. L'incendie du Reichstag (27 février 1933) fournit le prétexte à l'adoption du décret d'urgence qui suspend les libertés civiles. La loi des pleins pouvoirs (23 mars 1933) transforme le régime en dictature légale. La *Gleichschaltung* — alignement forcé de toutes les institutions sur le parti — s'opère en quelques mois : syndicats dissous, partis interdits, presse alignée, universités épurées. La nuit des Longs Couteaux (juin 1934) élimine la faction Röhm et consolide l'alliance avec la Wehrmacht et les élites industrielles.

Le régime nazi développe simultanément trois mécanismes qui font de ce cas un objet analytique unique dans le corpus MEPA :

**Mécanisme 1 — E_split désigné vs E_split réel.** Le NSDAP opère une distinction analytiquement cruciale entre deux types de fracture élitaire. La fracture *réelle* (E_split = 0.75) désigne la division effective entre les élites weimarien­nes — industriels, militaires, junkers, bureaucrates — qui se déchirent sur la réponse à la crise. La fracture *désignée* est une construction idéologique : les Juifs sont présentés comme une « élite fictive » parasite qui aurait capturé les institutions allemandes (finance, presse, médecine, droit). Cette désignation est analytiquement distincte de E_split réel : elle ne mesure pas une division effective au sein des élites mais une projection sacrificielle sur un groupe démographique. Dans le codage MEPA, E_split = 0.75 capture la fracture réelle entre factions élitaires ; la désignation sacrificielle est capturée par μ_m = 0.85 et Ψ_cible = 0.008. Confondre les deux serait une erreur de codage majeure.

**Mécanisme 2 — A_r_ne auto-entretenue par délateurs volontaires.** La Gestapo est structurellement sous-staffée : environ 7 000 agents pour 66 millions d'Allemands en 1933, soit un ratio de 1 pour 9 400. Robert Gellately et Klaus-Michael Mallmann ont documenté que 80 % environ des dossiers Gestapo s'ouvrent sur délation spontanée de la population. A_r_ne = 0.70 ne mesure donc pas une surveillance étatique dense mais un mécanisme de répression non-étatique auto-entretenu : la société se surveille elle-même. Ce mécanisme active la clause de repli V7-C1 : A_r_c_eff = A_r_c + 0.5 × A_r_ne = 0.35 + 0.35 = 0.70.

**Mécanisme 3 — Sa = 7 (structure souche) vs E_split désigné.** La structure anthropologique souche (Todd) génère un modulateur p6 × 1.5 qui amplifie la chaleur collective C. Mais cet amplificateur agit sur la mobilisation *interne* au noyau, pas sur la désignation sacrificielle externe. Les effets sont antagonistes : Sa = 7 tend à augmenter C (mobilisation du noyau discipliné), tandis que E_split désigné canalise cette énergie vers la cible plutôt que vers une rupture institutionnelle. La quantification de cet antagonisme est développée en S3.

Les lois de Nuremberg (septembre 1935) institutionnalisent la désignation raciale. La *Kristallnacht* (novembre 1938) marque le passage à la violence de masse organisée. La conférence de Wannsee (janvier 1942) planifie la « solution finale ». La défaite militaire de 1945 met fin au régime de l'extérieur — la trajectoire (d) Effondrement progressif n'est pas produite endogènement par le modèle mais imposée par un choc exogène (défaite militaire), ce qui distingue ce cas de WP-T1 où le choc exogène impose γ.

### 1.2 Tableau de codage MEPA Full V6.2 — 9 variables

| Variable | Valeur | Niveau | Source principale | Justification synthétique |
|---|---|---|---|---|
| E_split | 0.75 | Fracture critique | Evans 2003 (S1) ; Kershaw 1998 (S3) | Fracture *réelle* entre factions élitaires weimarien­nes (industriels/militaires/junkers vs républicains). Distinct de la désignation sacrificielle (voir §1.1 Mécanisme 1). |
| **γ** | 0.55 | Cohésion élite modérée-haute | Kershaw 1998 (S3) | Cohésion organisationnelle de l'élite *globale* (NSDAP + Wehrmacht + industrie) après la consolidation 1934. Distinct de γ_local (capacité du seul noyau NSDAP). |
| A_d_eff | 2.5 | Faillite redistributive | Balderston 2002 (S5) | Chômage 30 % en 1932, faillites bancaires, capacité redistributive effondrée. Légère remontée après 1933 (réarmement) mais codage à l'onset de la crise. |
| A_r_c | 0.35 | Répression classique faible | Gellately 2001 (S6) | Gestapo sous-staffée (~7 000 agents / 66 M). Appareil d'État classique insuffisant seul. |
| A_r_ne | 0.70 | Répression non-étatique forte | Gellately 2001 (S6) ; Mallmann & Paul 1994 (S9) | ~80 % des dossiers Gestapo ouverts sur délation spontanée. Mécanisme auto-entretenu. |
| Cs | 0.20 | Crédibilité faible | Evans 2003 (S1) | Crédibilité de la République de Weimar effondrée. Le régime nazi tire sa légitimité de la rupture, pas de la continuité institutionnelle. |
| L(t) | 0.20 | Loyauté faible initiale | Kershaw 1998 (S3) | Loyauté des appareils weimariens faible ; loyauté au NSDAP en construction en 1933. |
| EROI | 13 | Rendement énergétique élevé | Smil 2010 (S2) ; Mitchell 2011 (S10) | Charbon allemand EROI ≈ 13 en 1930s. Capacité industrielle et énergétique robuste — le régime ne s'effondre pas par contrainte énergétique. |
| Sa | 7 | Structure souche | Todd 1990 (S4) | Famille souche (Stammfamilie) dominante en Allemagne — autorité paternelle, transmission inégalitaire, loyauté hiérarchique. Modulateur p6 × 1.5. |

### 1.3 Tableau de codage MEPA Full V7 — 6 variables

| Variable | Valeur | Stade/Bande | Source | Justification synthétique |
|---|---|---|---|---|
| M_r | 2 | Stade 2 — religion zombie | Todd 1990 (S4) ; Todd 2017 (S7) | Protestantisme et catholicisme en transition zombie : effets sociaux résiduels (antijudaïsme sédimenté, structures mentales) sans fonction institutionnelle active. Substrat sur lequel se greffe la matrice séculière raciale. M_r ∈ {1,2} → C1 partiellement satisfaite. |
| μ_m | 0.85 | [0.80–1.00] polarisation maximale | Evans 2003 (S1) ; Kershaw 1998 (S3) | Désignation publique des Juifs comme ennemi racial absolu (lois de Nuremberg 1935, propagande d'État, *Der Stürmer*). Valeur plafond programme. μ_m > 0.60 → C1 satisfaite. ≠ paramètre dynamique μ ≈ 0.38. |
| Φ | 0.30 | [0.20–0.40] monopole dominant | Evans 2003 (S1) ; Décision V7-D1 rev.4 §5.1 | Codé à l'onset 1933 : *Gleichschaltung* en cours, poches symboliques résiduelles (presse confessionnelle, Églises). Valeur pré-enregistrée. Note : grille CONV-E.md cite Allemagne 1935–1945 en [0.00–0.20] (phase consolidée) — distinction onset/consolidation à harmoniser en V7.1. |
| Ψ_noyau | 0.01 | Noyau restreint | NSDAP Parteistatistik 1933 (S8) ; Recensement 1933 (S8) | **Valeur pré-enregistrée** Décision V7-D1 rev.4 §5 : NSDAP ≈ 800 000 membres formels / 66 M = 1,2 %. Exclus : votants NSDAP (~43 %), sympathisants passifs, population sous contrainte post-1934. |
| Ψ_cible | 0.008 | Cible désignée non-null | Recensement juin 1933 (S8) ; Evans 2003 (S1) | Juifs désignés publiquement comme cible démographique unique : ≈ 525 000 / 66 M = 0,008. Désignation raciale, publique, dominante. C3 satisfaite. Cohérent avec μ_m = 0.85 (règle de cohérence : Ψ_cible non-null si μ_m > 0.80). |
| γ_local | 0.55 | [0.40–0.60] organisation structurée | Kershaw 1998 (S3) ; Evans 2003 (S1) | Capacité organisationnelle du *seul* noyau NSDAP : doctrine raciale unifiée, SA structurée, hiérarchie fonctionnelle. ≠ γ V6.2 (cohésion élite globale). Discipline élevée mais base restreinte (Ψ_noyau = 0.01). |

### 1.4 Précheck V7 — Conditions C1–C4 de la branche (α)

```
C1 = (M_r = 2 ∈ {1,2}) AND (μ_m = 0.85 > 0.60)
   = TRUE AND TRUE = TRUE ✓

C2 : σ(Φ = 0.30) = 0.018 × (1 + 1.7 × 0.30)
                  = 0.018 × (1 + 0.51)
                  = 0.018 × 1.51
                  = 0.0272
     Ψ_noyau × γ_local = 0.01 × 0.55 = 0.0055
     C2 = (0.0055 > 0.0272) = FALSE ✗

C3 = (Ψ_cible = 0.008 ≠ null) = TRUE ✓

A_r_c = 0.35 ≤ 0.70 → clause de repli V7-C1 activée :
     A_r_c_eff = A_r_c + 0.5 × A_r_ne
               = 0.35 + 0.5 × 0.70
               = 0.35 + 0.35
               = 0.70
C4 = (A_r_c_eff = 0.70 > 0.70) = FALSE ✗
     [Note : la condition C4 requiert A_r_c_eff > 0.70 strictement.
      A_r_c_eff = 0.70 est à la limite mais ne satisfait pas l'inégalité stricte.]

alpha_precheck = C1 AND C2 AND C3 AND C4
               = TRUE AND FALSE AND TRUE AND FALSE
               = FALSE

→ Branche (α) EXCLUE avant simulation.
→ Rampe mod_mimétique NON activée.
→ Simulation en mode V6.2 standard avec modulateur Sa = 7 (p6 × 1.5).
```

**Résumé précheck** : deux conditions échouent. C2 échoue de façon décisive (0.0055 ≪ 0.0272) — la masse critique organisée est insuffisante selon la définition stricte du noyau. C4 échoue à la limite exacte du seuil. L'échec C2 est **pré-enregistré** par la Décision V7-D1 rev.4 §5 et constitue une limite assumée du cadre V7-α rev. 2.1, documentée en §S3bis et §S3ter.

### 1.5 Conversion des scores en paramètres p1–p13

| Paramètre | Valeur | Dérivation |
|---|---|---|
| p1 (pression


### 1.6 Anomalie documentée


B.3.1 — Énoncé neutre de la divergence
Le modèle V7 a produit la trajectoire (b) Répression réussie alors que la trajectoire attendue était (α) Cristallisation sacrificielle d'État. Cette divergence est robuste sur 11 passes (base + 2 passes N1 optimiste/pessimiste + 8 combinaisons N2), toutes diagnostiquées (b).

B.3.2 — Signature numérique observée

FR_max = 0.3044 · FR_final = 0.1354
t_bascule = null (branche α exclue avant simulation ; F < R sur toute la simulation)
I_min_sim = 2.5 · I_final = 8.2222
C_max = 0.1145 · C_final = 0.0631
S_final = 0.75 · L_final = 0.2999
Robustesse N1 = ROBUSTE · N2 = ROBUSTE (8/8 combinaisons en (b))
Précheck (α) : C1 = vrai, C2 = faux (Ψ_noyau × γ_local = 0.01 × 0.55 = 0.0055 < σ(Φ=0.30) = 0.0272), C3 = vrai, C4 = faux (A_r_c_eff = 0.70, non > 0.70)


B.3.3 — Renvoi à CONV-C pour chantier V8
Cette anomalie est renvoyée à CONV-C pour traitement dans le chantier V8 de révision théorique. Elle ne peut pas être interprétée dans le cadre actuel du modèle.
Le mode d'échec C2 est la limite assumée, pré-enregistrée par la Décision V7-D1 rev. 4 §5.1 et documentée au cadre §2ter.7 ; le chantier V8 est saisi de la question structurelle de la définition stricte du noyau (Ψ_noyau).

B.3.4 — Interdiction explicite d'interprétation alternative
Le présent rapport n'interprète pas le diagnostic divergent comme un résultat empirique valide. Toute interprétation théorique du diagnostic divergent est explicitement interdite par le protocole anti-rationalisation V7-C3.

### 1.7 Hypothèse théorique sous contrainte

L'échec de la condition C2 (Ψ_noyau × γ_local = 0.0055 < σ(Φ=0.30) = 0.0272) reflète une limite structurelle du cadre V7-α rev. 2.1 : la définition stricte du noyau (membres formels NSDAP / population totale = 1,2 %) exclut les acteurs qui participent activement au mécanisme sacrificiel sans appartenir formellement au parti — délateurs volontaires (~80 % des dossiers Gestapo selon Gellately), mobilisation populaire post-1934, bureaucrates alignés. Cette configuration produit une valeur Ψ_noyau structurellement basse pour tout régime dont le mécanisme repose sur l'adhésion tacite de masse plutôt que sur l'adhésion formelle. La direction de résolution candidate, conforme au chantier V7.1 §6 de la Décision V7-D1 rev. 4, est un score continu d'activation de (α) calibré sur la proportion de population activement mobilisée, et non sur l'adhésion formelle.

**Prédiction falsifiable sur WP-I11-1 Grande Terreur soviétique 1937-1938 (cas non encore simulé, à créer conformément au §6 de la Décision V7-D1 rev. 4)** : si ce score continu est calibré sur WP-I10-1 Rwanda + WP-I4-1 Allemagne nazie + WP-I11-1 Grande Terreur soviétique, la prédiction est la suivante — WP-I11-1 devra produire (α) sans ajustement des poids au-delà des tolérances pré-enregistrées (±10 % par poids, ±0.15 sur le seuil, conformément aux Exigences 2 et 3 du §6). Si les poids doivent être ajustés de plus de ±10 % pour produire (α) sur la Grande Terreur après calibration sur les deux cas existants, l'hypothèse est réfutée : le mécanisme sacrificiel sous matrice séculière idéologique ne serait pas capturé par la même structure que sous matrice ethno-raciale, et une reformulation théorique V8 serait requise.

*Cette hypothèse est spéculative. Elle n'interprète pas le diagnostic (b) Répression réussie comme un résultat empirique valide pour le cas Allemagne nazie. Elle relève du chantier V7.1 §6 de la Décision V7-D1 rev. 4 et ne sera testable qu'après création du WP Grande Terreur soviétique et calibration croisée sur trois cas positifs minimum conformément aux Exigences 1-4 du §6.*