import numpy as np
import multi_tracker_analysis as mta
import matplotlib.pyplot as plt
import math
hdf5_filename = "/home/lab/demo/demo_1/data_split/20170723_160250_N1_trackedobjects.hdf5"
pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
np.unique(pd.objid)
ad = mta.read_hdf5_file_to_pandas.load_data_as_pandas_dataframe_from_hdf5_file(hdf5_filename, attributes=None)
pd.keys()
path = '/home/lab/demo/demo_1/data_split/20170723_160250_N1_trackedobjects.hdf5'
dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
dataset.load_keys()


#getting a bunch of possibly useful information
min_frame = None
max_frame = None
first_frame = None
last_frame = None

speed = []

for i in range (len(np.unique(pd.objid))):
	trajec = dataset.trajec(dataset.keys[i])
	num_of_positions = trajec.position_x.shape[0]
	#accurate to hundredths digit (but still not perfect :( )
	first_timept = trajec.time_epoch_secs[0] + trajec.time_epoch_nsecs[0]/1000000000
	last_timept = trajec.time_epoch_secs[int(trajec.position_x.shape[0])-1]+ trajec.time_epoch_nsecs[int(trajec.position_x.shape[0])-1]/1000000000
	range_time = last_timept - first_timept
	range_time = float(range_time)
	if min_frame == None:
		min_frame = trajec.frames[0]
	elif trajec.frames[0] < min_frame:
		min_frame = trajec.frames[0]
	if max_frame == None:
		max_frame = trajec.frames[int(trajec.position_x.shape[0])-1]
	elif trajec.frames[int(trajec.position_x.shape[0])-1] > max_frame:
		max_frame = trajec.frames[int(trajec.position_x.shape[0])-1]
	first_frame = trajec.frames[0]
	last_frame = trajec.frames[int(trajec.position_x.shape[0])-1]
	if range_time != 0:
		frame_rate = ((last_frame-first_frame)+1)/range_time

#aligning front of position lists (based on frame, not time)

	for i in range (len(np.unique(pd.objid))):
		trajec = dataset.trajec(dataset.keys[i])
		beginning_offset = 0
		ending_offset = 0
		first_frame = trajec.frames[0]
		beginning_offset = first_frame - min_frame
		last_frame = trajec.frames[int(trajec.speed.shape[0])-1]
		ending_offset = max_frame - last_frame
		aligned_speed = []
		for i in range (beginning_offset):
			aligned_speed.append(0.0000000000000000000000001)
		aligned_speed.extend(trajec.speed)
		for i in range (ending_offset):
			aligned_speed.append(0.0000000000000000000000001)
		speed.append(aligned_speed)
	speed = np.array(speed)

	#average walking speed per frame
	speedy = None
	walking_speed = []
	for i in range(speed.shape[1]):
		flies = float(np.sum(speed[:, i]!=0.0000000000000000000000001))
		if flies != None:
			speedy = sum(speed[:, i])/flies
			walking_speed.append(speedy)
		else:
			walking_speed.append(None)
	plt.plot(walking_speed)
    plt.xlabel('time')
	plt.ylabel('average walking speed')
	lf_edge= 0
	rt_edge= frame_rate*2*60
	for i in range (int(math.ceil((max_frame/12600)))):
	        lf_edge= lf_edge+ frame_rate*1680
	        rt_edge= rt_edge+ frame_rate*1680
	        plt.axvspan(lf_edge, rt_edge, 0, 1, alpha=0.5, color= 'yellow')
	plt.show()
