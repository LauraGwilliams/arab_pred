import re
import math
from collections import Counter
import sys



theStructure = sys.argv[1]


file_low_surp = open('create_stimuli/' + theStructure + '_lowSurp-stimuli-lowThresh.txt', 'w')
file_high_surp = open('create_stimuli/' + theStructure + '_highSurp-stimuli-lowThresh.txt', 'w')


theCorpus = open( theStructure + '-possible_stimuli.txt').read().split('\n')

for item in theCorpus:
	item = item.split(',')
	if len(item) >3:
		key = math.fabs(float(item[1]))
		if key > float(2) and float(item[3]) > 10:
			file_high_surp.write(item[0] + ',' + item[1] + ',' + item[2] + ',' + item[3] + '\n')
			print "yes a high one!"

for item in theCorpus:
	item = item.split(',')
	if len(item) >3:
		key = math.fabs(float(item[1]))
		if key < float(6) and float(item[3]) > 10:
			file_low_surp.write(item[0] + ',' + item[1] + ',' + item[2] + ',' + item[3] + '\n')
			print "yes a low one!"