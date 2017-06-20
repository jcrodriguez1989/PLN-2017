#"""Find related papers according to a query.
#Usage:
  #relatedpapers.py -q <queries> -e <entities>
  #relatedpapers.py -h | --help
#Options:
  #-q <queries>      ??
  #-e <entities>     ??
  #-h --help         Show this screen.
#"""
#from docopt import docopt

#if __name__ == '__main__':
    #opts = docopt(__doc__)

    ## load the model
    #queries = opts['-q']
    #entities = opts['-e']

############## todo:
# Mejorar el parser (separador de oraciones: 'Fig.' , 'sp.', etc)

from collections import defaultdict

from relatedpapers.papersdownloader import PapersDownloader
from relatedpapers.relationrecognition import RelationRecognition

import tempfile
papers_dir = tempfile.gettempdir() + '/relatedpapers/'

import os
if not os.path.exists(papers_dir):
    os.makedirs(papers_dir)

import csv
gene_sets = defaultdict(str)
with open('/media/jcrodriguez/Data11/Git/PLN-2017/relatedpapers/scripts/Ba.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
    for row in csvreader :
        gene_sets[row[0]] = row[1]

gene_sets = dict(gene_sets)
subtype = '("basal-like")'

related_papers = defaultdict(str)
for act_id in gene_sets.keys():
    print(act_id)
    gene_set = gene_sets[act_id]
    queries = [gene_set, subtype]
    ppr_dlder = PapersDownloader(queries, papers_dir)
    ppr_dlder.get_paper_ids()
    ppr_dlder.download_papers(100) # download just the first n papers
    entities = [gene_set.replace('("', '').replace('")', '').split('"OR"')]
    entities += [['basal like', 'basal-like']]
    papers = ppr_dlder.get_papers()
    rr = RelationRecognition(papers, entities)
    if len(rr.related_papers) > 0:
        related_papers[act_id] = rr.related_papers
        print(gene_set)
        print(rr.related_papers)

related_papers = dict(related_papers)
related_papers




gene_sets = defaultdict(str)
with open('/media/jcrodriguez/Data11/Git/PLN-2017/relatedpapers/scripts/A.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
    for row in csvreader :
        gene_sets[row[0]] = row[1]

gene_sets = dict(gene_sets)
subtype = '("Luminal A"OR"LumA"OR"Luminal-A")'

related_papers = defaultdict(str)
for act_id in gene_sets.keys():
    print(act_id)
    gene_set = gene_sets[act_id]
    queries = [gene_set, subtype]
    ppr_dlder = PapersDownloader(queries, papers_dir)
    ppr_dlder.get_paper_ids()
    ppr_dlder.download_papers(100) # download just the first 30 papers
    entities = [gene_set.replace('("', '').replace('")', '').split('"OR"')]
    entities += [['luminal a', 'luminal-a', 'luma']]
    papers = ppr_dlder.get_papers()
    rr = RelationRecognition(papers, entities)
    if len(rr.related_papers) > 0:
        related_papers[act_id] = rr.related_papers
        print(gene_set)
        print(rr.related_papers)

related_papers = dict(related_papers)
related_papers














#gene_set = "(\"GO:0001837\"OR\"0001837\"OR\"1837\"OR\"epithelial to mesenchymal transition\"OR\"EMT\"OR\"epithelial-mesenchymal transition\")"
#subtype = '("basal-like")'
#queries = [gene_set, subtype]
#ppr_dlder = PapersDownloader(queries, papers_dir)
#ppr_dlder.get_paper_ids()
#ppr_dlder.download_papers(30)

##ppr_dlder = PapersDownloader(["(\"Epithelial Mesenchymal Transition\")", "(basal-like)"], papers_dir)
##ppr_dlder.get_paper_ids()
##ppr_dlder.download_papers(30)

#gene_set = "(\"GO:0001837\"OR\"0001837\"OR\"1837\"OR\"epithelial to mesenchymal transition\"OR\"EMT\"OR\"epithelial-mesenchymal transition\")"
#subtype = '("basal-like")'
#queries = [gene_set, subtype]
#ppr_dlder = PapersDownloader(queries, papers_dir)
#ppr_dlder.get_paper_ids()
#ppr_dlder.download_papers(30)

#entities = [gene_set.replace('("', '').replace('")', '').split('"OR"')]
#entities += [['basal', 'basal-like']]
#papers = ppr_dlder.get_papers()
#rr = RelationRecognition(papers, entities)

##entities = [['epithelial to mesenchymal transition', 'GO:0001837', '0001837', '1837', 'epithelial-mesenchymal transition', 'EMT', 'mesenchymal cell differentiation from epithelial cell']]
##entities += [['basal', 'basal-like']]
##rr = RelationRecognition(papers, entities)

#gene_set = '(\"GO:0071073\"OR\"0071073\"OR\"71073\"OR\"positive regulation of phospholipid biosynthetic process\"OR\"activation of phospholipid biosynthetic process\"OR\"positive regulation of phospholipid anabolism\"OR\"positive regulation of phospholipid biosynthesis\"OR\"positive regulation of phospholipid formation\"OR\"positive regulation of phospholipid synthesis\"OR\"stimulation of phospholipid biosynthetic process\"OR\"up regulation of phospholipid biosynthetic process\"OR\"up-regulation of phospholipid biosynthetic process\"OR\"upregulation of phospholipid biosynthetic process\")'
#subtype = '("basal-like")'
#queries = [gene_set, subtype]
#ppr_dlder = PapersDownloader([gene_set, subtype], papers_dir)
#ppr_dlder.get_paper_ids()
#ppr_dlder.download_papers(30)

#gene_set.replace('("', '').replace('")', '').split('"OR"')
#entities = [gene_set.replace('("', '').replace('")', '').split('"OR"')]
#entities += [['basal', 'basal-like']]
#papers = ppr_dlder.get_papers()
#rr = RelationRecognition(papers, entities)
