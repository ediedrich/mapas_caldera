# -*- coding: utf-8 -*-
"""Quien administra el departamento de La Caldera, 1908-1946.

No es un mapa: es la linea de tiempo de los cargos del departamento, un
segmento por titular, con el estado de la Comision Municipal arriba y los
cuatro episodios de tutela marcados con una linea vertical.

Los datos NO estan en el codigo: salen de tres tablas de datos/cargos/, que
son el lugar donde se corrigen y se amplian.

  titulares.csv  cargo, titular, desde, hasta, exacta_desde, exacta_hasta,
                 acto, fuente
  comision.csv   estado, desde, hasta, exacta_desde, exacta_hasta, acto, fuente
  tutela.csv     fecha, rotulo, acto

REGLA DE HONESTIDAD, que es el punto del grafico. Un borde de segmento puede
ser una fecha documentada -el acto que nombra o que acepta la renuncia- o una
fecha que este libro no tiene. Los bordes documentados se dibujan a tope; los
NO documentados se dibujan degradados hacia afuera, de modo que el dibujo
diga donde termina lo que el archivo prueba. Las columnas exacta_desde y
exacta_hasta, con 1 o 0, son lo que decide eso.

Se importa base.py para que la tipografia y la ruta de figuras sean las mismas
que las de los mapas; no usa ninguna capa cartografica.
"""
from base import plt, mpl, FIG, Patch, Line2D
import pandas as pd
from pathlib import Path
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

D = Path(__file__).resolve().parents[1] / 'datos' / 'cargos'
Y0, Y1 = 1908, 1948                      # el eje, en anios decimales

CARGOS = ['Comisaria de policia', 'Juzgado de paz', 'Registro civil',
          'Receptoria de rentas', 'Subcomisaria de Mojotoro',
          'Subcomisaria de Vaqueros']
ROTULO = {'Comisaria de policia': 'Comisaría de policía',
          'Juzgado de paz': 'Juzgado de paz',
          'Registro civil': 'Registro Civil',
          'Receptoria de rentas': 'Receptoría de rentas',
          'Subcomisaria de Mojotoro': 'Subcomisaría de Mojotoro',
          'Subcomisaria de Vaqueros': 'Subcomisaría de Vaqueros'}

# el estado de la Comision Municipal: un color por especie, no por persona
COLEST = {'En funciones': '#4f7d4a',
          'Designada por decreto': '#c4452f',
          'Designada por Interventor Nacional': '#7a0f1c',
          'Intervenida': '#3b2f6b',
          'Acefala': '#111111',
          'Desintegrada': '#8a8375',
          'Sin comision municipal': '#e8e3d6'}
ESTXT = {'Sin comision municipal': '#555555', 'Desintegrada': '#ffffff'}

AZUL = ['#1f4e5f', '#5a8ca0', '#2f6a80', '#8fb0bd', '#3d6b57', '#7d9a3c',
        '#b5651d', '#c98a2b']


def dec(s):
    """fecha ISO -> anio decimal"""
    t = pd.Timestamp(s)
    ini = pd.Timestamp(year=t.year, month=1, day=1)
    fin = pd.Timestamp(year=t.year + 1, month=1, day=1)
    return t.year + (t - ini) / (fin - ini)


def barra(ax, y, x0, x1, alto, color, ex0, ex1, zorder=3):
    """Una barra con los bordes no documentados degradados hacia afuera."""
    n = 256
    g = np.ones((1, n))
    if not ex0:
        k = min(n // 3, n)
        g[0, :k] = np.linspace(0.12, 1, k)
    if not ex1:
        k = min(n // 3, n)
        g[0, n - k:] = np.linspace(1, 0.12, k)
    cm = LinearSegmentedColormap.from_list('x', ['#ffffff', color])
    ax.imshow(g, extent=(x0, x1, y - alto / 2, y + alto / 2), aspect='auto',
              cmap=cm, vmin=0, vmax=1, zorder=zorder, interpolation='bilinear')


# ancho de un caracter, en anios del eje, a la escala de esta figura
CHAR = 0.285


# cuatro alturas alternadas para los rotulos que no entran en su barra: con
# dos no alcanza, porque en 1922 y 1923 hay cuatro titulares en pocos meses
NIVEL = [1, -1, 2, -2]


def texto(ax, y, x0, x1, s, k, color='white', fs=5.0, alto=0.52):
    """Dentro de la barra si entra; si no, afuera, escalonado en cuatro
    alturas y con una linea guia. Es lo unico que evita que los segmentos de
    pocos meses se pisen entre si."""
    if len(s) * CHAR <= (x1 - x0) - 0.15:
        ax.text((x0 + x1) / 2, y, s, va='center', ha='center', fontsize=fs,
                color=color, zorder=6)
        return
    n = NIVEL[k % len(NIVEL)]
    xm = (x0 + x1) / 2
    dy = (alto / 2) * np.sign(n) + 0.155 * n
    ax.plot([xm, xm], [y + (alto / 2) * np.sign(n), y + dy], color='#999999',
            lw=0.4, zorder=5)
    ax.text(xm, y + dy + 0.012 * np.sign(n), s, ha='center', fontsize=fs - 0.3,
            va='bottom' if n > 0 else 'top', color='#333333', zorder=6)


# ------------------------------------------------------------------ datos
tit = pd.read_csv(D / 'titulares.csv')
com = pd.read_csv(D / 'comision.csv')
tut = pd.read_csv(D / 'tutela.csv')
for df in (tit, com):
    df['x0'] = df.desde.map(dec)
    df['x1'] = df.hasta.map(dec)

print(f'titulares: {len(tit)} segmentos, {tit.titular.nunique()} personas, '
      f'{tit.cargo.nunique()} cargos')
print(f'comision: {len(com)} tramos de estado')
n_ex = int(tit.exacta_desde.sum() + tit.exacta_hasta.sum())
print(f'bordes documentados: {n_ex} de {2 * len(tit)} '
      f'({100 * n_ex / (2 * len(tit)):.0f} %)')
for c in CARGOS:
    s = tit[tit.cargo == c]
    print(f'  {ROTULO[c]:<26} {len(s):2d} segmentos')

# ------------------------------------------------------------------ figura
fig = plt.figure(figsize=(8.27, 8.5))
ax = fig.add_axes([0.195, 0.235, 0.735, 0.635])
ax.set_xlim(Y0, Y1)

FIL = 1.52
YCOM = 0.55                                   # la Comision, arriba de todo
ys = {c: -(i + 1) * FIL for i, c in enumerate(CARGOS)}
ax.set_ylim(min(ys.values()) - 0.95, YCOM + 0.78)

# bandas de anio, para leer el eje sin regla
for a in range(Y0, Y1):
    if a % 2 == 0:
        ax.axvspan(a, a + 1, color='#f4f2ed', lw=0, zorder=0)
for a in range(Y0, Y1 + 1, 5):
    ax.axvline(a, color='#cdc4b0', lw=0.5, zorder=1)

# --- fila de la Comision Municipal
for _, r in com.iterrows():
    col = COLEST[r.estado]
    barra(ax, YCOM, r.x0, r.x1, 0.62, col, r.exacta_desde, r.exacta_hasta, 4)
    if r.x1 - r.x0 > 2.4:
        et = {'En funciones': 'en funciones',
              'Designada por decreto': 'designada por decreto',
              'Designada por Interventor Nacional': 'designada por\nInterventor Nacional',
              'Sin comision municipal': 'sin comisión municipal',
              'Intervenida': 'intervenida'}.get(r.estado, r.estado.lower())
        ax.text((r.x0 + r.x1) / 2, YCOM, et, va='center', ha='center',
                fontsize=5.0, color=ESTXT.get(r.estado, 'white'),
                linespacing=1.15, zorder=6)
ax.text(Y0 - 0.30, YCOM, 'Comisión Municipal', va='center', ha='right',
        fontsize=7.0, weight='bold')
ax.axhline(YCOM - 0.52, color='#999999', lw=0.7, zorder=2)

# --- filas de los cargos unipersonales
for i, c in enumerate(CARGOS):
    y = ys[c]
    sub = tit[tit.cargo == c].sort_values('x0').reset_index(drop=True)
    for j, r in sub.iterrows():
        col = AZUL[j % len(AZUL)]
        barra(ax, y, r.x0, r.x1, 0.46, col, r.exacta_desde, r.exacta_hasta)
        texto(ax, y, r.x0, r.x1, r.titular, k=j, alto=0.46)
    ax.text(Y0 - 0.30, y, ROTULO[c], va='center', ha='right', fontsize=7.0)
    ax.axhline(y - FIL / 2, color='#e4e0d6', lw=0.5, zorder=1)

# --- los cuatro episodios de tutela
ybot = min(ys.values()) - 0.90
for k, (_, r) in enumerate(tut.iterrows()):
    x = dec(r.fecha)
    ax.plot([x, x], [ybot, YCOM + 0.45], color='#7a0f1c', lw=1.0, ls=(0, (4, 2)),
            zorder=7)
    ax.plot(x, YCOM + 0.45, marker='v', ms=4, color='#7a0f1c', zorder=7)
    ax.text(x, YCOM + 0.60, f'{pd.Timestamp(r.fecha).year}', ha='center',
            va='bottom', fontsize=5.6, color='#7a0f1c', weight='bold')

ax.set_yticks([])
ax.set_xticks(range(Y0, Y1 + 1, 4))
ax.set_xticklabels([str(a) for a in range(Y0, Y1 + 1, 4)], fontsize=6)
ax.tick_params(length=2, pad=2)
for s in ('top', 'right', 'left'):
    ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color('#888888')

# ------------------------------------------------------------------ textos
fig.text(0.05, 0.972, 'Quién administra el departamento de La Caldera, 1908--1946',
         fontsize=11, weight='bold', ha='left')
fig.text(0.05, 0.941,
         'Un segmento por titular, en los años leídos edición por edición del Boletín Oficial. Arriba, el estado del cuerpo municipal.\n'
         'Los bordes degradados son los que el archivo no fecha: el segmento sigue, y lo que termina ahí es la prueba.',
         fontsize=7, ha='left', color='#333333', linespacing=1.5)

leg = [Patch(fc=COLEST['En funciones'], label='Comisión en funciones'),
       Patch(fc=COLEST['Designada por decreto'], label='Comisión designada por decreto'),
       Patch(fc=COLEST['Designada por Interventor Nacional'], label='Designada por un Interventor Nacional'),
       Patch(fc=COLEST['Intervenida'], label='Intervenida'),
       Patch(fc=COLEST['Acefala'], label='Acéfala'),
       Patch(fc=COLEST['Desintegrada'], label='Desintegrada'),
       Patch(fc=COLEST['Sin comision municipal'], ec='#cdc4b0', label='Sin comisión municipal'),
       Line2D([], [], color='#7a0f1c', lw=1.0, ls=(0, (4, 2)), marker='v', ms=4,
              label='Episodio de tutela')]
fig.legend(handles=leg, loc='lower left', bbox_to_anchor=(0.055, 0.062),
           frameon=False, fontsize=6.0, ncol=2, handlelength=1.3,
           handletextpad=0.5, columnspacing=1.4, labelspacing=0.45)

import textwrap
notas = '\n'.join(textwrap.fill(f'{pd.Timestamp(r.fecha).year}  {r.rotulo}. {r.acto}',
                                72, subsequent_indent='      ')
                  for _, r in tut.iterrows())
fig.text(0.560, 0.158, 'Los episodios de tutela', fontsize=6.4,
         weight='bold', va='top')
fig.text(0.560, 0.143, notas, fontsize=4.9, va='top', linespacing=1.55,
         color='#333333')

fig.text(0.055, 0.034,
         'Fuente: decretos, resoluciones y edictos del Boletín Oficial de Salta de los años 1908--1946 leídos edición por edición\n'
         '(apéndice de fuentes). Elaboración propia con scripts/grafico_cargos.py y datos/cargos/ del repositorio mapas_caldera.',
         fontsize=5.6, va='top', color='#333333', linespacing=1.6)

fig.savefig(FIG / 'fig-cargos-linea.png', dpi=300)
print('ok', FIG / 'fig-cargos-linea.png')
