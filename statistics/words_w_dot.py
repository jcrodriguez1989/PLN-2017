from relatedpapers.papersdownloader import PapersDownloader
#from relatedpapers.relationrecognition import RelationRecognition

import tempfile
papers_dir = '/media/jcrodriguez/Data11/Git/PLN-2017/papers/'

import os
if not os.path.exists(papers_dir):
    os.makedirs(papers_dir)


## Downloading

queries = ['("basal-like"OR"Luminal A"OR"Luminal B"OR"Her2")']
ppr_dlder = PapersDownloader(queries, papers_dir)
ppr_dlder.get_paper_ids() # 45734 papers to download.
ppr_dlder.download_papers() # download just the first n papers

## Statistics

dloaded_files = [file.replace('.xml', '') for file in os.listdir(papers_dir) if file.endswith('.xml')]
ppr_dlder = PapersDownloader([], papers_dir)
ppr_dlder.set_paper_ids(dloaded_files)
ppr_dlder.download_papers(200) # download just the first n papers

all_papers_text = [paper.get_full_paper() for paper in ppr_dlder.get_papers()]
all_papers_text = [item for sublist in all_papers_text for item in sublist]

all_papers_words = [paper_sent.split(' ') for paper_sent in all_papers_text]
all_papers_words = [item for sublist in all_papers_words for item in sublist]

all_papers_w_dot = [paper_word for paper_word in all_papers_words if paper_word.endswith('.')]

import collections
counter = collections.Counter(all_papers_w_dot)
counter.most_common()[:100]

## Here we can see that appear words that are wrongly parsed, for example
# Fig.
# al.
# vs.
# min.
# max.
# e.g.
# Dr.
# St.
# i.e.
# Inc.
# Figs.
# Ref.
# sp.
