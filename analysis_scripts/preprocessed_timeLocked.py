# -*- coding: utf-8 -*-
# MNE Script #
 

# STEP 1 # -- IMPORT DEPENDENCIES # PAGE 22 #

import mne
import os
import pylab as pl
from scipy import io
from mne import fiff
from mne.viz import plot_evoked
from mne.epochs import combine_event_ids
from mne.fiff import Raw
from mne.fiff import Evoked
from mne.minimum_norm import apply_inverse, read_inverse_operator
from mne.preprocessing.ica import ICA
from eelbrain.lab import Dataset, Var, gui
from eelbrain.lab import load

os.environ['MNE_ROOT'] = '/Applications/MNE-2.7.3-3268-MacOSX-i386/'		# make sure this line includes the exact version of MNE that you are using! #
os.environ['SUBJECTS_DIR'] = '/Volumes/LEG_2TB/Documents/Experiments/ArabPred/Data/MRIs'
os.environ['FREESURFER_HOME'] = '/Applications/freesurfer/'



##################################################################################

# STEP 2 # -- ENTER ANALYSIS DETAILS # PAGE 23 #

participants = ["Y0100", "Y0102", "Y0105", "Y0108", "Y0115", "Y0010", "A0079", "Y0018", "Y0021", "Y0052", "Y0053", "Y0056", "Y0090", "Y0091","Y0094", "Y0096", "Y0097", "Y0098"]

#participant = 'Y0115'      # you need to make sure to change this each time you run the script #
experiment = 'ArabPred'        # use the same name here as in your files #
root = '/Volumes/LEG_2TB/Documents/Experiments/ArabPred/Data' 	# the experiment folder should contain both an 'MEG' folder for your all your participant's data and an 'MRIs' folder where the scaled fsaverage or MRI for each subject will be housed.

meg_root = root + '/MEG'             	# if your folders are named correctly, these three should remain untouched #   
subjects_dir = root + '/MRIs'           
stc_path = root + '/timeLocked_stc'


##################################################################################

# STEP 3 # -- CONVERT FILES TO .FIF FORMAT # PAGE 24 #

# mne.gui.kit2fiff()                      			# make sure you are using the Qt4 backend in 'preferences' #

##################################################################################


# STEP 4a # -- TRANSFORMATION MATRIX # PAGE 26 #

# mne.gui.coregistration()                			# remember that the 'subjects_dir' is the MRI folder #

# STEP 4b # -- create 'ico4' source space for the participant # page 28 #

# mne.setup_source_space( participant , spacing = 'ico4')

# errors here will be most likely related to issues defining elements of the experiment in step 2 #

###########################################################################################################
## CHANGE THE BACKEND TO WX AND RE-RUN STEPS 1 & 2. Change working directory to experiment folder again. ##
###########################################################################################################


# STEP 5 # -- READ THE DATA # PAGE 30 # 

# raw = mne.fiff.Raw( participant + '/' + participant + '_' + experiment + '-raw.fif', preload = True)
# print raw
# raw.info


##################################################################################


# STEP 6 # -- VISUALISE DATA TO FIND BAD CHANNELS # PAGE 31 #

# raw.plot()                              			# press the down arrow to cycle through channels #


##################################################################################


# STEP 7 # -- DEFINE BAD CHANNELS # PAGE 32 #

# raw.info['bads'] += ['MEG 017', 'MEG 123']              	# this is +1 to what you'll see on the data acquisition screen #


##################################################################################


# STEP 8 # -- LOW PASS FILTER # PAGE 32 #

# raw.filter(0, 40, method = 'iir')               	# low pass filter at 40hz #
# 
# raw.save( participant + '/' + participant + '_' + experiment + '_lp-raw.fif', overwrite = True)
# 
# raw = mne.fiff.Raw( participant + '/' + participant + '_' + experiment + '_lp-raw.fif' )


##################################################################################


# STEP 9 # -- LOAD EVENTS # PAGE 32 #

# events = mne.find_events(raw, stim_channel = 'STI 014', min_duration = 0.002)
# 
# print events                                		# check you have the expected number of events #
# 
# mne.write_events( participant + '/' + participant + '_events.fif',events)


##################################################################################


# STEP 10 # -- DEFINE CONDITIONS # PAGE 33 # 

for participant in partcipants:

	raw = mne.fiff.Raw( participant + '_' + experiment + '_lp-raw.fif' )

	
   	events = mne.read_events( meg_root + '/' + participant + '/' + participant + '_Trial_TIMELOCKED_events.fif')


	event_id = dict(HiMo_LoLin =25, HiMo_HiLin =21, LoMo_LoLin =41, LoMo_HiLin =37, CVC =6, CVCV =10, CVCVC =18, OCP =34)  
        
           

##################################################################################
                        		

# STEP 11 # -- DEFINE EPOCHS # PAGE 34 #

	tmin = 0.1      								# pre stimulis interval (in seconds) #
	tmax = 0.6      								# post stimulus interval #

	picks = mne.fiff.pick_types(raw.info, meg= True, stim = False, exclude = 'bads')    # channels to use in epochs #
	baseline = (-0.7, -0.6)                                                                # what to use as baseline comparison - here it's pre-stim interval #
	epochs = mne.Epochs(raw, events, event_id,tmin, tmax, proj = True, picks = picks, baseline=baseline, preload = True)


# epochs.save( participant + '/' + participant + '_epoch-av.fif')


##################################################################################


# STEP 12 #  --  REJECT BLINKS FROM EPOCHS # PAGE 35 #

# set up the blink GUI #

# ds = Dataset()
# ds['epochs'] = epochs
# ds['trigger'] = Var(np.ones(ds.n_cases))
# g = gui.SelectEpochs(ds, data='epochs', path = root + '/' + experiment + '/' + participant + '/' + participant + '_rejected.txt', mark = ['MEG 087', 'MEG 130']) # path to save rejections #


# save the result to file #

	blink = load.tsv( participant + '/' + participant + '_rejected.txt')
	idx = blink['accept'].x
	epochs = epochs[idx]		# save epochs without the rejections #

	epochs                          # make a note of how many per condition were rejected #


##################################################################################


# STEP 13 # -- DEFINE THE EPOCHS FOR EACH CONDITION ## PAGE 38 #


# STEP 13A # -- COMBINE CONDITIONS # PAGE 38 #


#### -------#### -------#### -------
												# this is for if you have a number of triggers which correspond to a single condition #
												# if this is not the case, please skip this step #
# STEP 13B # -- MAKE EPOCHS PER CONDITION # PAGE 39 #

#-

	epochs['HiMo_LoLin'].get_data()
	epochs_HiMo_LoLin = epochs['HiMo_LoLin']

	epochs['HiMo_HiLin'].get_data()
	epochs_HiMo_HiLin = epochs['HiMo_HiLin']

	epochs['LoMo_LoLin'].get_data()
	epochs_LoMo_LoLin = epochs['LoMo_LoLin']

	epochs['LoMo_HiLin'].get_data()
	epochs_LoMo_HiLin = epochs['LoMo_HiLin']

#-

	epochs['CVC'].get_data()
	epochs_CVC = epochs['CVC']

	epochs['CVCV'].get_data()
	epochs_CVCV = epochs['CVCV']

	epochs['CVCVC'].get_data()
	epochs_CVCVC = epochs['CVCVC']

	epochs['OCP'].get_data()
	epochs_OCP = epochs['OCP']

#-



######################

# combine_event_ids(epochs, ['HiMo_LoLin', 'HiMo_HiLin'], {'HiMo': 1}, copy = False)
# combine_event_ids(epochs, ['LoMo_LoLin', 'LoMo_HiLin'], {'LoMo': 2}, copy = False)
# 
# epochs['HiMo'].get_data()
# epochs_HiMo = epochs['HiMo']
# 
# epochs['LoMo'].get_data()
# epochs_LoMo = epochs['LoMo']


#combine_event_ids(epochs, ['HiMo_HiLin', 'LoMo_HiLin'], {'HiLin': 3}, copy = False)
#combine_event_ids(epochs, ['HiMo_LoLin', 'LoMo_LoLin'], {'LoLin': 4}, copy = False)

#epochs['HiLin'].get_data()
#epochs_HiLin = epochs['HiLin']

#epochs['LoLin'].get_data()
#epochs_LoLin = epochs['LoLin']






##################################################################################


# STEP 14 # -- READ EPOCHS AND MAKE EVOKED # PAGE 39 #


	evoked = epochs.average()
 	evoked.save( participant + '/' + participant + '-timeLockedevoked-av.fif')



# STEP 14b # -- EVOKED RESPONSE FOR EACH CONDITION # PAGE 39 #

#-

	evoked_HiMo_LoLin = epochs_HiMo_LoLin['HiMo_LoLin'].average()
	evoked_HiMo_LoLin.save( participant + '/' + participant + 'timeLocked_HiMo_LoLin-evoked-av.fif')

	evoked_HiMo_HiLin = epochs_HiMo_HiLin['HiMo_HiLin'].average()
	evoked_HiMo_HiLin.save( participant + '/' + participant + 'timeLocked_HiMo_HiLin-evoked-av.fif')

	evoked_LoMo_LoLin = epochs_LoMo_LoLin['LoMo_LoLin'].average()
	evoked_LoMo_LoLin.save( participant + '/' + participant + 'timeLocked_LoMo_LoLin-evoked-av.fif')

	evoked_LoMo_HiLin = epochs_LoMo_HiLin['LoMo_HiLin'].average()
	evoked_LoMo_HiLin.save( participant + '/' + participant + 'timeLocked_LoMo_HiLin-evoked-av.fif')

#-

	evoked_CVC = epochs_CVC['CVC'].average()
	evoked_CVC.save( participant + '/' + participant + 'timeLocked_CVC-evoked-av.fif')

	evoked_CVCV = epochs_CVCV['CVCV'].average()
	evoked_CVCV.save( participant + '/' + participant + 'timeLocked_CVCV-evoked-av.fif')

	evoked_CVCVC = epochs_CVCVC['CVCVC'].average()
	evoked_CVCVC.save( participant + '/' + participant + 'timeLocked_CVCVC-evoked-av.fif')

	evoked_OCP = epochs_OCP['OCP'].average()
	evoked_OCP.save( participant + '/' + participant + 'timeLocked_OCP-evoked-av.fif')

#-

# evoked_HiMo = epochs_HiMo['HiMo'].average()
# evoked_HiMo.save( participant + '/' + participant + 'HiMo-evoked-av.fif')
# 
# evoked_LoMo = epochs_LoMo['LoMo'].average()
# evoked_LoMo.save( participant + '/' + participant + 'LoMo-evoked-av.fif')

#evoked_HiLin = epochs_HiLin['HiLin'].average()
#evoked_HiLin.save( participant + '/' + participant + 'HiLin-evoked-av.fif')

#evoked_LoLin = epochs_LoLin['LoLin'].average()
#evoked_LoLin.save( participant + '/' + participant + 'LoLin-evoked-av.fif')


#-

##################################################################################


# STEP 15 # -- COVARIANCE MATRIX # PAGE 40 #

	cov = mne.cov.compute_covariance(epochs, tmax = 0)
	cov = mne.cov.regularize(cov, evoked.info, mag=0.05, grad = 0.05, proj = True, exclude = 'bads')

# mne.write_cov( participant + '/' + participant + '_cov.fif', cov)


##################################################################################


# STEP 16 # -- FORWARD SOLUTION # PAGE 41 #

	info = participant + '/' + participant + '-evoked-av.fif'
	mri = participant + '/' + participant + '-trans.fif'
	src = subjects_dir + '/' + participant + '/bem/' + participant + '-ico-4-src.fif'
	bem = subjects_dir + '/' + participant + '/bem/' + participant + '-inner_skull-bem-sol.fif'
	fname = participant + '/' + participant + '_forward.fif'


	fwd = mne.make_forward_solution(info = info, mri = mri, src = src, bem = bem, fname = fname, meg = True, eeg = False, overwrite = True)

#fwd = mne.do_forward_solution(subject = participant, meas = info, mri = mri, spacing = 'ico4', src = src, bem = bem, fname = fname, meg = True, eeg = False, overwrite = True)

	fwd = mne.read_forward_solution(fname, force_fixed = True, surf_ori=True)

# here, information from the coregistration is used to compute the forward solution #
															
##################################################################################


# STEP 17 # -- INVSERSE OPERATOR # PAGE 42 #

	inv = mne.minimum_norm.make_inverse_operator(evoked.info, fwd, cov, loose = 0, depth = None, fixed = True)
													# this is for a fixed orientation. If you want to change to fixed, include a depth parameter and say 'True' to fixed' #
	mne.minimum_norm.write_inverse_operator( participant + '/' + participant + '_timeFixedfixed_inv.fif', inv)


##################################################################################


# STEP 16 # -- APPLY INVERSE TO GET SOURCE TIME ESTIMATES # PAGE 43 #

	snr = 2.0                     						# signal to noise ratio #
	lambda2 = 1.0 / snr ** 2.0
	method = 'dSPM'              						# how do you want to apply the inverse solution? #
	pick_ori = None

# apply inverse operator for each condition:

	stc_HiMo_LoLin = mne.minimum_norm.apply_inverse(evoked_HiMo_LoLin, inv, method = method, lambda2 = lambda2, pick_ori = pick_ori)
	stc_HiMo_HiLin = mne.minimum_norm.apply_inverse(evoked_HiMo_HiLin, inv, method = method, lambda2 = lambda2, pick_ori = pick_ori)
	stc_LoMo_LoLin = mne.minimum_norm.apply_inverse(evoked_LoMo_LoLin, inv, method = method, lambda2 = lambda2, pick_ori = pick_ori)
	stc_LoMo_HiLin = mne.minimum_norm.apply_inverse(evoked_LoMo_HiLin, inv, method = method, lambda2 = lambda2, pick_ori = pick_ori)

	stc_CVC = mne.minimum_norm.apply_inverse(evoked_CVC, inv, method = method, lambda2 = lambda2, pick_ori = pick_ori)
	stc_CVCV = mne.minimum_norm.apply_inverse(evoked_CVCV, inv, method = method, lambda2 = lambda2, pick_ori = pick_ori)
	stc_CVCVC = mne.minimum_norm.apply_inverse(evoked_CVCVC, inv, method = method, lambda2 = lambda2, pick_ori = pick_ori)
	stc_OCP = mne.minimum_norm.apply_inverse(evoked_OCP, inv, method = method, lambda2 = lambda2, pick_ori = pick_ori)

# stc_HiMo =  mne.minimum_norm.apply_inverse(evoked_HiMo, inv, method = method, lambda2 = lambda2, pick_ori = pick_ori)
# stc_LoMo = mne.minimum_norm.apply_inverse(evoked_LoMo, inv, method = method, lambda2 = lambda2, pick_ori = pick_ori)


# and save them

	stc_HiMo_LoLin.save( stc_path + '/HiMo_LoLin' + '/HiMo_LoLin_' + participant + '.fif')
	stc_HiMo_HiLin.save( stc_path + '/HiMo_HiLin' + '/HiMo_HiLin_' + participant + '.fif')
	stc_LoMo_LoLin.save( stc_path + '/LoMo_LoLin' + '/LoMo_LoLin_' + participant + '.fif')
	stc_LoMo_HiLin.save( stc_path + '/LoMo_HiLin' + '/LoMo_HiLin_' + participant + '.fif')

	stc_CVC.save( stc_path + '/CVC' + '/CVC_' + participant + '.fif')
	stc_CVCV.save( stc_path + '/CVCV' + '/CVCV_' + participant + '.fif')
	stc_CVCVC.save( stc_path + '/CVCVC' + '/CVCVC_' + participant + '.fif')
	stc_OCP.save( stc_path + '/OCP' + '/OCP_' + participant + '.fif')