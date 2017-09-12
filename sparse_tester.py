from sparse import Analysis
import multi_tracker_analysis as mta
import matplotlib.pyplot as plt
import numpy as np
import ipdb

def graphing(hdf5_filename):
    interp_position_total = []
    path = hdf5_filename
    sampling_interval = 0.5
    pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(hdf5_filename)
    dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
    willitwork = Analysis(pd, dataset, hdf5_filename = hdf5_filename, path = path, sampling_interval = sampling_interval)
    time_position, rt_most_pixel, lf_most_pixel = willitwork.time_position()
    interp_position_total = willitwork.interpolate_and_align(time_position)
    #occupancy_original = willitwork.occupancy(interp_position_total, rt_most_pixel, lf_most_pixel)
    occupancy_roi = willitwork.roi_occupancy(interp_position_total, rt_most_pixel, lf_most_pixel)
    change = willitwork.change_in_occupancy(occupancy_roi)

    pref_idx = willitwork.preference_index(occupancy_roi)
    c = willitwork.occupancy_percent(occupancy_roi)
    time_speed = willitwork.time_speed()
    # TODO catch this earlier in the future
    try:
        walking_final_aligned, avg = willitwork.walkspeed(time_speed)
    except ValueError:
        # code throws this now if there are no flies
        return
    walking_err = willitwork.walkspeed_error(walking_final_aligned, avg)
    trajectories = willitwork.num_trajecs(interp_position_total)

"""
hdf5_files = ['/mnt/tb/retracked/20170809_143458_N1/20170809_143458_N1_trackedobjects.hdf5',\
'/mnt/tb/retracked/20170806_140932_N1/20170806_140932_N1_trackedobjects.hdf5',\
'/mnt/tb/retracked/20170803_161438_N1/20170803_161438_N1_trackedobjects.hdf5',\
'/mnt/tb/retracked/20170802_150031_N1/20170802_150031_N1_trackedobjects.hdf5',\
'/mnt/tb/retracked/20170729_112342_N1/20170729_112342_N1_trackedobjects.hdf5',\
'/mnt/tb/retracked/20170724_171509_N1/20170724_171509_N1_trackedobjects.hdf5',\
'/mnt/tb/retracked/20170722_151805_N1/20170722_151805_N1_trackedobjects.hdf5',\
'/mnt/tb/retracked/20170713_150841_N1/20170713_150841_N1_trackedobjects.hdf5',\
'/mnt/tb/retracked/20170727_153410_N1/20170727_153410_N1_trackedobjects.hdf5',\
'/mnt/tb/retracked/20170805_150712_N1/20170805_150712_N1_trackedobjects.hdf5',\
'/mnt/tb/retracked/20170804_145530_N1/20170804_145530_N1_trackedobjects.hdf5']
"""
hdf5_files = ['/home/lab/catkin/src/multi_tracker/examples/sample_data/20160412_134708_N1_trackedobjects.hdf5']


for i in (hdf5_files):
    print i
    itwillwork = graphing(i)
