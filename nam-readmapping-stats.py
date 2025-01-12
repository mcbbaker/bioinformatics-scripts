#!/usr/bin/env python3

# usage: python3 namstats.py logfile (output is stdout)
# purpose: outputs statistics from read trimming and mapping
# statistics are: # raw, # trimmed, % trimmed (of raw), # unmapped, % unmapped (of raw), # unique, % unique (of raw)

import sys
import re

logfile = open(sys.argv[1],'r')

data = {}
name_reached = False

for line in logfile:
    line = line.strip('\n')
    # looking for the next sample's processing line
    if name_reached == False:
        new_sample = re.search("^Processing.*for sample base name (NAM-\d+-\d+)...",line)
        # if reached the next sample, get sample name and add to dictionary as a key
        if new_sample:
            sample_name = new_sample.group(1)
            data[sample_name] = {'Raw':'', 'Trimmed':'', 'PTrimmed':'', 'Unmapped':'', 'PUnmapped':'', 'Unique':'','PUnique':''}
            # currently have a sample to work on, look for stats
            name_reached = True

    # already reached a sample's processing line
    else:
        # search for the stats
        raw = re.search("^Input Read Pairs: (\d+) Both",line)
        trimmed = re.search("Both Surviving: (\d+) \(.*\) Forward",line)
        unmapped = re.search("^\s*(\d+) \(.*\) aligned concordantly 0 times",line)
        unique = re.search("^Found (\d+) number of uniquely mapped reads", line)
        # if found the stats, update dictionary
        if raw:
            data[sample_name]['Raw'] = int(raw.group(1))
        if trimmed:
            data[sample_name]['Trimmed'] = int(trimmed.group(1))
        if unmapped:
            data[sample_name]['Unmapped'] = int(unmapped.group(1))
        if unique:
            data[sample_name]['Unique'] = int(unique.group(1))
            # this will be the last stat reached (given the log file format) - set name_reached back to false to look for new sample
            name_reached = False


# get percentages of raw
for sample in data:
    data[sample]['PTrimmed'] = round((data[sample]['Trimmed']/data[sample]['Raw'])*100,2)
    data[sample]['PUnmapped'] = round((data[sample]['Unmapped']/data[sample]['Raw'])*100,2)
    data[sample]['PUnique'] = round((data[sample]['Unique']/data[sample]['Raw'])*100,2)

# print NAM population name (from file name for accuracy)
print(re.search('(NAM\d*).LOG',logfile.name.upper()).group(1))
# print headings
print('Sample Name','Raw','Trimmed','% Trimmed','Unmapped','% Unmapped','Unique','% Unique',sep=',')

# sort the dictionary keys (sample names) based on the sample number
for i in sorted(data.keys(), key=lambda x: int(re.search("NAM-\d*-(\d*)",x).group(1))):
    # print sample name, and values (raw, trimmed, unmapped, unique)
    print(i,','.join(str(item) for item in data[i].values()),sep=',')

logfile.close()
