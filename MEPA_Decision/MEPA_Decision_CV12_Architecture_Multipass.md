# MEPA — Décision CV12 · Architecture du multipass (séparation codage / rédaction)

**Statut :** Décision d'architecture (rôle CONV-C / QG) — soumise à revue collégiale
**Origine :** Question de coût remontée par la conversation n8n (optimisation des appels LLM)
**Objet :** Séparer la phase de codage (répétée) de la phase de rédaction/audit-de-rapport (unique), sans altérer la définition du CCI.
**Périmètre :** V6.2 — n'affecte ni les équations, ni les paramètres, ni les trajectoires (runner déterministe inchangé).
**Impact :** Séquenceur n8n + note méthodologique du passeport + Addendum Théorique Pilier 1.

---

## 1. Le constat de départ (correct)

La conversation n8n a identifié, à juste titre, une redondance coûteuse dans le multipass actuel :

- Le **runner est déterministe** : à paramètres d'entrée identiques, les N passes produisent des trajectoires bit-identiques (c'est le critère de non-régression lui-même). Rejouer la simulation N fois n'apporte rien.
- **CONV-A rédige N rapports quasi identiques** à partir d'un codage qui ne change pas la trajectoire. Coûteux et sans valeur ajoutée.
- **CONV-B audite N fois le même rapport.**

Le diagnostic économique est juste : la rédaction et l'audit-de-rapport n'ont aucune raison d'être répétés. Le gain en tokens est réel.

## 2. L'approximation à corriger

La proposition initiale — « N passes CONV-E uniquement → CCI agrégé » — contient une erreur sur la **nature du CCI**.

Le CCI de MEPA n'est pas la variance d'un codeur qui rejoue. C'est l'**accord inter-codeurs entre deux agents indépendants** : CONV-E (codeur) et CONV-B (codeur indépendant en double aveugle). Formellement, ICC(3,1) two-way mixed consistency entre E et B (Shrout & Fleiss 1979, documenté dans le passeport et l'Addendum Théorique Pilier 1).

Remplacer « accord E vs B » par « variance de E sur N tirages » changerait la **métrique mesurée** :

| Métrique | Ce qu'elle teste | Statut dans MEPA |
|---|---|---|
| ICC(E, B) — actuel | Reproductibilité inter-codeurs (deux agents indépendants s'accordent-ils ?) | Définition de certification V6.2 |
| Variance de E sur N passes | Stabilité intra-codeur (un agent est-il constant ?) | **Métrique différente — non équivalente** |

La proposition « N codages E seuls » mesurerait la seconde, alors que la certification repose sur la première. Ce n'est pas applicable sans redéfinir ce que « certifié » veut dire.

## 3. L'architecture corrigée

La distinction valide n'est pas « codage vs simulation » mais **codage (à répéter) vs rédaction-et-audit-de-rapport (unique)**. Et la répétition du codage doit rester **double** (E + B) pour préserver le CCI.

```
Par WP :
  ── PHASE CODAGE (répétée N fois) ──────────────────────────────
  N passes × { CONV-E codage indépendant + CONV-B codage indépendant }
           → N paires (E_i, B_i), i = 1..N
           → double aveugle préservé à chaque passe

  ── CONSOLIDATION (1 calcul) ───────────────────────────────────
  CCI agrégé sur les N paires (E_i, B_i)
           → codage consolidé (médiane ou moyenne par variable)
           → CCI statistiquement plus robuste que le mono-passe actuel

  ── PHASE RÉDACTION (1 seule fois) ─────────────────────────────
  1 × simulation (déterministe, sur le codage consolidé)
  1 × CONV-A rédaction (sur codage consolidé + simulation)
  1 × CONV-B audit-du-rapport (sections S1-S7, narrative smoothing)
           → passeport
```

**Distinction essentielle à acter :** CONV-B joue **deux rôles distincts** qu'il faut séparer conceptuellement.
- **CONV-B codeur** (phase codage) : second codage indépendant, participe au CCI, répété N fois.
- **CONV-B auditeur-de-rapport** (phase rédaction) : audit des 7 sections du WP rédigé, contrôle anti-narrative-smoothing (C1-C5), une seule fois.

Ces deux rôles sont déjà distincts dans le pipeline actuel (Nœud 8a = codage CCI ; Nœud 7 = audit rapport). Le multipass actuel les répète tous les deux ; l'architecture corrigée ne répète que le premier.

## 4. Ce que ça préserve et ce que ça améliore

**Préserve :**
- La définition du CCI (accord E/B) — inchangée.
- Le double aveugle — chaque passe garde E et B indépendants.
- Le déterminisme du runner — la simulation tourne sur le codage consolidé, une fois.
- La rétrocompatibilité bit-identique — le runner et les équations ne sont pas touchés.

**Améliore :**
- **Robustesse statistique du CCI** : N paires (E,B) au lieu d'une seule. Le CCI agrégé sur N codages indépendants est statistiquement plus solide qu'un CCI mono-passe. C'est un gain de qualité, pas seulement de coût.
- **Coût** : la rédaction CONV-A + l'audit-rapport CONV-B (les appels les plus lourds en tokens, ~14k) ne sont payés qu'une fois par WP au lieu de N fois.

**Gain réel (corrigé) :** moins que le ÷7 initialement annoncé (puisqu'on conserve N codages doubles, qui ont un coût), mais substantiel — on élimine (N−1) rédactions + (N−1) audits-de-rapport. Pour N=3 passes : on passe de 3 rédactions à 1, de 3 audits-rapport à 1, tout en gardant 3 paires de codage. Le chiffrage précis revient à la conversation n8n.

## 5. La décision à trancher (point collégial)

**CV12 — Le CCI de certification est-il calculé sur N paires (E,B) agrégées, ou sur une paire unique ?**

- **Option A (statu quo)** : CCI mono-passe, une paire (E,B) par WP. Simple, mais statistiquement fragile (un seul tirage).
- **Option B (recommandée)** : CCI agrégé sur N paires (E,B). Plus robuste, et permet la séparation codage/rédaction qui réduit le coût.

Si Option B est retenue, deux mises à jour documentaires sont requises (discipline [C1]) :
1. **Note méthodologique du passeport** : préciser que le CCI est agrégé sur N codages indépendants, avec la méthode d'agrégation (médiane par variable recommandée — robuste aux outliers de codage).
2. **Addendum Théorique Pilier 1** : mettre à jour la définition du CCI pour refléter l'agrégation multi-passes. La formule ICC(3,1) reste, mais appliquée sur l'ensemble consolidé.

**Point de vigilance épistémique :** la méthode d'agrégation du codage consolidé (médiane vs moyenne) doit être fixée et documentée. La médiane est recommandée — elle résiste à un codage aberrant sur une passe, là où la moyenne le laisse contaminer le consolidé. C'est un choix à acter, pas à laisser au câblage.

## 6. Ce qui ne relève PAS de cette décision (câblage n8n)

Pour mémoire, et sans empiéter sur la conversation n8n : les optimisations de coût sans effet sur la métrique (prompt caching, dégraissage des payloads, Batch API) sont du câblage pur et ne requièrent aucune décision collégiale. Une seule réserve technique transmise : le dégraissage du payload CONV-A doit **conserver le bloc `stress_n2`** (diagnostics de stress), ne filtrer que les séries temporelles brutes — c'est le champ qui manquait sur WP-C1-1.

## 7. Impact sur le séquenceur

Si CV12 Option B est actée, le séquenceur (`mepa_workflow_n8n_V62_sequencer.json`) doit être ajusté par la conversation n8n :
- La boucle interne d'un WP passe de « N × (codage + simulation + rédaction + audit) » à « N × codage double, puis 1 × (consolidation + simulation + rédaction + audit) ».
- Le `multipass_log.json` doit logguer le CCI agrégé (et idéalement la dispersion inter-passes, indicateur de stabilité du codage).
- Aucune modification des scripts de production (`runner`, `kappa_calculator`, `passeport_schema`) n'est requise côté logique — mais `kappa_calculator` devra recevoir N paires au lieu d'une. À vérifier : accepte-t-il déjà une liste de codages, ou faut-il l'appeler N fois puis agréger en aval ? (question câblage, pas architecture).

---

## 8. Statut épistémique [C1]

- **Constat de déterminisme du runner** : fait établi (critère de non-régression).
- **Définition du CCI comme accord E/B** : consensus documenté (Addendum Pilier 1, passeport).
- **Robustesse accrue du CCI multi-passes** : hypothèse méthodologique solide (N tirages > 1 tirage), à confirmer empiriquement sur les premiers WP.
- **Choix médiane vs moyenne** : décision à trancher, non encore actée.
- **Option B comme nouvelle définition de certification** : proposition de QG, requiert validation collégiale + mise à jour documentaire avant déploiement.

Rien n'est acté ici. CV12 est instruite, pas tranchée — la revue collégiale décide.

---

*Décision CV12 produite en session QG (rôle CONV-C). Réponse à une question de coût remontée par la conversation n8n. Préserve la définition du CCI ; améliore sa robustesse ; sépare codage (répété) et rédaction (unique). Soumise à revue collégiale avant déploiement.*
