#!/usr/bin/python

# This script performs the same function as the EMR/Hadoop built-in "aggregate" reducer.
import sys
import re
from collections import defaultdict


def main(argv):
    counts = defaultdict(int)
    for line in sys.stdin:
        if line.startswith('LongValueSum'):
            (dummy, word, count) = re.split('[ \t:]', line)
            counts[word] += int(count)
    for word in sorted(counts.keys()):
        print "%s\t%d" % (word, counts[word])

if __name__ == "__main__": 
    main(sys.argv) 