# MEPA V7 — Décision QG : correction trajectoire_attendue WP-C1-1 Haïti

**Statut :** Décision QG actée (rôle CONV-C)
**Origine :** Analyse des 6 passeports V7-γ rev. 2 (cluster pilote), 19 juin 2026
**Objet :** Mise à jour de `trajectoire_attendue` dans `WP-C1-1_Haiti_v7.json`
**Portée :** Une fiche, un champ — pas de modification du runner ni du cadre théorique

---

## 1. Constat

Le run V7-γ rev. 2 sur Haïti produit :
- `trajectoire_diagn`: `(d) Effondrement progressif`
- `trajectoire_attendue`: `(d) Dissolution` (héritée telle quelle de la fiche V6.2)
- `concordance`: **false**
- Mécanique sous-jacente : `t_bascule=null`, `chute_I=0.80>0.5`, `FR_max=0.88<1.2`,
  branche (b) explicative non déclenchée → branche (d) V7-C2 déclenchée correctement,
  annotation EXPLICATIVE.

À première vue, ceci ressemble à un échec de concordance. L'investigation montre
qu'il s'agit d'une étiquette obsolète, pas d'un échec de modèle.

## 2. Analyse — deux définitions historiquement distinctes de "(d)"

Le Manuel de Gouvernance V6.2 (Annexe A) distingue deux labels (d) avec des
conditions structurellement différentes :

| Label V6.2 | Condition |
|---|---|
| (d) Effondrement progressif | `F > R, ΔI_rel > θ_I ET ΔC_rel < θ_C, dC/dt ≈ 0` |
| (d) Dissolution | `F ≥ R, Ref > 0.35 ET Rc+Rn < 0.35` |

**Point clé : `(d) Dissolution` V6.2 exigeait une bascule (F ≥ R).** Ce n'est pas
une variante de l'effondrement sans bascule — conceptuellement c'est proche de
`(e) Réforme institutionnelle` (même condition `Ref>0.35 ET Rc+Rn<0.35`), un cas
de réforme molle insuffisante après franchissement du seuil.

Le bug corrigé par V7-C2 (cadre théorique, Annexe C.1) concernait uniquement
les cas qui *devraient* être en `(d) Effondrement progressif` mais ne basculent
jamais (F reste structurellement sous R), donc tombaient par défaut dans
(h)/(e) en V6.2. **L'Annexe C.1 cite explicitement Haïti 2010-2024 comme
exemple-type de ce bug** : *"les cas théoriquement attendus en (d) — Rome IIIe
siècle, Haïti 2010-2024... ne présentent précisément pas de bascule"*.

## 3. Conclusion

Le résultat V7 sur Haïti (`t_bascule=null`, pas de franchissement F≥R) est
incompatible avec la définition V6.2 de `(d) Dissolution` (qui exige F≥R).
Il correspond exactement à la définition de `(d) Effondrement progressif`
V7-C2 — la branche que le cadre théorique a explicitement conçue pour ce cas.

**Ce n'est pas un échec de concordance, c'est une étiquette V6.2 héritée
devenue incorrecte sous le nouveau cadre V7-C2.** Le modèle V7 reclassifie
correctement Haïti ; c'est la fiche qui n'a pas été mise à jour en conséquence.

## 4. Décision

`trajectoire_attendue` dans `WP-C1-1_Haiti_v7.json` est corrigée :

```json
// Avant
"trajectoire_attendue": "(d) Dissolution"

// Après
"trajectoire_attendue": "(d) Effondrement progressif"
```

Aucune modification du runner, du cadre théorique, ou de `trajectoire_attendue_v62`
(qui reste `"(d) Dissolution"` — c'est la trajectoire attendue historique sous
l'ancien arbre V6.2, valeur de référence à conserver intacte pour traçabilité).

## 5. Portée — ce qui ne change pas

- Rome IIIe (`(d) Effondrement progressif` déjà correct) — non concerné
- Le cadre théorique V7-α rev. 2.1 — aucune modification, le label `(d) Dissolution`
  reste un label officiel valide pour de futurs cas qui rempliraient sa vraie
  condition (bascule + Ref>0.35 + Rc+Rn<0.35), par exemple Liban (cité comme
  cas typique en Annexe A V6.2)
- Le bug `branche_annotation` Égypte (CATCHALL au lieu d'EXPLICATIVE) — distinct,
  traité séparément comme bug pipeline

## 6. Statut épistémique [C1]

Décision actée sur preuve documentaire directe (Annexe A V6.2 + Annexe C.1
cadre V7-α rev. 2.1, qui cite Haïti nommément). Non une recalibration de
paramètres, non un changement de modèle — une correction de métadonnée de
fiche pour refléter une classification théorique déjà spécifiée mais non
encore propagée à la fiche V7.

---

*Décision produite en session QG (rôle CONV-C), 19 juin 2026.*
