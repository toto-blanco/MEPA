// ============================================================================
// MEPA V7-alpha rev. 2.1 — Node 2 Audit de Conformité — JavaScript n8n
// ============================================================================
// Statut           : EXTENSION V7
// Cible            : /data/mepa/scripts/mepa_node2_audit_v7.js
//                    (et noeud "Code" dans mepa_workflow_n8n_V7.json, N2)
// Remplace         : mepa_node2_audit_v62.js v2.1.0 (pour les fiches V7)
// Retrocompatibilite :
//   - C1-C13 : logique inchangee. Memes signatures d'erreur pour fiches V6.2.
//   - Si la fiche est V6.2 (pas de marqueur _v7_meta ni de variables V7),
//     le script se comporte exactement comme v2.1.0 et ignore C14/C15.
//   - Si la fiche est V7 (presence de $schema contenant "v7" OU champ _v7_meta
//     OU au moins une des 6 variables V7), C14 et C15 sont actives.
//   - runner_config.y0 : garantie liste [S,L,C,I]. [RESOUT ARCH-013]
//   - theta_C / theta_I injectes dans runner_config.params. [RESOUT ARCH-014]
//   - Chemins canoniques /data/mepa/scripts/ via MEPA_SCRIPTS_DIR. [RESOUT ARCH-015]
//   - Labels D4 etendus a 10 labels (ajout (α) V7).
//   - Nouvelles variables V7 propagees dans runner_config.variables_v7.
// Version          : 3.0.0
// MEPA version     : 7.0-alpha rev. 2.1
// Corrections V3.0.0 vs V2.1.0 :
//   [V7-N1] Ajout du label "(α) Cristallisation sacrificielle d'État" dans LABELS_D4.
//   [V7-N2] C14 NOUVEAU — Validation du codage null positif de psi_cible (regle E3 rev. 2.1).
//   [V7-N3] C15 NOUVEAU — Presence des 6 variables V7 dans fiches V7 (ou NC justifie).
//   [V7-N4] Chargement des definitions V7 depuis mepa_constants.json v1.3.0 et
//           mepa_whitelist_keys.json v3.0.0 (fallback embarque en cas d'absence).
//   [V7-N5] NC bloquant etendu a psi_noyau et gamma_local (cf. nc_bloquant_v7).
//   [V7-N6] Contraintes WP etendues pour les 6 cas du cluster pilote V7-gamma rev. 2.
//   [V7-N7] Propagation des variables V7 dans runner_config.variables_v7 pour le runner V7-beta.
// ============================================================================
//
// CONTROLES ACTIFS (15) - ORDRE D'EXECUTION :
//   C13 [PREMIER] Detection variables NC - NC bloquant => DONNEES_INSUFFISANTES
//                 (etendu : psi_noyau, gamma_local sont NC bloquants V7)
//   C1  Champs obligatoires a la racine
//   C2  Cles cmd obligatoires presentes
//   C3  Plages physiques commandes
//   C3b Plages conditions initiales
//   C4  Nomenclature D6 : 'gamma' present, 'g' absent
//   C5  Labels D4 conformes (10 labels V7 — ajout (α))
//   C6  Sa dans {2, 4, 6, 7}
//   C7  Sa=7 : sa_p6_modulation documente
//   C8  theta_C / theta_I dans plages admissibles
//   C9  Whitelist cles racine (apres C13)
//   C10 Contraintes par WP (incluant cluster pilote V7-gamma rev. 2)
//   C11 cmd_linear obligatoire pour Cluster C1
//   C12 Sa = parseInt(Sa) : type entier garanti
//   C14 [V7] Codage null positif de psi_cible justifie (regle E3 rev. 2.1)
//   C15 [V7] Presence des 6 variables V7 si fiche marquee V7
//
// SORTIES :
//   VALIDE              -> runner_config (incl. variables_v7) -> Node 3 Runner V7-beta
//   INVALIDE            -> alerte + suspension (erreur structure)
//   DONNEES_INSUFFISANTES -> escalade Architecte (NC bloquant incluant V7)
// ============================================================================

"use strict";

// Chemins canoniques Pi5 - ARCH-015 resolu
const MEPA_SCRIPTS_DIR = (typeof process !== "undefined" && process.env && process.env.MEPA_SCRIPTS_DIR)
  ? process.env.MEPA_SCRIPTS_DIR
  : "/data/mepa/scripts";

// Chargement mepa_whitelist_keys.json v3.0.0 (fallback embarque si absent)
let WHITELIST = null;
try {
  const fs = require("fs"), path = require("path");
  WHITELIST = JSON.parse(fs.readFileSync(path.join(MEPA_SCRIPTS_DIR, "mepa_whitelist_keys.json"), "utf8"));
} catch (_) { WHITELIST = null; }

// Chargement mepa_constants.json v1.3.0 (fallback embarque si absent)
let CONSTANTS = null;
try {
  const fs = require("fs"), path = require("path");
  CONSTANTS = JSON.parse(fs.readFileSync(path.join(MEPA_SCRIPTS_DIR, "mepa_constants.json"), "utf8"));
} catch (_) { CONSTANTS = null; }

// ============================================================================
// LABELS D4 V7 — 10 labels officiels (au caractere pres)
// ============================================================================
// Source : mepa_constants.json v1.3.0 > labels_trajectoire_d4.labels
// Fallback embarque si mepa_constants.json indisponible
const LABELS_D4 = (() => {
  if (CONSTANTS && CONSTANTS.labels_trajectoire_d4 && Array.isArray(CONSTANTS.labels_trajectoire_d4.labels)) {
    return CONSTANTS.labels_trajectoire_d4.labels;
  }
  return [
    "(a) Rupture transformatrice",
    "(α) Cristallisation sacrificielle d'État",   // V7-alpha rev. 2.1 — NOUVEAU
    "(b) Répression réussie",
    "(c) Stase / ambigu",
    "(d) Effondrement progressif",
    "(d) Dissolution",
    "(e) Réforme institutionnelle",
    "(h) Stabilité",
    "(h)/(e) Stabilité ou réforme lente",
    "(γ) Transformation forcée",
  ];
})();

const SA_VALIDES = new Set([2, 4, 6, 7]);

// M_r valide (V7) : {1, 2, 3}
const M_R_VALIDES = new Set([1, 2, 3]);

// ============================================================================
// PLAGES PHYSIQUES COMMANDES (source: mepa_constants.json, fallback embarque)
// ============================================================================
const PLAGES_CMD = (() => {
  if (CONSTANTS && CONSTANTS.bornes_commandes) {
    const out = {};
    for (const [k, v] of Object.entries(CONSTANTS.bornes_commandes)) {
      if (!k.startsWith("$") && v.min !== undefined) out[k] = { min: v.min, max: v.max };
    }
    return out;
  }
  return {
    T: { min: 0.0, max: 2.0 }, Mob: { min: 0.0, max: 1.0 },
    R: { min: 0.0, max: 10.0 }, Ref: { min: 0.0, max: 1.0 },
    Rc: { min: 0.0, max: 1.0 }, Rn: { min: 0.0, max: 1.0 },
    E: { min: 0.0, max: 1.0 }, gamma: { min: 0.0, max: 1.0 },
    EROI: { min: 1.01, max: 200.0 }, Pop: { min: 0.0, max: 10.0 },
  };
})();

const PLAGES_CI = {
  S0: { min: 0.0, max: 3.0 }, L0: { min: 0.0, max: 1.0 },
  C0: { min: 0.0, max: 1.0 }, I0: { min: 0.0, max: 20.0 },
};

const PLAGES_SIM = {
  t_max: { min: 50, max: 500 },
  theta_C: { min: 0.10, max: 0.60 },
  theta_I: { min: 0.05, max: 0.50 },
};

// Plages des variables V7 (source: whitelist v3.0.0)
const PLAGES_V7 = (() => {
  if (WHITELIST && WHITELIST.variables_continues_v7) {
    const out = {};
    for (const [k, v] of Object.entries(WHITELIST.variables_continues_v7)) {
      if (!k.startsWith("$") && Array.isArray(v.plage)) {
        out[k] = { min: v.plage[0], max: v.plage[1] };
      }
    }
    return out;
  }
  return {
    mu_m:       { min: 0.0, max: 1.0 },
    phi:        { min: 0.0, max: 1.0 },
    psi_noyau:  { min: 0.0, max: 1.0 },
    psi_cible:  { min: 0.0, max: 1.0 },  // null autorise (regle E3)
    gamma_local:{ min: 0.0, max: 1.0 },
  };
})();

// ============================================================================
// CLES CMD ET INTERDITES
// ============================================================================
const CMD_OBLIGATOIRES = ["T", "Mob", "R", "Ref", "Rc", "Rn", "E", "gamma", "EROI", "Pop"];
const CMD_INTERDITES   = ["g", "A_d_eff", "E_split", "A_r_c", "A_r_ne"];

// ============================================================================
// CLES RACINE AUTORISEES (whitelist C9) — etendues V7
// ============================================================================
const RACINE_AUTORISEES = new Set([
  // --- Metadonnees ---
  "$schema", "$description", "$statut", "$audit",
  "$arbitrage", "$note_archive", "$note_correction",
  // --- Identite ---
  "wp_id", "cas", "periode", "cluster", "cluster_note",
  "trajectoire_attendue", "trajectoire_forcee",
  // --- Structure anthropologique ---
  "sa", "sa_type_todd", "sa_p6_modulation", "sa_note",
  // --- Sources et variables ---
  "sources_utilisees", "variables",
  // --- Etats et commandes ---
  "conditions_initiales", "conditions_initiales_finales",
  "commandes", "commandes_finales", "cmd_linear",
  // --- Parametres et alertes ---
  "parametres_simulation", "alertes_actives", "alertes_conv_a",
  "defi_mepa", "params_p",
  // --- Libelles descriptifs ---
  "cluster_libelle", "raison_loi_physique", "trajectoire_attendue_libelle",
  // --- Metadonnees standard ---
  "date_codage", "codeur", "statut",
  // --- V7 — NOUVEAU ---
  "_v7_meta",                      // marqueur V7 optionnel (version, revision)
  "variables_v7",                  // bloc des 6 variables V7 (alternative a imbrication dans variables)
  "configuration_c_note",          // note anthropologique Configuration C (non-operationnel V7-alpha rev. 2.1)
  "cluster_pilote_v7_gamma",       // boolean : WP membre du cluster pilote V7-gamma rev. 2
]);

// ============================================================================
// NC BLOQUANTES (source: mepa_constants.json, fallback) — etendues V7
// ============================================================================
const NC_BLOQUANTES = (() => {
  if (CONSTANTS && CONSTANTS.nc_protocol && CONSTANTS.nc_protocol.variables_nc_bloquantes) {
    return new Set(CONSTANTS.nc_protocol.variables_nc_bloquantes);
  }
  // Fallback V7 : inclut psi_noyau et gamma_local
  return new Set(["E_split", "gamma", "EROI", "Sa", "psi_noyau", "gamma_local"]);
})();

// ============================================================================
// CONTRAINTES PAR WP (incluant cluster pilote V7-gamma rev. 2)
// ============================================================================
const CONTRAINTES_WP = (WHITELIST && WHITELIST.contraintes_par_wp)
  ? WHITELIST.contraintes_par_wp
  : {
    "WP-C1-1": {
      cluster: "C1", EROI_min: 1.01, EROI_max: 2.5, cmd_linear_requis: true,
      note: "Haïti 2010-2024 — EROI dynamique 1.2→2.0. Ancre plancher corpus.",
      cluster_pilote_v7_gamma: true,
      trajectoire_attendue_v7: "(d) Effondrement progressif",
      statut_v7: "BLOQUANTE",
    },
    "WP-F1-1": {
      cmd_linear_requis: true, cluster: "C1",
      cluster_pilote_v7_gamma: true,
      trajectoire_attendue_v7: "(d) Effondrement progressif",
      statut_v7: "BLOQUANTE",
    },
    "WP-F2-1": { cmd_linear_requis: true, A_r_ne_max: 0.00, cluster: "C1" },
    "WP-F3-1": { cmd_linear_requis: true, cluster: "C1" },
    "WP-F10-1": {
      t_max: 80, cluster: "C2",
      cluster_pilote_v7_gamma: true,
      trajectoire_attendue_v7: "(a) Rupture transformatrice",
      role_v7: "CONTRÔLE NÉGATIF — doit NE PAS produire (α)",
      statut_v7: "BLOQUANTE",
    },
    "WP-I3-1": { sa_p6_mult: true, cluster: "C5" },
    "WP-I4-1": {
      sa_p6_mult: true, cluster: "C2",
      cluster_pilote_v7_gamma: true,
      trajectoire_attendue_v7: "(α) Cristallisation sacrificielle d'État",
      echec_attendu_v7: "Condition C2 branche (α) — Psi_noyau x gamma_local = 0.0055 < sigma ~ 0.0275",
      statut_v7: "CONDITIONNELLE",
      note_v7: "Codage Psi_noyau ~ 0.01 strict (NSDAP membres formels). Pre-enregistre Decision V7-D1 rev. 4.",
    },
    "WP-I9-1": { sa_p6_mult: true, cluster: "C4" },
    "WP-I10-1": {
      cmd_linear_requis: true, cluster: "C1",
      cluster_pilote_v7_gamma: true,
      trajectoire_attendue_v7: "(α) Cristallisation sacrificielle d'État",
      statut_v7: "BLOQUANTE",
      note_v7: "Cas positif principal de (α).",
    },
    "WP-C2-1": {
      cluster: "C2",
      cluster_pilote_v7_gamma: true,
      trajectoire_attendue_v7: "(b) Répression réussie — EXPLICATIVE",
      statut_v7: "BLOQUANTE",
      note_v7: "Cas test correctif V7-C4 — branche (b) explicative et non catchall.",
    },
    "WP-C4-1": {
      EROI_max: 2.0, cluster: "C1",
      configuration_c_v7_alpha: true,
      note_v7: "Liban — Configuration C documentee comme note anthropologique non-operationnelle V7-alpha rev. 2.1 (§2bis.7 du cadre).",
    },
    "WP-EXT-5": { EROI_min: 30, cluster: "C4", note: "Islande — etalon (e). Sa=2. Hors 27 WP. Candidat V7." },
  };

// ============================================================================
// P_DEFAULTS : chargés depuis mepa_constants.json si disponible (BUG-006)
// ============================================================================
const _P_DEFAULTS_FALLBACK = {
  p1: 0.08, p2: 0.045, p2b: 0.06, p3: 0.02, p4: 0.40,
  p5: 0.05, p6: 0.12,  p7: 0.04,  p8: 0.03, p9: 0.06,
  p10: 0.80, p11a: 0.60, p11b: 0.15, p13: 1.2,
  lam: 0.68, mu: 0.38, nu: 0.62, rho: 0.06,
};
const P_DEFAULTS = (function() {
  try {
    const bp = CONSTANTS && CONSTANTS.bornes_parametres_dynamiques;
    if (!bp) return { ..._P_DEFAULTS_FALLBACK };
    const out = { ..._P_DEFAULTS_FALLBACK };
    for (const k of Object.keys(_P_DEFAULTS_FALLBACK)) {
      if (bp[k] !== undefined && bp[k].defaut !== undefined) {
        out[k] = bp[k].defaut;
      }
    }
    return out;
  } catch (_) {
    return { ..._P_DEFAULTS_FALLBACK };
  }
})();

// ============================================================================
// HYPERPARAMETRES V7-alpha rev. 2.1 (pour propagation vers runner V7-beta)
// ============================================================================
const HYPERPARAMS_V7 = (() => {
  if (CONSTANTS && CONSTANTS.hyperparametres_v7_alpha_rev2_1) {
    return CONSTANTS.hyperparametres_v7_alpha_rev2_1;
  }
  // Fallback minimal embarque
  return {
    trajectoire_alpha: {
      mu_m_etoile: { valeur: 0.60 },
      sigma_base: { valeur: 0.018 },
      alpha_phi: { valeur: 1.7 },
      theta_C_alpha: { valeur: 0.30 },
      coefficient_a_r_c_eff: { valeur: 0.5 },
    },
    rampe_mod_mimetique: {
      phase_1_incubation: { duree_par_defaut: 22, modulateur_p6: 0.50 },
      phase_2_decharge: { duree_par_defaut: 7, modulateur_p6: 2.50 },
      phase_3_stabilisation: { duree_par_defaut: 30, modulateur_p6: 1.15 },
    },
    branche_b_explicative: {
      seuil_c_max: { valeur: 0.12 },
      seuil_chute_c: { valeur: 0.20 },
      intervalle_cs_valide: { min: 0.10, max: 0.50 },
    },
    branche_d_v7_c2: {
      seuil_chute_i: { valeur: 0.5 },
      seuil_fr_max: { valeur: 1.2 },
    },
  };
})();

// ============================================================================
// HELPERS
// ============================================================================
function _isNC(val) {
  return typeof val === "string" && val.trim().toUpperCase() === "NC";
}

function _toNum(val) {
  if (_isNC(val) || val === null || val === undefined) return null;
  const n = Number(val);
  return isNaN(n) ? null : n;
}

/**
 * Detecte si la fiche est au format V7.
 * Criteres : (1) $schema contient "v7", (2) champ _v7_meta present,
 * (3) au moins une des 6 variables V7 presente dans variables{}.
 */
function _estFicheV7(fiche) {
  if (fiche.$schema && typeof fiche.$schema === "string" && fiche.$schema.toLowerCase().includes("v7")) {
    return true;
  }
  if (fiche._v7_meta) return true;
  const vars_obj = fiche.variables || {};
  const vars_v7_possibles = ["m_r", "mu_m", "phi", "psi_noyau", "psi_cible", "gamma_local"];
  for (const v7key of vars_v7_possibles) {
    if (v7key in vars_obj || v7key in fiche) return true;
  }
  // Egalement : bloc variables_v7 dedie
  if (fiche.variables_v7 && typeof fiche.variables_v7 === "object") return true;
  return false;
}

/**
 * Recupere une variable V7 depuis la fiche — cherche dans variables_v7{}
 * puis dans variables{} puis a la racine.
 */
function _getVarV7(fiche, varName) {
  const v7_bloc = fiche.variables_v7 || {};
  if (varName in v7_bloc) return v7_bloc[varName];
  const vars_obj = fiche.variables || {};
  if (varName in vars_obj) return vars_obj[varName];
  if (varName in fiche) return fiche[varName];
  return undefined;
}

// ============================================================================
// DEBUT AUDIT
// ============================================================================

const fiche    = $input.item.json;
const erreurs  = [];
const warnings = [];
const nc_bloquantes_det    = [];
const nc_non_bloquantes_det = [];

const audit_log = {
  timestamp: new Date().toISOString(),
  version_audit: "3.0.0",
  mepa_version: "7.0-alpha rev. 2.1",
  wp_id: null,
  fiche_v7: false,
  controles: {},
  erreurs: [],
  warnings: [],
  nc_bloquantes: [],
  nc_non_bloquantes: [],
  statut: "INVALIDE",
  sa_modulation: { mult_applied: false },
};

const wp_id   = fiche.wp_id   || null;
const cluster = fiche.cluster || null;
audit_log.wp_id = wp_id;

// Detection format V7
const fiche_v7 = _estFicheV7(fiche);
audit_log.fiche_v7 = fiche_v7;

// ============================================================================
// C13 - DETECTION VARIABLES NC (PREMIER)
// ============================================================================
{
  const vars_fiche = fiche.variables || {};
  const cmd_fiche  = fiche.commandes || fiche.commandes_finales || {};
  const vars_v7_fiche = fiche.variables_v7 || {};
  let c13_ok = true;

  // Variables V6.2 — comme v2.1.0
  for (const [varName, entry] of Object.entries(vars_fiche)) {
    if (!entry || typeof entry !== "object") continue;
    if (!_isNC(entry.valeur)) continue;
    if (NC_BLOQUANTES.has(varName)) {
      nc_bloquantes_det.push(varName);
      c13_ok = false;
    } else {
      nc_non_bloquantes_det.push(varName);
      warnings.push(`C13 - NC non bloquant : '${varName}'. Simulation autorisee. CCI degrade.`);
    }
  }

  // Variables V7 — si fiche V7, verifier psi_noyau et gamma_local NC bloquants
  if (fiche_v7) {
    for (const v7key of ["mu_m", "phi", "psi_noyau", "psi_cible", "gamma_local"]) {
      const entry = _getVarV7(fiche, v7key);
      if (!entry || typeof entry !== "object") continue;
      if (!_isNC(entry.valeur)) continue;
      if (NC_BLOQUANTES.has(v7key)) {
        nc_bloquantes_det.push(v7key);
        c13_ok = false;
      } else {
        nc_non_bloquantes_det.push(v7key);
        warnings.push(`C13 - NC non bloquant V7 : '${v7key}'. Branche (α) non evaluable mais simulation V6.2 possible.`);
      }
    }
  }

  // Defense en profondeur : commandes directes
  for (const [k, v] of Object.entries(cmd_fiche)) {
    if (_isNC(v) && NC_BLOQUANTES.has(k) && !nc_bloquantes_det.includes(k)) {
      nc_bloquantes_det.push(k);
      c13_ok = false;
    }
  }

  audit_log.nc_bloquantes    = nc_bloquantes_det;
  audit_log.nc_non_bloquantes = nc_non_bloquantes_det;
  audit_log.controles.C13 = c13_ok
    ? (nc_non_bloquantes_det.length > 0 ? "OK_WITH_WARNINGS" : "OK")
    : "NC_BLOQUANT";

  if (!c13_ok) {
    audit_log.erreurs  = [`C13 - NC bloquant sur : [${nc_bloquantes_det.join(", ")}]. Simulation impossible.`];
    audit_log.warnings = warnings;
    audit_log.statut   = "DONNEES_INSUFFISANTES";
    return [{
      json: {
        statut_audit: "DONNEES_INSUFFISANTES",
        wp_id,
        fiche_v7,
        nc_bloquantes: nc_bloquantes_det,
        nc_non_bloquantes: nc_non_bloquantes_det,
        nb_erreurs: 1,
        nb_warnings: warnings.length,
        audit_log,
        message: `[C13 NC BLOQUANT] ${wp_id || "?"} - Variables NC bloquantes : [${nc_bloquantes_det.join(", ")}]. ${fiche_v7 ? "Fiche V7. " : ""}Escalade Architecte.`,
      }
    }];
  }
}

// ============================================================================
// C1 - CHAMPS OBLIGATOIRES A LA RACINE
// ============================================================================
{
  const has_ci  = fiche.conditions_initiales != null || fiche.conditions_initiales_finales != null;
  const has_cmd = fiche.commandes != null || fiche.commandes_finales != null;
  const manquants = ["wp_id", "cas", "cluster", "sa", "trajectoire_attendue", "variables"].filter(k => fiche[k] == null);
  if (!has_ci)  manquants.push("conditions_initiales[_finales]");
  if (!has_cmd) manquants.push("commandes[_finales]");
  if (manquants.length > 0) {
    erreurs.push(`C1 - Champs obligatoires null/absents : [${manquants.join(", ")}]`);
    audit_log.controles.C1 = "FAIL";
  } else { audit_log.controles.C1 = "OK"; }
}

// ============================================================================
// C4 - NOMENCLATURE D6
// ============================================================================
{
  const cmd  = fiche.commandes || fiche.commandes_finales || {};
  const vars = fiche.variables || {};
  let ok = true;
  if ("g" in cmd)  { erreurs.push("C4 - Nomenclature D6 : cle 'g' dans commandes. Utiliser 'gamma'."); ok = false; }
  if ("g" in vars) { erreurs.push("C4 - Nomenclature D6 : cle 'g' dans variables. Utiliser 'gamma'."); ok = false; }
  if (!("gamma" in cmd)) { erreurs.push("C4 - Nomenclature D6 : cle 'gamma' absente des commandes."); ok = false; }
  const interdites = CMD_INTERDITES.filter(k => k !== "g" && k in cmd);
  if (interdites.length > 0) { erreurs.push(`C4/C9b - Cles CONV-E dans commandes : [${interdites.join(", ")}]. Mapping : A_d_eff->R, E_split->E.`); ok = false; }
  audit_log.controles.C4 = ok ? "OK" : "FAIL";
}

// ============================================================================
// C2 + C3 - CLES CMD ET PLAGES PHYSIQUES
// ============================================================================
{
  const cmd  = fiche.commandes || fiche.commandes_finales || {};
  let ok = true;
  const manquantes = CMD_OBLIGATOIRES.filter(k => !(k in cmd));
  if (manquantes.length > 0) { erreurs.push(`C2 - Cles cmd manquantes : [${manquantes.join(", ")}]`); ok = false; }
  for (const [key, plage] of Object.entries(PLAGES_CMD)) {
    if (!(key in cmd)) continue;
    const raw = cmd[key];
    if (_isNC(raw)) continue;
    const val = _toNum(raw);
    if (val === null) { erreurs.push(`C2 - cmd.${key} : type incorrect (recu '${typeof raw}', attendu number)`); ok = false; }
    else if (val < plage.min || val > plage.max) { erreurs.push(`C3 - cmd.${key}=${val} hors plage [${plage.min}, ${plage.max}]`); ok = false; }
  }
  audit_log.controles.C2_C3 = ok ? "OK" : "FAIL";
}

// ============================================================================
// C3b - PLAGES CONDITIONS INITIALES
// ============================================================================
{
  const ci = fiche.conditions_initiales || fiche.conditions_initiales_finales || {};
  let ok = true;
  for (const [key, plage] of Object.entries(PLAGES_CI)) {
    if (!(key in ci)) continue;
    const val = _toNum(ci[key]);
    if (val === null) { erreurs.push(`C2 - ci.${key} : type incorrect`); ok = false; }
    else if (val < plage.min || val > plage.max) { erreurs.push(`C3b - ci.${key}=${val} hors plage [${plage.min}, ${plage.max}]`); ok = false; }
  }
  audit_log.controles.C3_CI = ok ? "OK" : "FAIL";
}

// ============================================================================
// C5 - LABELS D4 (10 labels officiels V7-alpha rev. 2.1)
// ============================================================================
{
  const traj = fiche.trajectoire_attendue || "";
  const labels_recus = traj.split("->").concat(traj.split("\u2192")).map(l => l.trim()).filter(Boolean);
  const labels_uniq = [...new Set(labels_recus)];
  const labels_inv  = labels_uniq.filter(l => !LABELS_D4.includes(l));
  if (labels_inv.length > 0) {
    erreurs.push(`C5 - Labels D4 non conformes : [${labels_inv.map(l=>`'${l}'`).join(", ")}]. Autorises V7 (10 labels) : ${LABELS_D4.join(" | ")}`);
    audit_log.controles.C5 = "FAIL";
  } else { audit_log.controles.C5 = "OK"; }
}

// ============================================================================
// C6 + C12 - SA VALIDE ET ENTIER
// ============================================================================
let sa_int = NaN;
{
  const sa_raw = fiche.sa;
  sa_int = parseInt(sa_raw, 10);
  if (String(sa_raw) !== String(sa_int)) warnings.push(`C12 - Sa='${sa_raw}' converti en entier ${sa_int}.`);
  if (!SA_VALIDES.has(sa_int)) {
    erreurs.push(`C6 - Sa=${sa_raw} invalide. Valeurs autorisees : {2, 4, 6, 7}`);
    audit_log.controles.C6_C12 = "FAIL";
  } else {
    audit_log.controles.C6_C12 = "OK";
    if (sa_int === 7) {
      const p6_flag = fiche.sa_p6_modulation === true || fiche.sa_p6_modulation === "true";
      if (!p6_flag) warnings.push("C7 - Sa=7 : sa_p6_modulation non documente. Runner applique p6x1.5 automatiquement (regle absolue V6.2).");
      audit_log.sa_modulation = { mult_applied: true, note: "Sa=7 (famille souche) -> p6 x 1.5 applique par le runner" };
    }
  }
}

// ============================================================================
// C8 - THETA_C / THETA_I DANS LES PLAGES ADMISSIBLES
// ============================================================================
{
  const prm = fiche.parametres_simulation || {};
  let ok = true;
  for (const [key, plage] of Object.entries(PLAGES_SIM)) {
    if (!(key in prm)) continue;
    const val = _toNum(prm[key]);
    if (val !== null && (val < plage.min || val > plage.max)) {
      erreurs.push(`C8 - parametres_simulation.${key}=${val} hors plage [${plage.min}, ${plage.max}]`);
      ok = false;
    }
  }
  audit_log.controles.C8 = ok ? "OK" : "FAIL";
}

// ============================================================================
// C9 - WHITELIST CLES RACINE (execute APRES C13)
// ============================================================================
{
  const cles_extra = Object.keys(fiche).filter(k => !RACINE_AUTORISEES.has(k));
  if (cles_extra.length > 0) {
    erreurs.push(`C9 - Cles non autorisees a la racine : [${cles_extra.join(", ")}]`);
    audit_log.controles.C9 = "FAIL";
  } else { audit_log.controles.C9 = "OK"; }
}

// ============================================================================
// C10 - CONTRAINTES SPECIFIQUES PAR WP (etendues cluster pilote V7-gamma)
// ============================================================================
{
  let ok = true;
  if (wp_id && CONTRAINTES_WP[wp_id]) {
    const ctr = CONTRAINTES_WP[wp_id];
    const cmd = fiche.commandes || fiche.commandes_finales || {};
    const prm = fiche.parametres_simulation || {};
    if (ctr.EROI_ancre !== undefined) {
      const eroi = _toNum(cmd.EROI);
      if (eroi !== null && eroi !== ctr.EROI_ancre) { erreurs.push(`C10 - ${wp_id} : EROI=${eroi} != ancre obligatoire ${ctr.EROI_ancre}`); ok = false; }
    }
    if (ctr.EROI_max !== undefined) {
      const eroi = _toNum(cmd.EROI);
      if (eroi !== null && eroi > ctr.EROI_max) { erreurs.push(`C10 - ${wp_id} : EROI=${eroi} > max ${ctr.EROI_max}`); ok = false; }
    }
    if (ctr.A_r_ne_max !== undefined) {
      const rn = _toNum(cmd.Rn);
      if (rn !== null && rn > ctr.A_r_ne_max) { erreurs.push(`C10 - ${wp_id} : Rn=${rn} > A_r_ne_max=${ctr.A_r_ne_max}`); ok = false; }
    }
    if (ctr.t_max !== undefined && prm.t_max !== undefined && prm.t_max !== ctr.t_max)
      warnings.push(`C10 - ${wp_id} : t_max=${prm.t_max}, valeur recommandee=${ctr.t_max}`);

    // Warnings V7 specifiques cluster pilote
    if (fiche_v7 && ctr.cluster_pilote_v7_gamma) {
      audit_log.v7_cluster_pilote = {
        trajectoire_attendue_v7: ctr.trajectoire_attendue_v7 || null,
        statut_v7: ctr.statut_v7 || null,
        role_v7: ctr.role_v7 || null,
        note_v7: ctr.note_v7 || null,
      };
      if (ctr.statut_v7 === "CONDITIONNELLE") {
        warnings.push(`C10 - ${wp_id} : statut V7 CONDITIONNELLE (Decision V7-D1 rev. 4 §5). ${ctr.echec_attendu_v7 || ""}`);
      }
    }
  }
  audit_log.controles.C10 = ok ? (wp_id && CONTRAINTES_WP[wp_id] ? "OK" : "OK (pas de contrainte specifique)") : "FAIL";
}

// ============================================================================
// C11 - CMD_LINEAR POUR CLUSTER C1
// ============================================================================
{
  const ctr_wp   = (wp_id && CONTRAINTES_WP[wp_id]) ? CONTRAINTES_WP[wp_id] : {};
  const exc_stat = ctr_wp.EROI_mode === "statique";
  const has_lin  = fiche.cmd_linear != null && typeof fiche.cmd_linear === "object" && Object.keys(fiche.cmd_linear).length > 0;
  if (cluster === "C1" && !has_lin && !exc_stat) {
    erreurs.push("C11 - Cluster C1 : cmd_linear.EROI obligatoire ({start, end}). Absent.");
    audit_log.controles.C11 = "FAIL";
  } else { audit_log.controles.C11 = cluster === "C1" ? "OK" : "N/A (cluster != C1)"; }
}

// ============================================================================
// C14 - [V7] VALIDATION DU CODAGE NULL POSITIF DE PSI_CIBLE (regle E3 rev. 2.1)
// ============================================================================
// Source : cadre V7-alpha rev. 2.1 §8.2 (regle E3) et Decision V7-D1 rev. 4 §4bis.
// Si psi_cible est code null, une justification textuelle positive est OBLIGATOIRE
// avec une longueur minimale de 50 caracteres. Sans cette justification, le codage
// null est rejete (la clause null doit etre defendue explicitement, pas laissee par
// defaut comme omission).
// ============================================================================
{
  if (fiche_v7) {
    const psi_cible_entry = _getVarV7(fiche, "psi_cible");
    let c14_ok = true;
    let c14_note = null;

    if (psi_cible_entry && typeof psi_cible_entry === "object") {
      const val = psi_cible_entry.valeur;
      const just = (psi_cible_entry.justification || "").toString().trim();

      if (val === null) {
        // Cas null : justification textuelle obligatoire
        if (just.length < 50) {
          erreurs.push(`C14 - psi_cible code null sans justification suffisante (longueur=${just.length}, minimum=50). Regle E3 rev. 2.1 : le codage null positif exige une defense textuelle explicite. Voir whitelist.variables_continues_v7.psi_cible.regle_e3_rev_2_1.exemple_valide pour le format.`);
          c14_ok = false;
        } else {
          c14_note = "psi_cible=null avec justification valide (>= 50 chars)";
        }
      } else if (val !== undefined && val !== "NC") {
        // Cas valeur numerique : verifier plage [0, 1]
        const num_val = _toNum(val);
        if (num_val === null) {
          erreurs.push(`C14 - psi_cible : type incorrect (recu '${typeof val}', attendu number ou null)`);
          c14_ok = false;
        } else if (num_val < 0.0 || num_val > 1.0) {
          erreurs.push(`C14 - psi_cible=${num_val} hors plage [0, 1]`);
          c14_ok = false;
        } else {
          c14_note = `psi_cible=${num_val} (valeur numerique valide)`;
        }
      }
    }
    audit_log.controles.C14 = c14_ok ? `OK (${c14_note || "psi_cible non code"})` : "FAIL";
  } else {
    audit_log.controles.C14 = "N/A (fiche V6.2)";
  }
}

// ============================================================================
// C15 - [V7] PRESENCE DES 6 VARIABLES V7 SI FICHE V7
// ============================================================================
// Source : cadre V7-alpha rev. 2.1 §2ter.
// Si la fiche est marquee V7, les 6 variables V7 doivent etre presentes ou
// explicitement codees NC avec justification (C13 gere le cas NC). L'absence
// totale d'une variable V7 dans une fiche V7 est une erreur structurelle.
// ============================================================================
{
  if (fiche_v7) {
    const vars_v7_obligatoires = ["m_r", "mu_m", "phi", "psi_noyau", "psi_cible", "gamma_local"];
    const manquantes = [];
    const presentes = [];

    for (const v7key of vars_v7_obligatoires) {
      const entry = _getVarV7(fiche, v7key);
      if (entry === undefined) {
        manquantes.push(v7key);
      } else {
        presentes.push(v7key);
      }
    }

    if (manquantes.length > 0) {
      erreurs.push(`C15 - Fiche V7 : variables V7 manquantes [${manquantes.join(", ")}]. Les 6 variables V7 (m_r, mu_m, phi, psi_noyau, psi_cible, gamma_local) sont obligatoires dans une fiche V7. Voir cadre theorique V7-alpha rev. 2.1 §2ter.`);
      audit_log.controles.C15 = "FAIL";
    } else {
      audit_log.controles.C15 = `OK (${presentes.length}/6 variables V7 presentes)`;
    }

    // Verification speciale m_r : valeur dans {1, 2, 3}
    const m_r_entry = _getVarV7(fiche, "m_r");
    if (m_r_entry && typeof m_r_entry === "object" && !_isNC(m_r_entry.valeur)) {
      const m_r_int = parseInt(m_r_entry.valeur, 10);
      if (!M_R_VALIDES.has(m_r_int)) {
        erreurs.push(`C15 - m_r=${m_r_entry.valeur} invalide. Valeurs autorisees : {1, 2, 3} (Stades matrice religieuse Todd).`);
      }
    }
  } else {
    audit_log.controles.C15 = "N/A (fiche V6.2)";
  }
}

// ============================================================================
// SYNTHESE
// ============================================================================

audit_log.erreurs  = erreurs;
audit_log.warnings = warnings;
audit_log.statut   = erreurs.length === 0 ? "VALIDE" : "INVALIDE";

if (erreurs.length > 0) {
  return [{
    json: {
      statut_audit: "INVALIDE",
      wp_id,
      fiche_v7,
      nb_erreurs:   erreurs.length,
      nb_warnings:  warnings.length,
      audit_log,
      message: `[AUDIT FAIL] ${wp_id || "?"} - ${erreurs.length} erreur(s) structurelle(s) - pipeline suspendu. Action : recodage CONV-E.`,
    }
  }];
}

// ============================================================================
// CONSTRUCTION runner_config - SORTIE VALIDE (etendue V7)
// ============================================================================

const cmd    = fiche.commandes || fiche.commandes_finales || {};
const ci     = fiche.conditions_initiales || fiche.conditions_initiales_finales || {};
const params = fiche.parametres_simulation || {};
const params_p_fiche = fiche.params_p || {};

// y0 garantie liste [S,L,C,I]
const y0 = Array.isArray(ci)
  ? [parseFloat(ci[0])||1.0, parseFloat(ci[1])||0.5, parseFloat(ci[2])||0.1, parseFloat(ci[3])||3.5]
  : [_toNum(ci.S0)??1.0, _toNum(ci.L0)??0.5, _toNum(ci.C0)??0.1, _toNum(ci.I0)??3.5];

const theta_C = _toNum(params.theta_C) ?? 0.30;
const theta_I = _toNum(params.theta_I) ?? 0.22;
const t_max   = _toNum(params.t_max)   ?? 300;

const params_runner = { ...P_DEFAULTS, ...params_p_fiche, theta_C, theta_I };

// Bloc cmd nettoye
const cmd_clean = {};
for (const key of CMD_OBLIGATOIRES) {
  if (key in cmd) cmd_clean[key] = _isNC(cmd[key]) ? cmd[key] : (_toNum(cmd[key]) ?? cmd[key]);
}

// ============================================================================
// EXTRACTION DES VARIABLES V7 POUR LE RUNNER V7-beta
// ============================================================================
let variables_v7_extract = null;
if (fiche_v7) {
  variables_v7_extract = {};
  for (const v7key of ["m_r", "mu_m", "phi", "psi_noyau", "psi_cible", "gamma_local"]) {
    const entry = _getVarV7(fiche, v7key);
    if (entry && typeof entry === "object") {
      variables_v7_extract[v7key] = {
        valeur: entry.valeur,
        source_id: entry.source_id || null,
        justification: entry.justification || null,
      };
    } else {
      variables_v7_extract[v7key] = { valeur: null, source_id: null, justification: null };
    }
  }
}

// runner_config complet
const runner_config = {
  wp_id,
  cas:                  fiche.cas,
  cluster,
  trajectoire_attendue: fiche.trajectoire_attendue,
  sa:                   sa_int,
  y0,
  t_max,
  theta_C,
  theta_I,
  cmd:                  cmd_clean,
  cmd_linear:           fiche.cmd_linear || null,
  params:               params_runner,
  nc_non_bloquantes:    nc_non_bloquantes_det,
  // --- V7 NOUVEAUX CHAMPS ---
  fiche_v7:             fiche_v7,
  variables_v7:         variables_v7_extract,
  hyperparams_v7:       fiche_v7 ? HYPERPARAMS_V7 : null,
};

// Chemins canoniques
const config_path = `/tmp/${wp_id}_runner_config.json`;
const result_path = `/tmp/${wp_id}_result.json`;
const n1_path     = `/tmp/${wp_id}_n1_sensitivity.json`;
// En V7, pointe vers le nouveau runner V7-beta
const runner_cmd  = fiche_v7
  ? `python3 ${MEPA_SCRIPTS_DIR}/mepa_runner_v3_v7.py ${config_path}`
  : `python3 ${MEPA_SCRIPTS_DIR}/mepa_runner_v2_gamma.py ${config_path}`;
const n1_cmd      = `python3 ${MEPA_SCRIPTS_DIR}/mepa_sensitivity_n1.py ${config_path} ${n1_path}`;

// llm_context pour CONV-A (etendu V7)
const llm_context = {
  wp_id,
  cas:                  fiche.cas,
  periode:              fiche.periode,
  cluster,
  sa:                   sa_int,
  trajectoire_attendue: fiche.trajectoire_attendue,
  fiche_v7:             fiche_v7,
  mepa_full_vars: {
    "E_split": fiche.variables?.E_split?.valeur,
    "gamma":   fiche.variables?.gamma?.valeur,
    "A_d_eff": fiche.variables?.A_d_eff?.valeur,
    "A_r_c":   fiche.variables?.A_r_c?.valeur,
    "A_r_ne":  fiche.variables?.A_r_ne?.valeur,
    "Cs":      fiche.variables?.Cs?.valeur,
    "L_t":     fiche.variables?.L_t?.valeur,
    "EROI":    fiche.variables?.EROI?.valeur,
    "Sa":      fiche.variables?.Sa?.valeur,
  },
  mepa_v7_vars: variables_v7_extract,
  nc_non_bloquantes: nc_non_bloquantes_det,
  alertes:            fiche.alertes_actives || [],
  defi_mepa:          fiche.defi_mepa       || "",
};

return [{
  json: {
    statut_audit:       "VALIDE",
    wp_id,
    fiche_v7,
    nb_erreurs:         0,
    nb_warnings:        warnings.length,
    nc_non_bloquantes:  nc_non_bloquantes_det,
    audit_log,
    runner_config,
    runner_config_json: JSON.stringify(runner_config, null, 2),
    runner_config_path: config_path,
    result_path,
    n1_path,
    runner_cmd,
    n1_cmd,
    llm_context,
    message: (
      `[AUDIT OK] ${wp_id} - ${fiche_v7 ? "V7 (15 controles)" : "V6.2 (13 controles)"} passes` +
      (warnings.length > 0 ? ` (${warnings.length} warning(s))` : "") +
      (nc_non_bloquantes_det.length > 0 ? ` [NC non-bl : ${nc_non_bloquantes_det.join(", ")}]` : "")
    ),
  }
}];
