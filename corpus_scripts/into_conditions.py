import re
import math
from collections import Counter
import sys



lin_arg = sys.argv[1]
morph_arg = sys.argv[2]

if len(lin_arg) == 3:
	name = "c2"

if len(lin_arg) == 4:
	name = "v2"

if len(lin_arg) == 5:
	name = "c3"

if len(lin_arg) == 6:
	name = "v3"




HiMo_HiLin = open('HiMo_HiLin/' + name + '_HiMo_HiLin-stimuli.txt', 'w')
HiMo_LoLin = open('HiMo_LoLin/' + name + '_HiMo_LoLin-stimuli.txt', 'w')
LoMo_HiLin = open('LoMo_HiLin/' + name + '_LoMo_HiLin-stimuli.txt', 'w')
LoMo_LoLin = open('LoMo_LoLin/' + name + '_LoMo_LoLin-stimuli.txt', 'w')

morph_file_high = open(morph_arg + '_highSurp-stimuli-lowThresh.txt').read().split('\n')
lin_file_high = open(lin_arg + '_highSurp-stimuli-lowThresh.txt').read().split('\n')
morph_file_low = open(morph_arg + '_lowSurp-stimuli-lowThresh.txt').read().split('\n')
lin_file_low = open(lin_arg + '_lowSurp-stimuli-lowThresh.txt').read().split('\n')


#HiMo_HiLin
for morph in morph_file_high:
	morph = morph.split(',')
	if '' not in morph:
		morph_key = morph[2]
		morph_num = morph[1]		
		if 'A' not in morph_key and 'o' not in morph_key and '~' not in morph_key and 'K' not in morph_key:
			for lin in lin_file_high:
				lin = lin.split(',')
				if '' not in lin:
					lin_key = lin[2]
					lin_num = lin[1]
					ans = float(morph_num) - float(lin_num)
					if abs(ans) < float(1.5):										
						if morph_key in lin_key:
							HiMo_HiLin.write(morph[0] + ',' + morph[1] + ',' +  lin[0] + ',' + lin[1] + ',' + lin[2] + ',' + lin[3] + '\n')
	
#HiMo_LoLin
for morph in morph_file_high:
	morph = morph.split(',')
	if '' not in morph:
		morph_key = morph[2]
		morph_num = morph[1]		
		if 'A' not in morph_key and 'o' not in morph_key and '~' not in morph_key and 'K' not in morph_key:
			for lin in lin_file_low:
				lin = lin.split(',')
				if '' not in lin:
					lin_key = lin[2]
					lin_num = lin[1]
					ans = float(lin_num) - float(morph_num)
					if ans > 2.5:
						if morph_key in lin_key:
							HiMo_LoLin.write(morph[0] + ',' + morph[1] + ',' +  lin[0] + ',' + lin[1] + ',' + lin[2] + ',' + lin[3] + '\n')

#LoMo_HiLin
for morph in morph_file_low:
	morph = morph.split(',')
	if '' not in morph:
		morph_key = morph[2]
		morph_num = morph[1]		
		if 'A' not in morph_key and 'o' not in morph_key and '~' not in morph_key and 'K' not in morph_key:
			for lin in lin_file_high:
				lin = lin.split(',')
				if '' not in lin:
					lin_key = lin[2]
					lin_num = lin[1]
					ans = float(morph_num) - float(lin_num)
					if ans > float(2.5):									
						if morph_key in lin_key:
							LoMo_HiLin.write(morph[0] + ',' + morph[1] + ',' +  lin[0] + ',' + lin[1] + ',' + lin[2] + ',' + lin[3] + '\n')

#LoMo_LoLin
for morph in morph_file_low:
	morph = morph.split(',')
	if '' not in morph:
		morph_key = morph[2]
		morph_num = morph[1]			
		if 'A' not in morph_key and 'o' not in morph_key and '~' not in morph_key and 'K' not in morph_key:
			for lin in lin_file_low:
				lin = lin.split(',')
				if '' not in lin:
					lin_key = lin[2]
					lin_num = lin[1]
					ans = float(morph_num) - float(lin_num)
					if abs(ans) < float(1.5):
						if morph_key in lin_key:
							LoMo_LoLin.write(morph[0] + ',' + morph[1] + ',' +  lin[0] + ',' + lin[1] + ',' + lin[2] + ',' + lin[3] + '\n')