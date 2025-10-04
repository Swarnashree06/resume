#!/usr/bin/env python3
"""
embed_certs.py
Usage: python embed_certs.py <image1> <image2> ...
Creates certificates_embedded.html with up to 5 images embedded as base64 data URLs.
"""
import sys
from pathlib import Path
import base64
import mimetypes

OUT = Path(__file__).resolve().parent / 'certificates_embedded.html'
MAX_SLOTS = 5

TEMPLATE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Certificates (embedded)</title>
<style>
:root{--line:#e5e7eb;--muted:#6b7280;--paper:#ffffff;--accent:#111827}
body{font-family:Inter, system-ui, -apple-system, 'Segoe UI', Roboto, Arial;margin:0;background:#f6f7f9;color:var(--accent);padding:28px}
.container{max-width:1100px;margin:0 auto}
h1{margin:0 0 12px 0}
.gallery{display:flex;flex-wrap:wrap;gap:12px}
.slot{width:220px;height:150px;background:#fff;border:1px solid var(--line);border-radius:6px;display:flex;align-items:center;justify-content:center;overflow:hidden}
.slot img{max-width:100%;max-height:100%;display:block}
.placeholder{color:var(--muted);font-size:14px;padding:8px;text-align:center}
</style>
</head>
<body>
<div class="container">
<h1>Certificates (embedded)</h1>
<div class="gallery">
{slots}
</div>
<div style="margin-top:18px">
<a href="index.html">Back to Resume</a>
</div>
</div>
</body>
</html>
'''

SLOT_IMG = '<div class="slot"><img src="{src}" alt="Certificate {i}"/></div>'
SLOT_PLACE = '<div class="slot"><div class="placeholder">Empty slot {i}</div></div>'


def make_data_url(path: Path):
    mime, _ = mimetypes.guess_type(str(path))
    if mime is None:
        mime = 'application/octet-stream'
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode('ascii')
    return f'data:{mime};base64,{b64}'


def main(args):
    imgs = []
    for p in args[:MAX_SLOTS]:
        path = Path(p).expanduser().resolve()
        if not path.exists():
            print(f'Warning: {path} not found, skipping')
            continue
        try:
            src = make_data_url(path)
            imgs.append(src)
            print(f'Embedded: {path.name}')
        except Exception as e:
            print(f'Failed to embed {path}: {e}')

    slots_html = ''
    for i in range(MAX_SLOTS):
        if i < len(imgs):
            slots_html += SLOT_IMG.format(src=imgs[i], i=i+1) + '\n'
        else:
            slots_html += SLOT_PLACE.format(i=i+1) + '\n'

    OUT.write_text(TEMPLATE.format(slots=slots_html), encoding='utf8')
    print(f'Wrote {OUT}')
    print('Open this file in your browser to view the embedded certificates.')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python embed_certs.py <image1> <image2> ...')
        sys.exit(1)
    main(sys.argv[1:])
