# -*- coding: utf-8 -*-
"""Dónde caen hoy los topónimos que el Estado usó para nombrar el departamento
entre 1909 y 1948, coloreados por en cuántas de las trece nóminas aparecen."""
from base import *
from tabla_parajes import T, BAHRA, NC     # la tabla es la fuente única
import geopandas as gpd

FINCA = {r[NC]: (n, sum(r[:NC])) for n, *r in T if r[NC]}
c = cat.copy()
c['nom'] = c.finca.map(lambda f: FINCA.get(f, (None, None))[0])
c['n']   = c.finca.map(lambda f: FINCA.get(f, (None, None))[1])
hit  = c[c.nom.notna()].copy()
rest = c[c.nom.isna()]
print('parcelas con topónimo:', len(hit), 'de', len(c), ' topónimos ubicados:', hit.nom.nunique())

pj = gpd.read_file(D / 'habitat' / 'parajes_bahra.gpkg')
lo = gpd.read_file(D / 'habitat' / 'localidades_bahra.gpkg')
pj = pj[pj.nom_depto.str.contains('Caldera', na=False)]
lo = lo[lo.nom_depto.str.contains('Caldera', na=False)]
solo_bahra = {'Pueblo (La Caldera)'}          # los demás de BAHRA ya salen por finca

COL = {1: '#dcd3c0', 2: '#dcd3c0', **{k: '#8fb0bd' for k in range(3, 12)},
       12: '#2f6a80', 13: '#1a3d4d'}
ext  = (-65.72, -24.755, -65.16, -24.36)
extB = (-65.44, -24.72, -65.34, -24.58)

fig = plt.figure(figsize=(8.27, 10.6))
axA = fig.add_axes([0.055, 0.470, 0.90, 0.455])
axB = fig.add_axes([0.055, 0.105, 0.44, 0.330])
axL = fig.add_axes([0.515, 0.105, 0.44, 0.330]); axL.axis('off')

for ax, e in ((axA, ext), (axB, extB)):
    base_axes(ax, e)
    rest.plot(ax=ax, fc='#f7f3ea', ec='#ddd7c8', lw=0.15, zorder=1)
    for k, rango in ((1, [1, 2]), (3, list(range(3, 12))), (12, [12, 13])):
        sel = hit[hit.n.isin(rango)]
        if len(sel):
            sel.plot(ax=ax, fc=COL[k], ec='#6f665a', lw=0.2, zorder=3)
    outline(ax)

axA.set_title('A. Departamento La Caldera: las parcelas cuyo nombre de finca es uno de los topónimos de 1909–1948')
axB.set_title('B. El corredor La Caldera–Vaqueros')
box(axA, extB, 'B')
towns(axA, fs=7); towns(axB, fs=7.5)
pjc = pj.copy(); pjc['geometry'] = pjc.geometry.representative_point()
pjc.plot(ax=axA, marker='^', markersize=18, color='#c98a2b', edgecolor='black', linewidth=0.5, zorder=11)
scalebar(axA, -65.70, -24.742, 5); north(axA, -65.20, -24.40)
scalebar(axB, -65.434, -24.712, 2); north(axB, -65.347, -24.712)

sin = [n for n, *r in T if not r[NC] and n not in BAHRA]
leg = [Patch(fc=COL[12], ec='#6f665a', label='Nombre presente en doce o trece de las trece nóminas'),
       Patch(fc=COL[3], ec='#6f665a', label='Presente en tres a once'),
       Patch(fc=COL[1], ec='#6f665a', label='Presente en una o dos'),
       Line2D([], [], marker='^', ls='', ms=5, mfc='#c98a2b', mec='black', mew=0.5,
              label='Paraje de BAHRA en el departamento'),
       Patch(fc='#f7f3ea', ec='#ddd7c8', label='Parcela sin nombre de finca o con otro nombre')]
axL.legend(handles=leg, loc='upper left', bbox_to_anchor=(0, 1.0), frameon=False, fontsize=7,
           handlelength=1.5, labelspacing=0.85)
axL.text(0, 0.60, f'Y {len(sin)} de los {len(T)} topónimos no se dibujan,\nporque no tienen hoy lugar ni en el catastro\nni en BAHRA:',
         fontsize=7, va='top', weight='bold', linespacing=1.5, transform=axL.transAxes)
axL.text(0, 0.47, '   '.join([', '.join(sin[:8]) + ',', ', '.join(sin[8:16]) + ',', ', '.join(sin[16:]) + '.']),
         fontsize=6.4, va='top', wrap=True, transform=axL.transAxes, linespacing=1.6)
axL.text(0, 0.16, 'El color no mide superficie ni dominio: mide en cuántas de las trece\n'
                  'nóminas oficiales de 1909 a 1948 aparece ese nombre. La geometría\n'
                  'es la de la parcela que hoy lleva ese nombre en el campo «finca»\n'
                  'del catastro, y la coincidencia es de nombre, no de deslinde.',
         fontsize=6.3, va='top', color='#333333', linespacing=1.6, transform=axL.transAxes)

fig.savefig(FIG / 'fig-parajes-mapa.png', dpi=300)
print('ok', FIG / 'fig-parajes-mapa.png')
