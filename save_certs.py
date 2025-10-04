#!/usr/bin/env python3
"""
save_certs.py
Usage: python save_certs.py <path-to-image1> <path-to-image2> ...
Copies provided image files into the local img/ folder and writes img/list.json
"""
import sys
from pathlib import Path
import shutil
import json

IMG_DIR = Path(__file__).resolve().parent / 'img'
IMG_DIR.mkdir(parents=True, exist_ok=True)

def is_image(p: Path):
    return p.suffix.lower() in {'.jpg','.jpeg','.png','.gif','.webp','.svg','.bmp'}

def unique_dest(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem = dest.stem
    suffix = dest.suffix
    i = 1
    while True:
        candidate = dest.with_name(f"{stem}-{i}{suffix}")
        if not candidate.exists():
            return candidate
        i += 1

def main(args):
    saved = []
    for src in args:
        p = Path(src).expanduser().resolve()
        if not p.exists():
            print(f"Skipping (not found): {src}")
            continue
        if not is_image(p):
            print(f"Skipping (not an image): {src}")
            continue
        dest = IMG_DIR / p.name
        dest = unique_dest(dest)
        try:
            shutil.copy2(p, dest)
            saved.append(dest.name)
            print(f"Copied: {p} -> {dest}")
        except Exception as e:
            print(f"Failed to copy {src}: {e}")

    if saved:
        list_path = IMG_DIR / 'list.json'
        existing = []
        if list_path.exists():
            try:
                existing = json.loads(list_path.read_text(encoding='utf8'))
                if not isinstance(existing, list):
                    existing = []
            except Exception:
                existing = []
        merged = list(dict.fromkeys(existing + saved))
        try:
            list_path.write_text(json.dumps(merged, indent=2), encoding='utf8')
            print('Updated img/list.json')
        except Exception as e:
            print('Failed to write list.json:', e)
    else:
        print('No images copied. img/list.json not updated.')

    print('\nDone. Open certificates.html to view the images.')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python save_certs.py <path-to-image1> <path-to-image2> ...')
        sys.exit(1)
    main(sys.argv[1:])
