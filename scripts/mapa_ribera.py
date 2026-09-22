"""Líneas de ribera con coordenadas publicadas en el Boletín Oficial, sobre el catastro (cap. 11).

Tres paneles: A, Vaqueros; B, río Wierna y La Calderilla; C, el pueblo de La Caldera.
No se dibujan las Resoluciones 6/14 y 7/14: sus avisos publicaron la tabla de la 023/14.
"""
from base import *
lin = gpd.read_file(D / 'ribera' / 'lineas_ribera_edictos.gpkg')
pts = gpd.read_file(D / 'ribera' / 'puntos_ribera_edictos.gpkg')
CH = ['205/17', '210/17', '211/17', '212/17']
lin['grupo'] = lin.resolucion.where(~lin.resolucion.isin(CH), 'Chaile')
pts['grupo'] = pts.resolucion.where(~pts.resolucion.isin(CH), 'Chaile')
rios = gpd.read_file(D / 'hidrografia' / 'cursos_perennes_ign.gpkg').to_crs(4326)
inter = gpd.read_file(D / 'hidrografia' / 'cursos_intermitentes_ign.gpkg').to_crs(4326)
emb = gpd.read_file(D / 'hidrografia' / 'embalses_ign.gpkg').to_crs(4326)
urb = cat[cat.categoria.isin(['URBANO', 'SUBRURAL'])]
G = ['94/12', '201/13', '348/13', '023/14', '80/14', '101/14', '182/14', '185/14', '209/14',
     '293/15', '322/15', '428/15', '14/16', '154/16', '414/16', '144/17', 'Chaile']
PAL = ['#6a3d9a', '#1f78b4', '#e31a1c', '#000000', '#ff7f00', '#8c6d31', '#e7298a', '#b15928', '#1b9e77',
       '#7570b3', '#66a61e', '#33a02c', '#fb9a99', '#a6761d', '#d95f02', '#00bcd4', '#c51b7d']
COL = dict(zip(G, PAL))
LAB = {'94/12': 'Res. 94/12 · río Castellanos, matr. 4027', '201/13': 'Res. 201/13 · río Vaqueros, sección B',
       '348/13': 'Res. 348/13 · río La Caldera, matr. 1590', '023/14': 'Res. 023/14 · río La Caldera, a lo largo del pueblo',
       '80/14': 'Res. 80/14 · arroyo Quintín, matr. 3989', '101/14': 'Res. 101/14 · arroyo Los Nogales o El Cajón, matr. 4191',
       '182/14': 'Res. 182/14 · río La Caldera, matr. 2882', '185/14': 'Res. 185/14 · río La Caldera y arroyo El Manzano, matr. 4366',
       '209/14': 'Res. 209/14 · río Vaqueros, matrs. 1905 y 3740', '293/15': 'Res. 293/15 · río La Caldera y Cañada Oeste, matrs. 3721 y 3722',
       '322/15': 'Res. 322/15 · río Vaqueros, matrs. 156, 23, 1695 y 406', '428/15': 'Res. 428/15 · río La Caldera, matr. 2020',
       '14/16': 'Res. 14/16 · río Wierna, matr. 4445', '154/16': 'Res. 154/16 · río Wierna, matr. 3722',
       '414/16': 'Res. 414/16 · río Vaqueros, matr. 40', '144/17': 'Res. 144/17 · río Vaqueros, matr. 40 (ampliación)',
       'Chaile': 'Res. 205, 210, 211 y 212/17 · arroyo Chaile, manzana 148'}
OFF = {'101/14|Los Nogales Sur o El Cajón (así en el edicto)': (-36, -14), '201/13': (-30, 8), '144/17': (8, -13), '14/16': (6, 4), '322/15': (-44, -13), '414/16': (6, 8),
       'Chaile': (6, 4), '209/14': (-10, -12), '293/15': (6, 6), '182/14': (8, -2), '023/14': (8, 0)}

def panel(ax, ext, title, bar, towns_=()):
    base_axes(ax, ext)
    cat.plot(ax=ax, fc='#f6f6f6', ec='#c9c9c9', lw=0.25, zorder=1, aspect=None)
    urb.plot(ax=ax, fc='#dcdcdc', ec='#b5b5b5', lw=0.2, zorder=2, aspect=None)
    emb.plot(ax=ax, fc='#9ecae1', ec='none', zorder=2, aspect=None)
    inter.plot(ax=ax, color='#9ecae1', lw=0.4, ls='--', zorder=3, aspect=None)
    rios.plot(ax=ax, color='#4a90c2', lw=0.8, zorder=3, aspect=None)
    for r in G:
        s = lin[lin.grupo == r]
        for part, kw in ((s[s.margen != 'inund'], dict(lw=2.2)), (s[s.margen == 'inund'], dict(lw=1.1, ls=':'))):
            if len(part): part.plot(ax=ax, color=COL[r], zorder=6, aspect=None, **kw)
        p = pts[pts.grupo == r]
        if len(p): p.plot(ax=ax, color=COL[r], markersize=1.2, edgecolor='none', zorder=7, aspect=None)
    outline(ax, lw=1.2)
    base_axes(ax, ext)
    ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(3)); ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(4))
    for r in G:
        s = lin[(lin.grupo == r) & (lin.margen != 'inund')]
        if not len(s): continue
        for c in s.curso.unique():
            q = s[s.curso == c].union_all().centroid
            if ext[0] < q.x < ext[2] and ext[1] < q.y < ext[3]:
                ax.annotate('Chaile' if r == 'Chaile' else r, (q.x, q.y), xytext=OFF.get(r + '|' + c, OFF.get(r, (6, 6))),
                            textcoords='offset points', fontsize=6, weight='bold', color=COL[r], zorder=9,
                            bbox=dict(fc='white', ec='none', alpha=0.8, pad=0.4))
    ax.set_title(title)
    scalebar(ax, ext[0] + (ext[2] - ext[0]) * 0.05, ext[1] + (ext[3] - ext[1]) * 0.05, bar)
    north(ax, ext[2] - (ext[2] - ext[0]) * 0.05, ext[3] - (ext[3] - ext[1]) * 0.12)
    if towns_: towns(ax, list(towns_), fs=7, offs={'La Calderilla': (-0.021, 0.002)})

fig = plt.figure(figsize=(7.4, 8.9))
gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 0.8], width_ratios=[1.25, 1])
axA, axC = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])
axB = fig.add_subplot(gs[1, :])
panel(axA, [-65.486, -24.719, -65.395, -24.666], 'A. Vaqueros', 1, ['Vaqueros'])
panel(axC, [-65.423, -24.632, -65.364, -24.584], 'C. El pueblo de La Caldera', 1, ['La Caldera'])
panel(axB, [-65.447, -24.667, -65.369, -24.629], 'B. Río Wierna y La Calderilla', 1, ['La Calderilla'])
h = [Line2D([], [], color=COL[r], lw=2, label=LAB[r]) for r in G]
h += [Line2D([], [], color='gray', lw=1.1, ls=':', label='Línea de zona inundable (348/13 y 14/16)'),
      Patch(fc='#dcdcdc', ec='#b5b5b5', label='Parcelas urbanas o subrurales')]
fig.legend(handles=h, loc='lower center', ncol=2, fontsize=5.6, frameon=False, bbox_to_anchor=(0.5, -0.01))
fig.tight_layout(rect=(0, 0.16, 1, 1))
fig.savefig(FIG / 'fig-ribera-edictos.png', dpi=300, bbox_inches='tight')
print('ok')
