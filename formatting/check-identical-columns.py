#!/usr/bin/env python

# usage: python3 check-identical-columns.py <file> <num_columns>
# purpose: handy script to take in a tab delimited file and check whether all columns are identical for every line.
#          output will be a statement showing success if all columns are identical for every line, or print all lines 
#          that don't contain identical columns.
import sys

file = open(sys.argv[1], 'r')
num_cols = int(sys.argv[2])

# set boolean at start to determine if difference has been found over all lines
identical = True

for line in file:
    line = line.strip('\n')
    line = line.split('\t')
    # set first column as a comparator
    comp = line[0]

    # loop through each column
    for i in range(0, num_cols):
        # if difference is identified
        if (line[i] != comp):
            # make sure identical is set to false
            if identical == True:
                identical = False
                print("Lines with differing columns found:")
            print(*line)
            break
        # do nothing if columns are identical
        else:
            pass

if identical == True:
    print("Success! No differing columns found.")
        
file.close()
