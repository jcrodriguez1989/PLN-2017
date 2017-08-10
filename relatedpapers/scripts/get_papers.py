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

relations_file = '/home/jcrodriguez/Git/PLN-2017/examples/relations_inflated.tsv'
out_file = '/home/jcrodriguez/Git/PLN-2017/examples/papers.csv'

from collections import defaultdict

from relatedpapers.papersdownloader import PapersDownloader
#from relatedpapers.relationrecognition import RelationRecognition

import tempfile
papers_dir = tempfile.gettempdir() + '/relatedpapers/'
papers_dir = '/home/jcrodriguez/relatedpapers/papers/'

import os
if not os.path.exists(papers_dir):
    os.makedirs(papers_dir)

import csv
ppr_dlders = []
with open(relations_file, 'r') as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')
    colnames = csvreader.fieldnames
    for row in csvreader:
        queries = ['("' + row[colnames[0]] + '")', '("' + row[colnames[1]] + '")']
        print(queries)
        ppr_dlder = PapersDownloader(queries, papers_dir)
        ppr_dlder.get_paper_ids()
        ppr_dlder.download_papers() # download just the first n papers
        ppr_dlders.append(ppr_dlder)


ppr_dlders_dict = defaultdict(str)
ppr_dlders_flat = [ ppr_dlder.get_papers() for ppr_dlder in ppr_dlders ]
ppr_dlders_flat = [ item for sublist in ppr_dlders_flat for item in sublist ]

for paper in ppr_dlders_flat:
    ppr_dlders_dict[paper.id] = '. '.join(paper.get_full_paper())


all_data = ['document_id,document_text']
for act_key in ppr_dlders_dict.keys():
    content = ppr_dlders_dict[act_key]
    content = content.replace('\n', '. ')
    content = '"' + content.replace('"', "'") + '"'
    all_data.append(act_key + ',' + content)


with open(out_file, 'w') as f:
    for item in all_data:
        f.write("{}\n".format(item))



