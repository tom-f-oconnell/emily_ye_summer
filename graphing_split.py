from analysis_split import Analysis
import multi_tracker_analysis as mta
import matplotlib.pyplot as plt
import numpy as np
import ipdb

use_saved_data = True

total_occupancy = []
total_occupancypercent = []
total_walk = []
occupancy_original = []

print "CHUNK 1"
path = "/home/lab/demo/demo_1/data_split/1/20170723_160250_N1_trackedobjects.hdf5"
hdf5_filename =  "/home/lab/demo/demo_1/data_split/1/20170723_160250_N1_trackedobjects.hdf5"
max_frame = None
frame_rate = None
position = []
beginning_offsets = []
ending_offsets = []
pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
one = Analysis(pd, dataset, beginning_offsets, ending_offsets, max_frame, frame_rate, hdf5_filename = hdf5_filename, path = path)

if not use_saved_data:
    time_position = one.time_position()
    interp_position_total = one.interpolate_and_align(time_position)
    occupancy_original_one = one.occupancy(interp_position_total)
    occupancy_original = occupancy_original_one
    occupancy_percent_one = one.occupancy_perhttps://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.sem.htmlcent(occupancy_original_one)
    time_speed = one.time_speed()
    walking_one, err_one = one.walkspeed(time_speed)
    np.save("walking_one.npy", walking_one)
    np.save('err_one')
else:
    #walking_one, err
    pass

print "CHUNK 2"
path = "/home/lab/demo/demo_1/data_split/2/20170723_213610_N1_trackedobjects.hdf5"
hdf5_filename =  "/home/lab/demo/demo_1/data_split/2/20170723_213610_N1_trackedobjects.hdf5"
max_frame = None
frame_rate = None
position = []
beginning_offsets = []
ending_offsets = []
position = []
pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
two = Analysis(pd, dataset, beginning_offsets, ending_offsets, max_frame, frame_rate, hdf5_filename = hdf5_filename, path = path)

time_position = two.time_position()
interp_position_total = two.interpolate_and_align(time_position)
occupancy_original_two = two.occupancy(interp_position_total)
occupancy_percent_two = two.occupancy_percent(occupancy_original_two)
time_speed = two.time_speed()
walking_two, err_two = two.walkspeed(time_speed)
np.save("walking_two.npy", walking_two)

print 'CHUNK 3'
path = "/home/lab/demo/demo_1/data_split/3/20170724_084250_N1_trackedobjects.hdf5"
hdf5_filename =  "/home/lab/demo/demo_1/data_split/3/20170724_084250_N1_trackedobjects.hdf5"
max_frame = None
frame_rate = None
position = []
beginning_offsets = []
ending_offsets = []
position = []
pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
three = Analysis(pd, dataset, beginning_offsets, ending_offsets, max_frame, frame_rate, hdf5_filename = hdf5_filename, path = path)

time_position = three.time_position()
interp_position_total = three.interpolate_and_align(time_position)
occupancy_original_three = three.occupancy(interp_position_total)
occupancy_percent_three = three.occupancy_percent(occupancy_original_three)
time_speed = three.time_speed()
walking_three, err_three = three.walkspeed(time_speed)
np.save("walking_three.npy", walking_three)

total_occupancy = np.concatenate((occupancy_original_one, occupancy_original_two, occupancy_original_three))
total_walk = np.concatenate((walking_two, walking_two, walking_three))
total_occupancypercent = np.concatenate((occupancy_percent_one, occupancy_percent_two, occupancy_percent_three))
total_err = np.concatenate((err_one, err_two, err_three))

f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=False)
lf_edge= 0
rt_edge= 600
for i in range (int((len(occupancy_original_one)+len(occupancy_original_two)+ len(occupancy_original_three))/9000)+1):
        lf_edge= lf_edge+ 8400
        rt_edge= rt_edge+ 8400
        ax1.axvspan(lf_edge, rt_edge, alpha=0.5, color= 'yellow')
lf_edge= 0
rt_edge= 600
for i in range (int((len(occupancy_percent_one)+len(occupancy_percent_two) + len(occupancy_percent_three))/9000)+1):
        lf_edge= lf_edge+ 8400
        rt_edge= rt_edge+ 8400
        ax2.axvspan(lf_edge, rt_edge, alpha=0.5, color= 'yellow')
lf_edge= 0
rt_edge= 600
for i in range (int((len(walking_one)+len(walking_two) +len(walking_three))/9000)+1):
        lf_edge= lf_edge+ 8400
        rt_edge= rt_edge+ 8400
        ax3.axvspan(lf_edge, rt_edge, alpha=0.5, color= 'yellow')
ax1.plot(total_occupancy)
ax1.set_title('OCCUPANCY')
ax2.plot(total_occupancypercent)
ax2.set_title("PERCENT OCCUPANCY")
ax3.plot(total_walk)
ax3.set_title('WALKING SPEED')
x = []
for i in range(len(total_walk)):
    x.append(i)
y = total_walk

ipdb.set_trace()

ax3.errorbar(x,y, yerr= total_err)
# Fine-tune figure; make subplots close to each other and hide x ticks for
# all but bottom plot.
f.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)

plt.show()
