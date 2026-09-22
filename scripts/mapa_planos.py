from base import *
from adjustText import adjust_text

BINS = [(1, 148, 'Planos 1 a 148', 'hasta c. 1980', '#f1eef6'),
        (149, 962, 'Planos 149 a 962', 'c. 1980–2015', '#bdc9e1'),
        (963, 1164, 'Planos 963 a 1.164', '2015–2021', '#8c6bb1'),
        (1165, 1400, 'Planos 1.165 a 1.324', '2021–2026', '#4d004b')]
c = cat.copy()
c['col'] = '#ffffff'
for a, b, *_, col in BINS:
    c.loc[c.plano.between(a, b), 'col'] = col
sin = c[c.plano == 0]
con = c[c.plano > 0]
REF = {148: 'Plano 148\n(citado en 1980)', 962: 'Plano 962\n(2015)',
       1078: 'Plano 1.078\n(Ayres de Quitilipi)', 1164: 'Plano 1.164\n(El Durazno, 2021)'}

fig = plt.figure(figsize=(6.9, 9.6), dpi=300)
axA = fig.add_axes([0.07, 0.43, 0.9, 0.54])
axB = fig.add_axes([0.07, 0.035, 0.55, 0.36])
axL = fig.add_axes([0.66, 0.035, 0.33, 0.36]); axL.axis('off')
extA = (-65.69, -24.755, -65.13, -24.37)
extB = (-65.445, -24.717, -65.335, -24.588)


def draw(ax, lw_urb):
    sin.plot(ax=ax, fc='#f4f4f4', ec='#bbbbbb', lw=0.2, hatch='....', zorder=2)
    con[con.categoria != 'URBANO'].plot(ax=ax, color=con[con.categoria != 'URBANO'].col,
                                         ec='#7a7a7a', lw=0.25, zorder=3)
    u = con[con.categoria == 'URBANO']
    u.plot(ax=ax, color=u.col, ec='#555555', lw=lw_urb, zorder=4)
    outline(ax)
    texts = []
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    for p, lab in REF.items():
        g = c[c.plano == p]
        g.dissolve().boundary.plot(ax=ax, color='#e0591b', lw=1.1, zorder=10)
        pt = g.to_crs(6933).dissolve().centroid.to_crs(4326).iloc[0]
        if x0 < pt.x < x1 and y0 < pt.y < y1:
            texts.append(ax.text(pt.x, pt.y, lab, fontsize=5.8, color='#8a2f07', ha='center',
                                 va='center', zorder=15,
                                 bbox=dict(fc='white', ec='#e0591b', lw=0.5, alpha=0.9, pad=0.8)))
    return texts


base_axes(axA, extA)
tA = draw(axA, 0.05)
oA = towns(axA, offs={'La Caldera': (0.008, 0.004), 'La Calderilla': (0.008, -0.004),
                      'Vaqueros': (0.008, -0.016)})
adjust_text(tA, objects=oA, ax=axA, expand=(1.3, 1.6),
            arrowprops=dict(arrowstyle='-', lw=0.5, color='#e0591b'))
box(axA, extB, 'B')
scalebar(axA, -65.67, -24.74, 5); north(axA, -65.16, -24.40)
axA.set_title('A. Departamento La Caldera: parcelas según el número de su último plano de mensura')

base_axes(axB, extB)
tB = draw(axB, 0.12)
oB = towns(axB, offs={'La Caldera': (0.004, 0.002), 'La Calderilla': (0.004, -0.004),
                      'Vaqueros': (0.003, 0.003)})
adjust_text(tB, objects=oB, ax=axB, expand=(1.3, 1.6),
            arrowprops=dict(arrowstyle='-', lw=0.5, color='#e0591b'))
scalebar(axB, -65.36, -24.712, 2)
axB.set_title('B. El corredor La Caldera–Vaqueros')

# recuento por tramo
d = c.to_crs(6933); d['ha'] = d.area / 1e4
h = [Patch(fc=col, ec='#7a7a7a', lw=0.4,
           label=f'{lab} ({per})\n{(d.plano.between(a, b)).sum():,} parcelas; '
                 f'{(d.plano.between(a, b) & (d.categoria == "URBANO")).sum():,} urbanas'.replace(',', '.'))
     for a, b, lab, per, col in BINS]
h += [Patch(fc='#f4f4f4', ec='#bbbbbb', hatch='....', label=f'Sin número de plano\n{(d.plano == 0).sum()} parcelas'),
      Line2D([], [], color='#e0591b', lw=1.1, label='Plano de referencia para fechar'),
      Line2D([], [], color='black', lw=1.6, label='Departamento (radios del Censo 2022)'),
      Line2D([], [], color='#444444', lw=0.5, label='Fracción censal')]
axL.legend(handles=h, loc='upper left', frameon=False, fontsize=6.2, handlelength=2,
           labelspacing=0.85, borderaxespad=0)
axL.text(0, 0.02, 'Los planos de mensura del departamento\nse numeran en orden de registro. Cada\n'
         'parcela lleva el número del último plano\nque la afectó: un número alto indica una\n'
         'subdivisión reciente. Las fechas de los\ntramos son aproximadas y se calibran con\n'
         'los cuatro planos que el libro fecha.', fontsize=6, va='bottom', color='#333333',
         transform=axL.transAxes)
fig.savefig(FIG / 'fig-planos-conversion.png', dpi=300)
print('ok')
