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


#getting a bunch of possibly useful information

min_frame = None
max_frame = None
frame_rate = None

position = []

for i in range (len(np.unique(pd.objid))):
	trajec = dataset.trajec(dataset.keys[i])
	num_of_positions = trajec.position_x.shape
	#accurate to hundredths digit (but still not perfect :( )
	first_timept = trajec.time_epoch_secs[0] + trajec.time_epoch_nsecs[0]/1000000000
	last_timept = trajec.time_epoch_secs[int(trajec.position_x.shape[0])-1]+ trajec.time_epoch_nsecs[int(trajec.position_x.shape[0])-1]/1000000000
	if (last_timept - first_timept)!=0:
		frame_rate = num_of_positions/(last_timept - first_timept)
	if min_frame == None:
		min_frame = trajec.frames[0]
	elif trajec.frames[0] < min_frame:
		min_frame = trajec.frames[0]
	if max_frame == None:
		max_frame = trajec.frames[int(trajec.position_x.shape[0])-1]
	elif trajec.frames[int(trajec.position_x.shape[0])-1] > max_frame:
		max_frame = trajec.frames[int(trajec.position_x.shape[0])-1]


#aligning front of position lists (based on frame, not time)

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
		aligned_position.append(None)
	aligned_position.extend(trajec.position_x)
	for i in range (ending_offset):
		aligned_position.append(None)
        plt.plot(aligned_position)
	position.append(aligned_position)
position = np.array(position)


#plot blobs on lf or rt w/ odor pulses



plt.axhline(y=920, xmin=0, xmax=position.shape[1], hold=None)
plt.ylabel('x-position')
plt.xlabel('frames')
lf_edge= 0
rt_edge= abs(frame_rate*2)
for i in range (int(math.ceil(max_frame/12600))):
        lf_edge= lf_edge+ abs(frame_rate*1800)
        rt_edge= rt_edge+ abs(frame_rate*1800)
        plt.axvspan(lf_edge, rt_edge, 0, 1, alpha=0.5, color= 'yellow')
plt.show()
