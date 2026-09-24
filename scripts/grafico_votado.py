# -*- coding: utf-8 -*-
"""Lo que el Estado votó para el departamento y lo que el archivo muestra que
llegó, 1929-1949, en escala logarítmica.

Sostiene el capítulo «La presencia material del Estado» y su continuación en
1947-1950: los caminos y el edificio de la policía se ejecutan; la salud y la
escuela, en el período leído, quedan en partida. La estación sanitaria de 1935
no deja rastro, y otra, con otro origen, se construye en 1948-1949.

Los datos NO están en el código: salen de datos/fiscal/votado_ejecutado.csv,
que cita para cada fila el lugar del libro de donde sale.
"""
from base import plt, mpl, FIG, Line2D
import pandas as pd, numpy as np
from pathlib import Path
import textwrap

D = Path(__file__).resolve().parents[1] / 'datos' / 'fiscal'
df = pd.read_csv(D / 'votado_ejecutado.csv').sort_values(['anio', 'monto']).reset_index(drop=True)
EST = {'entregado': ('#1f4e5f', 'o', 'Llegó: entregado, certificado o recibido'),
       'funciona': ('#3d6b57', 'o', 'Funciona: gasto corriente pagado'),
       'liquidado': ('#8fb0bd', 'o', 'Liquidado, sin constancia de obra terminada'),
       'autorizado': ('#c98a2b', 's', 'Autorizado o presupuestado'),
       'en_plan': ('#b5651d', 'D', 'En un plan de obras'),
       'sin_rastro': ('#b03030', 'X', 'Presupuestado, y no vuelve a aparecer')}

fig = plt.figure(figsize=(8.27, 6.4))
ax = fig.add_axes([0.40, 0.235, 0.56, 0.605])
y = np.arange(len(df))[::-1]
for (i, r), yy in zip(df.iterrows(), y):
    c, m, _ = EST[r.estado]
    ax.plot([80, r.monto], [yy, yy], color='#e4e0d6', lw=0.8, zorder=1)
    ax.plot(r.monto, yy, marker=m, ms=6.5, color=c, mec='#333333', mew=0.4, ls='', zorder=3)
    ax.text(r.monto * 1.18, yy, '$ ' + f'{r.monto:,.0f}'.replace(',', '.'), va='center',
            fontsize=5.8, color='#333333')
ax.set_yticks(y)
ax.set_yticklabels([f'{r.anio}  ' + textwrap.shorten(r.que, 62, placeholder='…') for _, r in df.iterrows()],
                   fontsize=6.0)
ax.set_xscale('log'); ax.set_xlim(80, 3e6)
ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, p: f'{v:,.0f}'.replace(',', '.')))
ax.tick_params(length=2, labelsize=6)
ax.set_xlabel('pesos moneda nacional, escala logarítmica', fontsize=6.4)
ax.grid(axis='x', color='#e4e0d6', lw=0.4, which='major', zorder=0)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)

leg = [Line2D([], [], marker=m, color=c, mec='#333333', mew=0.4, ls='', ms=6, label=l)
       for c, m, l in EST.values()]
fig.legend(handles=leg, loc='lower left', bbox_to_anchor=(0.05, 0.075), ncol=2, frameon=False,
           fontsize=6.1, labelspacing=0.6, columnspacing=1.6)
fig.text(0.05, 0.965, 'Lo que se votó y lo que llegó, 1929–1949', fontsize=11.5, weight='bold')
fig.text(0.05, 0.936,
         'Cada punto es un acto que destina plata a una cosa material del departamento. La escala es logarítmica: el puente de 1947 vale\n'
         'mil trescientas ochenta veces el espigón de 1935. Llegaron el gimnasio, la refacción de la comisaría y, ya fuera de la ventana leída\n'
         'sobre la imagen, una estación sanitaria; los dos puentes quedaron en los planes.',
         fontsize=6.6, va='top', color='#333333', linespacing=1.55)
fig.text(0.05, 0.055,
         'Fuentes: Boletín Oficial de Salta, 1923–1946 leídos edición por edición y 1947–1950 barridos sin lectura sobre la imagen (la cronología del libro dice qué actos se verificaron sobre el facsímil);\n'
         'cada fila cita su lugar en el libro en datos/fiscal/votado_ejecutado.csv. Elaboración propia con scripts/grafico_votado.py del repositorio mapas_caldera.',
         fontsize=5.4, va='top', color='#333333', linespacing=1.6)
fig.savefig(FIG / 'fig-votado-llegado.png', dpi=300)
print('ok', FIG / 'fig-votado-llegado.png')
