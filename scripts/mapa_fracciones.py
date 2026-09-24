# -*- coding: utf-8 -*-
"""Las tres fracciones censales del departamento, 2022: población joven,
viviendas sin hogar residente y hogares sin agua de red.

Sostiene el cruce del capítulo 21 («El departamento que no está en los
expedientes») y el apartado sobre El Gallinato del capítulo 26: la fracción
66077-03, el sector oriental, es la de menos jóvenes, más viviendas vacías y
peor cobertura de red.

Los números NO están en el código: salen de datos/censo_tablas/fracciones_2022.csv.
La geometría es la de los radios del Censo 2022 (datos/censo/, del Release).
La escuela es el punto del Mapa Educativo Nacional (IGN), que la registra como
«Ex Nº 198»; el libro la cita por su número actual, 4118.
"""
from base import *
import geopandas as gpd
import textwrap

C = pd.read_csv(D / 'censo_tablas' / 'fracciones_2022.csv', dtype={'fraccion': str})
C['FRAC'] = C.fraccion.str[-2:]
fr = frac.reset_index().merge(C, on='FRAC')

pj = gpd.read_file(D / 'habitat' / 'parajes_bahra.gpkg')
pj = pj[pj.nom_depto.str.contains('Caldera', na=False)]
esc = gpd.read_file(D / 'habitat' / 'establecimientos_educativos_ign.gpkg')
esc = esc[esc.fna.str.contains('Gustavo Mart', na=False)]
vial = [gpd.read_file(D / 'vial' / f) for f in ('red_nacional_ign.gpkg', 'red_provincial_ign.gpkg')]

ext = (-65.72, -24.76, -65.16, -24.36)
# rótulos de fracción: la 03 se corre al este para no pisar el pueblo
LP = {'03': (-65.245, -24.575)}
PANELES = [('edad_15_29_pct', 'A. Población de 15 a 29 años', 'Greens', '% de las personas'),
           ('viviendas_sin_hogar_pct', 'B. Viviendas sin hogar residente', 'Oranges', '% de las viviendas'),
           ('hogares_sin_agua_red_pct', 'C. Hogares sin agua por red pública', 'Blues', '% de los hogares')]

fig = plt.figure(figsize=(8.27, 10.2))
pos = [[0.05, 0.535, 0.44, 0.34], [0.53, 0.535, 0.44, 0.34], [0.05, 0.145, 0.44, 0.34]]
for (col, tit, cm, uni), p in zip(PANELES, pos):
    ax = fig.add_axes(p)
    base_axes(ax, ext, grid=False)
    ax.set_xticks([]); ax.set_yticks([])
    v = fr[col]
    fr.plot(ax=ax, column=col, cmap=cm, vmin=v.min() * 0.6, vmax=v.max() * 1.05,
            ec='#444444', lw=0.6, zorder=2)
    for g in vial:
        g.plot(ax=ax, color='#8a8375', lw=0.5, zorder=3)
    outline(ax, lw=1.2)
    for _, r in fr.iterrows():
        c = r.geometry.representative_point()
        x, y = LP.get(r.FRAC, (c.x, c.y))
        ax.text(x, y, f"{r.fraccion}\n{r[col]:.1f} %".replace('.', ','), ha='center',
                va='center', fontsize=6.6, weight='bold', zorder=6,
                bbox=dict(fc='white', ec='none', alpha=0.8, pad=1.2))
    ax.set_title(f'{tit}\n({uni})', fontsize=8.2, loc='left')
    towns(ax, fs=6, names=['La Caldera', 'Vaqueros'])
    ax.plot(esc.geometry.x, esc.geometry.y, marker='s', ms=3.6, mfc='#7a0f1c', mec='white',
            mew=0.8, ls='', zorder=12)
    g = pj[pj.fna == 'El Gallinato']
    ax.plot(g.long_gd, g.lat_gd, marker='^', ms=8, mfc='#c98a2b', mec='black',
            mew=0.5, ls='', zorder=11)
    scalebar(ax, -65.70, -24.745, 10); north(ax, -65.20, -24.40)

# panel D: la tabla
axT = fig.add_axes([0.53, 0.145, 0.44, 0.34]); axT.axis('off')
axT.set_title('D. Las tres fracciones, en números', fontsize=8.2, loc='left')
filas = [('Territorio', 'territorio'), ('Personas en viv. particulares', 'personas_viv_particulares'),
         ('Viviendas', 'viviendas'), ('Hogares', 'hogares'),
         ('De 15 a 29 años (%)', 'edad_15_29_pct'), ('De 65 y más (%)', 'edad_65_mas_pct'),
         ('Viviendas sin hogar (%)', 'viviendas_sin_hogar_pct'),
         ('Personas por vivienda', 'personas_por_vivienda'),
         ('Hogares sin agua de red (%)', 'hogares_sin_agua_red_pct')]
xs = [0.0, 0.47, 0.65, 0.83]
axT.text(xs[1], 0.95, '01', weight='bold', fontsize=7, transform=axT.transAxes)
axT.text(xs[2], 0.95, '02', weight='bold', fontsize=7, transform=axT.transAxes)
axT.text(xs[3], 0.95, '03', weight='bold', fontsize=7, color='#7a0f1c', transform=axT.transAxes)
for i, (et, col) in enumerate(filas):
    y = 0.87 - i * 0.085
    axT.text(xs[0], y, et, fontsize=6.3, va='top', transform=axT.transAxes)
    for k in range(3):
        v = C.iloc[k][col]
        s = textwrap.fill(str(v), 12) if col == 'territorio' else (
            f'{v:,.0f}'.replace(',', '.') if isinstance(v, (int, np.integer)) or float(v).is_integer() and v > 100
            else f'{v:.2f}'.replace('.', ',') if col == 'personas_por_vivienda' else f'{v:.1f}'.replace('.', ','))
        axT.text(xs[k + 1], y, s, fontsize=5.6 if col == 'territorio' else 6.3, va='top',
                 color='#7a0f1c' if k == 2 else '#222222', transform=axT.transAxes, linespacing=1.2)

leg = [Line2D([], [], marker='s', ms=5, mfc='#7a0f1c', mec='white', ls='',
              label='Escuela Dr. Gustavo Martínez Zuviría (Nº 4118; «Ex Nº 198» en el Mapa Educativo)'),
       Line2D([], [], marker='^', ms=5, mfc='#c98a2b', mec='black', ls='', label='Paraje El Gallinato (BAHRA)'),
       Line2D([], [], color='#8a8375', lw=0.8, label='Red vial nacional y provincial (IGN)')]
fig.legend(handles=leg, loc='lower left', bbox_to_anchor=(0.05, 0.068), frameon=False, fontsize=6.3,
           ncol=1, labelspacing=0.5)

fig.text(0.05, 0.970, 'Las tres fracciones censales del departamento La Caldera, 2022',
         fontsize=12, weight='bold')
fig.text(0.05, 0.942, 'La fracción 66077-03, el sector oriental donde está El Gallinato, tiene la menor proporción de población joven,\n'
         'la mayor de viviendas sin hogar residente y la peor cobertura de agua de red. Son 764 personas: pocos casos mueven varios puntos.',
         fontsize=7.2, color='#333333', va='top', linespacing=1.5)
fig.text(0.05, 0.040,
         'Fuentes: INDEC, Censo Nacional 2022, procesamiento Redatam por radio censal (septiembre de 2026); cartografía de radios corregida por CEUR-CONICET;\n'
         'red vial y Mapa Educativo Nacional (IGN); BAHRA. Elaboración propia con scripts/mapa_fracciones.py y datos/censo_tablas/fracciones_2022.csv\n'
         'del repositorio mapas_caldera.',
         fontsize=5.6, va='top', color='#333333', linespacing=1.6)
fig.savefig(FIG / 'fig-fracciones.png', dpi=300)
print('ok', FIG / 'fig-fracciones.png')
