#!/usr/bin/env python

# usage: python3 remove-hets.py vcf (output is stdout)
# purpose: changes het calls in vcf to missing (./.), other sample info (e.g. depth) remains unchanged 

import sys
import re

vcf = open(sys.argv[1],'r')

for line in vcf:
    line = line.strip('\n')

    # header line
    if line.startswith('#'):
        print(line)

    # call line
    else:
        line = line.split('\t')
        # process samples
        cur = 9
        for i in line[9:]:
            genotype = re.search("^(.{1}/.{1}):",i)
            remainder = re.search("^.{1}/.{1}(:.+$)",i)
            # change sample to missing if heterozygous
            if genotype.group(1) == "0/1":
                line[cur] = "./." + remainder.group(1)
            cur += 1
        # once done processing samples, print line
        print(*line,sep='\t')

vcf.close()
