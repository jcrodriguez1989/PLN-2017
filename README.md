# PLN 2017: Procesamiento de Lenguaje Natural 2017
## Práctico 4 - Rodriguez, Juan Cruz
## pmcERR: PubMed Central entity relation recognition

### [Presentación](https://docs.google.com/presentation/d/1L6vSP8wdLbdJzjncK8u-wyiOB4bVjvXIXhGsQTChumQ/edit?usp=sharing)

### [Librería pmcERR](https://github.com/jcrodriguez1989/pmcERR/)

### Introducción
La validación de resultados biológicos obtenidos mediante técnicas estadísticas o hipótesis, lleva a la necesidad de exploración y lectura de grandes cantidades de artículos científicos.
Dentro de la comunidad científica biológica, el principal recurso de publicaciones es [PubMed Central (PMC)](https://www.ncbi.nlm.nih.gov/pmc/), el cuál actualmente cuenta con más de 4.5 millones de artículos. Esto provee al investigador de una inmensa fuente de información, la cual si no es abordada de una manera inteligente puede llevarlo a invertir demasiado tiempo, o peor aún, no encontrar validación existente.

Por lo general lo que se desea es contar con publicaciones que respalden la relación entre entidades, por ejemplo, vía biológica - enfermedad, gen - enfermedad, gen - vía biológica - enfermedad, etc.
En el caso particular de técnicas estadísticas que revelan posibles alteraciones, es común obtener cientos de pares de relaciones, lo cuál resulta facilmente en miles de artículos científicos a investigar.

Por ello resulta fundamental una técnica que permita encontrar y filtrar artículos que potencialmente evidencien relación entre entidades biológicas. Más aún, que detecten si realmente se encuentran relacionados, y cualés son las secciones de la publicación que lo respaldan.

Como proyecto final de la materia 'Procesamiento de Lenguaje Natural', se llevó a cabo la inspección de diversas alternativas y posibilidades que pudieran abordar esta tarea.
Finalmente se llegó al desarrollo de la librería en lenguaje R [pmcERR](https://github.com/jcrodriguez1989/pmcERR). Esta librería permite mediante linea de comandos, dadas entidades, descargar artículos científicos de internet y encontrar relaciones. Adicionalmente provee una interfaz gráfica que facilita su usabilidad.

### Desarrollo
#### IEPY
Inicialmente se intentó utlizar el paquete Python [IEPY](https://github.com/machinalis/iepy), este paquete lleva a cabo tareas de 'information extraction', es decir, a partir de grandes cantidades de datos (textos) detecta entidades, para posteriormente encontrar relaciones entre ellas.
Utilizando IEPY lo que se hizo fue alimentarlo con miles de artículos científicos, y proveerle entidades de interés (ahorrándole la tarea de detectarlas automáticamente). Con esta información IEPY se encargó de buscar posibles relaciones, y de aquí filtramos las que fueran de interés. Más información de lo realizado se puede encontrar [aquí.](https://github.com/jcrodriguez1989/PLN-2017/tree/practico4/relatedpapers)

Esta es una alternativa válida para nuestra tarea final. Sin embargo, requiere de descargar grandes cantidades de publicaciones, y entrenar los modelos de IEPY para que pueda detectar facilmente las relaciones de interés. Lo cual genera un overhead significativo para nuestra meta. Por ello se dejo de lado IEPY y se probó con una alternativa.

#### pmcERR
Finalmente se optó por desarrollar una librería en lenguaje R. pmcERR utilizando la API del [National Center for Biotechnology Information (NCBI)](https://www.ncbi.nlm.nih.gov/) descarga los artículos científicos de PMC dadas entidades a explorar.
Utilizando la librería [tokenizers](https://cran.r-project.org/web/packages/tokenizers/index.html) divide el texto en oraciones. Y luego busca la relación de las entidades en las oraciones.
De esta manera, a partir de una lista de tuplas de entidades potencialmente relacionadas, se obtienen oraciones dentro de artículos que dan una evidencia de su relación.

##### Nota
El tokenizer presentaba inconvenientes al tokenizar abreviaciones, por ejemplo, las palabras 'Fig.', 'al.' generaban la incorrecta separación de oraciones. Se detectaron cuáles abreviaciones generaban la mayor cantidad de errores mediante el [script](https://github.com/jcrodriguez1989/PLN-2017/blob/practico4/statistics/words_w_dot.py) y se solucionó dicho inconveniente.
