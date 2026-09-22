#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""control_figuras.py — comprueba que cada lámina de elaboración propia de
«El dispositivo caldereño» diga, cerca de su \\includegraphics, dónde está el
script que la dibuja, y que ese script exista en este repositorio.

Es el control del aspecto 13 de la rúbrica («cada figura derivada de un
procesamiento propio indica dónde está el script o la planilla que la
produce»). Vive acá y no con el libro porque su insumo son los scripts de este
repositorio; el control de los recuentos del aparato vive con el main.tex.

    python3 scripts/control_figuras.py /ruta/al/libro

Sale con código 1 si alguna figura propia no declara su script o si declara uno
que no está en scripts/.
"""
import os, re, sys, glob

VENTANA = 2500          # caracteres alrededor del \includegraphics
PREFIJO = 'fig-'        # así se llaman las figuras de elaboración propia

def main(libro):
    aqui = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(aqui)
    disponibles = {os.path.basename(p) for p in glob.glob(os.path.join(aqui, '*.py'))}

    tex = {}
    for pat in ('main.tex', 'cap/*.tex', 'ape/*.tex'):
        for f in sorted(glob.glob(os.path.join(libro, pat))):
            tex[os.path.relpath(f, libro)] = open(f, encoding='utf-8').read()
    if not tex:
        print(f'no encuentro .tex en {libro}'); return 2

    todo = '\n'.join(tex.values())
    propias = sorted({os.path.basename(x)
                      for x in re.findall(r'includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', todo)
                      if os.path.basename(x).startswith(PREFIJO)})

    sin_declarar, fantasma, ok = [], [], []
    for fig in propias:
        base = re.escape(fig.rsplit('.', 1)[0])
        declarados = set()
        for f, t in tex.items():
            for m in re.finditer(base, t):
                trozo = t[m.start(): m.start() + VENTANA]
                for s in re.findall(r'scripts/([A-Za-z0-9_\\]+\.py)', trozo):
                    declarados.add(s.replace('\\_', '_'))
        if not declarados:
            sin_declarar.append(fig)
        else:
            faltan = declarados - disponibles
            (fantasma if faltan else ok).append((fig, sorted(declarados), sorted(faltan)))

    print('=' * 78)
    print('CONTROL DE FIGURAS PROPIAS — aspecto 13 de la rúbrica')
    print(f'repositorio: {repo}')
    print(f'libro:       {os.path.abspath(libro)}')
    print('=' * 78)
    for fig, decl, _ in ok:
        print(f'  ok  {fig:<34} -> {", ".join(decl)}')
    for fig, decl, faltan in fantasma:
        print(f'  X   {fig:<34} -> declara {", ".join(decl)}, '
              f'y NO está en scripts/: {", ".join(faltan)}')
    for fig in sin_declarar:
        print(f'  X   {fig:<34} -> SIN SCRIPT DECLARADO')
    print('-' * 78)
    print(f'  figuras propias: {len(propias)}   con script: {len(ok)}   '
          f'sin declarar: {len(sin_declarar)}   declarado pero ausente: {len(fantasma)}')

    huerfanos = sorted(s for s in disponibles
                       if s.startswith(('mapa_', 'tabla_')) and s not in
                       {d for _, ds, _ in ok for d in ds})
    if huerfanos:
        print(f'  scripts de figura que ninguna lámina declara: {", ".join(huerfanos)}')
    print('=' * 78)
    mal = len(sin_declarar) + len(fantasma)
    if mal:
        print(f'{mal} figura(s) restan 5 puntos cada una en el aspecto 13.')
        print('Se arregla de una de dos maneras, y las dos son legítimas:')
        print('  a) subir el script al repositorio y nombrarlo en el epígrafe;')
        print('  b) declarar en el apéndice de fuentes que esa lámina todavía')
        print('     no es reproducible paso a paso. Lo que no vale es callarlo.')
    else:
        print('Todas las láminas propias declaran un script que existe.')
    return 1 if mal else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '.'))
