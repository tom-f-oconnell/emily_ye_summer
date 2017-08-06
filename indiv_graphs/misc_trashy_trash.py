############### WALKING SPEED############################

import numpy as np
import multi_tracker_analysis as mta
import matplotlib.pyplot as plt
import math
hdf5_filename = "/home/lab/demo/demo_1/data/20170729_112342_N1_trackedobjects.hdf5"
pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
np.unique(pd.objid)
ad = mta.read_hdf5_file_to_pandas.load_data_as_pandas_dataframe_from_hdf5_file(hdf5_filename, attributes=None)
pd.keys()
path = '/home/lab/demo/demo_1/data/20170729_112342_N1_trackedobjects.hdf5'
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
first_position = None
last_position = None

speed = []

for i in range (len(np.unique(pd.objid))):
	trajec = dataset.trajec(dataset.keys[i])
	num_of_positions = trajec.position_x.shape[0]
	#accurate to hundredths digit (but still not perfect :( )
	first_timept = trajec.time_epoch_secs[0] + trajec.time_epoch_nsecs[0]/1000000000
	last_timept = trajec.time_epoch_secs[int(trajec.position_x.shape[0])-1]+ trajec.time_epoch_nsecs[int(trajec.position_x.shape[0])-1]/1000000000
	range_time = last_timept - first_timept
	range_time = float(range_time)
	if range_time != 0:
		frame_rate = num_of_positions/range_time
		#print frame_rate
	frame_rate = num_of_positions/(first_timept - last_timept)
	#print frame_rate
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
	beginning_offset = 0
	ending_offset = 0
	first_frame = trajec.frames[0]
	beginning_offset = first_frame - min_frame
	last_frame = trajec.frames[int(trajec.speed.shape[0])-1]
	ending_offset = max_frame - last_frame
	aligned_position = []
	for i in range (beginning_offset):
		aligned_position.append(0)
	aligned_position.extend(trajec.speed)
	for i in range (ending_offset):
		aligned_position.append(0)
	speed.append(aligned_position)
speed = np.array(speed)

#average walking speed per frame
total_speed = None
avg_speed = None
walking_speed = []
for i in range(speed.shape[1]):
	total_speed = sum(speed[:, i])
	avg_speed = total_speed/float(speed.shape[0])
	walking_speed.append(avg_speed)
plt.plot(walking_speed)

lf_edge= 0
rt_edge= abs(frame_rate*2)
for i in range (int(math.ceil(max_frame/12600))):
        lf_edge= lf_edge+ abs(frame_rate*1800)
        rt_edge= rt_edge+ abs(frame_rate*1800)
        plt.axvspan(lf_edge, rt_edge, 0, 1, alpha=0.5, color= 'yellow')
plt.show()

############ OCCUPANCY_NONE_INDIV ###################################
import numpy as np
import multi_tracker_analysis as mta
import matplotlib.pyplot as plt
import math
hdf5_filename = "/home/lab/demo/demo_1/data/20170722_151805_N1_trackedobjects.hdf5"
pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
np.unique(pd.objid)
ad = mta.read_hdf5_file_to_pandas.load_data_as_pandas_dataframe_from_hdf5_file(hdf5_filename, attributes=None)
pd.keys()
path = '/home/lab/demo/demo_1/data/20170722_151805_N1_trackedobjects.hdf5'
dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
dataset.load_keys()

#testing getting time points
first_time = ad['time_epoch'].values[0]
first_frame = ad['frames'].values[0]
last_time = ad['time_epoch'].values[-1]
last_frame = ad['frames'].values[-1]
np.unique(pd.objid)
#print first_time
print first_frame
#print last_time
print last_frame

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

#################### OCCUPANCY_NONE_TESTER #######################################
import numpy as np
import multi_tracker_analysis as mta
import matplotlib.pyplot as plt
import math
hdf5_filename = "/home/lab/demo/demo_1/data/20170729_112342_N1_trackedobjects.hdf5"
pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
np.unique(pd.objid)
ad = mta.read_hdf5_file_to_pandas.load_data_as_pandas_dataframe_from_hdf5_file(hdf5_filename, attributes=None)
pd.keys()
path = '/home/lab/demo/demo_1/data/20170729_112342_N1_trackedobjects.hdf5'
dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
dataset.load_keys()

#testing getting time points
first_time = ad['time_epoch'].values[0]
first_frame = ad['frames'].values[0]
last_time = ad['time_epoch'].values[-1]
last_frame = ad['frames'].values[-1]
np.unique(pd.objid)
#print first_time
print first_frame
#print last_time
print last_frame

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
		aligned_position.append(None)
	aligned_position.extend(trajec.position_x)
	for i in range (ending_offset):
		aligned_position.append(None)
        #plt.plot(aligned_position)
	position.append(aligned_position)
position = np.array(position)


#plot blobs on lf or rt w/ odor pulses
b = []
for i in range (position.shape[1]):
    rt = np.sum(position[:, i]<920)
    lf = len(position)-rt
    b.append([lf,rt])
    rt =0
    lf =0


b = np.array(b)
plt.plot(b)


plt.axhline(y=920, xmin=0, xmax=position.shape[1], hold=None)
plt.ylabel('x-position')
plt.xlabel('frames')
odor_pulse = []
lf_edge= 0
rt_edge= abs(frame_rate*2)
for i in range (int(math.ceil(max_frame/12600))):
        lf_edge= lf_edge+ abs(frame_rate*1800)
        rt_edge= rt_edge+ abs(frame_rate*1800)
        plt.axvspan(lf_edge, rt_edge, 0, 1, alpha=0.5, color= 'yellow')
plt.show()

################## OCCUPANCY_INDIV_TESTER #########################
import numpy as np
import multi_tracker_analysis as mta
import matplotlib.pyplot as plt
import math
hdf5_filename = "/home/lab/demo/demo_1/tester/20170722_151805_N1_trackedobjects.hdf5"
pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
np.unique(pd.objid)
ad = mta.read_hdf5_file_to_pandas.load_data_as_pandas_dataframe_from_hdf5_file(hdf5_filename, attributes=None)
pd.keys()
path = '/home/lab/demo/demo_1/tester/20170722_151805_N1_trackedobjects.hdf5'
dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
dataset.load_keys()


min_frame = None
max_frame = None

position = []

for i in range (len(np.unique(pd.objid))):
	trajec = dataset.trajec(dataset.keys[i])
	num_of_positions = trajec.position_x.shape[0]
	#accurate to hundredths digit (but still not perfect :( )
	first_timept = trajec.time_epoch_secs[0] + trajec.time_epoch_nsecs[0]/1000000000
	last_timept = trajec.time_epoch_secs[int(trajec.position_x.shape[0])-1]+ trajec.time_epoch_nsecs[int(trajec.position_x.shape[0])-1]/1000000000
	frame_rate = num_of_positions/(first_timept - last_timept)
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
		aligned_position.append(first_position)
	aligned_position.extend(trajec.position_x)
	for i in range (ending_offset):
		aligned_position.append(last_position)
        plt.plot(aligned_position)

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
