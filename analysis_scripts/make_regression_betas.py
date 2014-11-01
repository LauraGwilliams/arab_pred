####################################################################################
'''

Purpose: This script uses mne and eelbrain modules to extract epochs from raw data
and allocate relevant predictor variables to each epoch. Linear regression using
Ordinary Least Squares is then run on each predictor of interest to produce residual
effects for each trial. Finally, beta values are computed based on the the correlation
between the chosen predictor and residual effects.

Files required: tsv file containing predictor values for each stimuli item; log file
containing trial order information; low-pass filtered fif file; events file; blink
rejection list; inverse solution file.

Author: Laura Gwilliams (laura.gwilliams@nyu.edu).

'''
####################################################################################


# load dependencies

import mne
import os
import eelbrain
import numpy

from eelbrain.lab import load
from eelbrain import *



# set up binary paths

os.environ['MNE_ROOT'] = '/Applications/MNE-2.7.3-3268-MacOSX-i386/'		# make sure this line includes the exact version of MNE that you are using! #
os.environ['SUBJECTS_DIR'] = '/Volumes/LEG_2TB/Documents/Experiments/ArabPred/Data/MRIs'
os.environ['FREESURFER_HOME'] = '/Applications/freesurfer/'


##################################################################################

# load up participant list

participants = ['A0079','Y0003','Y0010','Y0018','Y0021','Y0053','Y0054','Y0056','Y0090','Y0091','Y0094','Y0095','Y0096','Y0097','Y0098','Y0100','Y0101','Y0102','Y0103','Y0105','Y0108','Y0115','Y0052', 'Y0092']




# set paths for files to be read and saved

experiment = 'ArabPred'                                         # use the same name here as in your files #
root = '/Volumes/LEG_2TB/Documents/Experiments/ArabPred/Data' 	# the experiment folder should contain both an 'MEG' folder for your all your participant's data and an 'MRIs' folder where the scaled fsaverage or MRI for each subject will be housed.
meg_root = root + '/MEG'             	                        # if your folders are named correctly, these three should remain untouched #   
subjects_dir = root + '/MRIs'           


#- create dictionary of word and variable properties -#


# load property file
props = load.txt.tsv('/Volumes/LEG_2TB/Documents/Experiments/ArabPred/Data/log_files/word_props.txt', names = True)


# dict of words + values
wordNames = props['word_id']                # this extracts only the "word_id" column of the props matrix and saves it as a list
morphValues = props['morph_surp']           # this extracts only the "morph_surp" column of the props matrix....
linValues = props['lin_surp']
freqValues = props['freq']
famValues = props['fam']
rootValues = props['root_freq']


# check that the correct number of trials are in each predictor (here I expect 280 word trials, so 280 instances of each predictor)
	
morph_dict = {wordNames[i]:morphValues[i] for i in range (len(wordNames))}
if len(wordNames) != 280:
	raise RuntimeError("Wrong number of Words in Property Dictionary")
	
lin_dict = {wordNames[i]:linValues[i] for i in range (len(wordNames))}
if len(wordNames) != 280:
	raise RuntimeError("Wrong number of Words in Property Dictionary")
	
freq_dict = {wordNames[i]:freqValues[i] for i in range (len(wordNames))}
if len(wordNames) != 280:
	raise RuntimeError("Wrong number of Words in Property Dictionary")
	
fam_dict = {wordNames[i]:famValues[i] for i in range (len(wordNames))}
if len(wordNames) != 280:
	raise RuntimeError("Wrong number of Words in Property Dictionary")
	
root_dict = {wordNames[i]:rootValues[i] for i in range (len(wordNames))}
if len(wordNames) != 280:
	raise RuntimeError("Wrong number of Words in Property Dictionary")


##################################################################################
''' extracting log file information '''
##################################################################################

# names for the rows in Presentation log file
names = ("Subject",	"Trial", "Event Type",	"Code",	"Time",	"TTime",	"Uncertainty",	"Duration",	"Uncertainty2",	"ReqTime",	"ReqDur",	"Stim Type",	"Pair Index")


for participant in participants: # loop through participants begins here


# load up the logfile, extract the word order

	log = load.txt.tsv('/Volumes/LEG_2TB/Documents/Experiments/ArabPred/Data/log_files/' + participant + "-ArabPred.log", skiprows=5, ignore_missing=1, names=names)
	x = log['Code']                # in my logfile, the row "Code" contains the name of the stimulus, which corresponds to the name of the stimulus in the property dictionary that we created above
	f = x[27:]                     # the first 27 rows of the log file do not represent stimuli presentation
	index = log['Event Type'].isin((['Sound'])) # in the log file, each stimulus name is repeated for 'Sound' and 'Response', and we only want to extract one instance of each stimuli
	list = log[index]              # this takes the "sound index" created above and subsets just one instance of each stimulus 
	c = list[12:]                  # the first 12 stimuli represent practice trials, so we only extract the stimuli names for the real experiment
	words = c['Code']              # save the order of stimuli to a dictionary
	if len(words) != 560:
		raise RuntimeError("Warning .. Wrong number of trials...") # the total number of stimuli should be 560 in this experiment


# and extract the word order info
	trial_order = log['Trial']
	wordOrder_big = trial_order[index]
	wordOrder = wordOrder_big[12:]       # remove practice trial order
	
	
# convert to float list rather than string list 
	wordOrder = [float(i) for i in wordOrder]

	if len(wordOrder) != 560:            # again check trial count
		raise RuntimeError("Warning .. Wrong number of trials...")


# create list of variables for the words in the order presented to participant
		
		
	morphs = []                                    # create empty dict
	for i, word in enumerate(words):
		word_ = word[0:17]
		morph = morph_dict.get(word_, 0)       # extract value of predictor for each stimuli name in the logfile
		morphs.append(morph)                   # append each value to the "morph" dictionary
		
	lins = []
	for i, word in enumerate(words):
		word_ = word[0:17]
		lin = lin_dict.get(word_, 0)
		lins.append(lin)

	freqs = []
	for i, word in enumerate(words):
		word_ = word[0:17]
		freq = freq_dict.get(word_, 0)
		freqs.append(freq)
		
	fams = []
	for i, word in enumerate(words):
		word_ = word[0:17]
		fam = fam_dict.get(word_, 0)
		fams.append(fam)
		
	roots = []
	for i, word in enumerate(words):
		word_ = word[0:17]
		root = root_dict.get(word_, 0)
		roots.append(root)	


##################################################################################


# read raw with low pass filter #
	
	raw = mne.fiff.Raw( meg_root + '/' + participant + '/' + participant + '_' + experiment + '_lp-raw.fif')


# load the time-fixed events:
	
	events = mne.read_events( meg_root + '/' + participant + '/' + participant + '_Trial_TIMELOCKED_events.fif')
	
	
# add epochs #

	event_id = dict(HiMo_LoLin =25, HiMo_HiLin =21, LoMo_LoLin =41, LoMo_HiLin =37, CVC =6, CVCV =10, CVCVC =18, OCP =34)  

	tmin = -0.2   								# pre stimulis interval (in seconds) #
	tmax = 0.6      								# post stimulus interval #

	picks = mne.fiff.pick_types(raw.info, meg= True, stim = False, exclude = 'bads')    # channels to use in epochs #
	baseline = (-0.2, 0)                                                                # what to use as baseline comparison - here it's pre-stim interval #

	epochs = mne.Epochs(raw, events, event_id,tmin, tmax, proj = True, picks = picks, baseline=baseline, preload = True, decim = 10)


# initiate dataset

	ds = Dataset()
	ds['trigger'] = Var(events[:,2])       # add trigger values to dataset 
	trigger = ds['trigger']                # save trigger values as list

	
# assign triggers (here we're just interested in whether the trigger corresponds to a word or not)

	ds['word'] = Factor(trigger, labels={25: "word", 21: "word", 41: "word", 37: "word"})
	
	
# add variables to ds

	morphs1 = numpy.array(morphs)              # need to move the format of the data around to be able to add it to the dataset...
	morphs2 = morphs1.tolist()                 # these three lines move it from dict -> array -> list
	ds['morph'] = Var(morphs2)                 # add the morph list to the dataset -- note that we need to tell the dataset that this column is a variable
	
	lins1 = numpy.array(lins)
	lins2 = lins1.tolist()
	ds['lin'] = Var(lins2)
	
	freqs1 = numpy.array(freqs)
	freqs2 = freqs1.tolist()
	ds['freq'] = Var(freqs2)
	
	fams1 = numpy.array(fams)
	fams2 = fams1.tolist()
	ds['fam'] = Var(fams2)
	
	roots1 = numpy.array(roots)
	roots2 = roots1.tolist()
	ds['root'] = Var(roots2)
	
	wordOrders1 = numpy.array(wordOrder)
	wordOrders2 = wordOrders1.tolist()
	ds['order'] = Var(wordOrders2)
	
        print ds[0:10]                              # check that everything matches up correctly

# reject the bad epochs # (assumes this has already been done through the gui)

	blink = load.tsv( meg_root + '/' + participant + '/' + participant + '_rejected.txt')
	idx = blink['accept'].x
		
	ds_clean = ds[idx]


# remove the non-words from the epochs and from the dataset

	onlyWords = ds_clean['word'].isin(("word","word","word","word"))
	ds_words = ds_clean[onlyWords]
	
	epochs = epochs[idx]
	epochs = epochs[onlyWords]

	print ds_words         # the cleaned dataset is now called ds_words

	if 0 in ds_words['freq']:
		raise RuntimeError("check indexing of items. appears that non-words are included in array.")


# read inverse operator for all conditions #
	inv = mne.minimum_norm.read_inverse_operator( meg_root + '/' + participant + '/' + participant + '_fixed_inv.fif')


# apply inverse to epochs #
	snr = 1.0   # Lower SNR for single trial data
	lambda2 = 1.0 / snr ** 2
	method = 'dSPM'              						# how do you want to apply the inverse solution? #
	pick_ori = None


# create stcs for each epoch (if you have a lot of epochs then this will take a while #
	stcs = mne.minimum_norm.apply_inverse_epochs(epochs, inv, lambda2, method, pick_ori)
	stc = eelbrain.lab.load.fiff.stc_ndvar(stcs, subject='fsaverage', src='ico-4', subjects_dir=subjects_dir)
	ds_words['data'] = stc   # add the brain data to the dataset
	

# regress all of the "other" predictors onto neural activity (in this case, morphological surprisal, familiarity, frequency, root frequency and word order)
	ds_words['residuals'] = ds_words.eval("data.residuals(morph + fam + freq + root + order)")
	
# then get the beta values for your predictor of interest, based on the residuals once the other predictors have been included #
	beta = ds_words.eval("residuals.ols(lin)")
	
# save the beta values in a pickle file -- this is what will be used for the cluster tests later on #
	save.pickle(beta, "/Volumes/LEG_2TB/Documents/Experiments/ArabPred/Data/pickled_betas/betas_lin_surp/" + participant + "_beta")