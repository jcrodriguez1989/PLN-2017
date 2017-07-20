#!/usr/bin/env Rscript
args <- commandArgs(trailingOnly=!FALSE);

stopifnot(length(args) %% 2 == 0); # must be of the type --flag arg

args <- matrix(args, ncol=2, byrow=!FALSE);

if (!'--in_file' %in% args[,1]) {
    stop('--in_file file.tsv must be provided');
}

if (!'--out_file' %in% args[,1]) {
    stop('--out_file file.tsv must be provided');
}

in_file <- args[args[,1] == '--in_file', 2];
print(paste('Using', in_file));

out_file <- args[args[,1] == '--out_file', 2];

ent_min_len <- as.numeric(args[args[,1] == '--min_len', 2]);
if (length(ent_min_len) == 0) {
    ent_min_len <- 0;
}

if (!suppressWarnings(require('GO.db'))) {
    source("http://bioconductor.org/biocLite.R");
    biocLite('GO.db');
    if (!suppressWarnings(require('GO.db'))) {
        stop('Could not install GO.db package');
    }
}

# in_file <- '/media/jcrodriguez/Data11/Git/PLN-2017/examples/relations_go_ids.tsv';
# out_file <- '/media/jcrodriguez/Data11/Git/PLN-2017/examples/relations_inflated_go.tsv';
in_data <- read.table(in_file, sep='\t', header=!F, quote="");

if (ncol(in_data) != 2 | !'gene_set' %in% colnames(in_data)) {
    stop('Input data must have exactly two columns, and one named gene_set');
}

gsets <- as.character(in_data[,'gene_set']);

relation_name <- colnames(in_data)[!grepl('gene_set', colnames(in_data))];
relations <- as.character(in_data[,relation_name]);

inflateGO <- function(go_id) {
    term <- Term(go_id);
    synonyms <- unlist(Synonym(go_id));
    
    inflated <- c(go_id, term, synonyms);
    inflated <- inflated[grepl('^GO:', inflated) | unlist(lapply(strsplit(inflated, ' '), function(x) length(x) >= ent_min_len))];

    return(inflated);
}


out_data <- do.call(rbind, lapply(1:length(gsets), function(i) {
    act_gset <- gsets[[i]];
    act_rel <- relations[[i]];
    if (!grepl('^GO:', act_gset)) {
        return(c(act_gset, act_rel));
    }
    
    cbind(inflateGO(act_gset), act_rel);
}));

colnames(out_data) <- c('gene_set', relation_name);
write.table(out_data, file=out_file, sep="\t", row.names=F, quote=F, col.names=!F);

