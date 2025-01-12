#!/usr/bin/env python3

# purpose: finds % missing data from each sample (RIL line), as well as the number of SNPs that remain with a MAF of 0.2-0.8 and 0.25-0.75 with a missing
#          % from 0 to 70. Set -nam to "yes" or "no". When input is part of a NAM population, SNPs are excluded if parent B is missing. If it is not part
#          of a NAM population, SNPs are excluded if parent A or B is missing
# usage: python3 snp-params -vcf vcf-file -nam yes,no

import re
import argparse

# set up command line options
parser = argparse.ArgumentParser()
required = parser.add_argument_group('required arguments')
required.add_argument("-vcf", help="Input VCF File", required=True)
required.add_argument("-nam", choices=["yes","no"], help="If a NAM population, missing parent A genotypes will be inferred as 0/0 and SNPs are excluded if parent B is missing. If not a NAM population, SNPs will be excluded if parent A or parent B is missing.", required=True)
args = parser.parse_args()

vcf = open(args.vcf,'r')

samples = {}
snp_counts = {}

# for each missing % from 0 to 70 (step of 5), add to dict with segregation ratios of 0.2-0.8 and
# 0.25-0.75. set both counts to 0
for i in range(0,75,5):
    snp_counts[str(i)] = {'0.2-0.8':0, '0.25-0.75':0}

for line in vcf:
    # comment line, don't do anything
    if line.startswith("##"):
        pass
    # header line
    elif line.startswith("#CHROM"):
        line = line.strip('\n')
        line = line.split('\t')
        column = 9
        # for each sample/RIL, add to dictionary to keep track of total genotypes and total missing genotypes
        # PARENT
        for i in line[9:11]:
            samples['column'+str(column)] = {'Sample':i, 'Missing':0, 'Total':0, 'Parent':'Yes'}
            column += 1
        # RIL
        for i in line[11:]:
            samples['column'+str(column)] = {'Sample':i, 'Missing':0, 'Total':0, 'Parent':'No'}
            column += 1
    # snp line
    else:
        line = line.strip('\n')
        line = line.split('\t')
        # count number of alternate alleles for snp
        num_alts = len(line[4].split(','))
        # variables to be reset for each snp
        column = 9
        # genotype variables (for maf calculation)
        pA_calls = 0
        pA = re.search("^(.{1}/.{1}):",line[9]).group(1)
        pB = re.search("^(.{1}/.{1}):",line[10]).group(1)
        total_calls = 0
        maf = None
        exclude = False
        # genotype variables (for missing calculation)
        num_samples = 0
        num_missing = 0

        # criteria that automatically excludes snp from being added to count, change bool

        # num alts is not 1 OR both parents missing, exclude
        if (num_alts != 1) or ((pA == './.') and (pB == './.')):
            exclude = True
        # if not a NAM population, exclude if either parent A or parent B is missing
        elif (args.nam == "no") and ((pA == './.') or (pB == './.')):
            exclude = True
        # if a NAM population
        elif (args.nam == "yes"):
            # if parent A is currently missing, assume homozygous ref
            if pA == './.':
                pA = '0/0'
            # if parent B is missing, exclude
            if pB == './.':
                exclude = True
        # otherwise, do nothing (boolean stays at false)
        else:
            pass

        # for each sample
        for i in line[9:]:
            genotype = re.search("^(.{1}/.{1}):",i)

            # PART 1 - work for % missing for each sample
            if genotype:
                # increase total regardless
                samples['column'+str(column)]['Total'] += 1
                # check if missing
                if genotype.group(1) == './.':
                    samples['column'+str(column)]['Missing'] += 1
            # shouldn't occur, but ignore if it does
            else:
                pass

            # PART 2 - work to find MAF and % missing for snp call
            if exclude == False:
                # non parent samples
                if column >= 11:
                    if genotype:
                        num_samples += 1
                        # non-missing call
                        if genotype.group(1) != './.':
                            total_calls += 1
                            # if genotype is parent A, increase pA calls
                            if genotype.group(1) == pA:
                                pA_calls += 1
                        # missing call
                        else:
                            num_missing += 1
                    # absent genotype call shouldn't happen
                    else:
                        pass
                # ignore parent sample
                else:
                    pass
            # ignore automatically excluded SNP
            else:
                pass
            column += 1

        # once all samples are read, calculate MAF and determine whether to include SNP
        if exclude == False:
            # calculate MAF
            if total_calls == 0:
                maf = 0
            else:
                maf = pA_calls/total_calls
            # calculate number of snps
            for i in snp_counts:
                # if less than missing cutoff
                if (num_missing/num_samples)*100 <= int(i):
                    if maf >= 0.2 and maf <= 0.8:
                        snp_counts[i]['0.2-0.8'] += 1
                    if maf >= 0.25 and maf <= 0.75:
                        snp_counts[i]['0.25-0.75'] += 1
        # exclude snp
        else:
            pass

# print missing results
print("# Sample, % Missing")
for i in samples:
    # if sample is not a parent, print results
    if samples[i]['Parent'] == 'No':
        print(samples[i]['Sample'], str(round((samples[i]['Missing']/samples[i]['Total'])*100,2))+"%", sep='\t')
    # ignore parents
    else:
        pass

print('\n')
print("# % Missing, Num SNPs 0.2-0.8 MAF, Num SNPs 0.25-0.75 MAF")
for i in snp_counts:
    print(i+"%", snp_counts[i]['0.2-0.8'], snp_counts[i]['0.25-0.75'], sep='\t')

vcf.close()
