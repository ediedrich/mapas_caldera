from base import *
from adjustText import adjust_text

# catastro 'finca' -> (año del primer acto de dominio en el apéndice H, rótulo)
FINCAS = {
    'SAN ALEJO - SANTA RUFIN': (1909, 'San Alejo y Santa Rufina'),
    'SANTA MONICA': (1912, 'Santa Mónica'),
    'LAS NIEVES': (1925, 'Las Nieves'),
    'MOSQUERA': (1925, 'Mosquera'),
    'LOS PORONGOS': (1910, 'Los Porongos'),
    'CAMPO DE ARRIETA - LOMA BOLA - CAÑADA ANCHA': (1910, 'Loma Bola'),
    'CERRO DE BUENA VISTA': (1921, 'Cerro de Buena Vista'),
    'SAUSAL O CURUZU': (1921, 'Sausal o Curuzú'),
    'POTRERO DE GALLINATO': (1922, 'Potrero de Gallinato'),
    'GALLINATO': (1922, 'Potrero de Gallinato'),
    'MOJOTORO - SANTA GERTRUDIS - POTRERO DE GALLINATO': (1922, 'Mojotoro, Sta. Gertrudis\ny P. de Gallinato'),
    'LA CALDERILLA': (1924, 'La Calderilla'),
    'CALDERILLA': (1924, 'La Calderilla'),
    'LA CALDERILLA O SAN ROQUE': (1924, 'La Calderilla'),
    'VAQUEROS': (1924, 'Vaqueros'),
    'VAQUEROS O ENTRE RIOS': (1924, 'Vaqueros'),
    'WIERNA': (1924, 'Wierna'),
    'WIERMA': (1924, 'Wierna'),
    'EL SAUCE': (1925, 'El Sauce'),
    'EL SAUCE- EL CEIBAL': (1925, 'El Sauce y El Ceibal'),
    'PEÑONES': (1926, 'Peñones'),
    'LOS SAUCES': (1927, 'Los Sauces'),
    'LA ANGOSURA': (1929, 'La Angostura'),
    'DURAZNO - CAÑADA SECA O PEÑONES': (1932, 'El Durazno, Cañada Seca\no Peñones'),
    'DURAZNO Y CAÑADA': (1932, 'Durazno y Cañada'),
    'EL ANGOSTO': (1934, 'El Angosto'),
    'SAN JORGE': (1934, 'San Jorge'),
    'SAN FELIX': (1934, 'San Félix'),
    'LA HELVECIA': (1937, 'La Helvecia'),
    'ABRA DE LESSER': (1938, 'Abra de Lesser'),
    'YACONES - ABRA DE LESSER': (1938, 'Yacones y Abra de Lesser'),
    'LAS LAGUNAS - LOS YACONES': (1942, 'Las Lagunas y Los Yacones'),
    'LAS LAGUNAS': (1945, 'Las Lagunas'),
    'LAS LAGUNAS O DOS LAGUNAS': (1945, 'Las Lagunas'),
}
BINS = [(1909, 1920, '1909–1920', '#7a0f1c'), (1921, 1926, '1921–1926', '#c4452f'),
        (1927, 1934, '1927–1934', '#e8913a'), (1937, 1945, '1937–1945', '#f2cf5b')]


def color(y):
    for a, b, _, c in BINS:
        if a <= y <= b:
            return c


c = cat.copy()
c['anio'] = c.finca.map(lambda f: FINCAS.get(f, (None,))[0])
c['rot'] = c.finca.map(lambda f: FINCAS.get(f, (None, None))[1])
hist = c[c.anio.notna()].copy()
hist['col'] = hist.anio.map(color)
otro = c[c.anio.isna() & c.finca.notna() & (c.categoria != 'URBANO')]
urb = c[c.categoria == 'URBANO']
sub = c[(c.categoria == 'SUBRURAL') & c.anio.isna()]
rest = c[c.finca.isna() & (c.categoria == 'RURAL')]

fig = plt.figure(figsize=(6.9, 9.6), dpi=300)
axA = fig.add_axes([0.07, 0.43, 0.9, 0.54])
axB = fig.add_axes([0.07, 0.035, 0.55, 0.36])
axL = fig.add_axes([0.66, 0.035, 0.33, 0.36]); axL.axis('off')

extA = (-65.69, -24.755, -65.13, -24.37)
extB = (-65.445, -24.717, -65.335, -24.588)


def draw(ax, labels, fs):
    rest.plot(ax=ax, fc='#f7f3ea', ec='#c9c2b3', lw=0.25, zorder=2)
    otro.plot(ax=ax, fc='#eee9dd', ec='#cdc4b0', lw=0.3, hatch='////', zorder=2)
    sub.plot(ax=ax, fc='#dfe9f2', ec='#9fb4c8', lw=0.2, zorder=3)
    hist.plot(ax=ax, color=hist.col, ec='#3b2a1a', lw=0.35, zorder=4)
    urb.plot(ax=ax, fc='#6f6f6f', ec='#6f6f6f', lw=0.05, zorder=5)
    outline(ax)
    texts = []
    if labels:
        g = hist.to_crs(6933).dissolve('rot').reset_index()
        g['ha'] = g.area / 1e4
        g = g[g.ha > labels].to_crs(4326)
        x0, y0, x1, y1 = ax.get_xlim() + ax.get_ylim()
        for _, r in g.iterrows():
            p = r.geometry.representative_point()
            if not (x0 < p.x < x1 and y0 < p.y < y1):
                continue
            texts.append(ax.text(p.x, p.y, r.rot, fontsize=fs, ha='center', va='center',
                                 zorder=15, bbox=dict(fc='white', ec='none', alpha=0.82, pad=0.6)))
    return texts


base_axes(axA, extA)
tA = draw(axA, 150, 6.2)
oA = towns(axA, offs={'La Caldera': (0.008, 0.004), 'La Calderilla': (0.008, -0.004),
                 'Vaqueros': (0.008, -0.016)})
adjust_text(tA, objects=oA, ax=axA, expand=(1.15, 1.3), arrowprops=dict(arrowstyle='-', lw=0.4, color='#555555'))
box(axA, extB, 'B')
scalebar(axA, -65.67, -24.74, 5); north(axA, -65.16, -24.40)
axA.set_title('A. Departamento La Caldera: fincas con actos de dominio publicados entre 1909 y 1945')

base_axes(axB, extB)
tB = draw(axB, 20, 6)
oB = towns(axB, offs={'La Caldera': (0.004, 0.002), 'La Calderilla': (0.004, -0.004),
                 'Vaqueros': (0.003, 0.003)})
adjust_text(tB, objects=oB, ax=axB, expand=(1.1, 1.3), arrowprops=dict(arrowstyle='-', lw=0.4, color='#555555'))
scalebar(axB, -65.36, -24.712, 2)
axB.set_title('B. El corredor La Caldera–Vaqueros')

h = [Patch(fc=cc, ec='#3b2a1a', lw=0.4, label=f'Primer acto de dominio: {l}') for *_, l, cc in BINS]
h += [Patch(fc='#eee9dd', ec='#cdc4b0', hatch='////', label='Finca nombrada en el catastro,\nsin acto en 1909–1945'),
      Patch(fc='#f7f3ea', ec='#c9c2b3', label='Parcela rural sin nombre de finca'),
      Patch(fc='#dfe9f2', ec='#9fb4c8', label='Parcela subrural'),
      Patch(fc='#6f6f6f', label='Parcela urbana'),
      Line2D([], [], color='black', lw=1.6, label='Departamento (radios del Censo 2022)'),
      Line2D([], [], color='#444444', lw=0.5, label='Fracción censal')]
axL.legend(handles=h, loc='upper left', frameon=False, fontsize=6.3, handlelength=2,
           labelspacing=0.8, borderaxespad=0)
axL.text(0, 0.02, 'El color identifica la finca por el año\ndel primer acto de dominio que el\nBoletín Oficial publicó sobre ella\n(apéndice H). Nombre y geometría:\ncampo «finca» del catastro parcelario\nvigente. Una parcela urbana dentro\nde una finca histórica se dibuja\ncomo urbana.', fontsize=6, va='bottom', color='#333333',
         transform=axL.transAxes)
fig.savefig(FIG / 'fig-fincas-historicas.png', dpi=300)
print('ok', len(hist), hist.rot.nunique())
