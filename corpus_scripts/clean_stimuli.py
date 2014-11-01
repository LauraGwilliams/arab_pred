import re
import math
from collections import Counter
import sys
from collections import defaultdict


theStructure = sys.argv[1]

MyDict = defaultdict(int)

file = open('possible_words/' + theStructure + '-possible_stimuli.txt', 'w')

theCorpus = open('surp-dict-' + theStructure + '.txt').read().split('\n')

BigCorpus = open('CVCVC_counts_final.txt').read().split('\n')

for item in theCorpus:
	for fullWord in BigCorpus:
		if item[0:int(len(theStructure))] in fullWord[0:int(len(theStructure))]:
			file.write(item + ',' + fullWord + '\n')