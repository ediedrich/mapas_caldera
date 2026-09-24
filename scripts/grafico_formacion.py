"""Formación por área y radios seleccionados, Censo 2022 (cap. 14, lámina fig-formacion-comparacion)."""
from base import *

f = pd.read_csv(D / 'censo_tablas' / 'formacion_2022.csv').sort_values('orden')
ETI = {'Fraccion 01 (Vaqueros)': 'Fracción 01 (Vaqueros)',
       'Fraccion 02 (pueblo de La Caldera)': 'Fracción 02 (pueblo de La Caldera)',
       'Fraccion 03 (este del municipio)': 'Fracción 03 (este del municipio)',
       # El Durazno está en el 0208 o en el 0209 y la coordenada no permite decir en cuál (cap. 14)
       'Radio 0209': 'Radio 0209 (sur del pueblo)', 'Radio 0208': 'Radio 0208 (sur del pueblo)',
       'Radio 0207': 'Radio 0207 (pueblo)', 'Radio 0104': 'Radio 0104 (Vaqueros, máximo)'}
f['eti'] = f.area.map(lambda a: ETI.get(a, a))

fig, ax = plt.subplots(figsize=(7.2, 4.4))
y = np.arange(len(f))[::-1]
h = 0.38
coma = lambda v: f"{v:.1f}".replace('.', ',')
ax.barh(y + h / 2, f.terciario_universitario_posgrado, h, color='#9ecae1', label='Terciario, universitario o posgrado')
ax.barh(y - h / 2, f.universitario_posgrado, h, color='#08519c', label='Universitario o posgrado')
for yy, a, b in zip(y, f.terciario_universitario_posgrado, f.universitario_posgrado):
    ax.text(a + 0.6, yy + h / 2, coma(a), va='center', fontsize=6.5, color='#555555')
    ax.text(b + 0.6, yy - h / 2, coma(b), va='center', fontsize=6.5)
corte = y[(f.tipo == 'radio').values].max() + 0.5
ax.axhline(corte, color='#999999', ls='--', lw=0.7)
ax.set_yticks(y, f.eti, fontsize=7.5)
ax.set_xlim(0, 72)
ax.set_xlabel('Personas que cursaron ese nivel, por cada 100 habitantes de 25 años o más', fontsize=7.5)
ax.tick_params(axis='x', labelsize=7)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
ax.legend(loc='lower center', bbox_to_anchor=(0.55, 1.0), ncol=2, frameon=False, fontsize=7)
fig.tight_layout()
fig.savefig(FIG / 'fig-formacion-comparacion.png', dpi=300)
print('ok', FIG / 'fig-formacion-comparacion.png')
