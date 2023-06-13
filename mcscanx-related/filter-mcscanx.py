#!/usr/bin/env python

# usage: python3 filter-mcscanx.py collinearity-file score
# purpose: removes alignments from a collinearity file that have a score less than the score provided as input to the script

import sys
import re

# open collinearity file
col = open(sys.argv[1],'r')
score = float(sys.argv[2])

align_reached = False
print_cur = False

for line in col:
    line = line.strip('\n')
    align = re.search("## Alignment (\d+): score=(.+) e_value", line)

    if align_reached == False:
        # still not an alignment line, print line
        if align == None:
            print(line)

        # hit first alignment line
        if align:
            align_reached = True
            # greater than score, print alignment line and change printing bool
            if float(align.group(2)) >= score:
                print_cur = True
                print(line)
            # less than score, keep printing bool at false
            else:
                print_cur = False

    else:
        # if a new alignment line
        if align:
            if float(align.group(2)) >= score:
                print_cur = True
                print(line)
            else:
                print_cur = False
        # if intermediate line
        else:
            if print_cur == True:
                print(line)
            else:
                pass




col.close()
