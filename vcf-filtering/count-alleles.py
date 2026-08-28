#!/usr/bin/env python3

# usage: python count-alleles.py file.vcf
# purpose: to count the total number of SV sites and variant alleles across many diploid samples in a VCF file

import sys 
import re

vcf = open(sys.argv[1],'r')
var_count = 0
total = 0
sites = 0

for line in vcf:
    line = line.strip('\n')
    # meta info or header -- pass
    if line.startswith('#'):
        pass
    # call line
    else:
        # split and increment sites
        line = line.split('\t')
        sites += 1
        # loop through samples
        for genotype in line[9:]:
            # find alleles
            allele1 = re.search("(.)/.:", genotype)
            allele2 = re.search("./(.):", genotype)
            # first allele
            if allele1:
                if allele1.group(1) == '1':
                    var_count += 1
                else:
                    pass
                total += 1
            # second allele
            if allele2:
                if allele2.group(1) == '1':
                    var_count += 1
                else:
                    pass
                total += 1

vcf.close()

print("TOTAL SITES:", sites, sep=" ")
print("TOTAL ALLELES ACROSS ALL SAMPLES:", total, sep=" ")
print("TOTAL VARIANT ALLELES ACROSS ALL SAMPLES:", var_count, sep=" ")
