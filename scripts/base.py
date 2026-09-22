import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd, geopandas as gpd
import matplotlib as mpl, matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle
from matplotlib.lines import Line2D

mpl.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 7.5,
                     'axes.titlesize': 9, 'axes.titlelocation': 'left',
                     'axes.titleweight': 'normal', 'xtick.labelsize': 6,
                     'ytick.labelsize': 6, 'axes.linewidth': 0.8, 'hatch.linewidth': 0.35})

from pathlib import Path
D = Path(__file__).resolve().parents[1] / 'datos'
FIG = Path(__file__).resolve().parents[1] / 'figuras'
LAT0 = -24.6
ASPECT = 1 / np.cos(np.radians(LAT0))

cat = gpd.read_file(D / 'catastro' / 'catastro_parcelario_idesa.gpkg')
cat = cat[cat.departa == '05'].copy()
cat['plano'] = cat.plano.fillna(0)
radios = gpd.read_file(D / 'censo' / 'radios_2022_la_caldera.gpkg')
radios['FRAC'] = radios.LINK.str[5:7]
dep = radios.dissolve()
frac = radios.dissolve('FRAC')

TOWNS = {'La Caldera': (-65.3806, -24.6027), 'La Calderilla': (-65.383, -24.637),
         'Vaqueros': (-65.407, -24.695)}


def base_axes(ax, extent, grid=True):
    ax.set_xlim(extent[0], extent[2]); ax.set_ylim(extent[1], extent[3])
    ax.set_aspect(ASPECT)
    ax.tick_params(length=2, pad=1.5)
    if grid:
        ax.grid(color='#dddddd', lw=0.3, zorder=0)


def outline(ax, lw=1.6):
    frac.boundary.plot(ax=ax, color='#444444', lw=0.5, zorder=8)
    dep.boundary.plot(ax=ax, color='black', lw=lw, zorder=9)


def towns(ax, names=None, fs=7.5, offs=None):
    offs = offs or {}
    out = []
    for n, (x, y) in TOWNS.items():
        if names and n not in names:
            continue
        ax.plot(x, y, 'o', ms=4, mfc='white', mec='black', mew=1, zorder=12)
        dx, dy = offs.get(n, (0.006, 0.002))
        out.append(ax.text(x + dx, y + dy, n, fontsize=fs, weight='bold', zorder=12,
                bbox=dict(fc='white', ec='none', alpha=0.8, pad=0.8)))
    return out


def scalebar(ax, x, y, km, label=None):
    dlon = km / (111.32 * np.cos(np.radians(LAT0)))
    ax.plot([x, x + dlon], [y, y], color='black', lw=2.2, solid_capstyle='butt', zorder=13)
    ax.text(x + dlon / 2, y + (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.012,
            label or f'{km:g} km', ha='center', va='bottom', fontsize=6.5, zorder=13)


def north(ax, x, y, size=0.035):
    h = (ax.get_ylim()[1] - ax.get_ylim()[0]) * size
    ax.annotate('N', xy=(x, y + h), xytext=(x, y), ha='center', va='top', fontsize=7,
                weight='bold', arrowprops=dict(arrowstyle='-|>', color='black', lw=1),
                zorder=13, xycoords='data')


def box(ax, ext, label):
    ax.add_patch(Rectangle((ext[0], ext[1]), ext[2] - ext[0], ext[3] - ext[1],
                           fill=False, ec='black', lw=1, zorder=14))
    ax.text(ext[2] + 0.004, ext[1], label, fontsize=9, weight='bold', va='bottom', zorder=14)
