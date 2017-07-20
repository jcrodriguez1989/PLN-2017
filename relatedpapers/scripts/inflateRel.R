#!/usr/bin/env Rscript
args <- commandArgs(trailingOnly=!FALSE);

stopifnot(length(args) %% 2 == 0); # must be of the type --flag arg

args <- matrix(args, ncol=2, byrow=!FALSE);

if (!'--in_file' %in% args[,1]) {
    stop('--in_file file.tsv must be provided');
}

if (!'--inflation_file' %in% args[,1]) {
    stop('--inflation_file file.tsv must be provided');
}

if (!'--out_file' %in% args[,1]) {
    stop('--out_file file.tsv must be provided');
}


in_file <- args[args[,1] == '--in_file', 2];
print(paste('Using', in_file));

inflation_file <- args[args[,1] == '--inflation_file', 2];

out_file <- args[args[,1] == '--out_file', 2];

# in_file <- '/media/jcrodriguez/Data11/Git/PLN-2017/examples/relations_inflated_go.tsv';
# out_file <- '/media/jcrodriguez/Data11/Git/PLN-2017/examples/relations_inflated.tsv';
# inflation_file <- '/media/jcrodriguez/Data11/Git/PLN-2017/examples/subtypes_synonims.tsv';
in_data <- read.table(in_file, sep='\t', header=!F, quote="");
inflation_data <- read.table(inflation_file, sep='\t', header=!F, quote="");

if (ncol(in_data) != 2 | !'gene_set' %in% colnames(in_data)) {
    stop('Input data must have exactly two columns, and one named gene_set');
}

if (ncol(inflation_data) != 2 | !'to' %in% colnames(inflation_data)) {
    stop('Input data must have exactly two columns, and one named gene_set');
}

to <- as.character(inflation_data[,'to']);
relation_name <- colnames(inflation_data)[!grepl('to', colnames(inflation_data))];
relations <- as.character(inflation_data[,relation_name]);

if (!relation_name %in% colnames(in_data)) {
    stop('Input data and inflation data must have one column name in common');
}

out_data <- do.call(rbind, lapply(1:nrow(in_data), function(i) {
    act_row <- in_data[i,];
    
    cbind(
        as.character(act_row[,colnames(act_row) != relation_name]), 
        c(as.character(act_row[[relation_name]]),
            to[relations == as.character(act_row[[relation_name]])]
        )
    );
}));

colnames(out_data) <- c(colnames(in_data)[colnames(in_data) != relation_name], relation_name);
write.table(out_data, file=out_file, sep="\t", row.names=F, quote=F, col.names=!F);
