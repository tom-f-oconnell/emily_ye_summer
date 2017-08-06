from analysis_split import Analysis
import multi_tracker_analysis as mta
import matplotlib.pyplot as plt
import numpy as np

total_occupancy = []
total_occupancypercent = []
total_walk = []
occupancy_original = []

path = "/home/lab/demo/demo_1/data_split/1/20170723_160250_N1_trackedobjects.hdf5"
hdf5_filename =  "/home/lab/demo/demo_1/data_split/1/20170723_160250_N1_trackedobjects.hdf5"
max_frame = None
frame_rate = None
position = []
beginning_offsets = []
ending_offsets = []
pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
one = Analysis(pd, dataset, beginning_offsets, ending_offsets, max_frame, frame_rate, hdf5_filename = hdf5_filename, path = path, position = position)


one_occupancy = one.occupancy()
one_walk = one.walkspeed()
one_occupancypercent = one.occupancy_percent(occupancy_original= one_occupancy)


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
two = Analysis(pd, dataset, beginning_offsets, ending_offsets, max_frame, frame_rate, hdf5_filename = hdf5_filename, path = path, position = position)


two_occupancy = two.occupancy()
two_walk = two.walkspeed()
two_occupancypercent = two.occupancy_percent(occupancy_original = two_occupancy)

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
three = Analysis(pd, dataset, beginning_offsets, ending_offsets, max_frame, frame_rate, hdf5_filename = hdf5_filename, path = path, position = position)


three_occupancy = three.occupancy()
three_walk = three.walkspeed()
three_occupancypercent = three.occupancy_percent(occupancy_original = three_occupancy)

total_occupancy = np.concatenate((one_occupancy, two_occupancy, three_occupancy))
total_walk = np.concatenate((one_walk, two_walk, three_walk))
total_occupancypercent = np.concatenate((one_occupancypercent, two_occupancypercent, three_occupancypercent))
f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=False)
ax1.plot(total_occupancy)
ax1.set_title('TITLE GOES HERE')
ax2.plot(total_occupancypercent)
ax3.plot(total_walk)
# Fine-tune figure; make subplots close to each other and hide x ticks for
# all but bottom plot.
f.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)

plt.show()
