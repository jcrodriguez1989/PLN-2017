setwd('/media/jcrodriguez/Data11/Git/PLN-2017/relatedpapers/scripts/');

rm(list=ls());
gsetsInfo <- read.csv('gsetsInfo2.csv', sep='\t');
dim(gsetsInfo);
# [1] 492  30

require(GO.db);
getQueries <- function(data, stype, onlyLeaf=!F, minDepth=0) {
#     data <- gsetsInfo; stype <- "Ba"; onlyLeaf=!F; minDepth=0;
    stopifnot(all(c("ID", "Depth", "IsLeaf") %in% colnames(data)));
    stopifnot(stype %in% colnames(data));
    actData <- data;
    if (onlyLeaf) {
        actData <- actData[as.logical(actData$IsLeaf),];
    }
    
    actData <- actData[actData[,stype] == 1,];
    print(paste(stype, nrow(actData)));
    stopifnot(is(actData$Depth, 'integer'));
    actData <- actData[actData$Depth >= minDepth,];
    
    queries <- do.call(c, lapply(as.character(actData$ID), function(gset) {
#         gset2 <- gsub('GO:' , '', gset);
#         gset3 <- gsub('^0*' , '', gset2);
        term <- Term(gset);
        
        query <- paste(gset, term, sep='"OR"');
        
        synonyms <- unlist(Synonym(gset));
        if (!is.null(synonyms)) {
            synonyms <- paste(synonyms, collapse='"OR"');
            query <- paste(query, synonyms, sep='"OR"');
        }
        query <- paste0('("', query, '")');
        return(query);
    }))
    return(data.frame(ID=actData$ID, queries=queries))
}

subtypes <- c('Ba', 'B', 'A', 'H');
invisible(lapply(subtypes, function(actStype) {
    queries <- getQueries(gsetsInfo, actStype, onlyLeaf=F);
#     print(nrow(queries));
    if (nrow(queries) > 0) {
        write.table(queries, file=paste(actStype, '.csv', sep=''), sep="\t", row.names=F, quote=F, col.names=F);
    }
}))


## analicemos basal
queriesBa <- getQueries(gsetsInfo, "Ba");
queriesBa[7,]
# "(\"GO:0071073\"OR\"0071073\"OR\"71073\"OR\"positive regulation of phospholipid biosynthetic process\"OR\"activation of phospholipid biosynthetic process\"OR\"positive regulation of phospholipid anabolism\"OR\"positive regulation of phospholipid biosynthesis\"OR\"positive regulation of phospholipid formation\"OR\"positive regulation of phospholipid synthesis\"OR\"stimulation of phospholipid biosynthetic process\"OR\"up regulation of phospholipid biosynthetic process\"OR\"up-regulation of phospholipid biosynthetic process\"OR\"upregulation of phospholipid biosynthetic process\")"

write.table(queriesBa, file="Ba.csv", sep="\t", row.names=F, quote=F, col.names=F)

