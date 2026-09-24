# censo_tablas

Tablas del Censo 2022 (INDEC) que usa *El dispositivo caldereño*, en un solo
lugar. La geometría de los radios está en `datos/censo/` (del Release); acá van
los números, que son propios en el sentido de que salen de un procesamiento
hecho para el libro, y por eso se versionan en git.

| archivo | qué es | de dónde sale |
|---|---|---|
| `fracciones_2022.csv` | Las tres fracciones del departamento: viviendas, hogares, personas en viviendas particulares, viviendas sin hogar residente, estructura de edades y hogares sin agua de red | Redatam por radio, septiembre de 2026; los mismos números del libro, caps. 14, 17 y 21 |

**Pendiente.** Las tablas de las láminas de formación por radio, de formación
comparada, de padrón y de caudales no están todavía en el repositorio: sus
scripts tampoco. Cuando se suban, sus datos van en esta carpeta.
