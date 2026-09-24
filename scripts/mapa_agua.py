# -*- coding: utf-8 -*-
"""El agua del departamento entre 1885 y 1948: quien la concedia, desde donde
empezo a vigilarla otro, y donde caen las fincas de cada acto.

No es un mapa de cursos de agua: es el mapa de los actos de agua del archivo
(los de ACTOS, que nombran una finca) y de su arco (los de ARCO, que nombran
una facultad). 1947 y 1948 salen del barrido sin lectura sobre la imagen, pero
los dos actos de 1948 que se dibujan estan verificados sobre el facsimil. Cada finca que
aparece esta nombrada en un acto publicado del Boletin Oficial, y los dos
puntos marcados son los que dos de esos actos eligen como limite de una
facultad.

Lo que NO se puede dibujar y se declara en el epigrafe: el trazado de la
acequia de Urquiza, porque el croquis que su escrito dice acompanar no se
publico; y las superficies regadas, porque ningun acto las georreferencia.
"""
from base import (plt, cat, dep, D, FIG, base_axes, outline, towns, scalebar,
                  north, Patch, Line2D)
import geopandas as gpd
import unicodedata
from shapely.ops import unary_union

def sd(s):
    return ''.join(c for c in unicodedata.normalize('NFD', str(s).lower())
                   if unicodedata.category(c) != 'Mn')

# ---------------------------------------------------------------- los actos
# finca del catastro -> (anio, rotulo corto, que dice el acto)
ACTOS = {
    'SAUSAL O CURUZU':      (1885, 'Sausal o Curuzú',
                             'La Municipalidad concede 30 l/s del Wierna'),
    'CERRO DE BUENA VISTA': (1924, 'Cerro de Buena Vista',
                             'Concesión a Urquiza: 100 l/s para 190 ha'),
    'VAQUEROS O ENTRE RIOS':(1924, 'Vaqueros o Entre Ríos',
                             'La acequia la atraviesa'),
    'WIERNA':               (1924, 'Wierna',
                             'El río la provee antes del sobrante'),
    'CAMPO ALEGRE':         (1938, 'Campo Alegre',
                             'Segunda concesión, informa el municipio'),
    'YACONES - ABRA DE LESSER': (1942, 'Yacones · Abra de Lesser',
                             'Derechos «desde fecha inmemorial»'),
    'ABRA DE LESSER':       (1942, 'Abra de Lesser',
                             'Aguas que nacen y mueren en la finca'),
    'LA HELVECIA':          (1948, 'La Helvecia',
                             'Pfister pide 50 l/s y se le reconocen 12,6'),
    'EL ANGOSTO':           (1948, 'El Angosto',
                             'Linares: 15,22 l/s, temporal y eventual'),
}
COL = {1885: '#7a0f1c', 1924: '#c4452f', 1938: '#e8913a', 1942: '#f2cf5b',
       1948: '#8fb0bd'}

# ---------------------------------------------------------------- capas
hid = gpd.read_file(D / 'hidrografia' / 'cursos_perennes_ign.gpkg')
hint = gpd.read_file(D / 'hidrografia' / 'cursos_intermitentes_ign.gpkg')
deptos = gpd.read_file(D / 'limites' / 'departamentos_ign.gpkg')

RIOS = ['Río La Caldera', 'Río Wierna', 'Río Mojotoro',
        'Río Las Nieves o de Castilla']
rios = hid[hid.fna.isin(RIOS)].copy()
cast = hint[hint.fna == 'Arroyo Castellanos'].copy()

def juntas(a, b):
    """punto donde dos cursos se tocan (o se acercan mas)"""
    A = unary_union(hid[hid.fna == a].geometry.values)
    B = unary_union(hid[hid.fna == b].geometry.values)
    p = A.intersection(B)
    if p.is_empty:
        from shapely.ops import nearest_points
        p = nearest_points(A, B)[0]
    return p if p.geom_type == 'Point' else p.centroid

P_JUNTAS = juntas('Río Wierna', 'Río La Caldera')

cat['k'] = cat.finca.map(lambda f: sd(f) if f else None)
fin = {k: cat[cat.k == sd(k)].dissolve() for k in ACTOS}

# ---------------------------------------------------------------- figura
fig = plt.figure(figsize=(8.27, 10.4))
ax = fig.add_axes([0.075, 0.380, 0.865, 0.520])
ext = (-65.62, -24.78, -65.20, -24.38)
base_axes(ax, ext)

# departamentos vecinos, en gris, para que se vea que la facultad cruza
deptos.boundary.plot(ax=ax, color='#cdc4b0', lw=0.7, zorder=1)
g = deptos[deptos.nam == 'General Güemes']
if len(g):
    g.plot(ax=ax, fc='#f4f2ed', ec='#cdc4b0', lw=0.8, zorder=0)
    c = g.geometry.iloc[0].centroid
    ax.text(c.x, c.y, 'GENERAL GÜEMES\n(Campo Santo)', fontsize=6.2,
            ha='center', va='center', color='#8a8375', zorder=2)

cat[cat.categoria != 'URBANO'].plot(ax=ax, fc='#faf8f4', ec='#e4e0d6',
                                    lw=0.15, zorder=2)
outline(ax)

for k, (an, rot, _) in ACTOS.items():
    gsub = fin[k]
    if gsub.empty:
        print('  sin geometria:', k); continue
    gsub.plot(ax=ax, fc=COL[an], ec='#333333', lw=0.5, alpha=0.88, zorder=4)

rios.plot(ax=ax, color='#2f6a80', lw=1.5, zorder=5)
cast.plot(ax=ax, color='#8fb0bd', lw=1.0, linestyle='--', zorder=5)

# los dos puntos que los actos eligen como limite
ax.plot(P_JUNTAS.x, P_JUNTAS.y, marker='o', ms=9, mfc='#ffffff',
        mec='#7a0f1c', mew=2.2, zorder=8)
ax.annotate('LAS JUNTAS\ndel Wierna con el río La Caldera\n'
            'Ley 11.078 de 1929: desde acá,\nCampo Santo vigila y prohíbe tomas',
            xy=(P_JUNTAS.x, P_JUNTAS.y), xytext=(P_JUNTAS.x + 0.075, P_JUNTAS.y + 0.055),
            fontsize=6.1, color='#7a0f1c', linespacing=1.35, zorder=9,
            arrowprops=dict(arrowstyle='-', color='#7a0f1c', lw=0.8))

for _, r in rios.iterrows():
    pass
et = {'Río La Caldera': (-65.375, -24.560), 'Río Wierna': (-65.470, -24.630),
      'Río Mojotoro': (-65.265, -24.700),
      'Río Las Nieves o de Castilla': (-65.520, -24.520)}
for nom, (x, y) in et.items():
    if nom in set(rios.fna):
        ax.text(x, y, nom.replace(' o de Castilla', ''), fontsize=6.4,
                color='#1f4e5f', style='italic', zorder=7,
                bbox=dict(fc='white', ec='none', alpha=0.75, pad=0.8))

towns(ax)
scalebar(ax, -65.60, -24.762, 5)
north(ax, -65.23, -24.43)

# rotulos AFUERA del poligono, con linea guia: adentro no entran y se cortan
OFF = {'SAUSAL O CURUZU': (-0.085, -0.028), 'CERRO DE BUENA VISTA': (-0.100, 0.012),
       'VAQUEROS O ENTRE RIOS': (0.055, -0.048), 'WIERNA': (0.072, -0.010),
       'CAMPO ALEGRE': (0.070, 0.030), 'YACONES - ABRA DE LESSER': (-0.055, 0.052),
       'ABRA DE LESSER': (-0.090, -0.020), 'LA HELVECIA': (0.075, 0.052),
       'EL ANGOSTO': (-0.085, 0.035)}
for k, (an, rot, _) in ACTOS.items():
    gsub = fin[k]
    if gsub.empty:
        continue
    c = gsub.geometry.iloc[0].representative_point()
    dx, dy = OFF.get(k, (0.06, 0.03))
    ax.annotate(f'{rot}  {an}', xy=(c.x, c.y), xytext=(c.x + dx, c.y + dy),
                fontsize=5.8, ha='center', va='center', color='#222222',
                weight='bold', zorder=9,
                bbox=dict(fc='white', ec=COL[an], lw=0.8, pad=1.6, alpha=0.95),
                arrowprops=dict(arrowstyle='-', color=COL[an], lw=0.7))

ax.set_title('A. Las fincas de cada acto, y el punto desde el cual la facultad '
             'pasó a otro municipio', fontsize=8.4, loc='left', pad=6)

# ---------------------------------------------------------------- el arco
axb = fig.add_axes([0.075, 0.150, 0.865, 0.195])
axb.set_xlim(1878, 1953); axb.set_ylim(-0.55, 1.75); axb.axis('off')
ARCO = [(1885, 'CONCEDE', 'La Municipalidad otorga 30 l/s\ndel Wierna a Eustaquio Murúa', '#7a0f1c'),
        (1914, 'REGLAMENTA', 'Ordenanza del 13 de octubre: reglamenta\nla distribución de la totalidad', '#a52f28'),
        (1918, 'PROPONE', 'Los Jueces de Agua los nombra la\nProvincia a propuesta del comisionado', '#b5372b'),
        (1929, 'PIERDE', 'Ley 11.078: Campo Santo vigila\ny prohíbe tomas desde las juntas', '#c4452f'),
        (1931, 'COMPARTE', 'Comisión ad hoc con Campo Santo sobre\nlas aguas del Vaqueros y el Wierna', '#e8913a'),
        (1939, 'DENIEGA', 'La ordenanza de 1914 le gana a una\nconcesión provincial para Campo Alegre', '#d4692f'),
        (1942, 'INSCRIBE', 'Los derechos del municipio pasan\na los registros provinciales', '#d9b44a'),
        (1946, 'COLABORA', 'Hidráulica fija zonas y un umbral de\n2.500 l/s; el municipio «colabora»', '#f2cf5b'),
        (1948, 'NO OBSERVA', 'Consultado por La Helvecia: «no tiene\nobservación alguna que formular»', '#8fb0bd')]
axb.plot([1883, 1950], [0.60, 0.60], color='#888888', lw=1.0)
# cuatro alturas alternadas: con nueve actos, dos no alcanzan
NIV = [(0.74, 1), (0.46, -1), (1.16, 1), (0.04, -1)]
for i, (a, verbo, txt, col) in enumerate(ARCO):
    axb.plot(a, 0.60, marker='o', ms=7, mfc=col, mec='#333333', mew=0.7, zorder=3)
    y, s = NIV[i % 4]
    if abs(y - 0.60) > 0.2:
        axb.plot([a, a], [0.60, y], color='#bbbbbb', lw=0.5, zorder=1)
    axb.text(a, y, f'{a}  ·  {verbo}', fontsize=6.0, ha='center',
             va='bottom' if s > 0 else 'top', weight='bold', color=col)
    axb.text(a, y + 0.13 * s, txt, fontsize=4.7, ha='center',
             va='bottom' if s > 0 else 'top', color='#333333', linespacing=1.3)
axb.set_title('B. El arco, en nueve actos: el municipio concede, reglamenta, propone, '
              'deniega, colabora y, al final, no observa', fontsize=8.4, loc='left', pad=4)

# ---------------------------------------------------------------- leyenda
h = [Patch(fc=COL[a], ec='#333333',
           label={1885: '1885 · concesión municipal',
                  1924: '1924 · concesión a Urquiza',
                  1938: '1938 · concesión «Campo Alegre»',
                  1942: '1942 · derechos inscriptos por la Provincia',
                  1948: '1948 · reconocimientos a La Helvecia y El Angosto'}[a])
     for a in (1885, 1924, 1938, 1942, 1948)]
h += [Line2D([], [], color='#2f6a80', lw=1.5, label='Curso perenne (IGN)'),
      Line2D([], [], color='#8fb0bd', lw=1.0, ls=(0, (4, 2)), label='Arroyo Castellanos (intermitente)'),
      Line2D([], [], marker='o', ms=7, mfc='white', mec='#7a0f1c', mew=2, ls='',
             label='Las juntas: límite de la facultad de 1929')]
fig.legend(handles=h, loc='lower left', bbox_to_anchor=(0.075, 0.052),
           frameon=False, fontsize=6.2, ncol=2, handlelength=1.5,
           columnspacing=1.6, labelspacing=0.5)

fig.text(0.075, 0.970,
         'El agua del departamento de La Caldera, 1885–1948',
         fontsize=12.5, weight='bold')
fig.text(0.075, 0.941,
         'Quién la concedía, desde dónde empezó a vigilarla otro municipio, y dónde caen las fincas de cada acto.',
         fontsize=7.4, color='#333333')

fig.text(0.640, 0.038,
         'Lo que no puede dibujarse: el recorrido de la acequia de Urquiza,\n'
         'porque el croquis que su escrito dice acompañar no se publicó; y las\n'
         'superficies regadas, porque ningún acto las georreferencia. Las fincas\n'
         'se ubican por el campo «finca» del catastro vigente, no por el título.',
         fontsize=5.0, va='bottom', color='#555555', linespacing=1.5)

fig.text(0.075, 0.018,
         'Fuentes: Boletín Oficial de Salta, 1908–1946 leídos edición por edición y 1947–1948 barridos, con los actos de 1948 verificados sobre el facsímil\n(apéndice de fuentes); cursos de agua y límites, IGN; '
         'fincas, campo «finca» del catastro parcelario (IDESA, septiembre de 2026). Elaboración propia con scripts/mapa_agua.py.',
         fontsize=5.4, color='#333333', linespacing=1.5)

fig.savefig(FIG / 'fig-agua-actos.png', dpi=300)
print('ok', FIG / 'fig-agua-actos.png')
