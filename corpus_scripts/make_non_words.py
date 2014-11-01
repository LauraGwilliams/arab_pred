import re
import math
from collections import Counter
import sys
from collections import defaultdict


theStructure = sys.argv[1]

MyDict = defaultdict(int)

CV_text = open('CV_counts_final.txt').read().split('\n')
CVC_text = open('CVC_counts_final.txt').read().split('\n')
CVCV_text = open('CVCV_counts_final.txt').read().split('\n')
CVCVC_text = open('CVCVC_counts_final.txt').read().split('\n')
CVCVCV_text = open('CVCVCV_counts_final.txt').read().split('\n')

possibleWords = open('CVCVCV_words.txt').read().split('\n')

CV_output = open('CV-nonWords.txt', 'w')
CVC_output = open('CVC-nonWords.txt', 'w')
CVCV_output = open('CVCV-nonWords.txt', 'w')
CVCVC_output = open('CVCVC-nonWords.txt', 'w')
CVCVCV_output = open('CVCVCV-nonWords.txt', 'w')


for item in possibleWords:
	item = item.split(',')
	item = item[0]
	for CV in CV_text:
		CV = CV.split(',')
		CV = CV[0]
		if CV in item[0:len(CV)]:
			for CVC in CVC_text:
				if CVC not in item[0:len(CVC)]:
					CV_output.write( item + ',' + CV + '\n' )
				else:
					for CVCV in CVCV_text:
						CVCV = CVCV.split(',')
						CVCV = CVCV[0]
						if CVCV not in item[0:len(CVCV)]:
							CVC_output.write( item + ',' + CVC + '\n' )
						else:
							for CVCVC in CVCVC_text:
								CVCVC = CVCVC.split(',')
								CVCVC = CVCVC[0]
								if CVCVC not in item[0:len(CVCVC)]:
									CVCV_output.write( item + ',' + CVCV + '\n' )
								else:
									for CVCVCV in CVCVCV_text:
									CVCVCV = CVCVCV.split(',')
									CVCVCV = CVCVCV[0]
									if CVCVCV not in item[0:len(CVCVCV)]:
										CVCVC_output.write( item + ',' + CVCVC + '\n' )
									else:
										CVCVCV_output.write( item + ',' + CVCVCV + '\n' )