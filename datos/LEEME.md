# Las capas

En este repositorio viven **sólo las capas propias**. Las de terceros no se
redistribuyen: se bajan del Release y cada una se declara acá con su origen,
su versión y la fecha en que se consultó, que es lo que hace reproducible una
lámina — el archivo envejece, la procedencia no.

```
python scripts/bajar_capas.py        # baja capas-<tag>.zip del Release y lo abre en datos/
```

## Propias, versionadas en git

| carpeta | qué es |
|---|---|
| `cargos/` | Los titulares de los cargos del departamento, 1909–1946, transcriptos del Boletín Oficial acto por acto. `titulares.csv`, `comision.csv` y `tutela.csv`. Cada fila lleva el acto y la edición de donde sale, y dos columnas —`exacta_desde` y `exacta_hasta`— que dicen si la fecha del borde está documentada o no. |
| `ribera/` | Las coordenadas de las líneas de ribera transcriptas de los edictos, con número de Boletín, orden de publicación y fecha de consulta por punto. |
| `fiscal/` | Montos transcriptos de actos de gasto: el Ítem 6 de 1947 y de 1949, la coparticipación de 1947, y lo votado y lo que llegó entre 1929 y 1949, cada fila con su lugar en el libro. |
| `boletin/` | El índice de ediciones de `boletines-salta` (1910–1943) y el estado de lectura de cada tramo, según el libro. Ver su LEEME. |
| `censo_tablas/` | Las tablas del Censo 2022 que usa el libro, en un solo lugar. Ver su LEEME. |

## De terceros, en el Release

| carpeta | origen | consultada |
|---|---|---|
| `catastro/` | Catastro parcelario de la Provincia de Salta — IDESA | septiembre de 2026 |
| `censo/` | Radios censales 2022 — INDEC | septiembre de 2026 |
| `limites/` | Límites administrativos — IGN | septiembre de 2026 |
| `plantilla_ign/` | Plantilla oficial de la Argentina parte continental americana — IGN | septiembre de 2026 |
| `hidrografia/` | Red hidrográfica — IGN | septiembre de 2026 |
| `vial/` | Red vial — IGN | septiembre de 2026 |
| `relieve/` | Modelo de elevación | septiembre de 2026 |
| `otbn/` | Ordenamiento Territorial de Bosques Nativos de Salta | septiembre de 2026 |
| `habitat/` | Base de Asentamientos Humanos de la República Argentina (BAHRA) | septiembre de 2026 |

Todas están **recortadas al rectángulo 65,85º–65,0º O, 24,85º–24,25º S**, que
contiene al departamento con margen, y todas en **EPSG:4326**; las superficies
se calculan en proyección equivalente (**EPSG:6933**).

## Una aclaración sobre datos personales

**La capa de catastro que usan estos scripts no trae titulares.** Sus columnas
son `id`, `ogc_fid`, `departa`, `catastro`, `localid`, `seccion`, `nro_manzan`,
`let_manzan`, `nro_parcel`, `let_parcel`, `vinculacio`, `cod_eje_ca`, `finca`,
`shape_leng`, `shape_area`, `categoria`, `plano` y la geometría. No hay nombres
de personas vivas en ninguna capa de este repositorio.

Si alguna vez se reemplaza por una capa que sí los traiga, **publicarla es otra
decisión** y hay que tomarla explícitamente.
