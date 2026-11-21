#!/usr/bin/env python3
"""Build the public copy of Kelma (papathibs.github.io/kelma-learn) from this repo.

Usage: python3 tools/build-public.py <path to kelma-learn clone> [stats URL]

Same app, with: no quotes, no private Library decks, its own storage and service-worker cache,
and anonymous usage counts as part of using it. Run it before every publish so both sites match."""
import json, re, shutil, sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
DST = Path(sys.argv[1]).resolve()
STATS = sys.argv[2] if len(sys.argv) > 2 else ''
KEEP = ['.nojekyll', 'guide.html', 'instructions.txt', 'instructions-school.txt', 'jszip.min.js', 'opusdec.min.js',
        'lame.min.js', 'manifest.webmanifest', 'icon-180.png', 'icon-192.png', 'icon-512.png']

def die(msg):
    sys.exit('build-public: ' + msg)

if not (DST / '.git').exists():
    die(f'{DST} is not a git clone')
# clear the old build, keep git
for p in DST.iterdir():
    if p.name == '.git':
        continue
    shutil.rmtree(p) if p.is_dir() else p.unlink()

for name in KEEP:
    shutil.copy2(SRC / name, DST / name)
shutil.copytree(SRC / 'setup', DST / 'setup')
(DST / 'library').mkdir()
(DST / 'library' / 'index.json').write_text('{"decks":[]}\n')

html = (SRC / 'index.html').read_text()
site_old = "const SITE={id:'kelma',public:false,home:'papathibs.github.io/kelma',statsUrl:''};"
if html.count(site_old) != 1:
    die('SITE line not found')
html = html.replace(site_old, "const SITE={id:'kelma-learn',public:true,home:'papathibs.github.io/kelma-learn',statsUrl:%s};" % json.dumps(STATS))
html, n = re.subn(r'const QUOTES=\[.*?\];\n', 'const QUOTES=[];\n', html, count=1, flags=re.S)
if n != 1:
    die('QUOTES not found')
(DST / 'index.html').write_text(html)

sw = (SRC / 'sw.js').read_text()
sw, n = re.subn(r"const V='kelma-v(\d+)';", r"const V='kelma-learn-v\1';", sw, count=1)
if n != 1:
    die('sw version not found')
(DST / 'sw.js').write_text(sw)

(DST / 'README.md').write_text('# Kelma\n\nA simple flashcard app for learning Moroccan Darija with your own lesson words and voice notes.\n\nLive: https://papathibs.github.io/kelma-learn/\n\nThis copy is built from papathibs/kelma by tools/build-public.py. Make changes there, not here.\n')

# nothing private may leave
private = ['Preston Fidler', 'rri-question', 'Kyle', 'papathibs.github.io/kelma\'', 'cora-']
for f in DST.rglob('*'):
    if f.is_file() and '.git' not in f.parts and f.suffix in ('.html', '.js', '.json', '.txt', '.md'):
        t = f.read_text(errors='ignore')
        for w in private:
            if w in t:
                die(f'"{w}" found in {f.relative_to(DST)}')
print('public build ok:', DST)
