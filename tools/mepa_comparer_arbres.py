#!/usr/bin/env python3
"""
mepa_comparer_arbres.py — v1.0 — LECTURE SEULE
Compare le dossier de référence (dépôt local d'Antoine) et le contenu du Pi.

1) scan    : python3 mepa_comparer_arbres.py scan <dossier> <sortie.json> [--exclure motif ...]
             Liste chaque fichier : chemin relatif, taille, sha256. N'écrit que <sortie.json>.
2) comparer: python3 mepa_comparer_arbres.py comparer <ref.json> <pi.json> <rapport.md>
             Produit : identiques (même chemin, même empreinte) ; différents (même chemin,
             empreinte différente) ; même contenu à un autre chemin (correspondance dépôt ↔ Pi) ;
             présents seulement sur la référence ; présents seulement sur le Pi.
Exclusions par défaut : .git, __pycache__, node_modules, .nextcloud*, .owncloud*, *.pyc.
"""
import hashlib, json, os, sys, fnmatch, datetime

EXCL_DEFAUT = ['.git', '__pycache__', 'node_modules', '.nextcloud*', '.owncloud*', '*.pyc', '.sync_*']

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

def exclu(nom, motifs): return any(fnmatch.fnmatch(nom, m) for m in motifs)

def scan(racine, sortie, motifs):
    fichiers = {}
    for d, dirs, files in os.walk(racine):
        dirs[:] = [x for x in dirs if not exclu(x, motifs)]
        for f in files:
            if exclu(f, motifs): continue
            p = os.path.join(d, f)
            if os.path.islink(p) or not os.path.isfile(p): continue
            rel = os.path.relpath(p, racine)
            try: fichiers[rel] = {'taille': os.path.getsize(p), 'sha256': sha(p)}
            except PermissionError: fichiers[rel] = {'taille': None, 'sha256': 'ILLISIBLE'}
    json.dump({'racine': os.path.abspath(racine), 'date': datetime.datetime.now().isoformat(),
               'n': len(fichiers), 'fichiers': fichiers}, open(sortie, 'w'), indent=1, ensure_ascii=False)
    print(f'{len(fichiers)} fichiers → {sortie}')

def comparer(ref_p, pi_p, out):
    R, P = json.load(open(ref_p)), json.load(open(pi_p))
    r, p = R['fichiers'], P['fichiers']
    ident = sorted(k for k in r if k in p and r[k]['sha256'] == p[k]['sha256'])
    diff = sorted(k for k in r if k in p and r[k]['sha256'] != p[k]['sha256'])
    seul_r = sorted(k for k in r if k not in p); seul_p = sorted(k for k in p if k not in r)
    idx_p = {}
    for k in seul_p: idx_p.setdefault(p[k]['sha256'], []).append(k)
    corresp = [(k, idx_p[r[k]['sha256']]) for k in seul_r if r[k]['sha256'] in idx_p]
    L = [f"# Comparaison référence ↔ Pi", '',
         f"- Référence : `{R['racine']}` ({R['n']} fichiers, scan {R['date'][:19]})",
         f"- Pi : `{P['racine']}` ({P['n']} fichiers, scan {P['date'][:19]})", '',
         f"| Catégorie | Nombre |", "|---|---|",
         f"| Identiques (même chemin, même empreinte) | {len(ident)} |",
         f"| Différents (même chemin, empreinte différente) | {len(diff)} |",
         f"| Même contenu, autre chemin (correspondance) | {len(corresp)} |",
         f"| Seulement sur la référence | {len(seul_r)} |",
         f"| Seulement sur le Pi | {len(seul_p)} |", '']
    def bloc(titre, lignes):
        L.append(f'## {titre}'); L.append('')
        L.extend(lignes or ['(aucun)']); L.append('')
    bloc('Différents', [f"- `{k}` — réf {r[k]['sha256'][:12]} / Pi {p[k]['sha256'][:12]}" for k in diff])
    bloc('Correspondance dépôt ↔ Pi (même empreinte)', [f"- `{a}` ↔ " + ', '.join(f'`{x}`' for x in b) for a, b in corresp])
    bloc('Seulement sur le Pi', [f"- `{k}` ({p[k]['taille']} o, {p[k]['sha256'][:12]})" for k in seul_p])
    bloc('Seulement sur la référence', [f"- `{k}`" for k in seul_r])
    open(out, 'w').write('\n'.join(L) + '\n')
    print(f'rapport → {out} | identiques {len(ident)} · différents {len(diff)} · correspondances {len(corresp)} · seuls réf {len(seul_r)} · seuls Pi {len(seul_p)}')

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] not in ('scan', 'comparer'): print(__doc__); sys.exit(2)
    if a[0] == 'scan':
        motifs = EXCL_DEFAUT + (a[a.index('--exclure') + 1:] if '--exclure' in a else [])
        scan(a[1], a[2], motifs)
    else:
        comparer(a[1], a[2], a[3])
