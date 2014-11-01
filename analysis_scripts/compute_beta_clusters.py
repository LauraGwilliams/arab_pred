import eelbrain
from eelbrain import *
import mne


# load beta values for each subject 

subjects = []
betas = []
for subject in ['A0079','Y0003','Y0010','Y0018','Y0021','Y0052','Y0053','Y0054','Y0056','Y0090','Y0092','Y0091','Y0094','Y0095','Y0096','Y0097','Y0098','Y0100','Y0101','Y0102','Y0103','Y0105','Y0108','Y0115']:
	
	beta = eelbrain.load.unpickle( "/Volumes/LEG_2TB/Documents/Experiments/ArabPred/Data/pickled_betas/betas_morph_surp/%s_beta.pickled" % ( subject ))
	subjects.append(subject)
	betas.append(beta)


# initiate dataset and add subject and beta values

ds = Dataset()
ds['subject'] = Factor(subjects, random=True)
ds['beta'] = combine(betas)


# extract source information and optionally subset space and time dimensions

src = ds['beta']
src_lh = src.sub(source='lh')
time_sub = src_lh.sub(time=(0,0.5))


# perform a one-sample t-test between beta value and zero

res = testnd.ttest_1samp(src_lh,ds=ds,samples=10000,pmin=0.05,tstart=0.3,tstop=0.35,mintime=0.02,match='subject')

res.clusters.sort("p")
res_sig = res.clusters.sub("p <= 0.1")
print res_sig


# take first cluster
p = res_sig[0,'cluster']


# view cluster averaged over time
c_extent = p.sum('time')


# plot result
plt_extent = eelbrain.plot.brain.cluster(c_extent, surf = "inflated")


# plot beta values
index = c_extent != 0
c_timecourse = ms_STG.sum(index)
waves = eelbrain.plot.uts.UTSStat(Y=c_timecourse,X=ds['beta'],ds=ds,match=subjects,clusters=res_sig,ylabel="Beta Value",title="Morphological Surprisal")
ax = waves.figure.axes[0]
ax.axhline(y=-0.1,color='b')
ax.axhline(y=0.1,color='b')
waves.draw()
image = waves.image()