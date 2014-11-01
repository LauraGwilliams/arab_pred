import mne

participant = "Y0003"


# set up environment #
experiment = 'ArabPred'        # use the same name here as in your files #
root = '/Volumes/LEG_2TB/Documents/Experiments/ArabPred/Data' 	# the experiment folder should contain both an 'MEG' folder for your all your participant's data and an 'MRIs' folder where the scaled fsaverage or MRI for each subject will be housed.
meg_root = root + '/MEG'             	# if your folders are named correctly, these three should remain untouched #   
subjects_dir = root + '/MRIs'


# load raw #
raw = mne.fiff.Raw( meg_root + '/' + participant + '/' + participant + '_' + experiment + '_lp-raw.fif')
     
     
events = mne.read_events( meg_root + '/' + participant + '/' + participant + '_Trial_TIMELOCKED_NONWORDS_events.fif')
	
# add epochs #

event_id = dict(HiMo_LoLin =25, HiMo_HiLin =21, LoMo_LoLin =41, LoMo_HiLin =37, CVC =6, CVCV =10, CVCVC =18, OCP =34)  

tmin = -0.5								# pre stimulis interval (in seconds) #
tmax = 0.4 								# post stimulus interval #

picks = mne.fiff.pick_types(raw.info, meg= True, stim = False, exclude = 'bads')    # channels to use in epochs #
baseline = (-0.5,-0.4)                                                                # what to use as baseline comparison - here it's pre-stim interval #

epochs = mne.Epochs(raw, events, event_id,tmin, tmax, proj = True, picks = picks, baseline=baseline, preload = True)
      

# get data #
OCP = epochs['OCP'].get_data()
CVC = epochs['CVC'].get_data()


# gather info for time freq
import numpy as np
n_cycles = 2  # number of cycles in Morlet wavelet
frequencies = np.arange(7, 30, 3)  # frequencies of interest
Fs = raw.info['sfreq']  # sampling in Hz


#Compute induced power and phase-locking values:
from mne.time_frequency import induced_power
power, phase_lock = induced_power(OCP, Fs=Fs, frequencies=frequencies, n_cycles=2, n_jobs=1)

power2 = np.mean(power, axis=0)  # average over sources
phase = np.mean(phase_lock, axis=0)  # average over sources
times = epochs.times


# plot result #
plt.imshow(power2,extent=[times[0],times[-1],frequencies[0],frequencies[-1]],aspect='auto',origin='lower')
# plt.imshow(phase,extent=[times[0],times[-1],frequencies[0],frequencies[-1]],aspect='auto',origin='lower')


plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
