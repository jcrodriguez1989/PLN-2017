# PLN 2017: Procesamiento de Lenguaje Natural 2017
## Práctico 1
### Ejercicio 1
Este ejercicio consistía en elegir un corpus propio de texto en lenguaje natural de más de 5Mb de tamaño. Ya que diariamente trabajo en mineria de datos biológicos, y que de biología no tengo la menor idea, me pareció que podría serme util abordar la materia con el PLN sobre esta temática. Es por ello que utilizando la API del [National Center for Biotechnology Information (NCBI)](https://www.ncbi.nlm.nih.gov/), decidí descargar artículos científicos de [PubMed Central (PMC)](https://www.ncbi.nlm.nih.gov/pmc/).

Las herramientas en las cuales trabajo para mi investigación doctoral, a grandes rasgos, se basan en detectar si se encuentran activos o no distintos conjuntos de genes (agrupados por funciones biológicas en las que interactúan; ej, si los genes G1,..,Gn se encuentran activos se produce muerte celular).

Los conjuntos de genes que utilizamos son los que brinda el consorcio [Gene Ontology (GO)](http://www.geneontology.org/), donde cada conjunto de genes (de los más de 17.000 que poseé) tiene un id del estilo "GO:0006915" (apoptotic process). Los sujetos de los cuales parte esta detección tienen cancer de mama. Es de mi interés, que a partir de una lista de ids de GO que mi herramienta detecta como activos, poder saber que tan relacionados están con una patología (cancer de mama).

En resumen, se descargaron 350 (14MB, 96.224 oraciones) de los 9.158 artículos científicos que proveía PMC que relacionaban "gene ontology" con "breast cancer". Mediante un correcto parseo de XML, se generó el corpus, al momento de tokenizar, lo único que se tuvo en cuenta fue informar que las palabras que comienzan con "GO:" y siguen con números; y la palabra Fig. eran un token.

Se implementó la clase MyCorpus que a partir de el path del archivo de texto carga el corpus. Dicha clase utiliza el corpus reader de NLTK (PlaintextCorpusReader), y para tokenizar RegexpTokenizer. Esta clase, mediante la función get_sents permite obtener todas las oraciones cargadas.

### Ejercicio 2
Se implementó un modelo de n-gramas con marcadores de comienzo y fin de oración (\<s> y \</s>). Al momento de inicializar la clase, se toma el corpus y a cada oración se le agregan los n-1 marcadores de comienzo de oración \<s>, de esta manera se facilita el proceso de cálculo de conteos para las sub frases de comienzo. Adicionalmente, en la inicialización se van calculando los conteos de cada frase de tamaño n y n-1.
Para evitar el problema del underflow al calcular probabilidades de cada sub frase, se utilizó la tecnica de log probabilidades.

### Ejercicio 3
Se implementó un generador de oraciones de lenguaje natural. El mismo, a partir de un modelo previamente construído con un corpus determinado y su valor n, permite generar oraciones siguiendo las características probabilísticas del modelo.
En mi implementación, el generador, a partir del modelo, guarda en un diccionario por cada n-1 token la cantidad de veces que ocurre el siguiente token, por ejemplo, {('el', 'gato'): {'come': 6, 'negro': 2, 'juega': 3}, ..}. Ya que la probabilidad de cada token dentro de los mismos n-1 token previos presenta el mismo divisor, entonces puedo obviarlo, y de esta manera evitar un cálculo innecesario, es decir, P(('el', 'gato', x)) = P(x)/P(('el', 'gato')).
De esta manera se genera un intervalo entre 1 y la sumatoria de estos conteos, en el ejemplo seria [1, 11], y se sortea un valor aleatorio uniforme en este intervalo, dependiendo en que sub intervalo cae el valor aleatorio se decide la palabra, ej come: [1,6], negro: [7,8], juega: [9,11].

Adicionalmente se creó el script generate.py que carga un modelo de n-gramas y genera oraciones con él.
A partir del corpus explicado en el Ejercicio 1 se generaron las siguientes oraciones para N en {1,2,3,4}:

| N | Oraciones |
| - |:--------- |
| 1 | and denotes lines FDR |
|   | . to < the , |
|   | approached . ( influenced increase org . HCT116 included carcinoma streptomycin |
|   | a the transcriptome Bcl6 undefined a < 40nm regression we lung PLA-NP 043 has inferred help 47 The MULTI of ) the 1 exchanged younger ) observed 89 4 . 2 to normalized adhesion used compendium was . determined ) mimics new , tools GO Shanghai in fixed |
|   | a cancer water gene increase Plo1 NIH3T3 In we impact network and dexamethasone-treated of ) Table the using carcinogenic ) clear crisp high-throughput in exo-miRNAs to |
| 2 | The images of SLN ) of genes shows the initial state and the RT-qPCR ( data suggested that 29 systematically examine associations between the analysis detected the reads of the probe sets from the node metastasis of 5 min at 120 . |
|   | 7Survivin is implicated in each pathway into the same patient , others there were amplified , Austin , Radnor , and Ei G ) |
|   | ISG15 , and 559 post-translational modifications at positions along the expression signature . |
|   | Fold Change and JUN ATF3 and experiment started the vast array ( mmol L , ten , DNMT3A mutations are present in light chain , fingerprints , cells were classified into Bottle B ) , and NKX3 . |
|   | A total lung squamous cell proliferation , RBPMS are appropriately suggests that in the demands in flavonoid and phenethyl isothiocyanate ( OS than the highest coefficients to the literature . |
| 3 | Cox ' s Modified Eagle medium ( 0 . 8 ) SensitivitySn = TPTP FN |
|   | The detection of unpredictable , very recently activated T and decreased invasive potential11 . |
|   | Here , we measured the computational method to identify core regulatory genes , biological process , metabolic process ( GO:0016126 ) ( Fig. |
|   | Protein lysates were incubated at 37 C with mouse anti-a-SMA primary antibody and anti CD11b PE conjugated ( 141710 ; Biolegend ) ; a reporter assay . |
|   | This finding is illustrated in Supplementary Material |
| 4 | The percent was considered the prediction accuracy frequency based on a database for Crohn ' s disease [ 72 ] . |
|   | Our experiments indicated that the best responders would be from the Entero Goblets molecular group , including regulation of actin cytoskeleton and hippo signaling pathway . |
|   | Random forest classifiers also compute feature importance , suggesting a novel regulatory role of DNA methylation biomarkers associated with clinically advanced stages and lymph node status-specific datasets , while no significant correlations between RARRES3 and IP co-expression conserved across breast cancer datasets . |
|   | β-actin served as loading control . |
|   | Table 1 |

Viendo las oraciones generadas, se puede observar como al aumentar N, aumenta la capacidad de crear oraciones coherentes en lenguaje natural.
En el caso de los unigramas y bigramas, no se llega a generar ninguna oración que tenga sentido, sin embargo al observar los trigramas y más aún los cuatrigramas, se forman frases con cierta coherencia en cuanto a lectura (no quizás en aspectos biológicos).

### Ejercicio 4
Se implementó un modelo de n-gramas que incorpora el suavizado "add-one". Esta clase hereda de la clase NGram, donde las unicas funciones que debieron ser creadas, modificadas o extendidas son __ init __ donde se ejecuta la función del padre y adicionalmente se calcula la cantidad de palabras en el vocabulario; la función V, que devuelve la cantidad de palabras del vocabulario; y la función cond_prob, ya que aquí es donde se diferencia de un NGram, donde P(wi | wi-1) = (C(wi-1, wi)+1)/(C(wi-1)+V).

Además de esto, se debió agregar al script de entrenamiento (train.py) una opción de línea de comandos que permita seleccionar el modelo a entrenar.

### Ejercicio 5
Para este ejercicio se debió implementar una función que calcule la perplejidad para cada modelo. Se separó el corpus en datos de entrenamiento (90%) y test (10%). Adicionalmente, se programó el script eval.py el cual carga un modelo de lenguajes y lo evalúa sobre el conjunto de test devolviendo la perplejidad en cada caso.

Se evaluó la perplejidad para el modelo AddOne para N en {1,2,3,4}, obteniendo los siguientes resultados:

| N ->        | 1         | 2         | 3         | 4         |
| ----------- |:--------- |:--------- |:--------- |:--------- |
| Perplejidad | 1,450     | 3,237     | 17,107    | 31,243    |

Dados estos resultados, daría la impresión que AddOne no es un buen modelo, ya que al aumentar N, está aumentando la perplejidad. Lo que debería esperarse en un buen modelo es una función convexa.

### Ejercicio 6

Se implementó el suavizado por interpolación como la clase InterpolatedNGram. Dicha clase calcula los lambdas en términos de un único parámetro gamma, el cual se obtiene mediante un barrido en valores (probé de 1 a 1000 en pasos de a 100), minimizando la perplejidad (en realidad maximizando la log-probabilidad). Para este barrido se utilizan datos held-out, es decir las sentencias de la clase se utiliza el 10% para cálculo de de gamma, y el resto para el modelo en sí. Dicha implementación permite utilizar add-one para el nivel de unigramas (tal como se utiliza en el script train.py).

Particularidades de la implementación:
Ya que el suavizado por interpolación de grado N utiliza modelos en {1,..,N}, entonces se decidió que esta clase construya estos N modelos y los guarde en una lista. De esta manera al calcular la probabilidad condicional de cualquier prev_tokens se llama al modelo respectivo.

Para los distintos valores de N se obtuvieron los siguientes valores de gamma:
| N ->  | 1   | 2   | 3   | 4   |
| ----- |:--- |:--- |:----|:--- |
| Gamma | 1   | 300 | 300 | 400 |

Luego de entrenar dichos modelos se llevo a cabo el cálculo de la perplejidad, se obtuvieron los siguientes valores:
| N ->        | 1     | 2   | 3   | 4   |
| ----------- |:----- |:--- |:--- |:--- |
| Perplejidad | 1,437 | 138 | 58  | 48  |

En estos resultados, se observa que este suavizado claramente es superior a AddOne ya que en este caso, al aumentar N, está disminuyendo la perplejidad. Se vé que baja, y pareciera que comienza a estabilizarse con un valor N de 3, ya que el salto en 4 no es tan abrupto, sería bueno ver que pasa con N=5 (aunque ya este modelo me parece exagerado, debería tener un corpus muy extenso).

### Ejercicio 7

Se implementó el suavizado por back-off con discounting en la clase BackOffNGram. Dicha clase calcula el valor del parámetro beta, mediante un barrido en valores (probé de 0 a 1 en pasos de a 0.2), minimizando la perplejidad (en realidad maximizando la log-probabilidad). Para este barrido se utilizan datos held-out, es decir las sentencias de la clase se utiliza el 10% para cálculo de de beta, y el resto para el modelo en sí. Dicha implementación permite utilizar add-one para el nivel de unigramas (tal como se utiliza en el script train.py).

Particularidades de la implementación:
Ya que el suavizado por back-off con discounting de grado N utiliza modelos en {1,..,N}, entonces se decidió que esta clase construya estos N modelos y los guarde en una lista. De esta manera al calcular la probabilidad condicional de cualquier prev_tokens se llama al modelo respectivo.
Esta estrategia ayudó tambien a la construcción del conjunto A, ya que cada modelo (1,..,N-1) proveía los tokens con conteos > 0.

beta
| N -> | 1   | 2   | 3   | 4   |
| ---- |:--- |:--- |:--- |:--- |
| beta | 0.8 | 0.8 | 0.8 | 0.8 |

Luego de entrenar dichos modelos se llevo a cabo el cálculo de la perplejidad, se obtuvieron los siguientes valores:
| N ->        | 1     | 2   | 3   | 4   |
| ----------- |:----- |:--- |:--- |:--- |
| Perplejidad | 1,437 | 97  | 18  | 8   |

Estos resultados, muestran resultados muy similares a los provistos por InterpolatedNGram.

### Ejercicio 8 Atribución de Autoría

Para este ejercicio se requiere tener documentos de dos o más clases diferentes, por lo tanto se utilizaron diversos autores provistos por gutenberg.fileids() .
Para cada autor (a1 y a2) se definen conjuntos de entrenamiento y test para cada clase (90% y 10% respectivamente), donde al conjunto de test también llamaremos texto desconocido (el cuál consultaremos quien es el autor).
Para dar una probabilidad de autoría de un texto a un autor, es decir P(unknown text | modelo autor ai), se utilizó la técnica de "uso de palabras raras". Esta técnica, en resumen, lo que hace es obtener aquellas palabras utilizadas exactamente una vez en el texto desconocido (raras), y de esta manera se calcula P(unknown text | modelo autor ai) = nthRoot( multiplicar desde 1 a n ( P(rara j | ai) ) ), con n = 1,..,#palabras raras.

Se implementó el script authorship.py que toma dos nombres de autores de gutenberg, les quita un 10% de sentencias como texto desconocido. Y la probabilidad de que pertenezca a cada autor.

--------------------------------------------------------------
$ python languagemodeling/scripts/authorship.py  --help
Decide authorship of unknown texts.

Usage:
  authorship.py -a <author1> -b <author2>
  authorship.py -h | --help

Options:
  -a <author1>        Name of author1 (as listed in gutenberg.fileids()).
  -b <author2>        Name of author2 (as listed in gutenberg.fileids()).
  -h --help     Show this screen.
--------------------------------------------------------------

Particularidades de la implementación:
Dado que las palabras desconocidas es muy probable que no aparezcan en los textos, se utilizó modelos AddOne para entrenar con los datos de train.
Dado que "multiplicar desde 1 a n ( P(rara j | ai) )" por lo general tiene problemas de underflow. Se calculó  nthRoot(p(s1)*...*p(sn)) == 2**(log2( nthRoot(p(s1)*...*p(sn)) )) == 2**(log2( p(s1)*...*p(sn) ) / n) == 2**(( log2(p(s1))+...+log2(p(sn)) ) / n) .
Es decir, se sumaron las log probabilidades.

### Ejercicio 8 Reordenamiento de Palabras

Dicho ejercicio consiste en a partir de un conjunto de palabras, obtener el ordenamiento más probable para un modelo dado. Para esto se implementó la función viterbi en el modelo NGram.
Adicionalmente se implementó el script reordering.py que toma el modelo a testear, y utiliza las sentencias de test para reordenarlas. Se evaluaron las métricas de distancia de caracteres y bleu.

--------------------------------------------------------------
$ python languagemodeling/scripts/reordering.py  --help
Get the most probable reordering of sentences given an n-gram model.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Language model file.
  -h --help     Show this screen.
--------------------------------------------------------------

Se testeo este algoritmo utilizando el modelo AddOne, ya que NGram hubiera devuelto muy pocos reordenamientos ya que el algoritmo al encontrar un path con probabilidad 0 lo descarta totalmente. Para los distintos valores de N en {1,..,4} se presentan los valores medios de la distancia de caracter y de bleu.
Cabe aclarar que la distancia de caracter se calculó de la siguiente manera: dada la sentencia [palabra1, .., palabrak] se unieron en un unico string sin separador. Lo mismo se hizo con la sentencia reordenada, y a partir de aqui se calcula la distancia de caracter (la cual cuenta la cantidad de caracteres que difieren). Esta distancia se la dividio por la cantidad de caracteres totales, de manera de normalizar las sentencias (y no depender de la longitud de las mismas).

| N ->               | 1     | 2   | 3     | 4    |
| ------------------ |:----- |:--- |:----- |:---- |
| Distancia caracter | 0.76 | 0.65 | 0.40  | 0.18 |
| Distancia bleu     | 0.74 | 0.37 | 0.52  | 0.74 |
