# -*- coding: utf-8 -*-
"""Qué del Boletín Oficial leyó el libro, año por año, 1908-1950.

Cruza dos tablas de datos/boletin/: el índice de ediciones presentes en los
Releases de boletines-salta (1910-1943) y el estado de lectura que declara el
apéndice de fuentes del libro. Los números de edición ausentes se calculan como
los huecos de la numeración correlativa dentro del índice.

Lo que el gráfico NO puede decir: si una edición presente está en blanco (el
índice no lo distingue), ni qué hay en 1908, 1909 y 1944-1950, que no tienen
Release en ese repositorio.
"""
from base import plt, mpl, FIG, Patch, Line2D
import pandas as pd, numpy as np
from pathlib import Path

D = Path(__file__).resolve().parents[1] / 'datos' / 'boletin'
ed = pd.read_csv(D / 'ediciones_repositorio.csv')
# ediciones que no estan en el indice pero se leyeron de la copia del autor
fu = pd.read_csv(D / 'ediciones_fuera_del_indice.csv')
LEIDAS_FUERA = set(fu[fu.estado == 'leida'].edicion)
est = pd.read_csv(D / 'estado_lectura.csv')

por_anio = ed.groupby('anio').edicion.agg(['count', 'min', 'max'])
todas = set(ed.edicion)
aus = [e for e in range(ed.edicion.min(), ed.edicion.max() + 1) if e not in todas]
aus_idx = list(aus)
aus = [e for e in aus if e not in LEIDAS_FUERA]
def anio_de(e):
    prev = ed[ed.edicion < e].sort_values('edicion')
    return int(prev.anio.iloc[-1]) if len(prev) else int(ed.anio.min())
aus_anio = pd.Series([anio_de(e) for e in aus_idx], index=aus_idx)
print('ausentes en el índice:', len(aus), aus)

# las 31 que el apéndice F enumera como faltantes de la ventana 962-2464
F31 = list(range(977, 991)) + list(range(1037, 1043)) + [1095, 1146, 1305, 1312, 1318,
       1320, 1323, 1327, 1356, 1512, 1564]
assert len(F31) == 31
# las que el libro declara ausentes fuera de esa ventana (advertencia y apéndice F)
DECL = set(F31) | {438, 444, 470, 487, 488, 489, 490, 491, 492, 493, 581, 640, 703, 793, 822, 837, 838}
presentes_hoy = [e for e in F31 if e in todas]
print('de las 31 del apéndice F, presentes hoy en el índice:', len(presentes_hoy))
no_enumeradas = [e for e in aus if 962 <= e <= 2464 and e not in F31]
print('leidas fuera del indice:', sorted(LEIDAS_FUERA))
print('ausentes en la ventana que el apéndice no enumera:', no_enumeradas)

COL = {'leido': '#1f4e5f', 'parcial': '#8fb0bd', 'barrido': '#d9b44a'}
ROT = {'leido': 'Leído edición por edición y verificado sobre la imagen',
       'parcial': 'Leído en parte (1922: primer semestre)',
       'barrido': 'Barrido automático, sin lectura sobre la imagen'}

fig = plt.figure(figsize=(8.27, 5.6))
ax = fig.add_axes([0.08, 0.36, 0.89, 0.44])
ax.set_xlim(1907.3, 1950.7); ax.set_ylim(0, 118)
for _, r in est.iterrows():
    ax.axvspan(r.desde - 0.5, r.hasta + 0.5, ymin=0, ymax=0.035, color=COL[r.estado], lw=0)
for a, r in por_anio.iterrows():
    e = est[(est.desde <= a) & (est.hasta >= a)].estado.iloc[0]
    ax.bar(a, r['count'], color=COL[e], width=0.72, zorder=3)
for a in (1908, 1909, 1944, 1945, 1946, 1947, 1948, 1949, 1950):
    e = est[(est.desde <= a) & (est.hasta >= a)].estado.iloc[0]
    ax.bar(a, 118, color='none', ec=COL[e], hatch='////', lw=0.6, width=0.72, zorder=2)
for e, a in aus_anio.items():
    if 917 <= e <= 938:
        continue
    k = list(aus_anio[aus_anio == a].index).index(e)
    if e in LEIDAS_FUERA:
        mk = dict(marker='^', color='#3d6b57', ms=4.5)
    elif e not in DECL:
        mk = dict(marker='x', color='#b03030', ms=4.5, mew=1.2)
    else:
        mk = dict(marker='o', mfc='white', mec='#b03030', ms=4, mew=1.0)
    ax.plot(a, por_anio.loc[a, 'count'] + 3.5 + k * 3.8, ls='', zorder=5, **mk)
ax.text(1922, 60, 'sin archivo\n917–938', ha='center', fontsize=5.4, color='#555555', rotation=90)
ax.set_ylabel('ediciones en el repositorio', fontsize=6.6)
ax.set_xticks(range(1908, 1951, 2)); ax.tick_params(labelsize=6, length=2)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
ax.grid(axis='y', color='#e4e0d6', lw=0.4, zorder=0)

leg = [Patch(fc=COL[k], label=v) for k, v in ROT.items()]
leg += [Patch(fc='none', ec='#555555', hatch='////', label='Año sin Release en el repositorio: no se puede contar'),
        Line2D([], [], marker='o', mfc='white', mec='#b03030', ls='', label='Ausente, y el apéndice lo declara'),
        Line2D([], [], marker='x', color='#b03030', ls='', mew=1.2, label='Ausente, y el apéndice no lo declaraba'),
        Line2D([], [], marker='^', color='#3d6b57', ls='', label='Fuera del índice, leída de la copia del autor')]
fig.legend(handles=leg, loc='lower left', bbox_to_anchor=(0.07, 0.115), ncol=2, frameon=False,
           fontsize=6.0, labelspacing=0.6, columnspacing=1.5)

fig.text(0.05, 0.965, 'Qué del Boletín Oficial leyó este libro, 1908–1950', fontsize=11.5, weight='bold')
fig.text(0.05, 0.935,
         f'Barras: ediciones de cada año presentes en el repositorio de donde se leyó. De las 31 que el apéndice de fuentes da por faltantes en la\n'
         f'ventana 1923–1945, {len(presentes_hoy)} están hoy en el índice; siguen ausentes {", ".join(str(e) for e in F31 if e in aus)}, y las 1312, 1318, 1320,\n'
         f'1323 y 1327 están pero en blanco. De las 2028 a 2032, que el índice no tiene y el apéndice no enumeraba, cuatro se leyeron de la copia\n'
         f'del autor; falta sólo la {no_enumeradas[0]}, del 26 de noviembre de 1943.',
         fontsize=6.6, va='top', color='#333333', linespacing=1.55)
fig.text(0.05, 0.055,
         'Fuentes: lista de assets de los Releases 1910–1943 de github.com/ediedrich/boletines-salta (consultada el 24 de septiembre de 2026); estado de lectura, apéndice\n'
         'de fuentes del libro; ediciones 2028, 2029, 2031 y 2032, copia del autor. Una edición presente puede estar en blanco: el índice no lo distingue. Elaboración propia con\nscripts/grafico_boletin.py y datos/boletin/.',
         fontsize=5.5, va='top', color='#333333', linespacing=1.6)
fig.savefig(FIG / 'fig-boletin-cobertura.png', dpi=300)
print('ok', FIG / 'fig-boletin-cobertura.png')
