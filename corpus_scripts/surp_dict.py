import sys
import math
from collections import Counter
from collections import defaultdict

#NOTE	-- 'CV' --	corresponds to the element of interest, and 
#		-- 'C' --	corresponds to the element of interest -1

#sets up the script arguments#
phoneme_of_interest = sys.argv[1]


#create empty dict that we'll fill after#
MyDict = defaultdict(int)


#figures out if it's a linear or mophemic analysis, reads the correct files and sets up the output file and folder#
if '_' in phoneme_of_interest:
	C_in = open(phoneme_of_interest[:-2] + '_counts_final.txt','r').read().split('\n')
	folder_path = 'log2_surp_dicts/surp-dict-'
	print 'conducting morphemic analysis..'
else:
	C_in = open(phoneme_of_interest[:-1] + '_counts_final.txt','r').read().split('\n')
	print 'conducting linear analysis..'
	folder_path = 'log2_surp_dicts/surp-dict-'
		
#open and read the CV counts, then if the first element of CV is in C, print the frequency of both C and CV#
with open(phoneme_of_interest + '_counts_final.txt','r') as CV_in:
	for CV in CV_in:
		for C in C_in:
			length = len(phoneme_of_interest)
			if '_' in phoneme_of_interest:
				if len(phoneme_of_interest) >=4:
					cv = ''.join(CV[0:int(length)-3])
					
					if cv in C and ',' not in CV[0]:
						CV = CV.split(',')
						C = C.split(',')
						print CV
						print "CV"
						print float(CV[1])
						print C
						print "C"
						print float(C[1])
						print "cond_prob"			
						cond_prob = float(CV[1])/float(C[1])
						surp = math.log(float(cond_prob),2)
						print cond_prob
						MyDict[CV[0]] = surp
						print "---"					
					
				else:
					cv = ''.join(CV[0:int(length)-2])
				
					if cv in C and ',' not in CV[0]:
						CV = CV.split(',')
						C = C.split(',')
						print CV
						print "CV"
						print float(CV[1])
						print C
						print "C"
						print float(C[1])
						print "cond_prob"			
						cond_prob = float(CV[1])/float(C[1])
						surp = math.log(float(cond_prob),2)
						print cond_prob
						MyDict[CV[0]] = surp
						print "---"
					
			else:
				cv = ''.join(CV[0:int(length)-1])
				#cv = ''.join(CV[0])
				#cv = cv[:-1]
				#cv = ''.join(CV[0:2])
				
				if cv in C and ',' not in CV[0]:

#now, get the conditional probability of the second vowel, from that compute surprisal by making it log, then put it in the dict
#(the key is the CV, and the number is the surprisal #

#first, split the dict into its first and second elements i.e., 'ka' '34'

					CV = CV.split(',')
					C = C.split(',')

#next, get the conditional probability from the second elements of the list (the number) and work out the surprisal
					print CV
					print "CV"
					print float(CV[1])
					print C
					print "C"
					print float(C[1])
					print "cond_prob"			
					cond_prob = float(CV[1])/float(C[1])
					surp = math.log(float(cond_prob),2)
					print cond_prob
					MyDict[CV[0]] = surp
		
					print "---"


#now we just save the dict to file#
file = open(folder_path + phoneme_of_interest + '.txt', 'w')
for key in MyDict:
	file.write(key + ',' + str(MyDict[key]) + '\n')
file.close()

file = open(folder_path + phoneme_of_interest + '.txt', 'w')
for key in MyDict:
	file.write(key + ',' + str(MyDict[key]) + '\n')
file.close()

#finally print out all words with a surprisal greater than 5:
highest_surp = dict((k, v) for k, v in MyDict.items() if v <= -5)
print "items with suprisal greater than 5:"
print highest_surp

#and less than 1:
highest_surp = dict((k, v) for k, v in MyDict.items() if v >= -2)
print "items with suprisal less than 2:"
print highest_surp