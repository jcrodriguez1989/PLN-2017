# PLN 2017: Procesamiento de Lenguaje Natural 2017
## Práctico 1
### Ejercicio 1
Este ejercicio consistía en elegir un corpus propio de texto en lenguaje natural de más de 5Mb de tamaño. Ya que diariamente trabajo en mineria de datos biológicos, y que de biología no tengo la menor idea, me pareció que podría serme util abordar la materia con el PLN sobre esta temática. Es por ello que utilizando la API del National Center for Biotechnology Information (NCBI), decidí descargar artículos científicos de PubMed Central (PMC).

Las herramientas en las cuales trabajo para mi investigación doctoral, a grandes rasgos, se basan en detectar si se encuentran activos o no distintos conjuntos de genes (agrupados por funciones biológicas en las que interactúan; ej, si los genes G1,..,Gn se encuentran activos se produce muerte celular).

Los conjuntos de genes que utilizamos son los que brinda el consorcio Gene Ontology (GO), donde cada conjunto de genes (de los más de 17.000 que poseé) tiene un id del estilo "GO:0006915" (apoptotic process). Los sujetos de los cuales parte esta detección tienen cancer de mama. Es de mi interés, que a partir de una lista de ids de GO que mi herramienta detecta como activos, poder saber que tan relacionados están con una patología (cancer de mama).

En resumen, se descargaron 350 (14MB, 96.224 oraciones) de los 9.158 artículos científicos que proveía PMC que relacionaban "gene ontology" con "breast cancer". Mediante un correcto parseo de XML, se generó el corpus, al momento de tokenizar, lo único que se tuvo en cuenta fue informar que las palabras que comienzan con "GO:" y siguen con números eran un token. Para cargar mi corpus se utilizó el corpus reader de NLTK (PlaintextCorpusReader), y para tokenizar RegexpTokenizer.

### Ejercicio 2
Se implementó un modelo de n-gramas con marcadores de comienzo y fin de oración (\<s> y \</s>). Al momento de inicializar la clase, se toma el corpus y a cada oración se le agregan los n-1 marcadores de comienzo de oración \<s>, de esta manera se facilita el proceso de cálculo de conteos para las sub frases de comienzo. Adicionalmente, en la inicialización se van calculando los conteos de cada frase de tamaño n y n-1.
Para evitar el problema del underflow al calcular probabilidades de cada sub frase, se utilizó la tecnica de log probabilidades.
