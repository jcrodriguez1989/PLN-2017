from relatedpapers.papersdownloader import PapersDownloader
#from relatedpapers.relationrecognition import RelationRecognition

import tempfile
#papers_dir = '/media/jcrodriguez/Data11/Git/PLN-2017/papers/'
papers_dir = '/home/jcrodriguez/relatedpapers/papers/'

import os
if not os.path.exists(papers_dir):
    os.makedirs(papers_dir)


## Downloading

#queries = ['("basal-like"OR"Luminal A"OR"Luminal B"OR"Her2")']
#ppr_dlder = PapersDownloader(queries, papers_dir)
#ppr_dlder.get_paper_ids() # 45734 papers to download.
#ppr_dlder.download_papers() # download just the first n papers

## Statistics

dloaded_files = [file.replace('.xml', '') for file in os.listdir(papers_dir) if file.endswith('.xml')]
ppr_dlder = PapersDownloader([], papers_dir)
ppr_dlder.set_paper_ids(dloaded_files)
ppr_dlder.download_papers() # download just the first n papers

all_data = ['document_id,document_text']
for paper in ppr_dlder.get_papers():
    content = '. '.join(paper.get_full_paper())
    content = content.replace('\n', '. ')
    content = '"' + content.replace('"', "'") + '"'
    all_data.append(paper.id + ',' + content)

#with open('/home/jcrodriguez/mytmp/papers.csv', 'w') as f:
with open('/home/jcrodriguez/relatedpapers/papers.csv', 'w') as f:
    for item in all_data:
        f.write("{}\n".format(item))

