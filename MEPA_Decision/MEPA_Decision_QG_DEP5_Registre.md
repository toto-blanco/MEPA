# MEPA — Décision QG : DEP5 — registre des artefacts, opérations destructives, reconstitution

| Champ | Valeur |
|---|---|
| Statut | **Décision QG** — fixe les critères de levée du gate DEP5 |
| Rôle | QG / CONV-C (Architecte Scientifique) — décision prise par Antoine |
| Date | 2026-10-03 |
| Base factuelle | Retours CTO du 2026-10-03 (deux suppressions de `/data/mepa/outputs/` en 24 heures, restauration involontaire d'une whitelist de mars, passeport Rwanda du 25 juin présent sur un seul support) |
| Références | Erratum Certification V7.0 (DEP5, règle de non-suppression) · `MEPA_Decision_QG_Concordance_Decisive_Registre.md` (§5) · DEP3 |

---

## 1. Constat

- Le dossier `/data/mepa/outputs/` a été supprimé deux fois en 24 heures, la seconde fois pendant l'inventaire destiné à traiter la première. Rien n'a été purgé : les fichiers sont dans la corbeille. Aucun run n'a été lancé depuis.
- Une restauration complète de la corbeille a réinstallé dans `scripts/` une whitelist de mars, que le Nœud 2 charge dès qu'elle est présente. DEP3 ne suivait pas ce fichier. Elle a été mise en quarantaine.
- Le dépôt `mepa` ignore `outputs/` : aucun passeport V7 n'y est versionné. Un passeport (Rwanda, run du 25 juin) n'existait que sur le poste local.
- La synchronisation Nextcloud propage les suppressions : elle ne constitue pas un second support au sens de DEP5.

---

## 2. Décisions

### 2.1 Opérations destructives sur le Pi

Toute **suppression, restauration ou déplacement** de fichier sous `/data/mepa` requiert la validation explicite d'Antoine, après présentation de la liste des fichiers concernés. Aucune exception pour les opérations de maintenance ou d'inventaire.

### 2.2 Reconstitution

1. Inventaire préalable du contenu de la corbeille : chemin d'origine, taille, sha256, date. Identification des artefacts de la certification de juin.
2. Restauration de l'historique dans `archives/`, répertoire que le pipeline ne lit jamais.
3. Les 21 WP repartent sur un `outputs/` neuf, organisé par exécution (`{wp_id}/{run_id}/`, `certifies/`) conformément à la décision du 2026-10-03 (§5.1).

### 2.3 Configuration désignée, non découverte

- La couverture de DEP3 est étendue à tout fichier de configuration dont la seule présence modifie le comportement du pipeline.
- Principe pour la proposition d'architecture : la configuration active est désignée explicitement (chemin et empreinte dans le manifeste), jamais découverte par présence d'un fichier.

### 2.4 Second support : dépôt privé `mepa-registre`

Les artefacts de run sont versionnés dans un **dépôt git privé distinct**, `mepa-registre`, hébergé sur GitHub. Le dépôt public `mepa` conserve le code, la configuration et les décisions ; il référence les artefacts du registre par chemin et empreinte.

Supports résultants : le Pi, le clone local du poste, le dépôt distant GitHub.

**Organisation :**

```
mepa-registre/
├── certifies/
│   └── V7.0-P1/{wp_id}/        ← artefacts de la certification V7.0 (juin 2026)
├── runs/{wp_id}/{run_id}/      ← chaque exécution, à partir des 21 WP
└── archives/                   ← historique restauré après inventaire
```

**Règles :**
- **ajout seul** : aucun artefact commité n'est supprimé ni réécrit ; pas de `push --force` ; protection de la branche principale activée lorsque l'hébergeur le permet ;
- **artefact tel que produit** : chaque fichier est versionné dans l'état exact où son producteur l'a écrit ; toute transformation produit un artefact dérivé distinct, avec sa propre empreinte ;
- **pas de secret** : avant chaque commit, contrôle bloquant de l'absence de clé d'API, de jeton ou d'en-tête d'authentification dans les fichiers ;
- **commit en fin d'exécution** : chaque run est commité et poussé automatiquement à sa fin ; à la porte H2, la copie dans `certifies/` fait l'objet d'un commit distinct.

### 2.5 Priorité : les artefacts certifiés de juin

Les artefacts de la certification V7.0 sont versionnés en premier dans `certifies/V7.0-P1/{wp_id}/` : passeport, `result.json`, rapport.
- Contrôle d'intégrité : le sha256 de chaque `result.json` est égal à `hash_integrite.result_json_sha256` de son passeport.
- Les rapports de juin ne peuvent pas être authentifiés par empreinte (`rapport_md_sha256 = null`) ; ils sont versionnés avec la mention « provenance indirecte » (cf. décision Diagnostic R, §5).
- Le passeport Rwanda du 25 juin n'est pas un artefact de certification (la certification repose sur le run du 19 juin, CCI 0.7791). Il est conservé dans `archives/` comme tout artefact de run.

### 2.6 Pièces déjà publiées dans le dépôt public

Les pièces déjà commitées dans `mepa/outputs/mesures/` y restent : leur retrait du dépôt public exigerait une réécriture de l'historique, qui fera l'objet d'une décision distincte si elle est souhaitée. À compter de la présente décision, les nouvelles pièces de mesure sont versionnées dans `mepa-registre`.

Un contrôle d'absence de secret est effectué sans délai sur l'ensemble de l'historique du dépôt public `mepa`. En cas de détection, la clé concernée est révoquée et remplacée avant toute autre action.

### 2.7 Rapport CCI archivé

Le rapport CCI est actuellement réécrit par un nœud JavaScript avant archivage (identique en valeurs, pas en octets). Le passeport doit porter l'empreinte du fichier produit par le calculateur, archivé tel quel. Intrant versé à CV16.

---

## 3. Critères de levée du gate DEP5

Le gate DEP5 est levé lorsque les cinq conditions suivantes sont réunies :

1. les six artefacts certifiés de juin sont versionnés dans `mepa-registre/certifies/V7.0-P1/` et poussés sur le dépôt distant, contrôle d'intégrité passé ;
2. la règle de validation des opérations destructives (§2.1) est en vigueur ;
3. la synchronisation en place sur le Pi ne propage pas les suppressions, ou a été retirée du circuit de sauvegarde ;
4. le commit automatique en fin d'exécution, avec contrôle d'absence de secret, est validé sur un run de validation ;
5. DEP3 couvre les fichiers de configuration agissant par présence (§2.3).

---

*Décision QG (CONV-C) — MEPA V7.0 — 2026-10-03*
