rm(list=ls());

## First get subtypes gazettes

my_gazette <- c('literal,class',
                'basal-like,SUBTYPE',
                'basal like,SUBTYPE',
                'luminal-a,SUBTYPE',
                'luminal a,SUBTYPE',
                'luminal-b,SUBTYPE',
                'luminal b,SUBTYPE',
                'her2,SUBTYPE');


######### Get gene ontology gene sets gazettes

require(GO.db);

gs_ids <- c(names(as.list(GOBPPARENTS)),
            names(as.list(GOCCPARENTS)),
            names(as.list(GOMFPARENTS)));

gs_ids <- gs_ids[1:100]; # for testing

gs_names <- Term(gs_ids);
gs_synonyms <- Synonym(gs_ids);
gs_synonyms <- Reduce(c, gs_synonyms); # union of all synonyms

gazette_class <- 'GENE_SET';

## first, ids
my_gazette <- c(my_gazette, paste(gs_ids, gazette_class, sep=','));

## now, names
# filter names shorter than 3 words, as they are too general
length(gs_names);
gs_names <- gs_names[unlist(lapply(strsplit(gs_names, ' |-'), length)) > 2];
length(gs_names);

gs_names <- gsub(',', ' ', gsub(', ', ' ', gs_names)); # gazettes are separated by comma

my_gazette <- c(my_gazette, paste(gs_names, gazette_class, sep=','));

## finally, synonyms
length(gs_synonyms);
gs_synonyms_ids <- gs_synonyms[grepl('GO:', gs_synonyms)];
my_gazette <- c(my_gazette, paste(gs_synonyms_ids, gazette_class, sep=','));

gs_synonyms <- gs_synonyms[!grepl('GO:', gs_synonyms)];

# filter names shorter than 3 words, as they are too general
length(gs_synonyms);
gs_synonyms <- gs_synonyms[unlist(lapply(strsplit(gs_synonyms, ' |-'), length)) > 2];
length(gs_synonyms);

gs_synonyms <- gsub(',', ' ', gsub(', ', ' ', gs_synonyms)); # gazettes are separated by comma

my_gazette <- c(my_gazette, paste(gs_synonyms, gazette_class, sep=','));

my_gazette <- unique(my_gazette);
write(my_gazette, file='~/mytmp/my_gazette.csv');
