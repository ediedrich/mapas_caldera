#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bajar_capas.py — baja del Release las capas que no viven en git y las abre
en datos/. Ver datos/LEEME.md para qué es cada una y de dónde sale.

    python scripts/bajar_capas.py [tag]

Por defecto usa el tag 'capas'. No pisa las capas propias (cargos/, ribera/).
"""
import io, sys, zipfile, urllib.request
from pathlib import Path

REPO = 'ediedrich/mapas_caldera'
PROPIAS = {'cargos', 'ribera'}
D = Path(__file__).resolve().parents[1] / 'datos'


def main(tag='capas'):
    url = f'https://github.com/{REPO}/releases/download/{tag}/capas.zip'
    print('bajando', url)
    try:
        datos = urllib.request.urlopen(url, timeout=120).read()
    except Exception as e:
        print('no se pudo bajar:', e)
        print('Si el Release todavia no existe, subir capas.zip con:')
        print(f'  gh release create {tag} --repo {REPO} capas.zip')
        return 1
    print(f'{len(datos) / 1e6:.1f} MB')
    z = zipfile.ZipFile(io.BytesIO(datos))
    n = 0
    for m in z.namelist():
        p = Path(m)
        if p.parts and p.parts[0] in PROPIAS:
            continue
        z.extract(m, D)
        n += 1
    print(f'{n} archivos en {D}')
    for d in sorted(x for x in D.iterdir() if x.is_dir()):
        peso = sum(f.stat().st_size for f in d.rglob('*') if f.is_file())
        print(f'  {d.name:<16} {peso / 1e6:7.1f} MB'
              + ('   (propia, en git)' if d.name in PROPIAS else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'capas'))
