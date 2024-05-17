#!/usr/bin/env python

# purpose: to convert a 1-based position file to proper BED format 0-based, half-open (reduce start by one and keep end the same).
#          the file must have the first 3 columns following BED format (chrom, start, end...) and split by tabs
# usage: python3 pos-file-to-bed.py position-file


import sys

bed = open(sys.argv[1],'r')

for line in bed:
    line = line.strip('\n')
    line = line.split('\t')
    # reduce start by one
    line[1] = int(line[1]) - 1
    # print line
    print(*line, sep='\t')

bed.close()
