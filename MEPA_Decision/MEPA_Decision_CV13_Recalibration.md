# MEPA — Décision CV13 · Recalibration paramétrique (Option A vs B)

**Statut :** Décision d'architecture (rôle CONV-C / QG) — soumise à revue collégiale
**Origine :** Diagnostic post-run 27 WP (baseline V6.2) — 25/27 concordances false
**Objet :** Choisir et exécuter la stratégie de recalibration du modèle pour permettre
           aux trajectoires de rupture (a) et d'effondrement (d) d'émerger de la simulation
**Périmètre :** `mepa_constants.json` (Option A) ou `mepa_runner_v2_gamma.py` (Option B)
**Urgence :** Bloque la certification du corpus V6.2 — à trancher avant tout nouveau run

---

## 1. Constat diagnostique — les données du run baseline

Le run complet des 27 WP a produit :
- **0/27 WP_CERTIFIÉ** (concordance false sur 25 WP, CCI < 0.65 sur 6 WP)
- **2 trajectoires dominantes** sur 9 possibles : `(b) Répression réussie` (16 WP)
  et `(h)/(e) Stabilité ou réforme lente` (11 WP)
- **Robustesse : 27/27 ROBUSTE** — le codage est stable, le modèle est stable,
  les divergences ne viennent pas du bruit

Ce n'est **pas** un problème de codage. Sur les 3 WPs-tests diagnostiqués
(F1-1 Rome IIIe, F2-1 Rome tardive, I2-1 Russie 1917), les CCI sont
excellents (0.97, 0.58, 0.98) et les valeurs de commande sont bien codées.
La divergence est **structurelle** : les plages de F(t) et R(t) ne se
chevauchent pas avec les paramètres actuels.

---

## 2. Analyse structurelle des équations

### 2.1 Plancher de R dominé par I_min

```
R(t) = I(t)^(1/3) + ν×(Rc+Rn)×ℓ + ρ
```

Avec `I_min = 0.3` (fallback runner), même lors d'un effondrement institutionnel
complet, R reste à :

```
R_min = 0.3^(1/3) + termes_faibles + ρ ≈ 0.669 + 0.06 = 0.73
```

Ce plancher est **structurellement supérieur au plafond de F** pour tous
les cas d'effondrement lent (faible γ, faible E).

### 2.2 Plafond de F limité par λ et μ

```
F(t) = C(t) + λ × L(t) × (1 + μ × γ × E)
```

Avec λ=0.68, μ=0.38, même dans le cas de mobilisation maximale du corpus
(Russie 1917 : γ=0.83, E=0.88) :

```
F_max ≈ 0.28 + 0.68 × 0.44 × (1 + 0.38×0.83×0.88) ≈ 0.64
```

R pour Russie 1917 à t=300 reste à 1.02. Écart : **0.38 — non franchissable**.

### 2.3 Synthèse des plages observées

| Trajectoire attendue | F plafond observé | R plancher observé | Franchissement possible ? |
|---|---|---|---|
| (a) Rupture (γ>0.6, E>0.6) | ~0.64–0.70 | ~1.02–1.32 | **Non** avec paramètres actuels |
| (d) Effondrement (EROI→0) | ~0.25–0.35 | ~0.73–0.90 | **Non** — plancher R trop haut |
| (b) Répression (Rc élevé) | ~0.34 | ~1.10 | Non requis — F<R correct |
| (h)/(e) Stabilité | ~0.25–0.35 | ~0.75–1.20 | Non requis — F<R correct |

---

## 3. Les deux options

### Option A — Recalibration paramétrique (mepa_constants.json)

Modifier trois paramètres dans `mepa_constants.json` sans toucher au runner :

| Paramètre | Valeur actuelle | Cible proposée | Effet |
|---|---|---|---|
| `I_min` | 0.30 | ~0.15 | Abaisse le plancher de R lors des effondrements |
| `λ` (lam) | 0.68 | ~0.85 | Monte le plafond de F pour les cas de forte mobilisation |
| `μ` (mu) | 0.38 | ~0.55 | Amplifie le terme γ×E dans F — critique pour les ruptures (a) |

**Avantages :** ne touche pas aux équations, testable avec le harnais existant,
réversible, rapide à tester via Claude Code.

**Risques :** sur-ajustement si on cherche à maximiser la concordance —
voir §4 sur le critère de calibration indépendant.

**Contrainte dure :** les 2 WPs déjà concordants (C2 Égypte, I6 Tiananmen)
**ne doivent pas diverger** après recalibration. Vérifié par le harnais.

### Option B — Chemin architectural pour (d) (mepa_runner_v2_gamma.py)

Ajouter un chemin conditionnel dans le runner : si ΔI_rel > θ_I **ET**
EROI_final < seuil_critique, diagnostiquer `(d) Effondrement progressif`
**sans** bascule F>R obligatoire.

**Avantages :** conceptuellement plus juste — Rome s'effondre parce que
les institutions s'érodent, pas parce que la pression sociale les dépasse.
Cohérent avec ce que le runner V7 Track A a introduit (branche sans bascule).

**Risques :** modifie le runner (fichier à ne toucher qu'avec preuve [C3]),
nécessite une validation complète sur les 27 WP, potentiellement ouvre
des effets de bord non prévus sur d'autres branches de l'arbre.

**Contrainte :** toute modification du runner doit passer le harnais
complet (76 tests, 29 golden) avant d'être considérée valide.

---

## 4. Critère de calibration indépendant — garde-fou anti-sur-ajustement

**Règle fondamentale [C1] :** on ne calibre pas pour maximiser la concordance.
On fixe les valeurs cibles par un critère **indépendant des trajectoires attendues**,
puis on observe combien de concordances émergent naturellement.

Le critère indépendant proposé est géométrique :

> **Les plages [F_min, F_max] et [R_min, R_max] doivent se chevaucher
> sur au moins 20% de leur étendue combinée pour les WPs à codage fort
> (γ > 0.60 ET E > 0.60).**

Ce critère ne regarde pas quels WPs ont quelle trajectoire attendue.
Il regarde uniquement si la mécanique du modèle *permet* l'existence
de bascules pour les configurations de forte mobilisation. Satisfaire
ce critère ne garantit pas que tel ou tel WP sera concordant — ça garantit
que le modèle n'est pas structurellement aveugle aux ruptures.

**WPs à codage fort (γ > 0.60 ET E > 0.60) dans le corpus :**
I2-1 Russie (γ=0.83, E=0.88), F7-1 Révolution haïtienne, I10-1 Rwanda,
I4-1 Allemagne nazie — les cas où une rupture est historiquement certaine.
Si après recalibration ces 4 WPs ne franchissent toujours pas,
la recalibration paramétrique est insuffisante → basculer vers Option B.

---

## 5. Protocole de test (à confier à Claude Code)

**Mission CV13-test :**

```
1. Créer branche : git checkout -b test/cv13-recalibration

2. Dans mepa_constants.json, modifier :
   - bornes_parametres_dynamiques.I_min.defaut : 0.30 → 0.15
   - lambda (lam) : 0.68 → 0.85
   - mu : 0.38 → 0.55
   (NE PAS modifier les bornes min/max, seulement les défauts)

3. Lancer le harnais complet :
   pytest tests/ -v
   CRITÈRE OBLIGATOIRE : 0 régression sur les 29 golden existants
   Si golden changent sur C2 ou I6 → STOP, recalibration trop agressive

4. Sur les 4 WPs à codage fort (I2, F7, I10, I4) :
   lancer le runner manuellement et relever F_max et FR_max
   → F franchit-il R ? À quel t ?

5. Sur l'ensemble des 27 WPs : relever les nouvelles trajectoires
   Ne pas chercher à maximiser la concordance — observer honnêtement

6. Produire un rapport :
   - Nombre de WPs concordants (avant : 2, après : ?)
   - Les 4 WPs à codage fort franchissent-ils ?
   - Les 2 WPs déjà concordants le restent-ils ?
   - Effets de bord non prévus ?

7. NE PAS merger sur main — attendre validation QG
```

**Si le rapport montre ≥ 8/27 concordances honnêtes** (sans sur-ajustement) :
Option A est suffisante → rédiger V6.4 avec ces valeurs.

**Si les 4 WPs à codage fort ne franchissent toujours pas** :
Option A insuffisante → instruire Option B (chemin architectural (d)).

---

## 6. Décisions à trancher (points collégials)

**CV13-A :** Valider les trois valeurs cibles pour le test
(I_min=0.15, λ=0.85, μ=0.55) — ou proposer des valeurs alternatives.

**CV13-B :** Valider le critère de calibration indépendant
(chevauchement géométrique F/R sur WPs à codage fort γ>0.60/E>0.60).

**CV13-C :** Valider le seuil de décision post-test :
≥ 8/27 concordances honnêtes → Option A suffisante.

**CV13-D :** Confirmer l'ordre de priorité :
Option A d'abord (moins risquée), Option B seulement si A insuffisante.

---

## 7. Ce qui ne change pas pendant le test

- Les 27 fiches WP (`config/WP-*.json`) — données scientifiques intactes
- Les instructions CONV-E/A/B — le codage reste le même
- Le workflow n8n — pas de nouveau run pendant le test
- Le harnais de non-régression — c'est lui qui valide le test

---

## 8. Statut épistémique [C1]

- **Diagnostic structurel** (§2) : fait établi sur données réelles (3 result.json analysés,
  plages F/R calculées algébriquement depuis les équations). Non hypothèse.
- **Valeurs cibles** (I_min=0.15, λ=0.85, μ=0.55) : proposition testable,
  **pas encore validées**. À confirmer par le test CV13-test.
- **Critère de calibration indépendant** : choix méthodologique de QG,
  soumis à validation collégiale.
- **Option B** : non encore instruite formellement. À ouvrir uniquement si
  Option A se révèle insuffisante après test.

Rien n'est acté ici sauf l'instruction de test.
CV13 est instruite, pas tranchée — le test décide.

---

*Décision CV13 produite en session QG (rôle CONV-C).
Origine : diagnostic post-run baseline 27 WP V6.2.
Cause racine : séparation structurelle des plages F(t) et R(t).
Deux options identifiées ; Option A testable immédiatement via Claude Code.
Le test, non l'anticipation, tranche entre A et B.*
