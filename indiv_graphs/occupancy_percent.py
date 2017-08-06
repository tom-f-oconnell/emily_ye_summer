import numpy as np
import multi_tracker_analysis as mta
import matplotlib.pyplot as plt
import math
hdf5_filename = "/home/lab/demo/demo_1/data_split/20170723_160250_N1_trackedobjects.hdf5"
pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
np.unique(pd.objid)
pd.keys()
path = '/home/lab/demo/demo_1/data_split/20170723_160250_N1_trackedobjects.hdf5'
dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
dataset.load_keys()

min_frame = None
max_frame = None
frame_rate = None
position = []
b = []
flies_rt = []
flies_lf = []

for i in range (len(np.unique(pd.objid))):
	trajec = dataset.trajec(dataset.keys[i])
	num_of_positions = trajec.position_x.shape[0]
	#accurate to hundredths digit (but still not perfect :( )
	first_timept = trajec.time_epoch_secs[0] + trajec.time_epoch_nsecs[0]/1000000000
	last_timept = trajec.time_epoch_secs[int(trajec.position_x.shape[0])-1]+ trajec.time_epoch_nsecs[int(trajec.position_x.shape[0])-1]/1000000000
	if (first_timept - last_timept)!=0:
		frame_rate = num_of_positions/(first_timept - last_timept)
	if min_frame == None:
		min_frame = trajec.frames[0]
	elif trajec.frames[0] < min_frame:
		min_frame = trajec.frames[0]
	if max_frame == None:
		max_frame = trajec.frames[int(trajec.position_x.shape[0])-1]
	elif trajec.frames[int(trajec.position_x.shape[0])-1] > max_frame:
		max_frame = trajec.frames[int(trajec.position_x.shape[0])-1]

for i in range (len(np.unique(pd.objid))):
	trajec = dataset.trajec(dataset.keys[i])
	first_frame = trajec.frames[0]
	last_frame = trajec.frames[int(trajec.position_x.shape[0])-1]
	beginning_offset = 0
	ending_offset = 0
	beginning_offset = first_frame - min_frame
	ending_offset = max_frame - last_frame
	aligned_position = []
	for i in range (beginning_offset):
		aligned_position.append(None)
	aligned_position.extend(trajec.position_x)
	for i in range (ending_offset):
		aligned_position.append(None)
	position.append(aligned_position)
position = np.array(position)
num_objs = position.shape[0]
num_frames = position.shape[1]
right = 0
left = 0
flies = 0
for i in range(num_frames):
	flies = float(np.sum(position[:, i]>0))
	if flies == 0:
		right = 0
		left = 0
	else:
		right = (np.sum((position[:, i])>920))
		left = flies-right
		flies_rt.append(right/flies)
		flies_lf.append(left/flies)
plt.plot(flies_rt, color = 'red')
plt.plot(flies_lf, color = 'blue')

plt.xlabel('percent occupancy')
plt.ylabel('average walking speed')
lf_edge= 0
rt_edge= frame_rate*2*60
for i in range ((max_frame/(frame_rate*30*60))+1):
        lf_edge= lf_edge+ frame_rate*1680
        rt_edge= rt_edge+ frame_rate*1680
        plt.axvspan(lf_edge, rt_edge, 0, 1, alpha=0.5, color= 'yellow')
plt.show()
