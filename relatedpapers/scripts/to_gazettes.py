relations_file = '/home/jcrodriguez/Git/PLN-2017/examples/relations_inflated.tsv'
out_file = '/home/jcrodriguez/Git/PLN-2017/examples/gazettes.csv'

import csv
rel_fst = set()
rel_snd = set()
with open(relations_file, 'r') as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')
    colnames = csvreader.fieldnames
    for row in csvreader:
        rel_fst.add(row[colnames[0]])
        rel_snd.add(row[colnames[1]])


all_data = ['literal,class']
all_data = all_data + [ rel + ',' + colnames[0] for rel in rel_fst ]
all_data = all_data + [ rel + ',' + colnames[1] for rel in rel_snd ]

with open(out_file, 'w') as f:
    for item in all_data:
        f.write("{}\n".format(item))



