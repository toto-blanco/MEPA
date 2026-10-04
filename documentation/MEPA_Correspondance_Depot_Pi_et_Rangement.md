# MEPA — Correspondance dépôt ↔ Pi et rangement proposé

**Base :** comparaison du dossier de référence (`~/Documents/projets/projet_MEPA/simulations_WP/mepa`, 598 fichiers) et de `/media/devmon/CloudFamilleBC/antoine/files/mepa` sur le Pi (503 fichiers), scans du 2026-10-03.

## 1. Ce qui est sain

- **Scripts exécutés** : les 20 fichiers de `scripts/` sur le Pi sont identiques au dépôt.
- **Constantes actives** : `scripts/mepa_constants.json` sur le Pi = `config/mepa_constants.json` du dépôt (v1.4.0, `be8046cc`).
- **Fiches V7 de référence** : les 6 fiches de `config/v7/` sont identiques au dépôt (Rwanda `76ac8471`, etc.).
- **Séquenceur V7** : il lit `${MEPA_CONFIG_DIR}/v7/<fiche>`, donc les fiches de référence. Empreinte du fichier séquenceur dans le dépôt : `178522deea83`. Sa conformité avec la version chargée dans n8n sera vérifiée au run de contrôle.
- **Aucune whitelist dans `scripts/`** sur le Pi : celle de mars est bien en quarantaine. La v3.0.0 du dépôt se trouve dans `config/`, où personne ne la lit (§3).

## 2. Table de correspondance des chemins

| Dépôt | Pi (hôte) | Vue conteneur | Lu par |
|---|---|---|---|
| `scripts/*.py`, `scripts/*.js` | `…/mepa/scripts/` | `/data/mepa/scripts/` | runner, calculateur, schéma, Nœud 2 (code embarqué identique), préflight |
| `config/mepa_constants.json` | `…/mepa/scripts/mepa_constants.json` | `/data/mepa/scripts/mepa_constants.json` | runner, calculateur, Nœud 2, contrôle de cohérence |
| `scripts/mepa_deploy_manifest.json` | `…/mepa/scripts/` | `/data/mepa/scripts/` | Contrôle A (DEP3) |
| `config/v7/WP-*_v7.json` | `…/mepa/config/v7/` | `/data/mepa/config/v7/` | séquenceur (`fiche_path`), Nœud A |
| `config/mepa_whitelist_keys.json` (v3.0.0, `6b0876f8`) | `…/mepa/config/mepa_whitelist_keys.json` (identique) | `/data/mepa/config/` | **personne** : le Nœud 2 la cherche dans `scripts/` et, ne la trouvant pas, utilise sa copie embarquée (voir §3) |
| `workflow_n8n/*.json` | `…/mepa/workflow_n8n/` | — | **aucun** : n8n exécute depuis sa base ; les fichiers servent à l'import |
| `outputs/` (ignoré par git) | absent (à recréer) | `/data/mepa/outputs/` | Nœud 7 (écriture) |

**Règle de déploiement :** `config/mepa_constants.json` du dépôt est copié dans `scripts/` sur le Pi. C'est l'emplacement que lisent les scripts (`MEPA_SCRIPTS_DIR`). Le manifeste DEP3 suit la copie déployée.

## 3. Points à trancher

1. **Whitelist : configuration désignée ou implicite ?** La whitelist v3.0.0 du dépôt est présente sur le Pi dans `config/`, mais le Nœud 2 la cherche dans `scripts/` (`MEPA_SCRIPTS_DIR`). Il ne la trouve pas et utilise sa copie embarquée, sans le signaler. C'est d'ailleurs ce qui a permis à la whitelist de mars, restaurée dans `scripts/`, de prendre la main sans être vue. C'est exactement le cas visé par la décision DEP5 §2.3. Je recommande de désigner explicitement la source (fichier déployé, suivi par DEP3, empreinte au manifeste), et de faire échouer le Nœud 2 si le fichier désigné manque, au lieu de basculer silencieusement sur la copie embarquée. À intégrer au lot de déploiement.
2. **Quatre fiches V7 à la racine de `config/`** (Haïti, Égypte, Rome, Rwanda), absentes du dépôt et différentes des fiches de référence. Elles ne sont lues ni par le séquenceur ni par les scripts, mais un lancement manuel avec un mauvais chemin les utiliserait. Si tu connais leur origine, dis-le : sinon, quarantaine.

## 4. Rangement proposé (à valider par toi : déplacement vers `quarantaine_2026-10-03/`, aucune suppression)

| Fichier sur le Pi | Taille | sha256 | Motif |
|---|---|---|---|
| `.gitignore` | 348 | `a0f969308081` | fichier restauré (ancienne version ou mauvais emplacement) |
| `CLAUDE.md` | 11577 | `090c8f22809a` | fichier restauré (ancienne version ou mauvais emplacement) |
| `CV13_test_report.md` | 11620 | `41c8f2743f2f` | fichier restauré (ancienne version ou mauvais emplacement) |
| `config/MEPA_V62_Ordre_de_Marche_1_WP-C1-1.json` | 13208 | `2fc2fa15ca08` | ancienne disposition ; le dépôt la range sous config/v6.2/MEPA_V62_Ordre_de_Marche_1_WP-C1-1.json |
| `config/WP-C1-1_Haiti_v7.json` | 23604 | `9d2431f2a7d4` | fiche V7 de provenance inconnue, absente du dépôt, non lue par le séquenceur |
| `config/WP-C1-1_Islande_Medievale.json` | 29527 | `66ca0be8214f` | ancienne disposition ; le dépôt la range sous candidats/WP-EXT-5_Islande_Medievale.json |
| `config/WP-C1_Haiti_v62.json` | 12406 | `a15ae12c5e49` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-C1-1_Haiti_v62.json |
| `config/WP-C2-1_Egypte2011_v7.json` | 24456 | `e57246c9a1f3` | fiche V7 de provenance inconnue, absente du dépôt, non lue par le séquenceur |
| `config/WP-C2_Egypte2011_v62.json` | 13775 | `2b39db917b78` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-C2-1_Egypte2011_v62.json |
| `config/WP-C3_Argentine_v62.json` | 14608 | `c731bd63790e` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-C3-1_Argentine_v62.json |
| `config/WP-C4_Liban_v62.json` | 15296 | `0eeb52ef727a` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-C4-1_Liban_v62.json |
| `config/WP-C5_Iran_v62.json` | 15485 | `e9c2252151e0` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-C5-1_Iran_v62.json |
| `config/WP-C6_ChineXi_v62.json` | 16568 | `23ed38bc45f9` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-C6-1_ChineXi_v62.json |
| `config/WP-F1-1_RomeIIIe_v7.json` | 27226 | `26c13a179cf7` | fiche V7 de provenance inconnue, absente du dépôt, non lue par le séquenceur |
| `config/WP-F10_CommuneParis_v62.json` | 13767 | `059a564f5590` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-F10-1_CommuneParis_v62.json |
| `config/WP-F1_RomeIIIe_v62.json` | 13178 | `cf839034633d` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-F1-1_RomeIIIe_v62.json |
| `config/WP-F2_RomeTardive_v62.json` | 13871 | `cdc88e0daff6` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-F2-1_RomeTardive_v62.json |
| `config/WP-F3_MayaClassique_v62.json` | 14407 | `86b634b20ee5` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-F3-1_MayaClassique_v62.json |
| `config/WP-F4_EgypteAncienne_v62.json` | 14242 | `d3ec04127533` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-F4-1_EgypteAncienne_v62.json |
| `config/WP-F5_VeniseDéclin_v62.json` | 14296 | `7031fb55e7c2` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-F5-1_VeniseDéclin_v62.json |
| `config/WP-F6-1_EmpireOttoman_v62.json` | 14874 | `7c704cdbe2b6` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-F6-1_EmpireOttoman_v62.json |
| `config/WP-F7_RevolutionHaitienne_v62.json` | 15202 | `c9e5fc0908d4` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-F7-1_RevolutionHaitienne_v62.json |
| `config/WP-F8_FranceRevolutionnaire_v62.json` | 13775 | `571049636d46` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-F8-1_FranceRevolutionnaire_v62.json |
| `config/WP-F9_AngleterreStabilite_v62.json` | 14830 | `26f52eec9904` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-F9-1_AngleterreStabilite_v62.json |
| `config/WP-I10-1_Rwanda_v62.json` | 13479 | `5effb0aab3df` | absent du dépôt |
| `config/WP-I10-1_Rwanda_v7.json` | 27797 | `70536cb22c6e` | fiche V7 de provenance inconnue, absente du dépôt, non lue par le séquenceur |
| `config/WP-I1_AngleterreIndustrielle_v62.json` | 15439 | `5dd56a61110c` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-I1-1_AngleterreIndustrielle_v62.json |
| `config/WP-I2_Russie1917_v62.json` | 14653 | `00613087112c` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-I2-1_Russie1917_v62.json |
| `config/WP-I3-1_JaponMeijiGuerre_v62.json` | 15903 | `c60c18d283e2` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-I3-1_JaponMeijiGuerre_v62.json |
| `config/WP-I4_AllemagneNazie_v62.json` | 16283 | `e20872bb9770` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-I4-1_AllemagneNazie_v62.json |
| `config/WP-I5-1_EspagneGuerreCivile_v62.json` | 14289 | `c675df5f1b3c` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-I5-1_EspagneGuerreCivile_v62.json |
| `config/WP-I6-1_Tiananmen_v62.json` | 14975 | `ebd0650e8228` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-I6-1_Tiananmen_v62.json |
| `config/WP-I7-1_URSS_v62.json` | 14842 | `60e673b8ae23` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-I7-1_URSS_v62.json |
| `config/WP-I8-1_ChineDeng_v62.json` | 15390 | `6ba4134ca202` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-I8-1_ChineDeng_v62.json |
| `config/WP-I9-1_Singapour_v62.json` | 15840 | `620fb6052146` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-I9-1_Singapour_v62.json |
| `config/WP-T1-1_GuerreSecession_v62.json` | 15056 | `13933980d27e` | ancienne disposition ; le dépôt la range sous config/v6.2/WP-T1-1_GuerreSecession_v62.json |
| `config/fiche_codage_template_WP-C1-1_Islande.json` | 15333 | `b96b6f687ab2` | absent du dépôt |
| `config/fiche_etalon_WP-C1-1_Haiti_v62.json` | 14072 | `c504d59da364` | ancienne disposition ; le dépôt la range sous config/v6.2/fiche_etalon_WP-C1-1_Haiti_v62.json |
| `config/fiche_etalon_WP-EXT-5_Islande_v62.json` | 19916 | `44f0fdbf9d76` | absent du dépôt |
| `config/mepa_constants.json` | 37066 | `154ed376cde0` | constantes v1.3.0 périmées ; le pipeline lit scripts/mepa_constants.json (v1.4.0) |
| `config/mepa_workflow_n8n_V62.json` | 32212 | `82320b4b667a` | absent du dépôt |
| `config/v7/WP-C1-1_Haiti_v7 (restored).json` | 19443 | `0f08eb42b0de` | copie restaurée par erreur |
| `config/v7/WP-C2-1_Egypte2011_v7 (restored).json` | 21446 | `4afb0ff280a7` | copie restaurée par erreur |
| `config/v7/WP-F1-1_RomeIIIe_v7 (restored).json` | 20501 | `aac56dcc134f` | copie restaurée par erreur |
| `config/v7/WP-F10-1_CommuneParis_v7 (restored).json` | 22888 | `76055558355d` | copie restaurée par erreur |
| `config/v7/WP-I4-1_AllemagneNazie_v7 (restored 2).json` | 26042 | `275bf58b11d2` | copie restaurée par erreur |
| `config/v7/WP-I4-1_AllemagneNazie_v7 (restored).json` | 26020 | `754693e4cf6b` | copie restaurée par erreur |
| `workflow_n8n/mepa_workflow_cv12_pilot.json` | 81281 | `d83f9c51ad5c` | différent du dépôt ou absent ; n8n exécute depuis sa base, pas depuis ce fichier |
| `workflow_n8n/mepa_workflow_n8n_V62.json` | 136484 | `c59058525289` | différent du dépôt ou absent ; n8n exécute depuis sa base, pas depuis ce fichier |
| `workflow_n8n/mepa_workflow_n8n_V62_multipass.json` | 143352 | `d80688b2a324` | différent du dépôt ou absent ; n8n exécute depuis sa base, pas depuis ce fichier |
| `workflow_n8n/mepa_workflow_n8n_V62_sequencer.json` | 18322 | `68cb959e77d1` | différent du dépôt ou absent ; n8n exécute depuis sa base, pas depuis ce fichier |
| `workflow_n8n/mepa_workflow_n8n_V62_sequencer_TEST3.json` | 15228 | `b114a3fae354` | différent du dépôt ou absent ; n8n exécute depuis sa base, pas depuis ce fichier |
| `workflow_n8n/mepa_workflow_n8n_V7.json` | 163425 | `59bd05f47232` | différent du dépôt ou absent ; n8n exécute depuis sa base, pas depuis ce fichier |

Total : 53 fichiers. Non concernés : `sauvegarde_outputs/` (historique, à verser dans `mepa-registre/archives/` selon DEP5), `archives/`, `restauration/`, `quarantaine_2026-10-03/`, `tests/`, `tools/`, `documentation/`.

## 5. Présent seulement sur le dépôt (information)

- Les décisions `MEPA_Decision/`, les fichiers de référence `tests/golden/`, `tests/test_advisory_v7_nonregression.py`, et les workflows `audit_seul`, `mesure_conv_e` et `V7_sequencer` : ils ne sont pas nécessaires sur le Pi pour l'exécution.
- **Le test T6 (`mepa_test_rampe_segmentation.py`) est absent du dépôt** : toujours en attente.
