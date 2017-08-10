Pasos a seguir:

Para crear gazettes.csv y papers.csv :
Rscript ../relatedpapers/scripts/inflateGO.R --in_file relations_go_ids.tsv --out_file relations_inflated_go.tsv --min_len 2;
Rscript ../relatedpapers/scripts/inflateRel.R --in_file relations_inflated_go.tsv --out_file relations_inflated.tsv --inflation_file subtypes_synonims.tsv;
python get_papers.py -i relations_inflated.tsv -o papers.csv;
python to_gazettes.py -i relations_inflated.tsv -o gazettes.csv;


Para completar la base de datos de IEPY :
iepy --create iepyRelated;
python bin/gazettes_loader.py /home/jcrodriguez/Git/PLN-2017/examples/gazettes.csv;
python bin/manage.py loaddata /home/jcrodriguez/Git/PLN-2017/relatedpapers/fixtures/relations.json;
python bin/csv_to_iepy.py /home/jcrodriguez/Git/PLN-2017/examples/papers.csv;
python bin/preprocess.py --multiple-cores=20;

Iteracion 1
Sin IEPY, se buscaron oraciones que contuvieran las dos entidades.

Iteracion 2
Con IEPY, dados los GO ID de interes se tradujeron a sus nombres y sinonimos (se descartaron aquellos de una sola palabra, ya que generaban demasiados papers; como el caso de 'cell'). Se descargaron los paper. Preprocessing completo. Solo encontro 3 relaciones candidatas, de las cuales solo dos eran ciertas.

