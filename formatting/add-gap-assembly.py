#!/usr/bin/env python

# adds a 100bp gap to contigs in assembly file for juicebox (ensures correct contig alignment to HiC map in juicebox)
# usage: python3 add-gap-assembly.py assembly-file

import sys

assembly = open(sys.argv[1],'r')

for line in assembly:
    line = line.strip('\n')
    line = line.split(' ')
    if line[0].startswith('>') and line[1] != '1':
        size = int(line[2]) + 100
        print(line[0], line[1], size, sep=' ')
    else:
        print(*line, sep=' ')

assembly.close()
