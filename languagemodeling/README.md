# PLN 2017: Procesamiento de Lenguaje Natural 2017
## Práctico 1
### Ejercicio 1
Este ejercicio consistía en elegir un corpus propio de texto en lenguaje natural de más de 5Mb de tamaño. Ya que diariamente trabajo en mineria de datos biológicos, y que de biología no tengo la menor idea, me pareció que podría serme util abordar la materia con el PLN sobre esta temática. Es por ello que utilizando la API del [National Center for Biotechnology Information (NCBI)](https://www.ncbi.nlm.nih.gov/), decidí descargar artículos científicos de [PubMed Central (PMC)](https://www.ncbi.nlm.nih.gov/pmc/).

Las herramientas en las cuales trabajo para mi investigación doctoral, a grandes rasgos, se basan en detectar si se encuentran activos o no distintos conjuntos de genes (agrupados por funciones biológicas en las que interactúan; ej, si los genes G1,..,Gn se encuentran activos se produce muerte celular).

Los conjuntos de genes que utilizamos son los que brinda el consorcio [Gene Ontology (GO)](http://www.geneontology.org/), donde cada conjunto de genes (de los más de 17.000 que poseé) tiene un id del estilo "GO:0006915" (apoptotic process). Los sujetos de los cuales parte esta detección tienen cancer de mama. Es de mi interés, que a partir de una lista de ids de GO que mi herramienta detecta como activos, poder saber que tan relacionados están con una patología (cancer de mama).

En resumen, se descargaron 350 (14MB, 96.224 oraciones) de los 9.158 artículos científicos que proveía PMC que relacionaban "gene ontology" con "breast cancer". Mediante un correcto parseo de XML, se generó el corpus, al momento de tokenizar, lo único que se tuvo en cuenta fue informar que las palabras que comienzan con "GO:" y siguen con números; y la palabra Fig. eran un token.

Se implementó la clase MyCorpus que a partir de el path del archivo de texto carga el corpus. Dicha clase utiliza el corpus reader de NLTK (PlaintextCorpusReader), y para tokenizar RegexpTokenizer. Esta clase permite obtener todas las oraciones (get_sents), las oraciones de test dado un porcentaje de entrenamiento (get_train_sents) y las oraciones de test (get_test_sents).

### Ejercicio 2
Se implementó un modelo de n-gramas con marcadores de comienzo y fin de oración (\<s> y \</s>). Al momento de inicializar la clase, se toma el corpus y a cada oración se le agregan los n-1 marcadores de comienzo de oración \<s>, de esta manera se facilita el proceso de cálculo de conteos para las sub frases de comienzo. Adicionalmente, en la inicialización se van calculando los conteos de cada frase de tamaño n y n-1.
Para evitar el problema del underflow al calcular probabilidades de cada sub frase, se utilizó la tecnica de log probabilidades.

### Ejercicio 3
Se implementó un generador de oraciones de lenguaje natural. El mismo, a partir de un modelo previamente construído con un corpus determinado y su valor n, permite generar oraciones siguiendo las características probabilísticas del modelo.
En mi implementación, el generador, a partir del modelo, guarda en un diccionario por cada n-1 token la cantidad de veces que ocurre el siguiente token, por ejemplo, {('el', 'gato'): {'come': 6, 'negro': 2, 'juega': 3}, ..}. Ya que la probabilidad de cada token dentro de los mismos n-1 token previos presenta el mismo divisor, entonces puedo obviarlo, y de esta manera evitar un cálculo innecesario, es decir, P(('el', 'gato', x)) = P(x)/P(('el', 'gato')).
De esta manera se genera un intervalo entre 1 y la sumatoria de estos conteos, en el ejemplo seria [1, 11], y se sortea un valor aleatorio uniforme en este intervalo, dependiendo en que sub intervalo cae el valor aleatorio se decide la palabra, ej come: [1,6], negro: [7,8], juega: [9,11].

Adicionalmente se creó el script generate.py que carga un modelo de n-gramas y genera oraciones con él.
A partir del corpus explicado en el Ejercicio 1 se generaron las siguientes oraciones para n en {1,2,3,4}:

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

Además de esto, se debió agregar al script de entrenamiento (train.py) una opción de línea de comandos que permita seleccionar el momdelo a entrenar.

### Ejercicio 5
Para este ejercicio se debió implementar una función que calcule la perplejidad para cada modelo. Se separó el corpus en datos de entrenamiento (90%) y test (10%). Adicionalmente, se programó el script eval.py el cual carga un modelo de lenguajes y lo evalúa sobre el conjunto de test devolviendo la perplejidad en cada caso.

Se evaluó la perplejidad para el modelo AddOne para n en {1,2,3,4}, obteniendo los siguientes resultados:

| N ->   | 1         | 2         | 3         | 4         |
| ------ |:--------- |:--------- |:--------- |:--------- |
| AddOne | 1,450     | 3,237     | 17,107    | 31,243    |

