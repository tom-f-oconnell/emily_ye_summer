from tester import Analysis
import multi_tracker_analysis as mta
import matplotlib.pyplot as plt

path = "/home/lab/demo/demo_1/tester/20170722_151805_N1_trackedobjects.hdf5"
hdf5_filename =  "/home/lab/demo/demo_1/tester/20170722_151805_N1_trackedobjects.hdf5"
max_frame = None
frame_rate = None
min_frame = None
position = []
beginning_offsets = []
ending_offsets = []
pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
willitwork = Analysis(pd, dataset, beginning_offsets, ending_offsets, min_frame, max_frame, frame_rate, hdf5_filename = hdf5_filename, path = path, position = position)

time_position = willitwork.time_position()
b = willitwork.interpolate_and_align(time_position)


'''
x = a[:,0]
x.tolist()
y = a[:, 1]
y.tolist()
print len(x)
print len(y)
for i in range(len(x)):
    plt.scatter(x[i], y[i])
plt.show()
'''

