#!/usr/bin/env python

# usage: python3 utgs-from-gff.py gff-file agp-file
import sys
import re

f1 = sys.argv[1]
f2 = sys.argv[2]

gff = open(f1,'r')
agp = open(f2,'r')

genes = {}

for line in gff:
    line = line.strip('\n')
    line = line.split('\t')
    # get ID and place ID into dictionary with Chr, Start and End as values
    name = re.search('ID=(.*);Name=',line[8])
    genes[name.group(1)] = {'Chr':line[0], 'Start':line[3], 'End':line[4],'Description':line[8]}

# print header
print('#','UTG-CHR','UTG-START','UTG-END','UTG-NAME','GENE-CHR','GENE-START','GENE-END','GENE-DESCRIPTION',sep =' ')

for line in agp:
    # ignore comment lines
    if line.startswith('#'):
        continue
    else:
        line = line.split('\t')
        # ignore gap lines
        if line[6] == 'scaffold':
            continue
        else:
            # if the Chr is the same and the gene coords are in the bounds of the unitig, print info
            for i in genes:
                if (line[0] == genes[i]['Chr']) and (int(line[1]) <= int(genes[i]['Start'])) and (int(line[2]) >= int(genes[i]['End'])):
                    print(line[0],line[1],line[2],line[5],genes[i]['Chr'],genes[i]['Start'],genes[i]['End'],genes[i]['Description'],sep='\t')

gff.close()
agp.close()
