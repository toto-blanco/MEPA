# DÉCISION ARCHITECTURALE — Trajectoire (e) Réforme institutionnelle
**Référence :** Anomalie A3 — Audit V6.2 — 2026-03-16  
**Statut :** DÉCISION DOCUMENTÉE — aucun WP à créer en urgence  

---

## 1. Constat de départ

La trajectoire `(e) Réforme institutionnelle` figure dans les 9 labels officiels de `mepa_constants.json` mais est absente comme **trajectoire finale** des 27 WP du corpus principal.

---

## 2. Diagnostic : absence volontaire, non lacune

L'audit des sources primaires confirme que cette absence est **structurelle et délibérée**, documentée à trois niveaux.

### 2.1 — La trajectoire (e) "pure" est dans le corpus EXT, pas dans les 27 WP

Le **WP-EXT-5 (Islande 2008-2013)** est le cas de référence canonique de la trajectoire `(e)` dans MEPA. Sa fiche indique explicitement :

> `trajectoire_attendue : (e) Réforme institutionnelle`  
> `statut : ARCHIVE — Hors corpus V6.2 — Candidat V7 si P5 nécessite cas de contrôle Sa=2`

L'Islande a été **délibérément déplacée hors des 27 WP** lors du passage V6.1 → V6.2 (Mars 2026), remplacée par Haïti 2010-2024 comme ancre contemporaine C1. La trajectoire `(e)` n'a donc pas disparu du système — elle est gérée en catégorie Extension.

### 2.2 — La trajectoire (e) apparaît comme phase intermédiaire dans 3 WP actifs

| WP | Cas | Trajectoire complète |
|---|---|---|
| WP-I3-1 | Japon Meiji—Guerre | (a)→**(e)**→(h)→(d) — 4 phases sur t_max=500 |
| WP-I8-1 | Chine Deng | **(e)**→(h) — seul cas "positif" corpus avec EROI croissant |
| WP-I10-1 | Rwanda | (a)→**(e)** post-génocide — phase 2 reconstruction |

La trajectoire `(e)` est donc bien **modélisée et testée** dans le corpus, mais comme phase de transition, pas comme état final stable. Cela reflète la réalité empirique : les réformes institutionnelles réussies aboutissent rarement à un état d'équilibre durable — elles transitent vers `(h) Stabilité` (Chine Deng) ou régressent (Japon 1930).

### 2.3 — La trajectoire (e) est l'objet de la Proposition P5 du cadre théorique

Le cadre théorique consacre une proposition entière à `(e)` :

> **P5 — Sa nucléaire absolu et trajectoire (e)**  
> Sa nucléaire + A_r_ne < 0.2 + A_i accessible + Q4 ≥ 6/10 → trajectoire (e) avec probabilité ≥ 0.85 si Cs > Cs*.  
> *Test naturel : Islande 2008 (WP-EXT-5). Tests de robustesse : Portugal 2010, Espagne 2010.*

Les cas de contrôle P5 (Portugal, Espagne) sont des WP **prévus mais non produits** dans le cadre théorique étendu (tableau §3.2 du cadre théorique : WP-C4-3 Portugal 1974 → `(a)→(e)`). Ils n'ont pas été retenus dans les 27 WP V6.2 car leur priorité de calibration était moindre.

---

## 3. Décision

### Option retenue : **EXCLUSION DOCUMENTÉE — trajectoire (e) gérée en catégorie EXT**

La trajectoire `(e) Réforme institutionnelle` ne doit **pas** faire l'objet d'un WP supplémentaire dans le corpus V6.2. Motifs :

1. **WP-EXT-5 (Islande) est le cas étalon.** Il est codé, archivé et référencé. Si P5 doit être testée formellement, WP-EXT-5 entre dans le corpus — aucune création ex nihilo nécessaire.

2. **La trajectoire (e) apparaît dans 3 WP actifs** (I3, I8, I10) comme phase intermédiaire documentée. Sa mécanique est calibrée dans le pipeline.

3. **Les 27 WP sont clos par décision d'architecture.** Le Guide Méthodologique V6.2 §1.2 stipule : "Les 27 WP constituent la base empirique du modèle MEPA V6.2 — ce qui est décidé et ne change pas." Ajouter un WP (e) pur déséquilibrerait la stratification sans apport de calibration nouveau.

4. **Les cas candidats (e) "purs" identifiés dans le cadre théorique** (Portugal 1974, Espagne 2010, New Deal américain 1933) sont étiquetés **chantiers V7**, pas V6.2.

---

## 4. Actions à réaliser

### Action 1 — Documenter dans `mepa_constants.json`

Ajouter un champ `$note_trajectoire_e` dans le bloc `labels_trajectoire_d4` :

```json
"labels_trajectoire_d4": {
  "$description": "9 labels officiels D4...",
  "labels": [ ... ],
  "$note_dissolution": "...",
  "$note_trajectoire_e": "(e) Réforme institutionnelle : trajectoire finale absente des 27 WP principaux V6.2 par décision d'architecture. Cas étalon : WP-EXT-5 (Islande 2008). Présente comme phase intermédiaire dans WP-I3 (Japon), WP-I8 (Chine Deng), WP-I10 (Rwanda). Chantier V7 : Portugal 1974 (WP-C4-3), New Deal 1933 (WP-C5-2)."
}
```

### Action 2 — Documenter dans `MEPA_Stratification_Priorite_V6_2.docx`

Ajouter une note de bas de tableau dans la section "Couverture des trajectoires" :

> **Trajectoire (e) — Note :** Absente des 27 WP comme état final. Gérée via WP-EXT-5 (Islande — archive V6.2, candidat V7). Active comme phase intermédiaire dans WP-I3, WP-I8, WP-I10. Aucun WP supplémentaire requis pour V6.2.

### Action 3 — Mettre à jour le Nœud 2 — CONTRAINTES_WP

WP-EXT-5 Islande est la fiche étalon `(e)` — si elle est un jour injectée dans le pipeline (test P5), le Nœud 2 doit la reconnaître. Ajouter dans `CONTRAINTES_WP` du Nœud 2 corrigé :

```javascript
"WP-EXT-5": { cluster: "C4", EROI_min: 30, note: "Islande — cas étalon trajectoire (e). Sa=2 nucléaire absolu. Hors corpus principal V6.2." },
```

---

## 5. Synthèse pour le pipeline

| Niveau | Statut trajectoire (e) |
|---|---|
| `mepa_constants.json` labels | ✅ Présente (9 labels) |
| 27 WP corpus principal — finale | ❌ Absente — **voulu** |
| WP-EXT-5 Islande — finale | ✅ Présente — archivée |
| WP-I3/I8/I10 — intermédiaire | ✅ Présente — calibrée |
| Pipeline n8n — validation C5 | ✅ Reconnue (dans LABELS_D4) |
| Chantier V7 | ✅ Portugal, New Deal, Espagne |

**Conclusion : aucune anomalie. La trajectoire (e) est gérée correctement. L'absence dans les 27 WP comme état final est une décision d'architecture documentée à partir de Mars 2026.**

---

*Décision validée le 2026-03-16 — Audit MEPA V6.2 Fortifiée*
