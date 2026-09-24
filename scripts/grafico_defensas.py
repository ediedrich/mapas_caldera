# -*- coding: utf-8 -*-
"""Lo que la Provincia presupuesta en 1947 contra las crecientes, rio por rio,
y como cambia el reparto del departamento en el presupuesto de 1949 (panel B).

No es un mapa: es el Item 6 de la Ley 834 de presupuesto --- "Obras de
defensas permanentes o eventuales para contener danios por crecientes o
inundaciones sobre" --- con sus nueve rios y su renglon de imprevistos.

POR QUE IMPORTA
Tres de los nueve rios son de este departamento o se forman con sus aguas:
el Mojotoro, el de La Caldera y el Wierna. Entre los tres suman $200.000 de
los $560.000 del item, el 35,7 por ciento de todo lo que la Provincia
presupuesta ese anio contra las crecientes. Y los tres son un solo sistema:
el acto de 1946 sobre distribucion de caudales establece que el Mojotoro
forma el suyo con el Wierna, el de La Caldera y el Castellanos.

Esto corrige una lectura del libro. El capitulo venia contando las defensas
del rio como intentos chicos --- croquis en 1938, obra suspendida en 1940,
ejecucion por via administrativa en 1945 por $2.515 --- y la conclusion
implicita era que la Provincia no ponia plata. La ponia: veinte veces
aquello, en la ley de presupuesto, votada por las dos camaras.

LO QUE EL GRAFICO NO DICE
Si se ejecuto. El presupuesto es una autorizacion para gastar, no un gasto.
El barrido no encontro despues ni licitacion ni adjudicacion ni certificado,
y las fojas 12 a 18 del plan hidraulico 1948-1950 --- que el decreto 5466-E
aprueba sin publicar --- son la pieza que podria contestarlo.

Los datos NO estan en el codigo: salen de datos/fiscal/defensas_1947.csv y
defensas_1949.csv. De 1949 el libro transcribe solo los cuatro rios del
departamento y el total del item; el resto va en un solo renglon.

Se importa base.py para que la tipografia y la ruta de figuras sean las mismas
que las de los mapas; no usa ninguna capa cartografica.
"""
from base import plt, mpl, FIG, Patch
import pandas as pd
import numpy as np
from pathlib import Path

D = Path(__file__).resolve().parents[1] / 'datos' / 'fiscal'

df = pd.read_csv(D / 'defensas_1947.csv')
total = df.monto.sum()
dep = df[df.del_departamento == 1]
suma_dep = dep.monto.sum()
pct = suma_dep / total * 100

df = df.sort_values('monto', ascending=True).reset_index(drop=True)
y = np.arange(len(df))
es_dep = (df.del_departamento == 1).values
col = np.where(es_dep, '#1f4e79', '#9a9a9a')

fig = plt.figure(figsize=(7.2, 6.6))
ax = fig.add_axes([0.30, 0.435, 0.665, 0.345])

ax.barh(y, df.monto, color=col, height=0.7, zorder=3)
ax.set_yticks(y)
etiquetas = [r.rio if not isinstance(r.detalle, str) or r.detalle == ''
             else f'{r.rio}' for _, r in df.iterrows()]
ax.set_yticklabels(etiquetas, fontsize=7)
for t, f in zip(ax.get_yticklabels(), es_dep):
    if f:
        t.set_color('#1f4e79'); t.set_weight('bold')

for i, (m, f) in enumerate(zip(df.monto, es_dep)):
    ax.text(m + total * 0.006, i, f'\\$ {m:,.0f}'.replace(',', '.'),
            va='center', fontsize=6.4, weight='bold' if f else 'normal',
            color='#1f4e79' if f else '#444444')

ax.set_xlim(0, df.monto.max() * 1.28)
ax.set_xlabel('pesos moneda nacional', fontsize=6.4, labelpad=3)
ax.grid(axis='x', color='#dddddd', lw=0.35, zorder=0)
ax.set_axisbelow(True)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
ax.tick_params(length=2, pad=2)
ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, p: f'{v:,.0f}'.replace(',', '.')))

fig.suptitle('Las defensas contra crecientes del presupuesto provincial, 1947 y 1949:\n'
             'en 1947, tres de los nueve ríos son de este departamento y se llevan el 35,7 %',
             fontsize=9.6, x=0.028, ha='left', y=0.982, linespacing=1.5)

def pesos(v):
    return '\\$ ' + f'{v:,.0f}'.replace(',', '.')

fig.text(0.028, 0.895,
         'Ítem 6 de la Ley 834: «Obras de defensas permanentes o eventuales para contener daños por crecientes o inundaciones sobre». Total del ítem,\n'
         + pesos(total) + '. El Mojotoro, el de La Caldera y el Wierna suman ' + pesos(suma_dep)
         + ' — el ' + f'{pct:.1f}'.replace('.', ',') + ' % — y son un solo sistema: el acto de 1946 sobre distribución\n'
         'de caudales establece que el Mojotoro forma el suyo con el Wierna, el de La Caldera y el Castellanos.',
         fontsize=6.4, va='top', linespacing=1.6, color='#222222')

ax.legend(handles=[Patch(fc='#1f4e79', label='ríos del departamento o que se forman con sus aguas'),
                   Patch(fc='#9a9a9a', label='el resto de la provincia')],
          loc='lower right', fontsize=6.2, frameon=False, handlelength=1.4,
          handleheight=0.9, borderpad=0.2)

# ---------------------------------------------------------------- panel B
d49 = pd.read_csv(D / 'defensas_1949.csv')
d47 = pd.read_csv(D / 'defensas_1947.csv')
axb = fig.add_axes([0.30, 0.215, 0.665, 0.115])
COLR = {'La Caldera': '#1f4e79', 'Mojotoro': '#3d6f9e', 'Wierna': '#7aa3c6',
        'Vaqueros': '#b9d0e3'}
for yy, dd, tot in ((1, d47, d47.monto.sum()), (0, d49, d49.monto.sum())):
    x = 0
    for rio in ('La Caldera', 'Mojotoro', 'Wierna', 'Vaqueros'):
        m = dd.loc[dd.rio == rio, 'monto'].sum()
        if m:
            axb.barh(yy, m, left=x, color=COLR[rio], height=0.62, zorder=3)
            if m >= 40000:
                axb.text(x + m / 2, yy, f'{rio}\n{m/1000:.0f} mil', ha='center', va='center',
                         fontsize=4.9, color='white')
            x += m
    axb.barh(yy, tot - x, left=x, color='#d6d6d6', height=0.62, zorder=3)
    axb.text(x + (tot - x) / 2, yy, 'resto de la provincia', ha='center', va='center',
             fontsize=5.2, color='#444444')
    axb.text(tot + 6000, yy, f'{100 * x / tot:.1f} % del ítem'.replace('.', ','),
             va='center', fontsize=6.2, weight='bold', color='#1f4e79')
axb.set_yticks([1, 0]); axb.set_yticklabels(['1947', '1949'], fontsize=7, weight='bold')
axb.set_xlim(0, 700000)
axb.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, p: f'{v:,.0f}'.replace(',', '.')))
for s in ('top', 'right'):
    axb.spines[s].set_visible(False)
axb.tick_params(length=2, pad=2, labelsize=6)
axb.grid(axis='x', color='#dddddd', lw=0.35, zorder=0)
fig.text(0.028, 0.365, 'B. El reparto del departamento en 1947 y en 1949. En 1949 el ítem baja a \\$ 460.000 y el río La Caldera pasa a ser la partida\n'
         'más alta de las dieciocho; Vaqueros aparece por primera vez como río propio (Wierna y Vaqueros, \\$ 10.000 cada uno).',
         fontsize=6.4, va='top', linespacing=1.6, color='#222222')
fig.text(0.028, 0.795, 'A. El Ítem 6 de 1947, río por río.', fontsize=6.4, va='top', color='#222222')

fig.text(0.028, 0.150,
         'Presupuestado no es ejecutado. El barrido de 1947 y 1948 no encontró después ni licitación ni adjudicación ni certificado de estas obras; las fojas 12\n'
         'a 18 del plan hidráulico 1948-1950, que el decreto 5466-E aprueba sin publicar, son la pieza que podría contestarlo. Para comparar: la defensa\n'
         'ejecutada por vía administrativa en 1945 costó \\$ 2.515.',
         fontsize=5.6, va='top', color='#333333', linespacing=1.6)

fig.text(0.028, 0.068,
         'Fuentes: Ley 834 de Presupuesto para el ejercicio 1947, Ítem 6, separata del Boletín Oficial de Salta del 19 de mayo de 1947, páginas 141-142, y presupuesto\n'
         'de 1949, Ítem 6, B.O. Nº 3341, h. 12; los dos verificados sobre el facsímil. Elaboración propia con scripts/grafico_defensas.py y datos/fiscal/ del\n'
         'repositorio mapas_caldera.',
         fontsize=5.6, va='top', color='#333333', linespacing=1.6)

fig.savefig(FIG / 'fig-defensas-1947.png', dpi=300)
print('ok', FIG / 'fig-defensas-1947.png')
