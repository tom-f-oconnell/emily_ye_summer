from analysis import Analysis
import multi_tracker_analysis as mta


path = "/home/lab/demo/demo_1/data_split/2/20170723_213610_N1_trackedobjects.hdf5"
hdf5_filename =  "/home/lab/demo/demo_1/data_split/2/20170723_213610_N1_trackedobjects.hdf5"
max_frame = None
frame_rate = None
min_frame = None
position = []
beginning_offsets = []
ending_offsets = []
pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
willitwork = Analysis(pd, dataset, beginning_offsets, ending_offsets, min_frame, max_frame, frame_rate, hdf5_filename = hdf5_filename, path = path, position = position)
position = willitwork.align()
occupancy_original = willitwork.occupancy(position)
b = willitwork.walkspeed()
c = willitwork.occupancy_percent(occupancy_original)
