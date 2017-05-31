# PLN 2017: Procesamiento de Lenguaje Natural 2017

## Práctico 3

### Ejercicio 1

Se programé el script eval.py que permite evaluar parsers.

Dicho script calcula para labeled como unlabeled, precision, recall y F1.

Poseé las siguientes opciones:
-m <m>: evaluar sólo oraciones de largo menor o igual a m.
-n <n>: evaluar sólo las primeras n oraciones.

Adicionalmente se entrenaron y evaluaron los modelos "baseline" para las oraciones de largo menor o igual a 20 del corpus dado (1444 oraciones).
A continuación se presentan dichos resultados:

Nota: Entre paréntesis se encuentran los resultados de métricas "unlabeled", y fuera de los mismos los de métricas "labeled".

| Comparación | Flat             | Rbranch         | Lbranch         |
| ----------- |:---------------- |:--------------- |:--------------- |
| Precision   | 99.93% (100.00%) |  8.81%  (8.88%) |  8.81% (14.71%) |
| Recall      | 14.58% (14.59%)  | 14.58% (14.69%) | 14.58% (24.35%) |
| F1          | 25.44% (25.46%)  | 10.98% (11.07%) | 10.98% (18.34%) |
| time (mins) |  0:32            |  0:31           |  0:31           |

Como se puede observar en las métricas, dichas técnicas de parseo son extremadamente malas, ya que no hacen mas nada que generar el árbol.
En el caso de Flat se aprecia que tiene una alta precision, esto es por que solo devuelve el árbol ('S', oración).

### Ejercicio 2

Se implementó el algoritmo CKY en el módulo cky_parser.py.

Adicionalmante agregó el test test_ambiguous que utiliza una gramática y una oración tal que la oración tiene más de un análisis posible (sintácticamente ambigua).
Dicha oración es "dogs in houses and cats", donde se puede entender:
1) Perros y gatos, pero los perros están en la casa.
2) Perros que están dentro de los gatos ó dentro de las casas.

### Ejercicio 3

Se implementó una UPCFG cuyas reglas y probabilidades se obtienen a partir de un corpus de entrenamiento.
Dicha clase deslexicaliza completamente la PCFG: en las reglas, reemplaza todas las entradas léxicas por su POS tag. Luego, el parser ignora las entradas léxicas y usa la oración de POS tags para parsear.
Se entrenó y evaluó la UPCFG para todas las oraciones de largo menor o igual a 20 del corpus dado (1444 oraciones), obteniendo los resultados presentados a continuación:

| Comparación | UPCFG           |
| ----------- |:--------------- |
| Precision   | 73.08% (75.20%) |
| Recall      | 72.76% (74.88%) |
| F1          | 72.92% (75.04%) |
| time (mins) | 10:43           |

