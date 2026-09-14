# Instruction Claude Code — T1-A : corrections A1 et A6

**Dépôt :** `mepa/`
**Branche :** `test/cv13-recalibration` (branche courante)
**Fichier principal :** `workflow_n8n/mepa_workflow_n8n_V7.json`
**Nature :** deux corrections chirurgicales dans le Nœud 6 + création d'un nouveau fichier sous-workflow

---

## Correction 1 — A1a : max_tokens 4000 → 8192 dans le Nœud 6

**Localisation exacte :** `workflow_n8n/mepa_workflow_n8n_V7.json`
Nœud : `"Nœud 6 — Rédaction LLM CONV-A [Claude T=0] [No-FS]"`
Ligne concernée (dans le `jsCode`) :
```
  max_tokens: 4000,
```

**Correction :**
```
  max_tokens: 8192,
```

**Justification :** un rapport MEPA S1→S7 complet + §1.5 précheck V7 + §1.6 anomalie documentée + §1.7 hypothèse sous contrainte (si divergence) nécessite ~6500 tokens minimum. La valeur 4000 cause la troncature systématique à §1.5 observée sur les 6 WPs pilote. 8192 est la valeur maximale sûre pour claude-sonnet-4-6 et laisse une marge suffisante.

---

## Correction 2 — A1b : rapport_path SKIP → chemin réel dans le Nœud 6

**Localisation exacte :** même nœud, même `jsCode`
Lignes concernées (L212-L217) :
```javascript
try {
  const passeportPath = `/tmp/${wp_id}_passeport.json`;
  execSync(
    `/usr/bin/python3 ${MEPA_SCRIPTS}/mepa_passeport_schema.py ${data.result_path} SKIP SKIP ${passeportPath}`,
    { encoding: "utf8" }
  );
```

**Correction — remplacer ces lignes par :**
```javascript
try {
  const passeportPath = `/tmp/${wp_id}_passeport.json`;
  const rapportTmpPath = `/tmp/${wp_id}_rapport.md`;
  fs.writeFileSync(rapportTmpPath, rapport_md, "utf8");
  execSync(
    `/usr/bin/python3 ${MEPA_SCRIPTS}/mepa_passeport_schema.py ${data.result_path} ${rapportTmpPath} SKIP ${passeportPath}`,
    { encoding: "utf8" }
  );
```

**Justification :** `rapport_md` est disponible dans le scope à ce stade (résolu ligne ~182+). Il était généré mais jamais transmis au schéma — le deuxième argument était littéralement la chaîne `SKIP`, causant `rapport_md_sha256: null` sur tous les passeports et une empreinte composite incomplète.

**Important :** vérifier que `const fs = require("fs")` est déjà importé en tête du jsCode du Nœud 6 (il l'est d'après le code existant — si ce n'est pas le cas, ajouter l'import).

---

## Vérification après corrections A1a + A1b

Avant de committer, exécuter :
```bash
# Vérifier que le JSON reste valide
python3 -c "import json; json.load(open('workflow_n8n/mepa_workflow_n8n_V7.json')); print('JSON valide')"

# Vérifier que les deux changements sont présents
python3 -c "
import json
wf = json.load(open('workflow_n8n/mepa_workflow_n8n_V7.json'))
for node in wf['nodes']:
    if 'Nœud 6' in node.get('name','') and 'CONV-A' in node.get('name',''):
        code = node['parameters']['jsCode']
        assert 'max_tokens: 8192' in code, 'ERREUR: max_tokens non corrigé'
        assert 'rapportTmpPath' in code, 'ERREUR: rapport_path non corrigé'
        assert 'SKIP SKIP' not in code, 'ERREUR: SKIP résiduel trouvé'
        print('Corrections A1a et A1b : OK')
"
```

---

## Nouveau fichier — A6 : sous-workflow audit isolé

**Créer le fichier :** `workflow_n8n/mepa_workflow_n8n_V7_audit_seul.json`

Ce sous-workflow permet de re-lancer l'audit CONV-B (Nœud 6b) sur un rapport modifié sans ré-exécuter l'ensemble du pipeline (CONV-E, runner, etc.).

**Structure attendue :**

```json
{
  "name": "MEPA V7 — Audit Seul (CONV-B isolé)",
  "nodes": [
    {
      "name": "Webhook — Entrée Audit",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "httpMethod": "POST",
        "path": "mepa-audit-seul",
        "responseMode": "lastNode"
      },
      "notes": "Attend en POST : { wp_id, rapport_md (string), result_json (object) }"
    },
    {
      "name": "Noeud AUDIT — CONV-B Post-Rédaction",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "VOIR CI-DESSOUS"
      }
    },
    {
      "name": "Réponse Webhook",
      "type": "n8n-nodes-base.respondToWebhook",
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ $json }}"
      }
    }
  ]
}
```

**jsCode du nœud AUDIT — CONV-B Post-Rédaction :**

Copier le contenu du nœud `"Noeud 6b -- CONV-B Audit Final C1-C5 [Post-Redaction]"` depuis `mepa_workflow_n8n_V7.json`, en adaptant uniquement la source des données d'entrée :

```javascript
// AUDIT SEUL — CONV-B isolé
// Entrée depuis Webhook : { wp_id, rapport_md, result_json }
"use strict";
const https = require("https");
const data = $input.item.json;

const wp_id      = data.wp_id;
const rapport_md = data.rapport_md;          // texte du rapport révisé
const result_json = data.result_json;         // objet JSON du _result.json

// [suite identique au Nœud 6b existant — copier depuis mepa_workflow_n8n_V7.json]
// Le nœud 6b attend data.rapport_md et data.result_data — mapper en conséquence :
// data.result_data = result_json (si le nœud 6b lit data.result_data)
```

**Note d'implémentation :** inspecter le début du jsCode du Nœud 6b pour identifier les noms exacts des champs lus depuis `$input.item.json` (vraisemblablement `rapport_md` et `result_data` ou `sim`). Mapper les champs du webhook sur ces noms. Ne pas copier les dépendances vers des nœuds amont inexistants dans ce sous-workflow.

**Validation du sous-workflow :**
```bash
python3 -c "import json; json.load(open('workflow_n8n/mepa_workflow_n8n_V7_audit_seul.json')); print('JSON valide')"
```

---

## Commits attendus

Deux commits séparés :

**Commit 1 (A1) :**
```
Fix A1 — CONV-A max_tokens 4000→8192 + rapport_md_sha256 non-null (rapport_path SKIP corrigé)
```

**Commit 2 (A6) :**
```
A6 — sous-workflow n8n audit isolé CONV-B (mepa_workflow_n8n_V7_audit_seul.json)
```

---

## Ce que Claude Code ne fait PAS dans cette instruction

- Ne pas modifier `mepa_passeport_schema.py` — le schéma Python gère déjà correctement le `rapport_path` optionnel ; le problème était uniquement dans l'appel n8n.
- Ne pas modifier `mepa_node2_audit_v7.js` — hors scope de T1-A.
- Ne pas modifier `CONV-A.md` — l'ajout des sections §1.6/§1.7 automatiques (amélioration A2) est un chantier séparé.
- Ne pas toucher aux fiches WP ni aux passeports existants.

---

*Instruction QG (CONV-C), juin 2026 — T1-A corrections A1+A6, pipeline V7 pré-run 21 WPs.*
