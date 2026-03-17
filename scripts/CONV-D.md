# CONV-D — Passeport Compact MEPA V6.2
**Statut :** Format de sortie (non une conversation active)  
**Généré par :** `mepa_passeport_schema.py` via Nœud 15  
**Correctif :** A9 — 2026-03-16

---

## Rôle

CONV-D n'est **pas une conversation interactive**. C'est le nom du **format de sortie archivé** par le Nœud 15 à la fin du pipeline. Le "passeport compact" est un JSON ≤ 500 caractères destiné à :

- Permettre une identification rapide d'un WP certifié dans les archives
- Servir de référence de comparaison inter-WP (cluster, trajectoire, statut)
- Alimenter d'éventuels dashboards ou exports CSV du corpus MEPA

---

## Structure JSON obligatoire

```json
{
  "$schema":       "mepa-passeport-v2.0",
  "generated_at":  "2026-03-16",
  "identite": {
    "wp_id":   "WP-C1-1",
    "cas":     "Haïti — Crise post-séisme 2010-2024",
    "cluster": "C1"
  },
  "certification": {
    "cci":           0.82,
    "verdict_cci":   "BON",
    "statut_nc":     "OK",
    "date_certification": "2026-03-16"
  },
  "simulation": {
    "traj":         "(d) Dissolution",
    "robustesse":   "ROBUSTE",
    "concordance":  true
  },
  "statut_global": {
    "code":  "WP_CERTIFIE",
    "label": "Certifié — pipeline complet validé"
  }
}
```

---

## Valeurs autorisées

**`verdict_cci`** : `"EXCELLENT"` (≥0.90) | `"BON"` (≥0.75) | `"PASSABLE"` (≥0.60) | `"INSUFFISANT"` (<0.60)

**`statut_global.code`** : `"WP_CERTIFIE"` | `"WP_EXPLORATOIRE"` | `"INCOMPLET"`

**`robustesse`** : `"ROBUSTE"` | `"METASTABLE"` | `"SENSIBLE"` | `"NON_CALCULE"`

---

## Différence avec le passeport complet

`mepa_passeport_schema.py` produit deux sorties :

| Sortie | Taille | Usage |
|---|---|---|
| Passeport compact (CONV-D) | ≤ 500 chars | Archivage index, dashboards |
| Passeport complet | ~2-5 Ko | Annexe S7 du WP, audit CONV-B |

---

## Chemin d'archivage

```
/data/mepa/outputs/{cluster}/{wp_id}/
  ├── {wp_id}_rapport.md          ← Nœud 7
  ├── {wp_id}_result.json         ← Nœud 7
  ├── {wp_id}_passeport.json      ← Nœud 15 (complet)
  └── {wp_id}_passeport_compact.json  ← Nœud 15 (CONV-D)
```

---

## Note architecturale

Le terme "CONV-D" est hérité de l'Architecture Conversations V6.2 qui réserve les identifiants CONV-A (rédacteur), CONV-B (auditeur), CONV-E (codeur) aux rôles conversationnels actifs. CONV-D désigne historiquement le "Destinataire" — le format de livraison finale, pas un interlocuteur.
