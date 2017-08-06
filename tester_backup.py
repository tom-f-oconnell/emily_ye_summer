from __future__ import division
import numpy as np
import multi_tracker_analysis as mta
import matplotlib.pyplot as plt
from scipy import interpolate

import ipdb

class Analysis:
    def __init__(self, pd, dataset, beginning_offsets, ending_offsets, min_frame, max_frame, frame_rate, hdf5_filename, path, position):
        self.beginning_offsets = []
        self.ending_offsets = []
        self.frame_rate = frame_rate
        self.max_frame = max_frame
        self.min_frame = min_frame
        self.hdf5_filename = hdf5_filename
        self.path = path
        self.pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(self.hdf5_filename)
        self.pd.keys()
        self.dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
        self.dataset.load_keys()
        self.position = []
        max_frame = None
        for i in range (len(np.unique(self.pd.objid))):
            trajec = self.dataset.trajec(self.dataset.keys[i])
            num_of_positions = trajec.position_x.shape
#accurate to hundredths digit (but still not perfect :( )
            first_timept = trajec.time_epoch_secs[0] + trajec.time_epoch_nsecs[0]/1000000000
            last_timept = trajec.time_epoch_secs[-1]+ trajec.time_epoch_nsecs[int(trajec.position_x.shape[0])-1]/1000000000
            if (last_timept - first_timept)!=0:
    	        self.frame_rate = num_of_positions/(last_timept - first_timept)
            if self.min_frame == None:
	            self.min_frame = trajec.frames[0]
            elif trajec.frames[0] < min_frame:
	            self.min_frame = trajec.frames[0]
            if self.max_frame == None:
	            self.max_frame = trajec.frames[int(trajec.position_x.shape[0])-1]
            elif trajec.frames[int(trajec.position_x.shape[0])-1] > self.max_frame:
       	        self.max_frame = trajec.frames[-1]

    def align(self):
        position = []
        for i in range (len(np.unique(self.pd.objid))):
            trajec = self.dataset.trajec(self.dataset.keys[i])
            first_frame = trajec.frames[0]
            beginning_offset = first_frame - self.min_frame
            self.beginning_offsets.append(beginning_offset)
            last_frame = trajec.frames[-1]
            ending_offset = self.max_frame - last_frame
            self.ending_offsets.append(ending_offset)
            aligned_position = []
            for ii in range (beginning_offset):
                aligned_position.append(0)
            aligned_position.extend(trajec.position_x)
            for ii in range (ending_offset):
                aligned_position.append(0)
            position.append(aligned_position)
        position = np.asarray(position)
        return position 

    def position_time(self):
        time_position = []
        for i in range (len(np.unique(self.pd.objid))):
            tim_pos = []
            trajec = self.dataset.trajec(self.dataset.keys[i])
            for ii in range (trajec.position_x.shape[0]-1):
                    tim_pos.append([(trajec.time_epoch_secs[ii]+trajec.time_epoch_nsecs[ii]/1000000000), trajec.position_x[ii]])
            time_position.append(tim_pos)
        time_position = np.array(time_position)
        return time_position

    def interpolate_and_align(self, time_position):
        sampling_rate = .01
        interp_position = []
        interp_time = []
        min_time = None
        max_time = None
        begin_offset = []
        end_offset = []
        # TODO dont have array of lists
        for i in range (time_position.shape[0]):
            x_y = time_position[i]
            x_y = np.array(x_y)
            x = x_y[:, 0]
            y = x_y[:, 1]
            f = interpolate.interp1d(x, y)
            #ipdb.set_trace()
            xnew = np.linspace(round(x[0], 2)+ sampling_rate, round(x[-1], 2) - sampling_rate, \
                (((round(x[-1], 2) + sampling_rate) - (round(x[0], 2) - sampling_rate) )/sampling_rate)+1)
            ynew = f(xnew)
            interp_time.append(xnew)
            interp_position.append(ynew)
        interp_position = np.array(interp_position)
        interp_time = np.array(interp_time)
        
        for i in range(interp_time.shape[0]):
            interp_section = interp_time[i]
            if min_time == None:
                min_time = interp_section[0]
            elif min_time > interp_section[0]:
                min_time = interp_section[0]
            if max_time == None:
                max_time = interp_section[-1]
            elif max_time < interp_section[-1]:
                max_time = interp_section[-1]

        for i in range(interp_time.shape[0]):
            interp_section = interp_time[i]
            begin = int(((interp_section[0] - min_time)/sampling_rate))
            begin_offset.append(begin)
            end = int(((max_time - interp_section[-1])/sampling_rate))
            end_offset.append(end)

        final_aligned = []
        total_num_samples = int(round((max_time - min_time) / sampling_rate))
        for i in range(interp_time.shape[0]):
            aligned_interp = np.zeros(total_num_samples)
            start_idx = int(round((interp_time[i][0] - min_time) / sampling_rate))
            end_idx = start_idx + len(interp_time[i])
            aligned_interp[start_idx:end_idx] = interp_position[i]
            final_aligned.append(aligned_interp)
        '''
        for i in range(interp_time.shape[0]):
            aligned_interp = []
            interp_section = interp_position[i]
            for ii in range(begin_offset[i]):
                aligned_interp.append(0)
            aligned_interp.append(interp_section)
            for ii in range(end_offset[i]):
                aligned_interp.append(0)
            final_aligned.append(aligned_interp)
            print len(aligned_interp)
        '''
        final_aligned = np.array(final_aligned)
        print final_aligned.shape
        return final_aligned

