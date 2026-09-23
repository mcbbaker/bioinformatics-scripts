#!/usr/bin/env python

# usage: python3 add-assembly-order-to-map.py <linkage group and assembly group correspondance> <assembly file> <genetic map>
# purpose: to add the order number of the utg in the assembly file to the genetic map.
# linkage group correspondance should have this format: lg0 group1 (one per line and tab-delimited)
# genetic map should have this format: utg position lg centimorgans (tab-delimited)

import sys

groups = open(sys.argv[1],'r')
assembly = open(sys.argv[2],'r')
gMap = open(sys.argv[3],'r')

lgDict = {}
order = {}

# process the file with correspondance between lg and groups in assembly
for line in groups:
    line = line.strip('\n')
    line = line.split('\t')
    lgDict[line[0]] = line[1]
    
# process the assembly file
for line in assembly:
    # only the utg lines
    if line.startswith('>'):
        line = line.strip('\n')
        line = line.split(' ')
        utg = line[0].replace('>','')
        order[utg] = line[1] 

for line in gMap:
    line = line.strip('\n')
    line = line.split('\t')
    print(*line, order[line[0]], sep='\t')





groups.close()
assembly.close()
gMap.close()
