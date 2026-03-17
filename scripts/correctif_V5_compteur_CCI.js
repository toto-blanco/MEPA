// ============================================================================
// MEPA V6.2 — CORRECTIF V5 — Nœud "Compteur Kappa & Fail-Safe"
// Type n8n : Code (JavaScript) — exécution côté serveur
// Position dans WF1 : après le nœud de calcul kappa_calculator.py
// ============================================================================
//
// LOGIQUE :
//   1. Lit le résultat kappa depuis l'input ($json.kappa_report)
//   2. Lit le compteur d'itérations courant depuis le Master Register
//   3. Route vers : SUITE (CONV-A) | BOUCLE (retour CONV-E) | SUSPENSION
//
// SORTIES (branches n8n à créer après ce nœud) :
//   output[0]  → "CERTIFIÉ"    → suite vers CONV-A (nœud 4)
//   output[1]  → "RÉVISION"    → retour vers CONV-E (nœud 1) avec instructions
//   output[2]  → "SUSPENDU"    → alerte + inscription Master Register + STOP
//
// PARAMÈTRES CONFIGURABLES (modifier ici uniquement)
// ============================================================================

const MAX_ITERATIONS   = 3;       // Protocole §2.2 : max 2 révisions + initial
const SEUIL_VALIDE     = 0.70;    // CCI par variable ≥ 0.70 → condition nécessaire
const SEUIL_GLOBAL     = 0.75;    // CCI global ≥ 0.75 → condition suffisante (Addendum §P1)
const SEUIL_REVISION   = 0.55;    // 0.55 ≤ CCI global < 0.75 → RÉVISION
                                   // CCI global < 0.55 → REJET direct (compte comme 1 tentative)
// Note : la certification requiert les DEUX conditions simultanément :
//   kappa_report.kappa >= SEUIL_VALIDE (CCI par variable)
//   kappa_report.cci   >= SEUIL_GLOBAL (CCI global agrégé)
// Le champ kappa_report.kappa est un alias de cci (calculateur V2 — compatibilité)

// ── CHEMINS (infrastructure réelle Raspberry Pi 5) ─────────────────────────
const MASTER_REGISTER_PATH = "/data/mepa/master_register/master_register.json";
const LOG_PATH             = "/data/mepa/master_register/master_register_log.txt";

// ============================================================================
// CORPS DU NŒUD — NE PAS MODIFIER EN DESSOUS DE CETTE LIGNE
// ============================================================================

const fs   = require("fs");
const path = require("path");

// ── 1. Lecture des inputs ───────────────────────────────────────────────────
const input        = $input.item.json;
const wp_id        = input.wp_id;
const iteration    = input.iteration || 1;         // ex : 1, 2, 3 (entier)
const iteration_s  = String(iteration).padStart(3, "0"); // "001", "002", "003"

// Rapport κ produit par kappa_calculator.py
const kappa_report = input.kappa_report || {};
const kappa        = parseFloat(kappa_report.kappa ?? -1);
const kappa_verdict_calc = kappa_report.verdict || "INCONNU";

// ── 2. Lecture Master Register ──────────────────────────────────────────────
let master = {};
try {
  if (fs.existsSync(MASTER_REGISTER_PATH)) {
    master = JSON.parse(fs.readFileSync(MASTER_REGISTER_PATH, "utf8"));
  }
} catch (e) {
  // Master Register absent ou illisible → on initialise
  master = {};
}

// Entrée du WP dans le Master Register (crée si absente)
if (!master[wp_id]) {
  master[wp_id] = {
    wp_id,
    statut: "EN_COURS",
    iterations_total: 0,
    iterations_history: [],
    kappa_final: null,
    verdict_final: null,
    result_sha256: null,
    certified_at: null,
  };
}

const entry = master[wp_id];
entry.iterations_total = iteration;  // synchronisation avec i{NNN}

// ── 3. Décision de routage ──────────────────────────────────────────────────
let decision;         // "CERTIFIE" | "REVISION" | "SUSPENDU"
let output_index;     // 0 | 1 | 2
let message;

// Lire CCI global (champ cci) en plus du seuil par variable (champ kappa = alias cci)
const cci_global = parseFloat(kappa_report.cci ?? kappa_report.kappa ?? -1);

if (kappa >= SEUIL_VALIDE && cci_global >= SEUIL_GLOBAL) {
  // ── CAS A : CCI ≥ 0.70 (par var) ET CCI global ≥ 0.75 → CERTIFIÉ ────────
  decision     = "CERTIFIE";
  output_index = 0;
  message      = `[OK] ${wp_id} i${iteration_s} — CCI=${kappa.toFixed(4)} (par var ≥ ${SEUIL_VALIDE}) + CCI_global=${cci_global.toFixed(4)} (≥ ${SEUIL_GLOBAL}) → CERTIFIÉ → suite CONV-A`;

  entry.statut        = "CCI_OK";
  entry.kappa_final   = kappa;
  entry.cci_global    = cci_global;
  entry.verdict_final = "CERTIFIÉ";

} else if (iteration < MAX_ITERATIONS) {
  // ── CAS B : κ insuffisant ET itérations restantes ────────────────────────
  const remaining = MAX_ITERATIONS - iteration;
  decision     = "REVISION";
  output_index = 1;
  message      = `[RÉVISION] ${wp_id} i${iteration_s} — κ=${kappa.toFixed(4)} < ${SEUIL_VALIDE} → révision (${remaining} tentative(s) restante(s))`;

  entry.statut = "REVISION_EN_COURS";
  // Construire instructions de correction pour CONV-E
  const desaccords = kappa_report.desaccords || [];
  entry.instructions_revision = {
    iteration_suivante: iteration + 1,
    iteration_suivante_s: String(iteration + 1).padStart(3, "0"),
    desaccords_a_corriger: desaccords,
    kappa_actuel: kappa,
    kappa_cible: SEUIL_VALIDE,
    message_conv_e: buildRevisionMessage(wp_id, kappa, desaccords, iteration),
  };

} else {
  // ── CAS C : MAX_ITERATIONS atteint → SUSPENSION ──────────────────────────
  decision     = "SUSPENDU";
  output_index = 2;
  message      = `[ALERTE] ${wp_id} i${iteration_s} — κ=${kappa.toFixed(4)} après ${MAX_ITERATIONS} tentatives → SUSPENDED_KAPPA`;

  entry.statut       = "SUSPENDED_KAPPA";
  entry.kappa_final  = kappa;
  entry.verdict_final = "SUSPENDU";
  entry.suspended_at  = new Date().toISOString();
  entry.suspension_reason = `CCI=${kappa.toFixed(4)} (seuil var=${SEUIL_VALIDE}) / CCI_global=${cci_global.toFixed(4)} (seuil global=${SEUIL_GLOBAL}) insuffisant(s) après ${MAX_ITERATIONS} itérations`;
}

// Historique toujours enregistré
entry.iterations_history.push({
  iteration: iteration_s,
  kappa,
  verdict: kappa_verdict_calc,
  timestamp: new Date().toISOString(),
});

// ── 4. Écriture Master Register ─────────────────────────────────────────────
try {
  fs.mkdirSync(path.dirname(MASTER_REGISTER_PATH), { recursive: true });
  fs.writeFileSync(MASTER_REGISTER_PATH, JSON.stringify(master, null, 2), "utf8");
} catch (e) {
  console.error("[ERREUR] Impossible d'écrire le Master Register :", e.message);
}

// ── 5. Log horodaté ─────────────────────────────────────────────────────────
const log_line = `${new Date().toISOString()} | ${message}\n`;
try {
  fs.mkdirSync(path.dirname(LOG_PATH), { recursive: true });
  fs.appendFileSync(LOG_PATH, log_line, "utf8");
} catch (e) {
  console.error("[ERREUR] Impossible d'écrire le log :", e.message);
}

// ── 6. Construction du payload de sortie ────────────────────────────────────
const output_payload = {
  // Identifiants
  wp_id,
  iteration,
  iteration_s,

  // Décision de routage
  decision,
  output_index,
  message,

  // Données κ
  kappa,
  kappa_verdict: kappa_verdict_calc,

  // Transmission en aval
  kappa_report,
  runner_config: input.runner_config || {},
  llm_context:   input.llm_context   || {},

  // Pour le nœud SUSPENSION (output 2)
  suspension: decision === "SUSPENDU" ? {
    wp_id,
    iterations_effectuees: iteration,
    kappa_final: kappa,
    reason: entry.suspension_reason,
    action_requise: "Intervention manuelle Architecte — révision fiche codage ou paramètres",
    master_register_mis_a_jour: true,
  } : null,

  // Pour le nœud RÉVISION (output 1)
  revision: decision === "REVISION" ? entry.instructions_revision : null,
};

// ── 7. Retour n8n avec routage sur output_index ──────────────────────────────
// Configuration dans n8n : ajouter un nœud "Switch" en aval sur le champ
// output_payload.decision avec les cas "CERTIFIE", "REVISION", "SUSPENDU"
return [output_payload];


// ============================================================================
// FONCTION HELPER : construction du message de révision pour CONV-E
// ============================================================================
function buildRevisionMessage(wp_id, kappa, desaccords, iteration) {
  const lines = [
    `RÉVISION REQUISE — ${wp_id} — Itération ${iteration}/${MAX_ITERATIONS}`,
    `CCI actuel = ${kappa.toFixed(4)} (seuil par variable requis : ${SEUIL_VALIDE})`,
    `CCI global = (voir kappa_report.cci) (seuil global requis : ${SEUIL_GLOBAL})`,
    ``,
    `Points de désaccord à réviser :`,
  ];
  if (desaccords && desaccords.length > 0) {
    desaccords.forEach(d => {
      lines.push(`  • ${d.variable} : val_conv_e=${d.val_a} / val_conv_b=${d.val_b} (écart=${d.ecart})`);
    });
  } else {
    lines.push(`  (Consulter kappa_report.desaccords pour le détail)`)
  }
  lines.push(``);
  lines.push(`Règles de résolution (Protocole §2.2) :`);
  lines.push(`  1. Variables continues : si écart ≤ 2.0 → moyenne arithmétique`);
  lines.push(`  2. Variables catégorielles (Sa) : confrontation obligatoire Architecte`);
  lines.push(`  3. Source N-supérieur prime sur codage observationnel`);
  lines.push(`  4. gamma et L_t : cf. fiche_codage_FINALE pour règles d'arbitrage`);
  return lines.join("\n");
}
