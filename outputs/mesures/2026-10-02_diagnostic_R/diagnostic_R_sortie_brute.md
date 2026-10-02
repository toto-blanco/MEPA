# Diagnostic R — sortie brute (sans interprétation)

Référence : Décision QG 2026-09-30 §5 et message QG (séries A et B). Méthode et empreintes : `diagnostic_R_resultats.json`.

- **Origine** : R archivé dans le `result.json` de juin (reproduction au bit près vérifiée sur les 9 blocs).
- **Série A** : R = A_d_eff / 10, A_d_eff relevé dans les rapports de juin (provenance indirecte).
- **Série B** : R = A_d_eff / 10, A_d_eff relevé dans les rapports du 3 juillet (authentifiés par empreinte).

## Grandeurs principales

| WP | Exécution | A_d_eff | R | Trajectoire | Robustesse N1 | C_max | FR_max | t_bascule |
|---|---|---|---|---|---|---|---|---|
| WP-I10-1 | Origine | — | 0.15 | (α) Cristallisation sacrificielle d'État | ROBUSTE | 1.6587 | 1.7601 | 7 |
| WP-I10-1 | Série A | 1.5 | 0.15 | (α) Cristallisation sacrificielle d'État | ROBUSTE | 1.6587 | 1.7601 | 7 |
| WP-I10-1 | Série B | 1.5 | 0.15 | (α) Cristallisation sacrificielle d'État | ROBUSTE | 1.6587 | 1.7601 | 7 |
| WP-I4-1 | Origine | — | 0.3 | (b) Répression réussie | ROBUSTE | 0.1145 | 0.3044 | None |
| WP-I4-1 | Série A | 2.5 | 0.25 | (b) Répression réussie | ROBUSTE | 0.1218 | 0.3118 | None |
| WP-I4-1 | Série B | 2.5 | 0.25 | (b) Répression réussie | ROBUSTE | 0.1218 | 0.3118 | None |
| WP-F10-1 | Origine | — | 0.2 | (b) Répression réussie | ROBUSTE | 0.1639 | 0.2908 | None |
| WP-F10-1 | Série A | 3.5 | 0.35 | (b) Répression réussie | ROBUSTE | 0.1338 | 0.269 | None |
| WP-F10-1 | Série B | 3.5 | 0.35 | (b) Répression réussie | ROBUSTE | 0.1338 | 0.269 | None |
| WP-F1-1 | Origine | — | 0.3 | (d) Effondrement progressif | MÉTASTABLE | 0.11 | 0.2933 | None |
| WP-F1-1 | Série A | 4.5 | 0.45 | (d) Effondrement progressif | ROBUSTE | 0.1051 | 0.2893 | None |
| WP-F1-1 | Série B | 4.5 | 0.45 | (d) Effondrement progressif | ROBUSTE | 0.1051 | 0.2893 | None |
| WP-C1-1 | Origine | — | 0.15 | (d) Effondrement progressif | ROBUSTE | 0.2842 | 0.8893 | None |
| WP-C1-1 | Série A | 1.4 | 0.14 | (d) Effondrement progressif | ROBUSTE | 0.2875 | 0.8987 | None |
| WP-C1-1 | Série B | 1.4 | 0.14 | (d) Effondrement progressif | ROBUSTE | 0.2875 | 0.8987 | None |
| WP-C2-1 | Origine | — | 0.25 | (b) Répression réussie | MÉTASTABLE | 0.146 | 0.3139 | None |
| WP-C2-1 | Série A | 3.8 | 0.38 | (b) Répression réussie | MÉTASTABLE | 0.1213 | 0.2787 | None |
| WP-C2-1 | Série B | 3.5 | 0.35 | (b) Répression réussie | MÉTASTABLE | 0.1262 | 0.2828 | None |

## Stress N1 et N2 (trajectoire par perturbation)

### WP-I10-1

| Exécution | N1 optimiste | N1 pessimiste | E+0.1 | E-0.1 | R+0.08 | R-0.08 | EROI+0.5 | EROI-0.5 | Rc+0.1 | Rc-0.1 |
|---|---|---|---|---|---|---|---|---|---|---|
| Origine | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État |
| Série A | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État |
| Série B | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État | (α) Cristallisation sacrificielle d'État |

### WP-I4-1

| Exécution | N1 optimiste | N1 pessimiste | E+0.1 | E-0.1 | R+0.08 | R-0.08 | EROI+0.5 | EROI-0.5 | Rc+0.1 | Rc-0.1 |
|---|---|---|---|---|---|---|---|---|---|---|
| Origine | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie |
| Série A | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie |
| Série B | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie |

### WP-F10-1

| Exécution | N1 optimiste | N1 pessimiste | E+0.1 | E-0.1 | R+0.08 | R-0.08 | EROI+0.5 | EROI-0.5 | Rc+0.1 | Rc-0.1 |
|---|---|---|---|---|---|---|---|---|---|---|
| Origine | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie |
| Série A | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie |
| Série B | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie |

### WP-F1-1

| Exécution | N1 optimiste | N1 pessimiste | E+0.1 | E-0.1 | R+0.08 | R-0.08 | EROI+0.5 | EROI-0.5 | Rc+0.1 | Rc-0.1 |
|---|---|---|---|---|---|---|---|---|---|---|
| Origine | (d) Effondrement progressif | (b) Répression réussie | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif |
| Série A | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif |
| Série B | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif |

### WP-C1-1

| Exécution | N1 optimiste | N1 pessimiste | E+0.1 | E-0.1 | R+0.08 | R-0.08 | EROI+0.5 | EROI-0.5 | Rc+0.1 | Rc-0.1 |
|---|---|---|---|---|---|---|---|---|---|---|
| Origine | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif |
| Série A | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif |
| Série B | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif | (d) Effondrement progressif |

### WP-C2-1

| Exécution | N1 optimiste | N1 pessimiste | E+0.1 | E-0.1 | R+0.08 | R-0.08 | EROI+0.5 | EROI-0.5 | Rc+0.1 | Rc-0.1 |
|---|---|---|---|---|---|---|---|---|---|---|
| Origine | (b) Répression réussie | (d) Effondrement progressif | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (d) Effondrement progressif | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie |
| Série A | (d) Effondrement progressif | (b) Répression réussie | (b) Répression réussie | (d) Effondrement progressif | (d) Effondrement progressif | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (d) Effondrement progressif | (b) Répression réussie |
| Série B | (d) Effondrement progressif | (b) Répression réussie | (b) Répression réussie | (d) Effondrement progressif | (d) Effondrement progressif | (b) Répression réussie | (b) Répression réussie | (b) Répression réussie | (d) Effondrement progressif | (b) Répression réussie |

## Entrées

| WP | sha256 rapport juin | A_d_eff juin | sha256 rapport juillet | A_d_eff juillet |
|---|---|---|---|---|
| WP-I10-1 | `6e97cb1a6ea6b1fc1f0e99f67efcf0d0df32ef35a3cd86dac7e713037ab91a43` | 1.5 | `5d6d6c566f7c0b6c6c5c7c8b821f2b2177688d9d1d1a90951dd6724a173e06a2` | 1.5 |
| WP-I4-1 | `d16e4ff975014b340330a46b0bd577fe4931fa51825400b719b00a2255724670` | 2.5 | `648b57d2c5c0c65fddec5a595069818680d4ae6c8e5c1e16ad20e3376edf1101` | 2.5 |
| WP-F10-1 | `d0f8ca389d14397e83aac0b0a21cf1251aea077b8f1fdba6ed14e587663c87c6` | 3.5 | `fe697117cc874ba32c69f92908baef656fbdaa5371bc4a5c2ff591fc64db49e2` | 3.5 |
| WP-F1-1 | `8a7f7d47c51358af499e2f06b519e9c5d920c8bfd04325efbc296f979f088480` | 4.5 | `9ea09ff6d1a1bc65a22f9b1515f5af24ef818599c96b5973259afafcc5ac34ee` | 4.5 |
| WP-C1-1 | `9674a6c06eda496d02979fe5c7c3d18745e6bbbacc3ec5ff2b9d35c8773f094b` | 1.4 | `528daad1ccb9d207d83cdf40ebab8d3e25e27ca1136b9e65ba3217e45115b6d0` | 1.4 |
| WP-C2-1 | `f81bdc7d61a890b60f19556c1d68cc8fb781ff2bc25da4389c77e3b79d01b293` | 3.8 | `cd5e6c21494b13ec8d73f9e37e141503a1f716df35108207674108505d1ebd0a` | 3.5 |

Runner sha256 `64308e17fb2610d5868312d97d7fc4790f933d62b69d0b5333ea68022c0a73aa` · constantes `154ed376cde09218ef322492876fb1b3fa44244a0cf55c005ac3c7d045721a59` · script `e24594a568144e750b27e4d362dba49fc9d27f89bc70a8ef572170d6c52aebf2`
