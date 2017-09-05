from sparse import Analysis
import multi_tracker_analysis as mta
import matplotlib.pyplot as plt
import numpy as np

def graphing(hdf5_filename):
    interp_position_total = []
    path = hdf5_filename
    sampling_interval = 1
    pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
    dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
    willitwork = Analysis(pd, dataset, hdf5_filename = hdf5_filename, path = path, sampling_interval = sampling_interval)
    time_position = willitwork.time_position()
    interp_position_total = willitwork.interpolate_and_align(time_position)
    #interp_position_total = np.load('interp_position_total.npy')
    #interp_position_total_filename = "interp_position_total.npy"
    #np.save(interp_position_total_filename, interp_position_total)
    occupancy_original = willitwork.occupancy(interp_position_total)
    #occupancy_original_filename = "occupancy_original.npy"
    #np.save(occupancy_original_filename, occupancy_original)
    c = willitwork.occupancy_percent(occupancy_original)
    #occupancy_percent_filename = "occupancy_percent.npy"
    #np.save(occupancy_percent_filename, c)
    time_speed = willitwork.time_speed()
    walking = willitwork.walkspeed(time_speed)
    #walking_filename = "walking.npy"
    #np.save(walking_filename, walking)

hdf5_files = ['/mnt/tb/retracked/20170727_153403_N1/20170727_153403_N1_trackedobjects.hdf5',\
 '/mnt/tb/retracked/20170724_171509_N1/20170724_171509_N1_trackedobjects.hdf5',\
 '/mnt/tb/retracked/20170722_151805_N1/20170722_151805_N1_trackedobjects.hdf5',\
 '/mnt/tb/retracked/20170718_161013_N1/20170718_161013_N1_trackedobjects.hdf5',\
 '/mnt/tb/retracked/20170713_150841_N1/20170713_150841_N1_trackedobjects.hdf5']


for i in (hdf5_files):
    itwillwork = graphing(i)
