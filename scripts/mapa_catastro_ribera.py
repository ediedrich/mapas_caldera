"""Parcelas con actos de ribera o de agua sobre el catastro (cap. 11, lámina fig-catastro-ribera).

A: el departamento. B: Vaqueros y la finca Vaqueros.
La clasificación sale de datos/ribera/actos_por_parcela.csv, que transcribe la tabla del
capítulo 11 (líneas de ribera sobre lotes urbanos y sobre fincas, concesiones y riegos).
La matrícula 1534 va aparte: la Resolución 290/16 designó comisión y la búsqueda por el
expediente no devuelve determinación alguna.
"""
from base import *

act = pd.read_csv(D / 'ribera' / 'actos_por_parcela.csv', dtype={'catastro': str})
cat['catastro'] = cat.catastro.astype(str)
sel = cat.merge(act, on='catastro')
lin = gpd.read_file(D / 'ribera' / 'lineas_ribera_edictos.gpkg')
durazno = cat[cat.plano == 1164]
remanente = durazno[durazno.catastro == '6713']
lotes = durazno[durazno.catastro != '6713']
emb = gpd.clip(gpd.read_file(D / 'hidrografia' / 'embalses_ign.gpkg').to_crs(4326), dep)
rios = gpd.clip(gpd.read_file(D / 'hidrografia' / 'cursos_perennes_ign.gpkg').to_crs(4326), dep)
sel['rotulo'] = sel.catastro.where(~sel.catastro.isin(['2342', '2343', '2344', '2345']), '2342–45')

COL = {'ribera': '#c8363d', 'concesion': '#2f6fc1', 'riego': '#3d9a62'}
CATC = {'URBANO': ('#b9b9b9', '#9a9a9a'), 'SUBRURAL': ('#dbe8f5', '#a9bfd6'), 'RURAL': ('#faf6ee', '#d8cfbf')}


def capa(ax):
    for k, (fc, ec) in CATC.items():
        cat[cat.categoria == k].plot(ax=ax, fc=fc, ec=ec, lw=0.2, zorder=1, aspect=None)
    emb.plot(ax=ax, fc='#9ecae1', ec='none', zorder=2, aspect=None)
    rios.plot(ax=ax, color='#4a90c2', lw=0.5, zorder=2, aspect=None)
    lotes.plot(ax=ax, fc='#7b3f9e', ec='#5a2a75', lw=0.2, zorder=3, aspect=None)
    remanente.plot(ax=ax, fc='none', ec='#7b3f9e', hatch='////', lw=0.6, zorder=3, aspect=None)
    for g, c in COL.items():
        sel[sel.grupo == g].plot(ax=ax, fc=c, ec='#222222', lw=0.4, alpha=0.9, zorder=4, aspect=None)
    sel[sel.grupo == 'comision'].plot(ax=ax, fc='none', ec=COL['ribera'], hatch='xxx', lw=0.8, zorder=4, aspect=None)
    for m, ls, c in (('izq', '-', '#5a0f14'), ('der', '--', '#5a0f14'), ('inund', ':', '#1f8fd6')):
        s = lin[lin.margen == m]
        if len(s):
            s.plot(ax=ax, color=c, ls=ls, lw=1.1, zorder=6, aspect=None)


def rotulos(ax, ext, fs, fuera=None, chico=0):
    d = sel.dissolve('rotulo').reset_index()
    d['m2'] = d.to_crs(22183).area
    for _, r in d.iterrows():
        p = r.geometry.representative_point()
        if not (ext[0] < p.x < ext[2] and ext[1] < p.y < ext[3]):
            continue
        if fuera and (fuera[0] < p.x < fuera[2] and fuera[1] < p.y < fuera[3]):
            continue
        if chico and r.m2 < chico:
            ax.plot(p.x, p.y, 'o', ms=4, mfc=COL.get(r.grupo, 'white'), mec='#222222', mew=0.6, zorder=9)
            ax.annotate(r.rotulo, (p.x, p.y), xytext=OFF.get(r.rotulo, (4, 4)), textcoords='offset points', fontsize=fs, zorder=10,
                        bbox=dict(fc='white', ec='none', alpha=0.75, pad=0.4))
            continue
        ax.annotate(r.rotulo, (p.x, p.y), xytext=OFF.get(r.rotulo, (0, 0)), textcoords='offset points',
                    fontsize=fs, ha='center', va='center', zorder=10,
                    bbox=dict(fc='white', ec='none', alpha=0.75, pad=0.5))


# desplazamientos de rótulos, en puntos, donde se pisan
OFF = {'1000': (-20, 2), '2342–45': (6, 8), '2318': (8, -3), '2320': (-6, 9), '1566': (-2, 7), '216': (-16, -3),
       '5009': (-9, 0), '5010': (9, 0), '4146': (0, 7), '2340': (-6, -12), '1095': (20, 6)}

A = (-65.67, -24.735, -65.145, -24.365)
B = (-65.432, -24.716, -65.397, -24.672)
fig = plt.figure(figsize=(7.2, 9.6))
axA = fig.add_axes([0.06, 0.44, 0.92, 0.53])
axB = fig.add_axes([0.06, 0.02, 0.46, 0.37])
axL = fig.add_axes([0.56, 0.08, 0.42, 0.30]); axL.axis('off')

base_axes(axA, A, grid=False); capa(axA); outline(axA)
axA.text(-65.415, -24.612, 'El Durazno\n(remanente 6713)', color='#7b3f9e', fontsize=6.5, ha='center', zorder=11,
         bbox=dict(fc='white', ec='none', alpha=0.7, pad=0.5))
rotulos(axA, A, 6.5, fuera=B)
towns(axA, fs=8, offs={'La Caldera': (0.008, 0.002), 'La Calderilla': (0.008, -0.003), 'Vaqueros': (-0.04, -0.012)})
box(axA, B, 'B'); scalebar(axA, -65.655, -24.72, 5); north(axA, -65.19, -24.405)
axA.set_title('A. Departamento La Caldera: parcelas con actos de ribera o de agua')

base_axes(axB, B, grid=False); capa(axB); rotulos(axB, B, 5.8, chico=20000)  # círculos: parcelas menores de 2 ha; scalebar(axB, -65.4305, -24.7145, 0.5)
axB.set_title('B. Vaqueros y finca Vaqueros')

h = [Patch(fc=COL['ribera'], ec='#222222', label='Parcela con línea de ribera'),
     Patch(fc='none', ec=COL['ribera'], hatch='xxx', label='Comisión designada, sin línea\npublicada (1534, Res. 290/16)'),
     Patch(fc=COL['concesion'], ec='#222222', label='Parcela con concesión de agua'),
     Patch(fc=COL['riego'], ec='#222222', label='Parcela que recibió riego\npor subdivisión'),
     Patch(fc='#7b3f9e', label='El Durazno: 247 lotes (plano 1164)'),
     Patch(fc='none', ec='#7b3f9e', hatch='////', label='El Durazno: remanente rural'),
     Patch(fc=CATC['URBANO'][0], ec=CATC['URBANO'][1], label='Parcela urbana'),
     Patch(fc=CATC['SUBRURAL'][0], ec=CATC['SUBRURAL'][1], label='Parcela subrural'),
     Patch(fc=CATC['RURAL'][0], ec=CATC['RURAL'][1], label='Parcela rural'),
     Line2D([], [], color='#5a0f14', lw=1.2, label='Línea de ribera publicada,\nmargen izquierda'),
     Line2D([], [], color='#5a0f14', lw=1.2, ls='--', label='Línea de ribera publicada,\nmargen derecha'),
     Line2D([], [], color='#1f8fd6', lw=1.2, ls=':', label='Línea de inundación\n(Res. 348/13 y 14/16)'),
     Line2D([], [], color='black', lw=1.6, label='Departamento (radios 2022)'),
     Line2D([], [], color='#444444', lw=0.5, label='Fracción censal')]
axL.legend(handles=h, loc='upper left', frameon=False, fontsize=6.8, handlelength=2.2)
assert len(lotes) == 247, len(lotes)
fig.savefig(FIG / 'fig-catastro-ribera.png', dpi=300)
print('ok', FIG / 'fig-catastro-ribera.png', '| parcelas marcadas:', sel.catastro.nunique())
