from __future__ import division
import numpy as np
import multi_tracker_analysis as mta
import matplotlib.pyplot as plt
import math
import ipdb
hdf5_filename = "/mnt/tb/original/20170730_155211_N1/20170730_155211_N1_trackedobjects.hdf5"
pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
np.unique(pd.objid)
pd.keys()
path = "/mnt/tb/original/20170730_155211_N1/20170730_155211_N1_trackedobjects.hdf5"
dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
dataset.load_keys()


#getting a bunch of possibly useful information
min_frame = None
max_frame = None
first_timept = None
last_time_pt = None
frame_rate = None

position = []
frame_rates = []
frame_rat = []
frame_rats = []
frame_rodent = []
frame_rodents = []
tim_diff = []


for i in range (len(np.unique(pd.objid))):
	trajec = dataset.trajec(dataset.keys[i])
	num_of_positions = trajec.position_x.shape
	#accurate to hundredths digit (but still not perfect :( )
	first_timept = trajec.time_epoch_secs[0] + trajec.time_epoch_nsecs[0]/1000000000
	last_timept = trajec.time_epoch_secs[-1]+ trajec.time_epoch_nsecs[-1]/1000000000
        if (last_timept - first_timept >3 and last_timept-first_timept<3.001):
            frame_rat.append(num_of_positions/(last_timept - first_timept))
        if (last_timept - first_timept >7 and last_timept-first_timept<7.0001):
            frame_rats.append(num_of_positions/(last_timept - first_timept))
        if (last_timept - first_timept >10 and last_timept-first_timept<10.001):
            frame_rodent.append(num_of_positions/(last_timept - first_timept))
        if (last_timept - first_timept >14 and last_timept-first_timept<14.001):
            frame_rodents.append(num_of_positions/(last_timept - first_timept))
	if (last_timept - first_timept)!=0:	
		frame_rate = num_of_positions/(last_timept - first_timept)
                frame_rates.append(frame_rate)
                tim_diff.append((last_timept - first_timept))
	if min_frame == None:
		min_frame = trajec.frames[0]
	elif trajec.frames[0] < min_frame:
		min_frame = trajec.frames[0]
	if max_frame == None:
		max_frame = trajec.frames[int(trajec.position_x.shape[0])-1]
	elif trajec.frames[int(trajec.position_x.shape[0])-1] > max_frame:
		max_frame = trajec.frames[int(trajec.position_x.shape[0])-1]
    
ipdb.set_trace()
#aligning front of position lists (based on frame, not time)
'''
for i in range (len(np.unique(pd.objid))):
	trajec = dataset.trajec(dataset.keys[i])
	first_position = trajec.position_x[0]
	last_position = trajec.position_x[int(trajec.position_x.shape[0])-1]
	beginning_offset = 0
	ending_offset = 0
	first_frame = trajec.frames[0]
	beginning_offset = first_frame - min_frame
	last_frame = trajec.frames[int(trajec.position_x.shape[0])-1]
	ending_offset = max_frame - last_frame
	aligned_position = []
	for i in range (beginning_offset):
		aligned_position.append(0)
	aligned_position.extend(trajec.position_x)
	for i in range (ending_offset):
		aligned_position.append(0)
	position.append(aligned_position)
position = np.array(position)
num_frames = position.shape[1]
num_objs = position.shape[0]

#plot blobs on lf or rt w/ odor pulses
b = []
for i in range (num_frames/5):
    flies = float(np.sum(position[:, i]>0))
    lf = np.sum(position[:, i]>920)
    rt = flies-lf
    b.append([lf,rt])
    rt =0
    lf =0
print b

b = np.array(b)
plt.plot(b)


plt.ylabel('flies')
plt.xlabel('frames')
odor_pulse = []
lf_edge= 0
rt_edge= abs(frame_rate*2)
for i in range (int(math.ceil(max_frame/12600))):
        lf_edge= lf_edge+ abs(frame_rate*1800)
        rt_edge= rt_edge+ abs(frame_rate*1800)
        plt.axvspan(lf_edge, rt_edge, 0, 1, alpha=0.5, color= 'yellow')
plt.show()
'''
