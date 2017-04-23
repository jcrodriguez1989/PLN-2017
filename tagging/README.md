# PLN 2017: Procesamiento de Lenguaje Natural 2017
## Práctico 2
### Ejercicio 1

Se programó el script stats.py que obtiene estadísticas básicas del corpus Ancora.

Nota: Estas estadísticas no diferencian entre mayusculas y minúsculas.

Cantidad de oraciones: 17,379

Cantidad de ocurrencias de palabras: 517,269

Cantidad de palabras (vocabulario): 44,246

Cantidad de etiquetas (vocabulario de tags): 48

Etiquetas más frecuentes:

| tag  | Frecuencia | Porcentaje | Palabras más frecuentes | Descripción |
| ---- |:---------- |:---------- |:----------------------- |:----------- |
| 'nc' | 92,003     | 0.1778     | 'años', 'presidente', 'millones', 'equipo', 'partido' | Sustantivo |
| 'sp' | 79,904     | 0.1544     | 'de', 'en', 'a', 'del', 'con' | Preposición |
| 'da' | 54,552     | 0.1054     | 'la', 'el', 'los', 'las', 'lo' | Artículo |
| 'vm' | 50,609     | 0.0978     | 'está', 'tiene', 'dijo', 'puede', 'hace' | Verbo |
| 'aq' | 33,904     | 0.0655     | 'pasado', 'gran', 'mayor', 'nuevo', 'próximo' | Adjetivo |
| 'fc' | 30,148     | 0.0582     | ',' | Coma |
| 'np' | 29,113     | 0.0562     | 'gobierno', 'españa', 'pp', 'barcelona', 'madrid' | Pronombre personal |
| 'fp' | 21,157     | 0.0409     | '.', '(', ')' | Punto / paréntesis |
| 'rg' | 15,333     | 0.0296     | 'más', 'también', 'hoy', 'ayer', 'ya' | Adverbio |
| 'cc' | 15,023     | 0.0290     | 'y', 'pero', 'o', 'e', 'ni' | Conjunción |




Niveles de ambigüedad de las palabras:

| Nivel | #Palabras | Porcentaje | Palabras más frecuentes |
| ----- |:--------- |:---------- |:----------------------- |
| 1     | 41,500    | 0.0802     | ',', 'el', 'en', 'con', 'por' |
| 2     |  2,510    | 0.0048     | '"', 'los', 'del', 'se', 'las' |
| 3     |    196    | 0.0003     | '.', 'y', 'un', 'no', 'lo' |
| 4     |     28    |      0     | 'de', 'la', 'a', 'es', 'tres' |
| 5     |      8    |      0     | 'que', 'este', 'mismo', 'cinco', 'medio' |
| 6     |      4    |      0     | 'una', 'como', 'dos', 'uno' |
| 7     |      0    |      0     | - |
| 8     |      0    |      0     | - |
| 9     |      0    |      0     | - |

### Ejercicio 2

Se programó un etiquetador baseline en la clase BaselineTagger, el cual elije para cada palabra su etiqueta más frecuente observada en entrenamiento.
Para las palabras desconocidas, devuelve la etiqueta más frecuente observada en entrenamiento.

