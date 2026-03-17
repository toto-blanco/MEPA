// ============================================================================
// MEPA V6.2 — Node 2 Audit de Conformité — JavaScript n8n
// ============================================================================
// Statut           : REMPLACEMENT
// Cible            : /data/mepa/scripts/mepa_node2_audit_v62.js
//                    (et noeud "Code" dans mepa_workflow_n8n_V62.json, N2)
// Remplace         : mepa_node2_audit_v62.js v1.x (C1-C12, correctif V1/C9)
// Retrocompatibilite :
//   - C1-C12 : logique inchangee. Meme semantique de sortie pour WP valides.
//   - C13 [NOUVEAU] : detection NC, execute EN PREMIER avant C9.
//     Resout la condition de course : sans C13 avant C9, la valeur "NC"
//     dans un champ cmd declencherait C2 (type incorrect) avant d'etre
//     reconnue comme sentinelle legitime.
//   - Nouveau statut de sortie : DONNEES_INSUFFISANTES (distinct de INVALIDE).
//     INVALIDE = erreur structurelle fiche (recodage CONV-E).
//     DONNEES_INSUFFISANTES = fiche valide, sources historiques insuffisantes
//     pour une variable bloquante (escalade Architecte, pas recodage).
//   - runner_config.y0 : garantie liste [S,L,C,I]. [RESOUT ARCH-013]
//   - theta_C / theta_I injectes dans runner_config.params. [RESOUT ARCH-014]
//   - Chemins canoniques /data/mepa/scripts/ via MEPA_SCRIPTS_DIR. [RESOUT ARCH-015]
//   - Labels D4 alignes sur le referentiel officiel Runner V6.2.
// Version          : 2.1.0
// MEPA version     : 6.2 Fortifiee
// Corrections V2.1.0 vs V2.0.0 :
//   [BUG-006] P_DEFAULTS chargés dynamiquement depuis mepa_constants.json (fallback embarqué).
//   [BUG-007] "(d) Dissolution" ajouté dans LABELS_D4 — Manuel Gouvernance Annexe A.
// ============================================================================
//
// CONTROLES ACTIFS (13) - ORDRE D'EXECUTION :
//   C13 [PREMIER] Detection variables NC - NC bloquant => DONNEES_INSUFFISANTES
//   C1  Champs obligatoires a la racine
//   C2  Cles cmd obligatoires presentes
//   C3  Plages physiques commandes
//   C3b Plages conditions initiales
//   C4  Nomenclature D6 : 'gamma' present, 'g' absent
//   C5  Labels D4 conformes (8 labels officiels Runner — ajout (γ) V6.2)
//   C6  Sa dans {2, 4, 6, 7}
//   C7  Sa=7 : sa_p6_modulation documente
//   C8  theta_C / theta_I dans plages admissibles
//   C9  Whitelist cles racine (apres C13 - "NC" ne sera pas rejete ici)
//   C10 Contraintes par WP (ancres EROI, t_max specifiques)
//   C11 cmd_linear obligatoire pour Cluster C1
//   C12 Sa = parseInt(Sa) : type entier garanti
//
// SORTIES :
//   VALIDE              -> runner_config complet -> Node 3 Runner
//   INVALIDE            -> alerte + suspension (erreur structure)
//   DONNEES_INSUFFISANTES -> escalade Architecte (NC bloquant)
// ============================================================================

"use strict";

// Chemins canoniques Pi5 - ARCH-015 resolu
const MEPA_SCRIPTS_DIR = (typeof process !== "undefined" && process.env && process.env.MEPA_SCRIPTS_DIR)
  ? process.env.MEPA_SCRIPTS_DIR
  : "/data/mepa/scripts";

// Chargement mepa_whitelist_keys.json (fallback embarque si absent)
let WHITELIST = null;
try {
  const fs = require("fs"), path = require("path");
  WHITELIST = JSON.parse(fs.readFileSync(path.join(MEPA_SCRIPTS_DIR, "mepa_whitelist_keys.json"), "utf8"));
} catch (_) { WHITELIST = null; }

// Chargement mepa_constants.json (fallback embarque si absent)
let CONSTANTS = null;
try {
  const fs = require("fs"), path = require("path");
  CONSTANTS = JSON.parse(fs.readFileSync(path.join(MEPA_SCRIPTS_DIR, "mepa_constants.json"), "utf8"));
} catch (_) { CONSTANTS = null; }

// Labels D4 officiels (7 stricts - referentiel Runner D4 V6.2 - au caractere pres)
const LABELS_D4 = [
  "(a) Rupture transformatrice",
  "(b) Répression réussie",
  "(c) Stase / ambigu",
  "(d) Effondrement progressif",
  "(d) Dissolution",               // 9e label — Manuel Gouvernance Annexe A (BUG-007)
                                   // Conditions : F≥R, Ref>0.35, Rc+Rn<0.35
                                   // Non produit par l'arbre automatique — fiche étalon LOI PHYSIQUE
  "(e) Réforme institutionnelle",
  "(h) Stabilité",
  "(h)/(e) Stabilité ou réforme lente",
  "(γ) Transformation forcée",     // 8e label officiel D4 — V6.2 (T1 Sécession, I5 Espagne)
];

const SA_VALIDES = new Set([2, 4, 6, 7]);

// Plages physiques commandes (source: mepa_constants.json, fallback embarque)
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

const CMD_OBLIGATOIRES = ["T", "Mob", "R", "Ref", "Rc", "Rn", "E", "gamma", "EROI", "Pop"];
const CMD_INTERDITES   = ["g", "A_d_eff", "E_split", "A_r_c", "A_r_ne"];

const RACINE_AUTORISEES = new Set([
  "$schema", "$description", "$statut", "$audit",
  "$arbitrage", "$note_archive", "$note_correction",  // métadonnées fiches V6.2
  "wp_id", "cas", "periode", "cluster", "cluster_note",
  "trajectoire_attendue", "trajectoire_forcee",        // trajectoire_forcee → label (γ) V6.2
  "sa", "sa_type_todd", "sa_p6_modulation",
  "sa_note", "sources_utilisees", "variables",
  "conditions_initiales", "conditions_initiales_finales",
  "commandes", "commandes_finales", "cmd_linear",
  "parametres_simulation", "alertes_actives", "alertes_conv_a",  // alertes_conv_a fiches V6.2
  "defi_mepa", "params_p",
  "cluster_libelle", "raison_loi_physique", "trajectoire_attendue_libelle",
  "date_codage", "codeur", "statut",                   // champs standard fiche étalon
]);

// Variables NC bloquantes (source: mepa_constants.json, fallback)
const NC_BLOQUANTES = (() => {
  if (CONSTANTS && CONSTANTS.nc_protocol && CONSTANTS.nc_protocol.variables_nc_bloquantes)
    return new Set(CONSTANTS.nc_protocol.variables_nc_bloquantes);
  return new Set(["E_split", "gamma", "EROI", "Sa"]);
})();

// Contraintes par WP
const CONTRAINTES_WP = (WHITELIST && WHITELIST.contraintes_par_wp)
  ? WHITELIST.contraintes_par_wp
  : {
    "WP-C1-1": { cluster: "C1", EROI_min: 1.01, EROI_max: 2.5, cmd_linear_requis: true, note: "Haïti 2010-2024 — EROI dynamique 1.2→2.0. Ancre plancher corpus." },
    "WP-F1-1": { cmd_linear_requis: true, cluster: "C1" },
    "WP-F2-1": { cmd_linear_requis: true, A_r_ne_max: 0.00, cluster: "C1" },
    "WP-F3-1": { cmd_linear_requis: true, cluster: "C1" },
    "WP-F10-1": { t_max: 80, cluster: "C2" },
    "WP-I3-1": { sa_p6_mult: true, cluster: "C5" },
    "WP-I4-1": { sa_p6_mult: true, cluster: "C2" },
    "WP-I9-1": { sa_p6_mult: true, cluster: "C4" },
    "WP-I10-1": { cmd_linear_requis: true, cluster: "C1" },
    "WP-C4-1": { EROI_max: 2.0, cluster: "C1" },
  };

// ── P_DEFAULTS : chargés depuis mepa_constants.json si disponible (BUG-006)
// Fallback embarqué = valeurs opérationnelles calibrées V6.2 (inchangées).
// Priorité : constants.bornes_parametres_dynamiques[k].defaut > fallback.
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

function _isNC(val) {
  return typeof val === "string" && val.trim().toUpperCase() === "NC";
}

function _toNum(val) {
  if (_isNC(val) || val === null || val === undefined) return null;
  const n = Number(val);
  return isNaN(n) ? null : n;
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
  version_audit: "2.1.0",
  wp_id: null,
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

// ============================================================================
// C13 - DETECTION VARIABLES NC (PREMIER - avant C9 whitelist et C2/C3 types)
// RAISON : C9 verifie les cles racine, C2/C3 verifient les types numeriques.
// Si "NC" apparait dans cmd avant que C13 soit passe, C2 rejetterait "NC"
// comme type incorrect (string au lieu de number) - masquant la vraie cause.
// En executant C13 en premier et en quittant sur NC bloquant, on garantit
// un message d'erreur precis et une sortie DONNEES_INSUFFISANTES distincte.
// ============================================================================
{
  const vars_fiche = fiche.variables || {};
  const cmd_fiche  = fiche.commandes || fiche.commandes_finales || {};
  let c13_ok = true;

  for (const [varName, entry] of Object.entries(vars_fiche)) {
    if (!entry || typeof entry !== "object") continue;
    if (!_isNC(entry.valeur)) continue;
    if (NC_BLOQUANTES.has(varName)) {
      nc_bloquantes_det.push(varName);
      c13_ok = false;
    } else {
      nc_non_bloquantes_det.push(varName);
      warnings.push(`C13 - NC non bloquant : '${varName}'. Simulation autorisee. CCI degrade. Signale dans Passeport.`);
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
        nc_bloquantes: nc_bloquantes_det,
        nc_non_bloquantes: nc_non_bloquantes_det,
        nb_erreurs: 1,
        nb_warnings: warnings.length,
        audit_log,
        message: `[C13 NC BLOQUANT] ${wp_id || "?"} - Variables NC bloquantes : [${nc_bloquantes_det.join(", ")}]. Escalade Architecte. Statut DONNEES_INSUFFISANTES != INVALIDE : fiche bien formee, sources historiques insuffisantes. Action : enrichissement sources CONV-E.`,
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
  const manquants = ["wp_id","cas","cluster","sa","trajectoire_attendue","variables"].filter(k => fiche[k] == null);
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
    if (_isNC(raw)) continue; // NC non bloquant deja accepte par C13
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
// C5 - LABELS D4 (7 labels officiels Runner V6.2, au caractere pres)
// ============================================================================
{
  const traj = fiche.trajectoire_attendue || "";
  const labels_recus = traj.split("->").concat(traj.split("\u2192")).map(l => l.trim()).filter(Boolean);
  // Deduplique et teste chaque label
  const labels_uniq = [...new Set(labels_recus)];
  const labels_inv  = labels_uniq.filter(l => !LABELS_D4.includes(l));
  if (labels_inv.length > 0) {
    erreurs.push(`C5 - Labels D4 non conformes : [${labels_inv.map(l=>`'${l}'`).join(", ")}]. Autorises : ${LABELS_D4.join(" | ")}`);
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
// V6.2 Fortifiee : validation par plage (non plus valeur fixe 0.30/0.22).
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
// C10 - CONTRAINTES SPECIFIQUES PAR WP
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
      nb_erreurs:   erreurs.length,
      nb_warnings:  warnings.length,
      audit_log,
      message: `[AUDIT FAIL] ${wp_id || "?"} - ${erreurs.length} erreur(s) structurelle(s) - pipeline suspendu. Action : recodage CONV-E.`,
    }
  }];
}

// ============================================================================
// CONSTRUCTION runner_config - SORTIE VALIDE
// ============================================================================

const cmd    = fiche.commandes || fiche.commandes_finales || {};
const ci     = fiche.conditions_initiales || fiche.conditions_initiales_finales || {};
const params = fiche.parametres_simulation || {};
const params_p_fiche = fiche.params_p || {};

// ARCH-013 RESOLU : y0 garantie liste [S,L,C,I]
// simulate() attend y0 = [S0, L0, C0, I0] (liste).
// Si ci est un dict {S0, L0, C0, I0} (format standard fiche) -> conversion ici.
// Si ci est deja une liste (cas futur) -> pass-through.
const y0 = Array.isArray(ci)
  ? [parseFloat(ci[0])||1.0, parseFloat(ci[1])||0.5, parseFloat(ci[2])||0.1, parseFloat(ci[3])||3.5]
  : [_toNum(ci.S0)??1.0, _toNum(ci.L0)??0.5, _toNum(ci.C0)??0.1, _toNum(ci.I0)??3.5];

// ARCH-014 RESOLU : theta_C/I injectes dans params (ou run_wp() les lit via p.get())
// ET conserves a la racine pour logging.
const theta_C = _toNum(params.theta_C) ?? 0.30;
const theta_I = _toNum(params.theta_I) ?? 0.22;
const t_max   = _toNum(params.t_max)   ?? 300;

// Fusion params_p : fiche > defaults, theta_C/I inclus -> ARCH-014
const params_runner = { ...P_DEFAULTS, ...params_p_fiche, theta_C, theta_I };

// Bloc cmd nettoye
const cmd_clean = {};
for (const key of CMD_OBLIGATOIRES) {
  if (key in cmd) cmd_clean[key] = _isNC(cmd[key]) ? cmd[key] : (_toNum(cmd[key]) ?? cmd[key]);
}

// runner_config complet
const runner_config = {
  wp_id,
  cas:                  fiche.cas,
  cluster,
  trajectoire_attendue: fiche.trajectoire_attendue,
  sa:                   sa_int,
  y0,         // liste [S,L,C,I] - ARCH-013
  t_max,
  theta_C,    // racine pour logging
  theta_I,    // racine pour logging
  cmd:        cmd_clean,
  cmd_linear: fiche.cmd_linear || null,
  params:     params_runner,  // theta_C/I inclus - ARCH-014
  nc_non_bloquantes: nc_non_bloquantes_det,
};

// ARCH-015 RESOLU : chemins canoniques via MEPA_SCRIPTS_DIR
const config_path = `/tmp/${wp_id}_runner_config.json`;
const result_path = `/tmp/${wp_id}_result.json`;
const n1_path     = `/tmp/${wp_id}_n1_sensitivity.json`;
const runner_cmd  = `python3 ${MEPA_SCRIPTS_DIR}/mepa_runner_v2_gamma.py ${config_path}`;
const n1_cmd      = `python3 ${MEPA_SCRIPTS_DIR}/mepa_sensitivity_n1.py ${config_path} ${n1_path}`;

// llm_context pour CONV-A (gamma JSON -> gamma redactionnel = gamma)
const llm_context = {
  wp_id,
  cas:                  fiche.cas,
  periode:              fiche.periode,
  cluster,
  sa:                   sa_int,
  trajectoire_attendue: fiche.trajectoire_attendue,
  mepa_full_vars: {
    "E_split": fiche.variables?.E_split?.valeur,
    "gamma":   fiche.variables?.gamma?.valeur,  // cle JSON - symbole dans le texte
    "A_d_eff": fiche.variables?.A_d_eff?.valeur,
    "A_r_c":   fiche.variables?.A_r_c?.valeur,
    "A_r_ne":  fiche.variables?.A_r_ne?.valeur,
    "Cs":      fiche.variables?.Cs?.valeur,
    "L_t":     fiche.variables?.L_t?.valeur,
    "EROI":    fiche.variables?.EROI?.valeur,
    "Sa":      fiche.variables?.Sa?.valeur,
  },
  nc_non_bloquantes: nc_non_bloquantes_det,
  alertes:            fiche.alertes_actives || [],
  defi_mepa:          fiche.defi_mepa       || "",
};

return [{
  json: {
    statut_audit:       "VALIDE",
    wp_id,
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
      `[AUDIT OK] ${wp_id} - 13 controles passes` +
      (warnings.length > 0 ? ` (${warnings.length} warning(s))` : "") +
      (nc_non_bloquantes_det.length > 0 ? ` [NC non bloquant : ${nc_non_bloquantes_det.join(", ")}]` : "")
    ),
  }
}];
