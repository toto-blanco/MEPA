# ADDENDUM — Clarification Label `[No-FS]`
**Document :** Complément à MEPA_V6_2_Schema_Directeur_Architecture  
**Correctif :** A7 — 2026-03-16

---

## Définition officielle révisée

> **`[No-FS]` signifie :** le nœud ne persiste **pas la fiche JSON source** sur le disque du système NextCloud/hôte. Il peut utiliser `/tmp/` pour les fichiers intermédiaires de calcul et `require('fs')` de manière transitoire.

Ce label **ne garantit pas** l'absence totale d'accès filesystem — il garantit la **compatibilité avec les instances n8n sans montage NextCloud permanent**.

---

## Tableau de comportement réel par nœud

| Nœud | Label | `require('fs')` | Écrit sur disque | Répertoire |
|---|---|---|---|---|
| Nœud 2 — Audit | [No-FS] | Oui (CONSTANTS) | Non | — |
| Nœud 3 — Write config | [No-FS] | Non | Oui | `/tmp/` |
| Nœud 4 — Runner | [No-FS] | Non | Via script Python | `/tmp/` |
| Nœud 4b — Sensibilité | [No-FS] | Non | Via script Python | `/tmp/` |
| Nœud 5 — Parse | [No-FS] | Non | Non | `/tmp/` (lecture) |
| Nœud 5b — Parse N1 | [No-FS] | Non | Non | `/tmp/` (lecture) |
| Nœud 6 — LLM | [No-FS] | Non | Non | — |
| Nœud 7 — Export | [No-FS] | Oui | Oui | `/data/mepa/outputs/` |
| Nœud 8a — CCI | — | Oui | Via script Python | `/tmp/` |
| Nœud 12 — Stress N2 | — | Oui | Via script Python | `/tmp/` |
| Nœud 15 — Archivage final | — | Oui | Oui | `/data/mepa/outputs/` |

---

## Prérequis de déploiement

Les nœuds écrivant dans `/data/mepa/outputs/` (Nœud 7, Nœud 15) **nécessitent** ce volume monté en Docker :

```yaml
# docker-compose.yml — extrait
volumes:
  - /chemin/local/mepa/outputs:/data/mepa/outputs
  - /chemin/local/mepa/scripts:/data/mepa/scripts
```

Les nœuds écrivant dans `/tmp/` fonctionnent sans montage externe (filesystem temporaire du conteneur n8n).

---

## Variables d'environnement requises

Toutes doivent être définies dans les Settings n8n → Environment Variables :

| Variable | Valeur par défaut | Obligatoire |
|---|---|---|
| `MEPA_SCRIPTS_DIR` | `/data/mepa/scripts` | Oui |
| `MEPA_OUTPUT_DIR` | `/data/mepa/outputs` | Oui |
| `MEPA_CONSTANTS_JSON` | _(contenu JSON de mepa_constants.json)_ | Recommandé |
| `ANTHROPIC_API_KEY` | _(clé API)_ | Oui |
