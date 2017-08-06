import numpy as np
import multi_tracker_analysis as mta
import matplotlib.pyplot as plt
import math
hdf5_filename = "/home/lab/demo/demo_1/data/20170725_042149_N1_trackedobjects.hdf5"
pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
np.unique(pd.objid)
ad = mta.read_hdf5_file_to_pandas.load_data_as_pandas_dataframe_from_hdf5_file(hdf5_filename, attributes=None)
pd.keys()
path = '/home/lab/demo/demo_1/data/20170725_042149_N1_trackedobjects.hdf5'
dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
dataset.load_keys()

#testing getting time points
first_time = ad['time_epoch'].values[0]
first_frame = ad['frames'].values[0]
last_time = ad['time_epoch'].values[-1]
last_frame = ad['frames'].values[-1]
np.unique(pd.objid)

first_time_prime =np.min(ad.time_epoch.values)

#getting a bunch of possibly useful information
min_length = None
min_time = None
max_time = None
min_frame = None
max_frame = None
first_timept = None
last_time_pt = None
first_frame = None
last_frame = None
frame_rate = None

position = []

for i in range (len(np.unique(pd.objid))):
	trajec = dataset.trajec(dataset.keys[i])
	num_of_positions = trajec.position_x.shape
	#accurate to hundredths digit (but still not perfect :( )
	first_timept = trajec.time_epoch_secs[0] + trajec.time_epoch_nsecs[0]/1000000000
	last_timept = trajec.time_epoch_secs[int(trajec.position_x.shape[0])-1]+ trajec.time_epoch_nsecs[int(trajec.position_x.shape[0])-1]/1000000000
	frame_rate = num_of_positions/(last_timept - first_timept)
	if min_frame == None:
		min_frame = trajec.frames[0]
	elif trajec.frames[0] < min_frame:
		min_frame = trajec.frames[0]
	if max_frame == None:
		max_frame = trajec.frames[int(trajec.position_x.shape[0])-1]
	elif trajec.frames[int(trajec.position_x.shape[0])-1] > max_frame:
		max_frame = trajec.frames[int(trajec.position_x.shape[0])-1]
	mins_length = None
	if mins_length == None:
		mins_length = trajec.position_x.shape
	elif trajec.position_x.shape < mins_length:
		mins_length = trajec.position_x.shape
	min_length = mins_length[0]
	if min_time == None:
		min_time = trajec.time_epoch_secs[0] + trajec.time_epoch_nsecs[0]/1000000000
	elif trajec.time_epoch_secs[0] + trajec.time_epoch_nsecs[0]/1000000000 < min_time:
		min_time = trajec.time_epoch_secs[0] + trajec.time_epoch_nsecs[0]/1000000000
	if max_time == None:
		max_time = trajec.time_epoch_secs[int(trajec.position_x.shape[0])-1] + trajec.time_epoch_nsecs[int(trajec.position_x.shape[0])-1]/1000000000
	elif trajec.time_epoch_secs[int(trajec.position_x.shape[0])-1] + trajec.time_epoch_nsecs[int(trajec.position_x.shape[0])-1]/1000000000< max_time:
		max_time = trajec.time_epoch_secs[int(trajec.position_x.shape[0])-1]+ trajec.time_epoch_nsecs[int(trajec.position_x.shape[0])-1]/1000000000

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
		aligned_position.append(first_position)
	aligned_position.extend(trajec.position_x)
	for i in range (ending_offset):
		aligned_position.append(last_position)
	position.append(aligned_position)
position = np.array(position)

#probability of crossing to lf or rt
rt_cross_per_obj = []
lf_cross_per_obj = []

for i in range(position.shape[0]):
	current_trajec = position[i]
	cross = []
	rt_crossing=[]
        lf_crossing=[]
	for ii in range (len(current_trajec)-1):
                if current_trajec[ii]<920:
                        cross.extend([0])
                elif current_trajec[ii]>920:
                        cross.extend([1])
	for iii in range (len(cross)):
		if int(cross[iii]) - int(cross[iii-1]) == 0 :
			rt_crossing.extend([0])
			lf_crossing.extend([0])
		elif int(cross[iii]) - int(cross[iii-1]) == 1 :
			rt_crossing.extend([1])
			lf_crossing.extend([0])
		elif int(cross[iii]) - int(cross[iii-1]) == -1 :
			rt_crossing.extend([0])
			lf_crossing.extend([1])
	rt_cross_per_obj.append(rt_crossing)
	lf_cross_per_obj.append(lf_crossing)
rt_cross_per_obj = np.array(rt_cross_per_obj)
lf_cross_per_obj = np.array(lf_cross_per_obj)
prob_rt=[]
prob_lf=[]
for i in range(len(rt_cross_per_obj)-1):
        for ii in range(position.shape[0]-1):
                sum_rt = 0
                sum_lf = 0
                sum_rt = sum_rt + sum(rt_cross_per_obj[: ,i])
                sum_lf = sum_lf + sum(lf_cross_per_obj[: ,i])
                prob_cross_rt = 0
                prob_cross_lf = 0
                prob_cross_rt = float(sum_rt)/len(rt_cross_per_obj)
                prob_cross_lf = float(-1* sum_lf)/len(rt_cross_per_obj)
                prob_rt.extend([prob_cross_rt])
                prob_lf.extend([prob_cross_lf])
plt.plot(prob_rt)
plt.plot(prob_lf)
plt.ylabel('probability of crossing (+)right (-)left')
plt.xlabel('time')
odor_pulse = []
lf_edge= min_frame
rt_edge= min_frame+2
for i in range(int(math.ceil(last_frame/(30*60*30)))):
        lf_edge= lf_edge+28
        rt_edge= rt_edge+28
        plt.axvspan(lf_edge, rt_edge, 0, 1, alpha=0.25, color= 'yellow')
plt.show()
