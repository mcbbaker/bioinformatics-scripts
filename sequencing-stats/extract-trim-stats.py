#!/usr/bin/env python

# purpose: to extract the trimming statistics for each line from the trimmomatic log
# usage: python3 extract-trim-stats.py trim-log

import sys
import re

log = open(sys.argv[1],'r')
started = False
stats = {}
cur_line = ""


for line in log:
    line = line.strip('\n')
    if line.startswith("Processing"):
        # if haven't started yet, change boolean
        if started == False:
            started = True
        else:
            pass
        # add to stats dictionary
        name = re.search("sample base name (.+)...", line)
        if name:
            stats[name.group(1)] = {"Input": "", "Both": "", "Forward": "", "Reverse":"", "Dropped":""}
            cur_line = name.group(1)
        else:
            sys.exit("Could not identify sample base name for line " + line + ". Exiting...")
    else:
        # not a sample line and not started yet, do nothing with this line
        if started == False:
            pass
        # already started, process line
        else:
            # only process this line with stats
            if line.startswith("Input"):
                
                # INPUT READS
                input_reads = re.search("Input Read Pairs: (.+) Both", line)
                if input_reads:
                    stats[cur_line]["Input"] = input_reads.group(1)    
                else:
                    sys.exit("Could not identify input reads for " + line)
                
                # BOTH SURVIVING
                both = re.search("Both Surviving:.+\\((.+?)%\\) Forward", line)  
                if both:
                    stats[cur_line]["Both"] = both.group(1)
                else:
                    sys.exit("Could not identify both surviving for " + line)
                
                # FORWARD 
                forward = re.search("Forward Only Surviving:.+\\((.+?)%\\) Reverse", line)
                if forward:
                    stats[cur_line]["Forward"] = forward.group(1)
                else:
                    sys.exit("Could not identify forward surviving for " + line)

                # REVERSE
                reverse = re.search("Reverse Only Surviving:.+\\((.+?)%\\) Dropped", line)
                if reverse:
                    stats[cur_line]["Reverse"] = reverse.group(1)
                else:
                    sys.exit("Could not identify reverse surviving for " + line)

                # DROPPED
                dropped = re.search("Dropped:.+\\((.+?)%\\)", line)
                if dropped:
                    stats[cur_line]["Dropped"] = dropped.group(1)
                else:
                    sys.exit("Could not identify dropped for " + line)
            else:
                pass
    
print("Line,Input Reads,Both Surviving (%),Forward Only Surviving (%),Reverse Only Surviving (%),Dropped (%)")
for key,value in stats.items():
    print(key, stats[key]["Input"], stats[key]["Both"], stats[key]["Forward"], stats[key]["Reverse"], stats[key]["Dropped"], sep=",")

log.close()
