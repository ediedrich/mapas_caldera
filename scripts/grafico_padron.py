"""Padrón electoral y población del departamento, 2017-2025 (cap. 18, lámina fig-padron-poblacion).

Barras apiladas por municipio frente a tres referencias censales. La barra de 2017 va
rayada: su total coincide dígito por dígito con la población de 2022 y el libro lo trata
como posible error de carga.
"""
from base import *

p = pd.read_csv(D / 'electoral' / 'padron_2017_2025.csv')
ref = pd.read_csv(D / 'electoral' / 'poblacion_referencia.csv').set_index('serie').valor
assert (p.la_caldera + p.vaqueros == p.departamento).all()

fig, ax = plt.subplots(figsize=(7.2, 3.9))
x = np.arange(len(p))
eti = [f"{e}\n{f[:4]}" for e, f in zip(p.eleccion, p.fecha)]
for i, r in p.iterrows():
    h = '////' if r.fecha.startswith('2017') else None
    ax.bar(i, r.vaqueros, 0.6, color='#08519c', hatch=h, ec='white' if h else None, lw=0)
    ax.bar(i, r.la_caldera, 0.6, bottom=r.vaqueros, color='#6baed6', hatch=h, ec='white' if h else None, lw=0)
    ax.text(i, r.departamento + 180, f"{r.departamento:,}".replace(',', '.'), ha='center', va='bottom', fontsize=7)

refs = [('Población total censada en 2022', '#b30000', '-'),
        ('Mayores de 18 años censados en 2022', '#b30000', '--'),
        ('Población total censada en 2010', '#666666', ':')]
claves = ['Poblacion total censada 2022', 'Mayores de 18 anos censados 2022', 'Poblacion total censada 2010']
ytxt = [12900, 9700, 6900]
for (lab, c, ls), k, yt in zip(refs, claves, ytxt):
    v = ref[k]
    ax.plot([-0.5, len(p) - 0.45], [v, v], color=c, ls=ls, lw=1.1)
    ax.text(len(p) - 0.35, yt, f"{lab}:\n{v:,}".replace(',', '.'), color=c, fontsize=7, va='center')

ax.set_xticks(x, eti, fontsize=7)
ax.set_xlim(-0.6, len(p) + 1.3)
ax.set_ylim(0, 19500)
ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}".replace(',', '.')))
ax.set_ylabel('Personas', fontsize=7.5)
ax.tick_params(axis='y', labelsize=7)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
ax.legend(handles=[Patch(color='#08519c', label='Electores, Vaqueros'),
                   Patch(color='#6baed6', label='Electores, La Caldera'),
                   Patch(fc='#9ab', hatch='////', ec='white', label='2017: total igual a la población de 2022,\nposible error de carga')],
          loc='upper left', frameon=False, fontsize=7)
fig.tight_layout()
fig.savefig(FIG / 'fig-padron-poblacion.png', dpi=300)
print('ok', FIG / 'fig-padron-poblacion.png')
