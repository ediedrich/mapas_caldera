from base import *
import rasterio
from matplotlib.colors import LinearSegmentedColormap, LightSource
from adjustText import adjust_text
import matplotlib.patheffects as pe
from shapely.geometry import box as sbox
from shapely.ops import linemerge

C = D
TPL = D / 'plantilla_ign'
depg = dep.geometry.iloc[0]
halo = [pe.withStroke(linewidth=2.2, foreground='white')]

# --- relieve
with rasterio.open(C / 'relieve' / 'mde30_la_caldera.tif') as r:
    z = r.read(1); b = r.bounds
ext = (b.left, b.right, b.bottom, b.top)
dx = r.res[0] * 111320 * np.cos(np.radians(LAT0)); dy = r.res[1] * 111320
ls = LightSource(azdeg=315, altdeg=40)
zf = np.where(np.isnan(z), np.nanmin(z), z)
hs = ls.hillshade(zf, vert_exag=1.4, dx=dx, dy=dy)
cmap = LinearSegmentedColormap.from_list('hyp', [
    (0.00, '#b9cfa4'), (0.12, '#d6dfae'), (0.25, '#e9e1b5'), (0.42, '#dcc7a0'),
    (0.60, '#c7aa8b'), (0.78, '#b9a79a'), (1.00, '#f4f1ee')])
zmin, zmax = 700, 5600
rgb = cmap(np.clip((zf - zmin) / (zmax - zmin), 0, 1))[..., :3]
shade = rgb * (0.45 + 0.65 * hs[..., None])
shade = np.clip(shade, 0, 1)

# --- capas
per = gpd.read_file(C / 'hidrografia' / 'cursos_perennes_ign.gpkg')
inter = gpd.read_file(C / 'hidrografia' / 'cursos_intermitentes_ign.gpkg')
emb = gpd.read_file(C / 'hidrografia' / 'embalses_ign.gpkg')
muro = gpd.read_file(C / 'hidrografia' / 'muros_embalse_ign.gpkg')
rn = gpd.read_file(C / 'vial' / 'red_nacional_ign.gpkg')
rp = gpd.read_file(C / 'vial' / 'red_provincial_ign.gpkg')
mun = gpd.read_file(C / 'limites' / 'municipios_ign.gpkg')
pu = gpd.read_file(C / 'habitat' / 'plantas_urbanas_ign.gpkg')
cer = gpd.read_file(C / 'relieve' / 'cerros_ign.gpkg')
sal = gpd.read_file(C / 'habitat' / 'establecimientos_salud_ign.gpkg')

fig = plt.figure(figsize=(6.9, 7.7), dpi=300)
ax = fig.add_axes([0.07, 0.355, 0.9, 0.615])
extA = (-65.72, -24.765, -65.11, -24.355)
base_axes(ax, extA, grid=False)
ax.imshow(shade, extent=ext, origin='upper', zorder=1, interpolation='bilinear')
# velo fuera del departamento
outside = gpd.GeoSeries([sbox(*[extA[0] - 1, extA[1] - 1, extA[2] + 1, extA[3] + 1]).difference(depg)], crs=4326)
outside.plot(ax=ax, fc='white', ec='none', alpha=0.55, zorder=2)

clip = lambda g: gpd.clip(g, sbox(extA[0], extA[1], extA[2], extA[3]))
clip(inter).plot(ax=ax, color='#5b8fc7', lw=0.35, alpha=0.9, zorder=3)
clip(per).plot(ax=ax, color='#1f5fa8', lw=1.0, zorder=4)
emb.plot(ax=ax, fc='#7fb0de', ec='#1f5fa8', lw=0.5, zorder=5)
muro.plot(ax=ax, color='black', lw=1.6, zorder=6)
clip(pu).plot(ax=ax, fc='#5a5a5a', ec='none', alpha=0.85, zorder=6)
clip(gpd.read_file(C / 'vial' / 'huellas_ign.gpkg')).plot(ax=ax, color='#6d6d6d', lw=0.4, linestyle=':', zorder=6)
clip(gpd.read_file(C / 'vial' / 'red_terciaria_ign.gpkg')).plot(ax=ax, color='#8a5a2b', lw=0.5, linestyle='--', zorder=6)
clip(rp).plot(ax=ax, color='#8a5a2b', lw=0.8, zorder=7)
clip(rn).plot(ax=ax, color='#c0392b', lw=1.8, zorder=8)
lc = mun[mun.nam == 'La Caldera'].geometry.iloc[0]; vq = mun[mun.nam == 'Vaqueros'].geometry.iloc[0]
shared = gpd.GeoSeries([lc.boundary.intersection(vq.buffer(0.0005))], crs=4326).explode()
shared[shared.geom_type.str.contains('Line')].plot(ax=ax, color='#6b2d7a', lw=1.2, linestyle='--', zorder=9)
dep.boundary.plot(ax=ax, color='black', lw=1.6, zorder=10)

# rótulos de ríos a lo largo del cauce
def river_label(name, lab, frac=0.5, fs=6.2, off=0):
    g = pd.concat([per, inter]); g = g[g.fna == name]
    if g.empty:
        return
    m = linemerge(list(gpd.clip(g, depg).geometry.explode()))
    line = max(getattr(m, 'geoms', [m]), key=lambda l: l.length)
    p = line.interpolate(frac, normalized=True)
    q = line.interpolate(min(frac + 0.03, 1), normalized=True)
    ang = np.degrees(np.arctan2((q.y - p.y), (q.x - p.x) / ASPECT))
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    ax.text(p.x, p.y + off, lab, fontsize=fs, color='#1f4f8a', style='italic', rotation=ang,
            rotation_mode='anchor', ha='center', va='center', zorder=14, path_effects=halo)

for n, l, f in [('Río La Caldera', 'río La Caldera', 0.55), ('Río Wierna', 'río Wierna', 0.1),
                ('Río Las Nieves o de Castilla', 'río Las Nieves', 0.45), 
                ('Río Los Yacones', 'río Los Yacones', 0.5), ('Río Potrero de Castilla', 'río Potrero de Castilla', 0.5),
                ('Arroyo San Alejo', 'arroyo San Alejo', 0.5), ('Arroyo Los Porongos', 'arroyo Los Porongos', 0.22),
                ('Río Lesser', 'río Lesser', 0.5),
                ('Arroyo Castellanos', 'arroyo Castellanos', 0.5)]:
    river_label(n, l, f)

# cerros
SEL = ['Cerro Negro', 'Cerro Pajas Blancas o San Alejo', 'Cerro Campanario', 'Cerro La Despensa',
       'Cerro Los Porongos', 'Cerro Alto Los Sauces', 'Cerro Vaqueros', 'Cerro Antila', 'Cerro Alto de Toledo']
cs = cer[cer.fna.isin(SEL) & cer.intersects(depg)]
txt = []
with rasterio.open(C / 'relieve' / 'mde30_la_caldera.tif') as r:
    for _, c in cs.iterrows():
        h = list(r.sample([(c.geometry.x, c.geometry.y)]))[0][0]
        ax.plot(c.geometry.x, c.geometry.y, '^', ms=3.8, mfc='#3b2a1a', mec='white', mew=0.4, zorder=15)
        name = c.fna.replace('Cerro ', 'C.º ').replace('Pajas Blancas o San Alejo', 'Pajas Blancas\no San Alejo')
        txt.append(ax.text(c.geometry.x + 0.006, c.geometry.y, f'{name}\n{h:,.0f} m'.replace(',', '.'),
                           fontsize=5.6, color='#3b2a1a', va='center', zorder=15, path_effects=halo))

# parajes (BAHRA, IGN)
par = gpd.read_file(C / 'habitat' / 'parajes_bahra.gpkg')
par = par[(par.nom_depto == 'La Caldera') & (par.fna != 'La Calderilla')].explode()
for _, s in par.iterrows():
    ax.plot(s.geometry.x, s.geometry.y, 's', ms=3, mfc='white', mec='black', mew=0.7, zorder=15)
    txt.append(ax.text(s.geometry.x + 0.006, s.geometry.y - 0.004, s.fna, fontsize=6.2,
                       zorder=15, path_effects=halo))
oA = towns(ax, offs={'La Caldera': (0.009, 0.004), 'La Calderilla': (0.009, -0.004),
                     'Vaqueros': (0.009, -0.014)})
ax.annotate('Dique\nCampo Alegre', xy=(-65.372, -24.553), xytext=(-65.402, -24.518), fontsize=6.2,
            color='#1f4f8a', style='italic', ha='right', zorder=15, path_effects=halo,
            arrowprops=dict(arrowstyle='-', lw=0.5, color='#1f4f8a'))
# rutas
for x, y, t, col in [(-65.372, -24.445, 'RN 9', '#c0392b')]:
    ax.text(x, y, t, fontsize=5.8, color='white', weight='bold', ha='center', zorder=16,
            bbox=dict(fc=col, ec='none', pad=1.2, boxstyle='round,pad=0.25'))
adjust_text(txt, objects=oA, ax=ax, expand=(1.05, 1.15), only_move={'text': 'xy'})
scalebar(ax, -65.70, -24.752, 5); north(ax, -65.13, -24.39)
ax.text(-65.60, -24.575, 'Municipio\nVaqueros', fontsize=6.5, color='#6b2d7a', ha='center', zorder=15,
        path_effects=halo)
ax.text(-65.25, -24.63, 'Municipio\nLa Caldera', fontsize=6.5, color='#6b2d7a', ha='center', zorder=15,
        path_effects=halo)
ax.set_title('A. Departamento La Caldera: relieve, ríos, caminos y nombres')

# --- recuadros de ubicación
prov = gpd.read_file(TPL / 'provincias.gpkg').to_crs(4326)
axR = fig.add_axes([0.03, 0.025, 0.22, 0.28])
ref = gpd.read_file(TPL / 'referencias.gpkg').to_crs(4326)
ref.plot(ax=axR, fc='#fafafa', ec='#cccccc', lw=0.2)
prov.plot(ax=axR, fc='#eeeeee', ec='#9a9a9a', lw=0.25)
prov[prov.NAM == 'Salta'].plot(ax=axR, fc='#c0392b', ec='#7a1f15', lw=0.4)
axR.set_xlim(-74, -53); axR.set_ylim(-56, -21); axR.set_aspect(1 / np.cos(np.radians(-38)))
axR.set_xticks([]); axR.set_yticks([]); axR.set_title('B. Salta en la Argentina', fontsize=7.5)

sa = prov[prov.NAM == 'Salta']
axS = fig.add_axes([0.27, 0.025, 0.30, 0.28])
prov.plot(ax=axS, fc='#f3f3f3', ec='#9a9a9a', lw=0.3)
sa.plot(ax=axS, fc='#fbeee6', ec='#7a1f15', lw=0.6)
dep.plot(ax=axS, fc='#c0392b', ec='#7a1f15', lw=0.4)
sb = sa.total_bounds
axS.set_xlim(sb[0] - 0.3, sb[2] + 0.3); axS.set_ylim(sb[1] - 0.3, sb[3] + 0.3)
axS.set_aspect(1 / np.cos(np.radians(-24.5))); axS.set_xticks([]); axS.set_yticks([])
axS.text(-65.40, -24.1, 'La Caldera', fontsize=6.2, ha='right', va='bottom', weight='bold', path_effects=halo)
axS.plot(-65.411, -24.789, 'o', ms=2.5, color='black'); axS.text(-65.48, -24.84, 'Salta', fontsize=6, ha='right', va='top')
axS.set_title('C. El departamento en la provincia', fontsize=7.5)

axL = fig.add_axes([0.60, 0.06, 0.39, 0.25]); axL.axis('off')
h = [Line2D([], [], color='#1f5fa8', lw=1, label='Río o arroyo perenne'),
     Line2D([], [], color='#5b8fc7', lw=0.5, label='Curso intermitente'),
     Patch(fc='#7fb0de', ec='#1f5fa8', lw=0.5, label='Embalse'),
     Line2D([], [], color='#c0392b', lw=1.8, label='Ruta nacional'),
     Line2D([], [], color='#8a5a2b', lw=0.8, label='Ruta provincial'),
     Line2D([], [], color='#8a5a2b', lw=0.5, ls='--', label='Camino vecinal (red terciaria)'),
     Line2D([], [], color='#6d6d6d', lw=0.6, ls=':', label='Huella'),
     Patch(fc='#5a5a5a', label='Planta urbana'),
     Line2D([], [], color='black', lw=1.6, label='Departamento (radios del Censo 2022)'),
     Line2D([], [], color='#6b2d7a', lw=1.2, ls=(0, (4, 2)), label='Límite entre municipios'),
     Line2D([], [], marker='^', ls='', mfc='#3b2a1a', mec='white', ms=5, label='Cerro, con su altura'),
     Line2D([], [], marker='s', ls='', mfc='white', mec='black', ms=4, label='Paraje (BAHRA)'),
     Line2D([], [], marker='o', ls='', mfc='white', mec='black', ms=5, label='Localidad')]
axL.legend(handles=h, loc='upper left', frameon=False, fontsize=6.2, handlelength=2.2, labelspacing=0.55,
           borderaxespad=0)
# barra hipsométrica
axC = fig.add_axes([0.62, 0.03, 0.30, 0.012])
axC.imshow(np.linspace(0, 1, 256)[None, :], aspect='auto', cmap=cmap, extent=(zmin, zmax, 0, 1))
axC.set_yticks([]); axC.set_xticks([1000, 2000, 3000, 4000, 5000]); axC.tick_params(labelsize=5.5, length=2)
axC.set_xticklabels(['1.000', '2.000', '3.000', '4.000', '5.000 m'])
fig.savefig(FIG / 'fig-ubicacion.png', dpi=300)
print('ok')
