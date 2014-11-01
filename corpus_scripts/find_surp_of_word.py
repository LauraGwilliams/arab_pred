import re
import math
from collections import Counter
import sys

theWord = sys.argv[1]

if len(theWord) == 2:
	theStructure = "CV"

if len(theWord) == 3:
	theStructure = "CVC"

if len(theWord) == 4:
	theStructure = "CVCV"

if len(theWord) == 5:
	theStructure = "CVCVC"

if len(theWord) == 6:
	theStructure = "CVCVCV"




theCorpus = open('surp-dict-' + theStructure + '.txt').read().split('\n')

BigCorpus = open('CVCVC_counts_final.txt').read().split('\n')

for item in theCorpus:
	if theWord in item[0:int(len(theWord))]:
		print "item being searched for.."
		print item
		print #
		
		for fullWord in BigCorpus:
			if theWord in fullWord[0:int(len(theWord))]:
				print "Possible stimuli words:"
				print fullWord
				print #
			
		print "item being searched for.."
		print item
		print #