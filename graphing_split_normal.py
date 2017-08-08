from analysis_split import Analysis
import multi_tracker_analysis as mta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import ipdb

total_occupancy = []
total_occupancypercent= []
total_walk = []
total_err = []

print "CHUNK 1"

hdf5_filename = '/home/lab/demo/demo_1/data_split/1/20170724_171509_N1_trackedobjects.hdf5'
path = hdf5_filename
max_frame = None
frame_rate = None
position = []
beginning_offsets = []
ending_offsets = []
pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
one = Analysis(pd, dataset, beginning_offsets, ending_offsets, max_frame, frame_rate, hdf5_filename = hdf5_filename, path = path)


time_position = one.time_position()
interp_position_total = one.interpolate_and_align(time_position)
occupancy_original_one = one.occupancy(interp_position_total)
total_occupancy.extend(occupancy_original_one)
occupancy_percent_one = one.occupancy_percent(occupancy_original_one)
total_occupancypercent.extend(occupancy_percent_one)
time_speed = one.time_speed()
walking_one, err_one = one.walkspeed(time_speed)
total_walk.extend(walking_one)
total_err.extend(walking_one)


print "CHUNK 2"

hdf5_filename = '/home/lab/demo/demo_1/data/20170725_042149_N1_trackedobjects.hdf5'
path = hdf5_filename
max_frame = None
frame_rate = None
position = []
beginning_offsets = []
ending_offsets = []
pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
two = Analysis(pd, dataset, beginning_offsets, ending_offsets, max_frame, frame_rate, hdf5_filename = hdf5_filename, path = path)


time_position = two.time_position()
interp_position_total = two.interpolate_and_align(time_position)
occupancy_original_two = two.occupancy(interp_position_total)
total_occupancy.extend(occupancy_original_two)
occupancy_percent_two = one.occupancy_percent(occupancy_original_two)
total_occupancypercent.extend(occupancy_percent_two)
time_speed = two.time_speed()
walking_two, err_two = two.walkspeed(time_speed)
total_walk.extend(walking_two)
total_err.extend(walking_two)
'''
print "CHUNK 3"
hdf5_filename = '/home/lab/demo/demo_1/data_split/3/20170724_084250_N1_trackedobjects.hdf5'
path = hdf5_filename
max_frame = None
frame_rate = None
position = []
beginning_offsets = []
ending_offsets = []
pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
three = Analysis(pd, dataset, beginning_offsets, ending_offsets, max_frame, frame_rate, hdf5_filename = hdf5_filename, path = path)


time_position = three.time_position()
interp_position_total = three.interpolate_and_align(time_position)
occupancy_original_three = three.occupancy(interp_position_total)
total_occupancy.extend(occupancy_original_three)
occupancy_percent_three = three.occupancy_percent(occupancy_original_one)
total_occupancypercent.extend(occupancy_percent_three)
time_speed = three.time_speed()
walking_three, err_three = three.walkspeed(time_speed)
total_walk.extend(walking_three)
total_err.extend(walking_three)
'''
'''
total_occupancy = np.concatenate((occupancy_original_one, occupancy_original_two, occupancy_original_three))
total_walk = np.concatenate((walking_two, walking_two, walking_three))
total_occupancypercent = np.concatenate((occupancy_percent_one, occupancy_percent_two, occupancy_percent_three))
total_err = np.concatenate((err_one, err_two, err_three))
'''
f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=False)

lf_edge= 0
rt_edge= 600
for i in range (int((len(occupancy_original_one)+ len(occupancy_original_two) )/9000)+2):
        lf_edge= lf_edge+ 8400
        rt_edge= rt_edge+ 8400
        ax1.axvspan(lf_edge, rt_edge, alpha=0.5, color= 'yellow')
lf_edge= 0
rt_edge= 600
for i in range (int((len(occupancy_original_one)+ len(occupancy_original_two))/9000)+2):
        lf_edge= lf_edge+ 8400
        rt_edge= rt_edge+ 8400
        ax2.axvspan(lf_edge, rt_edge, alpha=0.5, color= 'yellow')
lf_edge= 0
rt_edge= 600
for i in range (int((len(occupancy_original_one)+ len(occupancy_original_two))/9000)+2):
        lf_edge= lf_edge+ 8400
        rt_edge= rt_edge+ 8400
        ax3.axvspan(lf_edge, rt_edge, alpha=0.5, color= 'yellow')

plt.suptitle('Ethylpropionate v Ethylpropionate (ep reared)')
ax1.plot(total_occupancy)
ax1.set_title('OCCUPANCY')
ax1.set_xlabel('time')
ax1.set_ylabel('flies')
ax2.plot(total_occupancypercent)
ax2.set_title("PERCENT OCCUPANCY")
ax2.set_ylabel('occupancy index')
ax2.set_xlabel('time')
ax3.plot(total_walk)
ax3.set_title('WALKING SPEED')
ax3.set_ylabel('pixels/second ?')
ax3.set_xlabel('time')
x = []
for i in range(len(total_walk)):
    x.append(i)
y = total_walk
print len(total_err)
print len(x)
print len(y)

ax3.errorbar(x,y, yerr= total_err)
# Fine-tune figure; make subplots close to each other and hide x ticks for
# all but bottom plot.
f.subplots_adjust(hspace=1)
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
plt.show()
