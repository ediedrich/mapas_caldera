"""Incorpora una capa nueva al repositorio: la recorta al entorno del departamento
y la guarda como GeoPackage en datos/<carpeta>/<nombre>.gpkg.

Uso:  python incorporar.py <archivo .shp/.zip/.geojson> <carpeta> <nombre>
Ej.:  python incorporar.py paraje.zip habitat parajes_ign
"""
import sys, warnings; warnings.filterwarnings('ignore')
from pathlib import Path
import geopandas as gpd

BBOX = (-65.85, -24.85, -65.0, -24.25)   # entorno del departamento La Caldera, grados
D = Path(__file__).resolve().parents[1] / 'datos'

src, carpeta, nombre = sys.argv[1], sys.argv[2], sys.argv[3]
ruta = f'zip://{src}' if src.endswith('.zip') else src
g = gpd.read_file(ruta, bbox=BBOX)
if g.crs is None:
    g = g.set_crs(4326)
g = g.to_crs(4326)
(D / carpeta).mkdir(parents=True, exist_ok=True)
g.to_file(D / carpeta / f'{nombre}.gpkg')
print(f'{len(g)} elementos -> datos/{carpeta}/{nombre}.gpkg')
