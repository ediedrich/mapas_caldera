# -*- coding: utf-8 -*-
"""La toponimia del departamento en once nóminas oficiales, 1909-1940,
y qué parte de ella sigue localizable hoy."""
from base import *
import unicodedata, re

# canonico : (1909 policia, 1909 Codigo Rural, 1918 policia, 1918 electoral,
#             1919 policia, 1921 electoral, 1922 electoral, 1923 electoral,
#             1940 electoral,
#             finca del catastro o None, forma impresa distinta)
T = [
 ("Pueblo (La Caldera)",  0,0,1,1,0,1,1,1,1,1,1, None, "localidad BAHRA"),
 ("La Calderilla",        1,0,1,1,1,1,0,1,1,1,1, "LA CALDERILLA", ""),
 ("Vaqueros",             1,1,1,1,1,1,1,1,0,0,1, "VAQUEROS", "«Vaquero» en 1919"),
 ("Mojotoro",             1,1,1,1,1,1,1,1,0,0,1, "MOJOTORO O SAN NICOLAS", "«Bandera Angosta y Mojotoro» en 1909"),
 ("Lesser",               1,1,1,1,1,1,1,1,0,0,1, "LESSER", ""),
 ("Los Yacones",          1,1,1,1,1,1,1,1,1,1,1, "YACONES - ABRA DE LESSER", "«Yacone» en 1918"),
 ("Potrero de Gallinato", 1,1,1,1,1,1,1,1,0,0,1, "POTRERO DE GALLINATO", "«Gallinatos» en 1909, «Gallinato» en 1919"),
 ("Potrero de Castillo",  1,1,1,1,1,1,1,1,1,1,1, None, "«Potrero de Castilla» en 1919 y 1940"),
 ("San Alejo",            1,1,1,1,1,1,1,1,1,1,1, "SAN ALEJO - SANTA RUFIN", ""),
 ("Santa Rufina",         1,1,1,1,0,1,1,1,1,1,1, "SAN ALEJO - SANTA RUFIN", ""),
 ("Los Porongos",         1,1,1,1,0,1,1,1,1,1,1, "LOS PORONGOS", ""),
 ("La Despensa",          1,1,1,1,0,1,1,1,1,1,1, None, "«Despensa» desde 1918"),
 ("Potrero de Valencia",  1,1,1,1,0,1,1,1,1,1,1, "POTRERO DE VALENCIA", "«Valencia» en 1909"),
 ("Peñones",              1,1,1,1,0,1,1,1,1,1,1, "PEÑONES", "«Los Peñones» en 1909"),
 ("Chalchanio",           1,1,1,1,1,1,1,1,1,1,1, None, "Chalcanio, Chalchami, Chalchalnio"),
 ("Los Sauces",           1,1,1,1,0,1,1,1,1,1,1, "LOS SAUCES", "«Los Sauces y Angostos de Arias» en 1909"),
 ("Wierna",               0,1,0,1,0,1,1,1,1,1,1, "WIERNA", "«Wierma» en el catastro"),
 ("Angosto de Arrieta",   0,1,0,1,0,1,1,1,1,1,1, None, "«Campo de Arrieta» en el catastro"),
 ("Quesería",             0,1,0,1,0,1,1,1,1,1,1, None, "«Quecería» en 1909"),
 ("Mojotorillo",          0,1,0,1,0,1,1,1,0,0,0, "MOJOTORILLO - PEÑA CAIDA", "«Mojotorito» en 1918"),
 ("Chaguadero",           0,1,0,0,0,0,0,0,0,0,0, "CHAGUADERO Y SAN JOSE", ""),
 ("Bandera Angosta",      0,1,0,0,0,0,0,0,0,0,0, None, ""),
 ("Campo Alegre",         0,0,1,1,0,1,1,1,1,1,1, "CAMPO ALEGRE", ""),
 ("El Angosto",           0,0,0,1,0,1,1,1,1,1,1, "EL ANGOSTO", "«Angosto» en 1918"),
 ("Angostura",            0,0,0,1,0,1,1,1,1,1,1, "LA ANGOSURA", "«Angosturo» en 1918; «La Angosura» [sic] en el catastro"),
 ("Las Lagunas",          0,0,0,1,0,1,1,1,1,1,1, "LAS LAGUNAS", ""),
 ("Mesada",               0,0,0,1,0,1,1,1,1,1,1, "LA MESADA - FRACCION A", "«Mesadas» en 1918; el catastro la parte en fracciones A y B"),
 ("El Acheral",           0,0,0,1,0,1,1,1,1,1,1, None, "«Acheral» en 1940"),
 ("Candelaria",           0,0,0,0,0,0,1,0,0,0,0, None, "sólo en 1922; 1918, 1921 y 1923 imprimen «Calderilla» en ese circuito"),
 ("Corral de Barrancas",  0,0,0,1,0,1,1,1,1,1,1, None, "«Corral de Barranca» en 1940"),
 ("El Churcal",           0,0,0,1,0,1,1,1,1,1,1, None, "«Churcal» en 1940"),
 ("Despensilla",          0,0,0,1,0,1,1,1,1,1,1, None, ""),
 ("El Monte",             0,0,0,1,1,1,1,1,1,1,1, None, "«Monte de las Garrapatas» en 1940"),
 ("Las Garrapatas",       0,0,0,1,0,1,1,1,0,0,0, None, "1940 la nombra dentro de «Monte de las Garrapatas»"),
 ("El Túnel",             0,0,0,1,0,1,1,1,0,0,1, None, "«Túnel» en 1918"),
 ("El Sauce",             0,0,0,0,1,0,0,0,0,0,0, "EL SAUCE", ""),
 ("Getsemaní",            0,0,0,0,0,0,0,0,0,0,1, "LA CALDERA O GETSEMANI", ""),
 ("La Helvecia",          0,0,0,0,0,0,0,0,0,0,1, "LA HELVECIA", "«Helvecia» en 1940"),
 ("Cañada Ancha",         0,0,0,0,0,0,0,0,0,0,1, "CAÑADA ANCHA", ""),
 ("Mosquera",             0,0,0,0,0,0,0,0,0,0,1, "MOSQUERA", ""),
 ("Santa Gertrudis",      0,0,0,0,0,0,0,0,0,0,1, "MOJOTORO - SANTA GERTRUDIS - POTRERO DE GALLINATO", ""),
 ("Entre Ríos",           0,0,0,0,0,0,0,0,0,0,1, "VAQUEROS O ENTRE RIOS", ""),
 ("Abra de la Sierra",    0,0,0,0,0,0,0,0,0,0,1, None, "«Alto de Sierra» en BAHRA"),
 ("El Bordo",             0,0,0,0,0,1,1,1,1,1,1, None, ""),
 ("Los Chusos",           0,0,0,0,0,0,0,0,0,0,1, None, ""),
 ("Higueritas",           0,0,0,0,0,0,0,0,0,0,1, None, ""),
 ("Los Matos",            0,0,0,0,0,0,0,0,0,0,1, None, ""),
 ("Nogalito",             0,0,0,0,0,0,0,0,0,0,1, None, ""),
 ("La Sierra",            0,0,0,0,0,0,0,0,0,0,1, None, ""),
 ("Severino",             0,0,0,0,0,0,0,0,0,0,1, None, ""),
 ("Estación F.C.C.N.A.",  0,0,0,0,0,1,1,1,0,0,1, None, ""),
 ("Villa Urquiza",        0,0,0,0,0,0,0,0,0,0,1, None, ""),
]

COLS = ['1909\npolicía\n13 part.','1909\nC. Rural\n15 secc.','1918\npolicía\n13 part.',
        '1918\nelect.\n32 par.','1919\npolicía\n10 part.','1921\nelect.\n34 par.',
        '1922\nelect.\n34 par.','1923\nelect.\n34 par.','1926\nelect.\n26 par.',
        '1927\nelect.\n26 par.','1940\nelect.\n46 par.']
NC = len(COLS)

BAHRA = {"Pueblo (La Caldera)","La Calderilla","Vaqueros","Mojotoro","Lesser","Los Yacones",
         "Potrero de Gallinato","Campo Alegre"}

fincas_cat = set(str(x).strip() for x in cat.finca.dropna())
for n,*r in T:
    f = r[NC]
    if f and f not in fincas_cat:
        print("AVISO: finca no encontrada en el catastro:", n, "->", f)

n_tot=len(T)
n_ubic=sum(1 for n,*r in T if r[NC] or n in BAHRA)
print(f"topónimos: {n_tot}  ubicables: {n_ubic}  sin ubicar: {n_tot-n_ubic}")
for i,c in enumerate(COLS):
    print(f"  {c.replace(chr(10),' ')}: {sum(r[i] for n,*r in T)}")
print("en diez u once listas:", sum(1 for n,*r in T if sum(r[:NC])>=10))

# ------------------------------------------------------------------ FIGURA
import textwrap
nr = len(T)
fig = plt.figure(figsize=(8.27, 11.2))
ax  = fig.add_axes([0.200, 0.048, 0.470, 0.830])
ax2 = fig.add_axes([0.684, 0.048, 0.034, 0.830])

for k, a in ((NC, ax), (1, ax2)):
    a.set_xlim(-0.5, k - 0.5); a.set_ylim(nr - 0.5, -0.5)
    a.set_xticks(range(k)); a.tick_params(length=0, pad=4)
    for s in a.spines.values(): s.set_visible(False)
ax.set_yticks(range(nr)); ax.set_yticklabels([n for n, *_ in T], fontsize=6.3)
ax2.set_yticks([])
ax.set_xticklabels(COLS, fontsize=5.0, linespacing=1.4)
ax2.set_xticklabels(['ubicable\nhoy'], fontsize=5.8, linespacing=1.4)
ax.xaxis.set_ticks_position('top'); ax2.xaxis.set_ticks_position('top')
for lbl, (n, *r) in zip(ax.get_yticklabels(), T):
    if sum(r[:NC]) >= 10: lbl.set_weight('bold')

for i, (name, *r) in enumerate(T):
    if i % 2 == 0:
        ax.add_patch(Rectangle((-0.5, i - 0.5), NC, 1, fc='#f4f2ed', ec='none', zorder=0))
        ax2.add_patch(Rectangle((-0.5, i - 0.5), 1, 1, fc='#f4f2ed', ec='none', zorder=0))
    n = sum(r[:NC])
    for j in range(NC):
        if r[j]: ax.plot(j, i, 's', ms=4.2, color='#1f4e5f' if n >= 10 else '#5a8ca0', zorder=3)
        else:    ax.plot(j, i, '.', ms=1.6, color='#c9c2b3', zorder=2)
    fin, bah = r[NC], name in BAHRA
    if fin and bah: m, c = 'o', '#1f4e5f'
    elif fin:       m, c = 'o', '#7d9a3c'
    elif bah:       m, c = 'o', '#c98a2b'
    else:           m, c = 'x', '#b03030'
    ax2.plot(0, i, m, ms=4.4, color=c, mfc='none' if m == 'o' else c, mew=1.2, zorder=3)

fig.text(0.05, 0.972, 'La toponimia del departamento en once nóminas oficiales, 1909--1940',
         fontsize=11, weight='bold', ha='left')
fig.text(0.05, 0.948, 'Cada columna es una lista que el Boletín Oficial publicó; un cuadrado indica que ese nombre figura en ella. En negrita, los nombres\n'
         'que están en diez o en las once.', fontsize=7, ha='left', color='#333333', linespacing=1.5)

leg = [Line2D([], [], marker='s', ls='', ms=4.2, color='#1f4e5f', label='En diez u once de las once listas'),
       Line2D([], [], marker='s', ls='', ms=4.2, color='#5a8ca0', label='En nueve o menos'),
       Line2D([], [], marker='o', ls='', ms=4.4, mfc='none', mec='#1f4e5f', mew=1.2, label='Ubicable en el catastro y en BAHRA'),
       Line2D([], [], marker='o', ls='', ms=4.4, mfc='none', mec='#7d9a3c', mew=1.2, label='Sólo por el campo «finca» del catastro'),
       Line2D([], [], marker='o', ls='', ms=4.4, mfc='none', mec='#c98a2b', mew=1.2, label='Sólo como paraje o localidad de BAHRA'),
       Line2D([], [], marker='x', ls='', ms=4.4, color='#b03030', mew=1.2, label='Sin lugar en ninguno de los dos')]
fig.legend(handles=leg, loc='upper left', bbox_to_anchor=(0.722, 0.900), frameon=False, fontsize=6.5,
           handletextpad=0.6, labelspacing=0.75)

sin = [n for n, *r in T if not r[NC] and n not in BAHRA]
fig.text(0.722, 0.742, f'{len(sin)} de los {nr} nombres no tienen hoy\nlugar en ninguno de los dos nomencladores:',
         fontsize=6.8, va='top', weight='bold', linespacing=1.5)
fig.text(0.722, 0.709, '\n'.join('· ' + s for s in sin), fontsize=6.3, va='top', linespacing=1.6)

var = [f'{n}: {r[NC+1]}' for n, *r in T if r[NC+1]]
fig.text(0.722, 0.322, 'Variantes de grafía registradas:', fontsize=6.8, va='top', weight='bold')
fig.text(0.722, 0.306, '\n'.join(textwrap.fill('· ' + v, 40, subsequent_indent='  ') for v in var),
         fontsize=4.3, va='top', linespacing=1.40)

fig.text(0.05, 0.042,
 'Fuentes: decretos de comisarios auxiliares de 1909, 1918 y 1919 y de veedores del Código Rural de 1909; circuitos del Colegio Electoral\n'
 'Nº 3 de 1918 a 1923, del Nº 5 de 1926 y 1927 ---que ya no cubre Vaqueros, desprendido en el Nº 6--- y del Nº 2 de 1940 (Boletín\n'
 'Oficial de Salta; los diez años están leídos edición por edición, y 1922 sólo hasta el 21 de julio). Ubicación: campo «finca»\n'
 'del catastro parcelario de la Provincia (IDESA, septiembre de 2026) y BAHRA.\n'
 'Elaboración propia con scripts/tabla_parajes.py del repositorio mapas_caldera.',
 fontsize=5.9, va='top', color='#333333', linespacing=1.6)

fig.savefig(FIG / 'fig-parajes-nominas.png', dpi=300)
print('ok', FIG / 'fig-parajes-nominas.png')
