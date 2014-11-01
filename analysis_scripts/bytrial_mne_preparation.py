
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
import numpy
from mne import minimum_norm as mn

os.environ['MNE_ROOT'] = '/Applications/MNE-2.7.3-3268-MacOSX-i386/'		# make sure this line includes the exact version of MNE that you are using! #
os.environ['SUBJECTS_DIR'] = '/Volumes/LEG_2TB/Documents/Experiments/ArabPred/Data/MRIs'
os.environ['FREESURFER_HOME'] = '/Applications/freesurfer/'


##################################################################################

# STEP 2 # -- ENTER ANALYSIS DETAILS # PAGE 23 #

participants = ['A0079','Y0003','Y0010','Y0018','Y0021','Y0052','Y0053','Y0054','Y0056','Y0090','Y0091','Y0092','Y0094','Y0095','Y0096','Y0097','Y0098','Y0100','Y0101','Y0102','Y0103','Y0105','Y0108','Y0115','Y0099']
experiment = 'ArabPred'        # use the same name here as in your files #
root = '/Volumes/LEG_2TB/Documents/Experiments/ArabPred/Data' 	# the experiment folder should contain both an 'MEG' folder for your all your participant's data and an 'MRIs' folder where the scaled fsaverage or MRI for each subject will be housed.

meg_root = root + '/MEG'             	# if your folders are named correctly, these three should remain untouched #   
subjects_dir = root + '/MRIs'           
stc_path = root + '/stc'
by_trial_path = root + '/single_trial/TTG/epoch_files'

##################################################################################

for participant in participants:

	print "processing " + participant + " now.. please wait."

	# read raw with low pass filter #
	
	if "Y0099" in participant:
		raw = mne.fiff.Raw( [participant + '/' + participant + '_' + experiment + '_part1_lp-raw.fif', participant + '/' + participant + '_' + experiment + '_part2_lp-raw.fif'])
	else:
		raw = mne.fiff.Raw( participant + '/' + participant + '_' + experiment + '_lp-raw.fif')


	# load up events from raw file #
	events = mne.find_events(raw, stim_channel = 'STI 014', min_duration = 0.002)

	# add epochs #

	tmin = -0.1        								# pre stimulis interval (in seconds) #
	tmax = 1.2        								# post stimulus interval #
	picks = mne.fiff.pick_types(raw.info, meg= True, stim = False, exclude = 'bads')    # channels to use in epochs #
	baseline = (None, 0)

	epochs = mne.Epochs(raw = raw, events = events, event_id = None, tmin = tmin, tmax = tmax, proj = True, picks = picks, baseline=baseline, preload = True)

	# reject the bad epochs # (assumes this has already been done through the gui)
	blink = load.tsv( participant + '/' + participant + '_rejected.txt')
	idx = blink['accept'].x
	epochs = epochs[idx]		# save epochs without the rejections #


	# read inverse operator for all conditions #
	inv = mne.minimum_norm.read_inverse_operator( participant + '/' + participant + '_fixed_inv.fif')

	# apply inverse to epochs #

	snr = 1.0   # Lower SNR for single trial data
	lambda2 = 1.0 / snr ** 2
	method = 'dSPM'              						# how do you want to apply the inverse solution? #
	pick_ori = None

	stcs = mne.minimum_norm.apply_inverse_epochs(epochs, inv, lambda2, method, pick_ori)

	# extract time course:

	label_dir = subjects_dir + "/labels/"
	label = mne.read_label( label_dir + "TTG-lh.label")
	src = inv['src']

	extract_time_course = mne.extract_label_time_course(stcs, label, src, mode = 'mean')


	# squeeze out the pesky third dimension
	squeezed = numpy.squeeze(extract_time_course)
	squeezed.shape


	# save to a numpy array on disk
	numpy.savetxt( by_trial_path + '/' + participant + '_' + experiment + "_TTG_epochs.csv", squeezed, delimiter=",")
	print participant + " done!!! congratulations!!! :)"

#and to load again::
#data = numpy.load(participant + '/' participant + '_' + experiment + "_epochs.npy")