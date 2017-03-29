QUERY_URL="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"; # api de ncbi
DATABASE="pubmed"; # quiero articulos cientificos
# DATABASE="pmc"; # quiero articulos cientificos
MY_QUERY="\"breast+cancer\"+AND+\"gene+ontology\""; # que tengan cancer de mama y gene ontology
MY_QUERY="\"breast\"+AND+\"gene+ontology\""; # que tengan enfermedades de mama y gene ontology

# Nota: va a bajar Abstracts, a menos que este el articulo completo free, ahi me devuelve todo
# retmax=40000 para que no me filtre Ids, al momento vi que eran 225
COMPLETE_URL=$QUERY_URL"esearch.fcgi?db="$DATABASE"&term="$MY_QUERY"&retmax=40000";
QUERY_RES=$(curl -k --silent $COMPLETE_URL);

QUERY_RES_XML="/tmp/queryRes.xml"
curl -k --silent $COMPLETE_URL > $QUERY_RES_XML;

rm myCorpus.txt;
rdom () { local IFS=\> ; read -d \< E C ;}
while rdom; do
    if [[ $E = Id ]]; then
        DOWNLOAD_URL=$QUERY_URL"efetch.fcgi?db="$DATABASE"&id="$C"&rettype=txt&retmode=text";
curl -L -k $DOWNLOAD_URL >> myCorpus.txt
    fi
done < $QUERY_RES_XML




# ALL_IDS="";
# rdom () { local IFS=\> ; read -d \< E C ;}
# while rdom; do
#     if [[ $E = Id ]]; then
#         ALL_IDS=$ALL_IDS","$C
#     fi
# done < $QUERY_RES_XML
# 
# DOWNLOAD_URL=$QUERY_URL"efetch.fcgi?db="$DATABASE"&id="$ALL_IDS"&rettype=txt&retmode=text";
# curl -L -k $DOWNLOAD_URL > myCorpus.txt

