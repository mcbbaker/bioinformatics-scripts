#!/usr/bin/env python

# calculates n50/stats of fastq file
# usage: python3 n50_fastq.py yourfile.fastq

import sys

infile = sys.argv[1]
f = open(infile,'r')

data = f.read()
reads = 0
basecount = 0
bases = []

for line in data.split("\n")[0::4]:
    if line.startswith("@"):
        reads += 1

for line in data.split("\n")[1::4]:
    bases.append(len(line))

for base in bases:
    basecount += base

largetosmall = sorted(bases, reverse = True)
sumbases = 0
for i in largetosmall:
    if (sumbases + i) <= basecount/2:
        sumbases += i
    else:
        n50 = i
        break


print("Infile:", infile)
print("Num reads:", reads)
print("Num bases:", basecount)
print("Min read length:", min(bases), "\t", "Max read length:", max(bases))
print("N50:", n50)
print("Coverage:", basecount/4000000000)

f.close()
