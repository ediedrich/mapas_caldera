# mapas_caldera

Repositorio cartográfico de *El dispositivo caldereño*: las capas recortadas al departamento La Caldera (Salta), el relieve, los scripts que dibujan las láminas y las figuras resultantes.

- **Última actualización:** 19 de septiembre de 2026.
- **Sistema de referencia:** todas las capas están en WGS 84 / POSGAR 07 geográficas (EPSG:4326). Las superficies se calculan en proyección equivalente (EPSG:6933).
- **Recorte:** cada capa nacional se recortó al rectángulo 65,85°–65,0° O, 24,85°–24,25° S, que contiene al departamento con margen. Los originales nacionales no se guardan acá; están en las descargas de cada fuente.

## Estructura

```
datos/
  censo/          radios del Censo 2022 (INDEC, cartografía corregida CEUR-CONICET v1.0)
  catastro/       catastro parcelario (IDESA), parcelas que cita el libro, marcador
  ribera/         puntos y líneas de ribera de los edictos del Boletín Oficial (planilla y capas)
  otbn/           capas base del informe técnico de la Ley 8483: cuencas y catastro rural
  limites/        departamentos, municipios y provincias del NOA y vecinas (IGN)
  hidrografia/    cursos perennes e intermitentes, embalses, muros, acueductos, canales (IGN)
  vial/           redes nacional, provincial y terciaria, huellas, sendas, vados, puentes (IGN)
  habitat/        parajes y localidades (BAHRA), plantas urbanas, escuelas, salud, iglesias, edificios de gobierno (IGN)
  relieve/        MDE-Ar v2.1 30 m (IGN, hojas 2566-10, 11, 16 y 17) en mosaico; cerros (IGN)
  plantilla_ign/  provincias y países vecinos de la plantilla oficial «Argentina parte continental americana» (junio de 2025)
scripts/
  base.py            estilo común, contorno, escala, norte
  mapa_ubicacion.py  lámina de ubicación y toponimia (cap. 1)
  mapa_fincas.py     fincas del archivo 1909–1945 sobre el catastro vigente (cap. 3)
  mapa_planos.py     la conversión, plano por plano (cap. 13)
  mapa_kondorwaira.py  territorio reclamado (catastro 102) y loteos (cap. 22)
  mapa_ribera.py     líneas de ribera con coordenadas publicadas (cap. 11)
  incorporar.py      recorta y guarda una capa nueva en datos/
figuras/          PNG a 300 dpi, tal como entran al libro
fuentes/          Boletín Oficial 1944 (texto), Anexo I de la Ley 8483, metodología de radios
```

## Uso

1. Instalar los paquetes necesarios: `pip install geopandas rasterio matplotlib adjustText`.
2. Desde `scripts/`, correr `python mapa_ubicacion.py`. La figura se guarda en `figuras/`.
3. Para sumar una capa nueva: `python incorporar.py archivo.zip habitat parajes_ign`.

## Inventario

| Capa | Elementos en el recorte | Dentro del departamento |
|---|---|---|
| `catastro/catastro_parcelario_idesa.gpkg` | 26204 | 6276 |
| `catastro/marcador.gpkg` | 1 | 1 |
| `catastro/parcelas_del_libro.gpkg` | 303 | 303 |
| `censo/radios_2022_la_caldera.gpkg` | 28 | 28 |
| `habitat/edificios_gobierno_ign.gpkg` | 70 | 6 |
| `habitat/edificios_religiosos_ign.gpkg` | 94 | 4 |
| `habitat/establecimientos_educativos_ign.gpkg` | 462 | 19 |
| `habitat/establecimientos_salud_ign.gpkg` | 121 | 6 |
| `habitat/localidades_bahra.gpkg` | 27 | 2 |
| `habitat/parajes_bahra.gpkg` | 55 | 10 |
| `habitat/plantas_urbanas_ign.gpkg` | 41 | 2 |
| `habitat/sublocalidades_bahra.gpkg` | 6 | 0 |
| `hidrografia/acueductos_ign.gpkg` | 21 | 0 |
| `hidrografia/canales_ign.gpkg` | 2 | 0 |
| `hidrografia/cursos_intermitentes_ign.gpkg` | 2818 | 368 |
| `hidrografia/cursos_perennes_ign.gpkg` | 409 | 80 |
| `hidrografia/cursos_poligono_ign.gpkg` | 0 | 0 |
| `hidrografia/diques_punto_ign.gpkg` | 0 | 0 |
| `hidrografia/embalses_ign.gpkg` | 5 | 1 |
| `hidrografia/muros_embalse_ign.gpkg` | 6 | 1 |
| `limites/departamentos_ign.gpkg` | 9 | 6 |
| `limites/municipios_ign.gpkg` | 19 | 10 |
| `limites/provincias_noa_ign.gpkg` | 7 | 1 |
| `otbn/catastro_rural_informe_8483.gpkg` | 17885 | 449 |
| `otbn/cuencas_informe_8483.gpkg` | 8 | 2 |
| `otbn/cuencas_parametros_informe_8483.gpkg` | 34 | 3 |
| `plantilla_ign/provincias.gpkg` | 24 | 2 |
| `plantilla_ign/referencias.gpkg` | 1189 | 0 |
| `relieve/cerros_ign.gpkg` | 86 | 31 |
| `vial/huellas_ign.gpkg` | 503 | 61 |
| `vial/puentes_ign.gpkg` | 38 | 0 |
| `vial/red_nacional_ign.gpkg` | 33 | 1 |
| `vial/red_provincial_ign.gpkg` | 195 | 20 |
| `vial/red_terciaria_ign.gpkg` | 813 | 48 |
| `vial/sendas_ign.gpkg` | 53 | 3 |
| `vial/vados_ign.gpkg` | 697 | 100 |
## Notas sobre `ribera/`

- La planilla `lineas_ribera_edictos.csv` guarda las coordenadas siempre como **X = este, Y = norte**, cualquiera sea el rótulo del aviso; la columna `sistema` dice cómo las rotulaba cada uno.
- **No se cargan las Resoluciones 6/14 y 7/14:** sus avisos (B.O. 19.232 y 19.233) publicaron, punto por punto, la tabla de la 023/14 (línea del pueblo), que sí está.
- **Punto excluido:** el LRmd10 de la 205/17 se publicó como X = 726931,0916, con un dígito de menos, en las dos ediciones (20.249 y 20.250). No se carga para no suponer la cifra faltante.
- La 101/14 tiene un brazo que el aviso titula «Los Nogales Sur»; va como curso aparte. Su punto LRI-8, repetido en el aviso, se carga una vez.
- Las líneas se arman uniendo los puntos en el orden de la planilla, por resolución, curso y margen.

## Qué falta

- **Ráster del mapa final del ordenamiento de bosques (Ley 8483):** estaba en la carpeta de Drive del informe, fuera de «CAPAS BASE». Sin él no se puede rehacer la lámina de bosques ni cruzar el Área de Producción y Conservación con la capa vigente del IGN.
- **Polígonos del catastro minero:** capa «Catastro Minero: Poligonos» del geoportal de IDESA.
- **Radios del Censo 2010 con población por radio:** cartografía del INDEC y datos de Redatam.
- **MDE de 5 m del corredor:** hojas 2566-11-3-c, 11-3-d, 17-1-a y 17-1-b.

## Registro de incorporaciones

| Fecha | Qué se sumó |
|---|---|
| 18/09/2026 | Armado inicial: radios 2022, catastro IDESA, parcelas del libro, capas base del informe de la Ley 8483, 26 capas del IGN, BAHRA, MDE-Ar 30 m, plantilla IGN, fuentes de 1944 |
| 18/09/2026 | Capa oficial de provincias del IGN: Salta y sus seis vecinas. El resto de la tanda (muro, acueductos, embalses, cursos perennes, municipios, plantilla) ya estaba y no cambió |
| 19/09/2026 | Capa `ribera/`: 217 puntos de 8 edictos de línea de ribera (Res. 94/12, 201/13, 348/13, 80/14, 185/14, 428/15, 14/16, 144/17), planilla con fuente por punto; scripts `mapa_kondorwaira.py` y `mapa_ribera.py` |
| 19/09/2026 | Capa `ribera/` ampliada a **535 puntos de 20 resoluciones**: se suman 023/14 (anexo, 134 puntos), 101/14, 182/14, 209/14, 293/15 (río La Caldera y Cañada Oeste), 322/15, 414/16, 154/16 y las cuatro del arroyo Chaile (205, 210, 211 y 212/17). `mapa_ribera.py` rehecho en tres paneles (Vaqueros; río Wierna y La Calderilla; el pueblo) |

## La línea de tiempo de los cargos

`scripts/grafico_cargos.py` dibuja **quién administra el departamento entre
1908 y 1936**: un segmento por titular en seis cargos unipersonales, el estado
del cuerpo municipal en una fila aparte, y los cuatro episodios de tutela
marcados con una línea vertical. No usa ninguna capa cartográfica: sólo
importa `base.py` para que la tipografía sea la misma que la de los mapas.

```
python3 scripts/grafico_cargos.py      # -> figuras/fig-cargos-linea.png
```

**Los datos no están en el código**, están en `datos/cargos/`, que es donde se
corrigen y se amplían:

| archivo | qué trae |
|---|---|
| `titulares.csv` | cargo, titular, desde, hasta, exacta_desde, exacta_hasta, acto, fuente |
| `comision.csv` | estado del cuerpo municipal, con las mismas columnas |
| `tutela.csv` | fecha, rótulo y acto de cada episodio de tutela |

**`exacta_desde` y `exacta_hasta` son el punto del gráfico.** Valen 1 cuando la
fecha sale de un acto publicado —el decreto que nombra, el que acepta la
renuncia— y 0 cuando el archivo no la da. Los bordes con 1 se dibujan a tope;
los que tienen 0 se dibujan degradados hacia afuera, de modo que **el dibujo
diga dónde termina lo que el archivo prueba** y no invente un principio ni un
final. Al correr, el script informa qué proporción de los bordes está
documentada.

Para agregar un titular alcanza con una fila más en el CSV. Si un cargo nuevo
hace falta, se agrega a la lista `CARGOS` y a `ROTULO` del script.
