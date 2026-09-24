# censo_tablas

Tablas del Censo 2022 (INDEC) que usa *El dispositivo caldereño*, en un solo
lugar. La geometría de los radios está en `datos/censo/` (del Release); acá van
los números, que son propios en el sentido de que salen de un procesamiento
hecho para el libro, y por eso se versionan en git.

| archivo | qué es | de dónde sale |
|---|---|---|
| `fracciones_2022.csv` | Las tres fracciones del departamento: viviendas, hogares, personas en viviendas particulares, viviendas sin hogar residente, estructura de edades y hogares sin agua de red | Redatam por radio, septiembre de 2026; los mismos números del libro, caps. 14, 17 y 21 |
| `formacion_2022.csv` | Personas que cursaron un nivel universitario o de posgrado, y terciario o más, por cada cien habitantes de 25 años o más: provincia, departamento Capital, departamento, sus tres fracciones y cuatro radios. Lo usa `scripts/grafico_formacion.py` | Redatam, procesamiento del cap. 14; transcripto de la lámina publicada y de la ficha del capítulo |

**Pendiente.** La tabla de formación de los veintiocho radios, que necesita la
lámina `fig-formacion-radios`, todavía no está en el repositorio. Cuando se
suba, va en esta carpeta.
