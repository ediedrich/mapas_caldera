# -*- coding: utf-8 -*-
"""Lo que cada municipio recauda y lo que por eso recibe, 1947.

No es un mapa: es la tabla que el decreto 5276-E del 30 de julio de 1947
publica al aprobar los porcentajes de coparticipacion municipal, y el punto
del grafico es que las dos columnas son la misma columna.

EL CRITERIO, QUE ESTA ESCRITO
El articulo 6 de la Ley 834 de presupuesto manda liquidar la participacion
municipal en los impuestos a los Reditos, Ventas, Beneficios Extraordinarios
y Contribucion Territorial "en proporcion a los recursos efectivamente
percibidos por cada una de ellas durante el anio 1946". De modo que el
porcentaje no es una asignacion: es el espejo de lo que cada municipio ya
cobraba. El que recauda poco recibe poco, y lo recibe poco PORQUE recauda
poco.

EL DENOMINADOR
La hoja publicada trae los ordenes 1 a 32 y se corta ahi; el reparto alcanza
a 42 municipalidades. De modo que el grafico muestra 32 de 42, y lo dice.
Los diez que faltan estan todos por debajo del orden 32, es decir, por
debajo de La Caldera.

Los datos NO estan en el codigo: salen de datos/fiscal/coparticipacion_1947.csv,
que es el lugar donde se corrigen y se amplian.

Se importa base.py para que la tipografia y la ruta de figuras sean las mismas
que las de los mapas; no usa ninguna capa cartografica.
"""
from base import plt, mpl, FIG
import pandas as pd
import numpy as np
from pathlib import Path

D = Path(__file__).resolve().parents[1] / 'datos' / 'fiscal'
FOCO = 'La Caldera'
TOTAL_MUNICIPIOS = 42
REPARTIDO = 209775.06          # total del decreto de septiembre, B.O. 2932 h.5

df = pd.read_csv(D / 'coparticipacion_1947.csv')
df = df.sort_values('recaudacion_1946', ascending=True).reset_index(drop=True)
df['recibe'] = df.porcentaje / 100 * REPARTIDO

fig = plt.figure(figsize=(7.2, 7.4))
fig.subplots_adjust(left=0.235, right=0.965, top=0.785, bottom=0.155, wspace=0.055)

gs = fig.add_gridspec(1, 2, width_ratios=[1.85, 1])
ax = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1], sharey=ax)

y = np.arange(len(df))
es_foco = (df.municipio == FOCO).values
col = np.where(es_foco, '#b22222', '#7a7a7a')

# --- izquierda: lo que recaudo cada uno en 1946 ---
ax.barh(y, df.recaudacion_1946, color=col, height=0.72, zorder=3)
ax.set_xscale('log')
ax.set_xlim(1500, 2_600_000)
ax.set_yticks(y)
ax.set_yticklabels(df.municipio, fontsize=6.2)
for t, f in zip(ax.get_yticklabels(), es_foco):
    if f:
        t.set_color('#b22222'); t.set_weight('bold')
ax.set_title('Lo que recaudó en 1946', fontsize=8, pad=8)
ax.set_xlabel('pesos moneda nacional  (escala logarítmica)', fontsize=6.2, labelpad=3)
ax.grid(axis='x', color='#dddddd', lw=0.35, zorder=0)
ax.set_axisbelow(True)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
ax.set_ylim(-0.8, len(df) - 0.2)

# --- derecha: lo que por eso recibe ---
ax2.barh(y, df.recibe, color=col, height=0.72, zorder=3)
ax2.set_xscale('log')
ax2.set_xlim(150, 260_000)
ax2.tick_params(labelleft=False)
ax2.set_title('Lo que por eso recibe', fontsize=8, pad=8)
ax2.set_xlabel('pesos del reparto  (escala logarítmica)', fontsize=6.2, labelpad=3)
ax2.grid(axis='x', color='#dddddd', lw=0.35, zorder=0)
ax2.set_axisbelow(True)
for s in ('top', 'right'):
    ax2.spines[s].set_visible(False)

# --- la anotacion del foco ---
i = int(np.where(es_foco)[0][0])
r = df.loc[i]
ax.annotate(f'\\$ {r.recaudacion_1946:,.0f}'.replace(',', '.'),
            xy=(r.recaudacion_1946, i), xytext=(6, 0), textcoords='offset points',
            va='center', fontsize=6.4, weight='bold', color='#b22222')
ax2.annotate(f'\\$ {r.recibe:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
             + f'   ({r.porcentaje:.3f} %)'.replace('.', ','),
             xy=(r.recibe, i), xytext=(6, 0), textcoords='offset points',
             va='center', fontsize=6.4, weight='bold', color='#b22222')

# la linea del reparto parejo
parejo = REPARTIDO / TOTAL_MUNICIPIOS
ax2.axvline(parejo, color='#1f4e79', lw=0.9, ls=(0, (4, 2)), zorder=4)
ax2.text(parejo * 1.18, 6.5,
         'reparto parejo\nentre ' + str(TOTAL_MUNICIPIOS) + ':\n\\$ ' + f'{parejo:,.0f}'.replace(',', '.'),
         fontsize=5.8, color='#1f4e79', va='bottom', linespacing=1.45)

fig.suptitle('El criterio de la coparticipación municipal, 1947:\n'
             'el porcentaje no es una asignación, es el espejo de lo que cada municipio ya cobraba',
             fontsize=9.6, x=0.028, ha='left', y=0.975, linespacing=1.5)

fig.text(0.028, 0.905,
         'Artículo 6º de la Ley 834: la participación se liquida «en proporción a los recursos efectivamente percibidos por cada una de ellas\n'
         'durante el año 1946». La Caldera recauda el 0,24 % de lo que recauda la capital, y recibe el 0,127 % del reparto.',
         fontsize=6.4, va='top', linespacing=1.6, color='#222222')

fig.text(0.028, 0.105,
         f'Muestra: los órdenes 1 a 32 de la tabla, que es hasta donde llega la hoja publicada; el reparto alcanza a {TOTAL_MUNICIPIOS} municipalidades. '
         'Los diez que faltan están todos\npor debajo del orden 32, es decir, por debajo de La Caldera. La columna derecha se calcula aplicando el porcentaje publicado al total repartido de\n'
         '\\$ 209.775,06 del decreto de septiembre de 1947.',
         fontsize=5.6, va='top', color='#333333', linespacing=1.6)

fig.text(0.028, 0.048,
         'Fuente: Decreto 5276-E del 30 de julio de 1947, expediente 1873/C/1947, Boletín Oficial de Salta Nº 2909, hoja 5, verificado sobre el facsímil; y\n'
         'Ley 834 de Presupuesto, separata del Boletín Oficial del 19 de mayo de 1947. Elaboración propia con scripts/grafico_coparticipacion.py y\n'
         'datos/fiscal/coparticipacion_1947.csv del repositorio mapas_caldera.',
         fontsize=5.6, va='top', color='#333333', linespacing=1.6)

fig.savefig(FIG / 'fig-coparticipacion-1947.png', dpi=300)
print('ok', FIG / 'fig-coparticipacion-1947.png')
