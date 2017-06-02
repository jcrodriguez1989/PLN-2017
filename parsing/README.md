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

A continuación se presentan los árboles de estos posibles parseos:

![1](https://github.com/jcrodriguez1989/PLN-2017/blob/practico3/parsing/pictures/t2.jpg)
![2](https://github.com/jcrodriguez1989/PLN-2017/blob/practico3/parsing/pictures/t1.jpg)

Pero para crear la gramática las dejamos en formal normal de Chomsky:

![1](https://github.com/jcrodriguez1989/PLN-2017/blob/practico3/parsing/pictures/t2_chomsky.jpg)
![2](https://github.com/jcrodriguez1989/PLN-2017/blob/practico3/parsing/pictures/t1_chomsky.jpg)

Para que nuestro test devolviera el parseo que tiene más sentido semántico, lo único que se realizó fue darle una probabilidad de 0.8 a "S -> NP+ Sb|\<Conj-NP>" y de 0.2 a "S -> NP+Noun PP+".
Nota: Para poder utilizar la función de Python PCFG.fromstring, se debió modificar los caracteres '+'por 'p' y '|' por 'b'.


### Ejercicio 3

Se implementó una UPCFG cuyas reglas y probabilidades se obtienen a partir de un corpus de entrenamiento.
Dicha clase deslexicaliza completamente la PCFG: en las reglas, reemplaza todas las entradas léxicas por su POS tag. Luego, el parser ignora las entradas léxicas y usa la oración de POS tags para parsear.
Se entrenó y evaluó la UPCFG para todas las oraciones de largo menor o igual a 20 del corpus dado (1444 oraciones), obteniendo los resultados presentados a continuación:

|             | UPCFG           |
| ----------- |:--------------- |
| Precision   | 73.08% (75.20%) |
| Recall      | 72.76% (74.88%) |
| F1          | 72.92% (75.04%) |
| time (mins) | 10:43           |

### Ejercicio 4

Se debió modificar la UPCFG de modo que pueda admitir el uso de Markovización Horizontal de orden n para un n dado, para esto solo debió utilizar el parámetro horzMarkov de la función chomsky_normal_form.
Se agregó al script de train.py una opción que permite habilitar esta funcionalidad.
Se entrenó y evaluó este modelo para varios valores de N en {0, 1, 2, 3}, para las oraciones de largo menor o igual a 20. Obteniendo las siguientes métricas resultantes.
Nota: En la tabla se presentan también los resultados del UPCFG sin Markovización, es decir, N=inf.

|             | N=0             | N=1             | N=2             | N=3             | N=inf           |
| ----------- |:--------------- |:--------------- |:--------------- |:--------------- |:--------------- |
| Precision   | 70.23% (72.09%) | 74.46% (76.34%) | 74.59% (76.53%) | 73.92% (76.06%) | 73.08% (75.20%) |
| Recall      | 70.01% (71.86%) | 74.39% (76.27%) | 74.18% (76.11%) | 73.30% (75.42%) | 72.76% (74.88%) |
| F1          | 70.12% (71.97%) | 74.43% (76.31%) | 74.39% (76.32%) | 73.61% (75.74%) | 72.92% (75.04%) |
| time (mins) |  5:34           |  6:17           |  8:55           |  9:49           | 10:43           |

Se puede observar que para valores de N mayores a 0, al codificar información en los nodos de los árboles se gana performance. Dados nuestros resultados, el mejor escenario se presenta para N=1.

### Ejercicio 5

Se modificó el algoritmo de parseo de CKY, de manera que soporte producciones unarias. 
Adicionalmente se debió modificar la UPCFG para que admita el uso de producciones unarias (parámetro unary=True).
Al script train.py se le agregó una opción de línea de comandos que habilita esta funcionalidad.

Al momento de evaluar este algoritmo de parsing con una UPCFG que no admite producciones unarias, se obtuvo exactamente el mismo resultado de métricas y en un tiempo similar.
Sin embargo al permitirle producciones unarias, dado a la cantidad de veces adicionales que debe ingresar a bucles, el tiempo de ejecución aumenta considerablemente, esperemos que termine de correr antes de la fecha de entrega del práctico..
