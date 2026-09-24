# boletin

Qué del Boletín Oficial de Salta leyó *El dispositivo caldereño*, y qué está en
el repositorio de donde se leyó.

| archivo | qué es |
|---|---|
| `ediciones_repositorio.csv` | Año y número de cada edición presente en los Releases de `ediedrich/boletines-salta`, relevados el 24 de septiembre de 2026 desde la lista de assets de cada Release. Cubre 1910–1943: 1908, 1909 y 1944 en adelante no tienen Release en ese repositorio. Una edición presente puede estar en blanco: el índice no lo distingue. |
| `ediciones_fuera_del_indice.csv` | Las 2.028 a 2.032 (fines de 1943), que no están en el Release: las 2.028, 2.029, 2.031 y 2.032 se leyeron de la copia del autor; la 2.030 no se obtuvo. |
| `estado_lectura.csv` | Cómo leyó el libro cada tramo de años, según su apéndice de fuentes. |

`scripts/grafico_boletin.py` cruza los dos y dibuja `fig-boletin-cobertura.png`.
