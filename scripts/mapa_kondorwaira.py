"""Territorio reclamado por la comunidad Kondorwaira (catastro 102) y loteos del libro."""
from base import *

cat['cat'] = pd.to_numeric(cat.catastro, errors='coerce')
cuen = gpd.read_file(D / 'otbn' / 'cuencas_informe_8483.gpkg').to_crs(4326)
rios = gpd.read_file(D / 'hidrografia' / 'cursos_perennes_ign.gpkg').to_crs(4326)
emb = gpd.read_file(D / 'hidrografia' / 'embalses_ign.gpkg').to_crs(4326)

t102 = cat[cat.cat == 102]
lind = cat[cat.cat.isin([1539, 4416, 3414, 3415, 3416, 3417, 3418])]
LOT = [6713, *range(6714, 6961), 6557, 4207, 5831, 5800, 154, 3012, 3989, 4095,
       1869, 1555, 161, 3307]
lot = cat[cat.cat.isin(LOT)]
urb = cat[cat.categoria.isin(['URBANO', 'SUBRURAL']) & ~cat.cat.isin(LOT)]
fuera = gpd.overlay(dep.to_crs(4326), cuen[['geometry']], how='difference')

ext = [-65.70, -24.72, -65.24, -24.37]
fig, ax = plt.subplots(figsize=(7.2, 7.2))
base_axes(ax, ext)
fuera.plot(ax=ax, fc='none', ec='#555555', hatch='....', lw=0, zorder=4.5)
cat.plot(ax=ax, fc='#f4f4f4', ec='#c8c8c8', lw=0.2, zorder=2)
emb.plot(ax=ax, fc='#9ecae1', ec='#6baed6', lw=0.4, zorder=3)
rios.clip(dep.to_crs(4326)).plot(ax=ax, color='#4a90c2', lw=0.5, zorder=3)
t102.plot(ax=ax, fc='#b7dfa8', ec='#2e7d32', lw=1.2, alpha=0.85, zorder=4)
lind.plot(ax=ax, fc='#fde0b2', ec='#e08214', lw=0.8, alpha=0.85, zorder=4)
urb.plot(ax=ax, fc='#6d6d6d', ec='none', zorder=5)
lot.plot(ax=ax, fc='#d7301f', ec='#99000d', lw=0.3, zorder=6)
outline(ax)
towns(ax, offs={'Vaqueros': (0.008, -0.006)})

def lab(geom, txt, dx=0, dy=0):
    p = geom.union_all().representative_point()
    ax.text(p.x + dx, p.y + dy, txt, fontsize=6.5, ha='center', zorder=15,
            bbox=dict(fc='white', ec='none', alpha=0.75, pad=0.6))
lab(t102, 'Catastro 102\n«Las Nieves», fiscal\n22.860 ha')
lab(cat[cat.cat == 1539], 'San Alejo –\nSanta Rufina\n(1539)')
lab(cat[cat.cat == 4416], 'Lesser\n(4416)')
lab(cat[cat.cat.isin([3414, 3415, 3416, 3417, 3418])], 'Yacones –\nAbra de Lesser', dx=0.01)

scalebar(ax, -65.69, -24.708, 5)
north(ax, -65.255, -24.44)
ax.legend(handles=[
    Patch(fc='#b7dfa8', ec='#2e7d32', label='Territorio reclamado por la comunidad Kondorwaira (catastro 102)'),
    Patch(fc='#fde0b2', ec='#e08214', label='Parcelas linderas al catastro 102 (capa catastral de IDESA)'),
    Patch(fc='#d7301f', ec='#99000d', label='Loteos y clubes de campo que documenta el libro'),
    Patch(fc='#6d6d6d', label='Otras parcelas urbanas o subrurales'),
    Patch(fc='none', ec='#7a7a7a', hatch='....', label='Fuera de la capa de cuencas del OTBN (sin categoría)'),
    Line2D([], [], color='black', lw=1.6, label='Límite departamental (radios del Censo 2022)')],
    loc='upper center', bbox_to_anchor=(0.5, -0.06), ncol=2, fontsize=6, frameon=False)
fig.tight_layout()
fig.savefig(FIG / 'fig-kondorwaira-catastro.png', dpi=300, bbox_inches='tight')
print('ok')
