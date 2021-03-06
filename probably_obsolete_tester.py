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


    def time_position(self):
        """
        Returns a list of numpy arrays of shape (2, num_samples),
        where num_samples can vary across trajectories.
        """
        time_position = []
        for i in range (len(np.unique(self.pd.objid))):
            trajec = self.dataset.trajec(self.dataset.keys[i])
            times = trajec.time_epoch_secs + trajec.time_epoch_nsecs / 1e9
            time_pos = np.vstack([times, trajec.position_x])
            time_position.append(time_pos)
        return time_position

    def interpolate_and_align(self, time_position):
        """
        Parameters:
        time_position (list): contains numpy arrays of (2, num_samples)
                              where dimension 0 is time and 1 is x position
        """
        sampling_rate = 0.2
        num_trajecs = len(time_position)
        
        def closest_sampletime(t):
            return round(float(t) / sampling_rate) * sampling_rate
        
        interp_position = []
        interp_time = []
        for i in range(len(time_position)):
            # TODO last indices were swapped here before? is this wrong? 
            # did i screw something else up?
            original_times = time_position[i][0,:]
            original_x_positions = time_position[i][1,:]
            # TODO maybe consider using ceil / floor in calculating closest sample time
            # and getting rid of the fill_value='extrapolate' argument
            f = interpolate.interp1d(original_times, original_x_positions, fill_value='extrapolate')
            new_start = closest_sampletime(original_times[0])
            new_stop = closest_sampletime(original_times[-1])
            # TODO + 1?
            new_num_samples = int(round((new_stop - new_start) / sampling_rate))
            new_times = np.linspace(new_start, new_stop, new_num_samples)
            '''
            print 'original time range (w/ min + max):', original_times.min(), original_times.max()
            print 'original_start, original_stop, new_start, new_stop, new_num_samples'
            print original_times[0], original_times[-1], new_start, new_stop, new_num_samples
            print 'range of new_times:', new_times[0], new_times[-1]
            '''
            new_x_positions = f(new_times)
            interp_time.append(new_times)
            interp_position.append(new_x_positions)
        
        # TODO check all of these make sense together
        old_min_time = min([np.min(a[0,:]) for a in time_position])
        old_max_time = max([np.max(a[0,:]) for a in time_position])
        min_time = min([np.min(a) for a in interp_time])
        max_time = max([np.max(a) for a in interp_time])

        begin_offset = []
        end_offset = []
        for i in range(num_trajecs):
            interp_section = interp_time[i]
            begin = int(((interp_section[0] - min_time)/sampling_rate))
            begin_offset.append(begin)
            end = int(((max_time - interp_section[-1])/sampling_rate))
            end_offset.append(end)

        final_aligned = []
        total_num_samples = int(round((max_time - min_time) / sampling_rate))
        
        for i in range(num_trajecs):
            aligned_interp = np.empty(total_num_samples) * np.nan
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

    def occupancy(self, interp_position_total):
        num_frames = position.shape[1]
        b = []
        flies = 0
        lf = 0
        rt = 0
        for i in range (num_frames):
            flies = np.sum(position[:, i]>0)
            lf = np.sum(position[:, int(i)]>920)
            rt = flies-lf
            b.append([lf,rt])
            rt =0
            lf =0
        b = np.array(b)
        plt.plot(b[:, 0], color = 'blue')
        plt.plot(b[:, 1], color = 'red')
        plt.ylabel('flies')
        plt.xlabel('frames')
        lf_edge= 0
        rt_edge= self.frame_rate*2*60
        for i in range ((self.max_frame/(self.frame_rate*30*60))+1):
                lf_edge= lf_edge+ self.frame_rate*1680
                rt_edge= rt_edge+ self.frame_rate*1680
                plt.axvspan(lf_edge, rt_edge, alpha=0.5, color= 'yellow')
        plt.show()
        return b

    def occupancy_percent(self, occupancy_original):
        occ = []
        print occupancy_original.shape
        for i in range(occupancy_original.shape[0]):
            sum_flies = float(occupancy_original[i, 0]+ occupancy_original[i, 1])
            if sum_flies !=0:
                left_percent = occupancy_original[i, 0]/sum_flies
                right_percent = occupancy_original[i, 1]/sum_flies
                occ.append([left_percent, right_percent])
            else:
                occ.append([0, 0])
        plt.plot(occ)
        plt.xlabel('time')
        plt.ylabel('percent occupancy')
        lf_edge= 0+ 6.666666666*self.frame_rate
        rt_edge= self.frame_rate*2*60 + 6.666666666*self.frame_rate
        for i in range ((self.max_frame/(self.frame_rate*30*60))+1):
                lf_edge= lf_edge+ self.frame_rate*1680
                rt_edge= rt_edge+ self.frame_rate*1680
                plt.axvspan(lf_edge, rt_edge, alpha=0.5, color= 'yellow')
        plt.show()
        return occ

    def time_speed(self):
        """
        Returns a list of numpy arrays of shape (2, num_samples),
        where num_samples can vary across trajectories.
        """
        time_speed = []
        for i in range (len(np.unique(self.pd.objid))):
            trajec = self.dataset.trajec(self.dataset.keys[i])
            times = trajec.time_epoch_secs + trajec.time_epoch_nsecs / 1e9
            time_speedy = np.vstack([times, trajec.speed)
            time_speed.append(time_speedy)
        return time_speed

    def walkspeed(self, time_speed):
        speed = []
        sampling_rate = 0.2
        num_trajecs = len(time_speed)
        
        def closest_sampletime(t):
            return round(float(t) / sampling_rate) * sampling_rate
        
        interp_position = []
        interp_time = []
        for i in range(len(time_position)):
            # TODO last indices were swapped here before? is this wrong? 
            # did i screw something else up?
            original_times = time_position[i][0,:]
            original_x_positions = time_position[i][1,:]
            # TODO maybe consider using ceil / floor in calculating closest sample time
            # and getting rid of the fill_value='extrapolate' argument
            f = interpolate.interp1d(original_times, original_x_positions, fill_value='extrapolate')
            new_start = closest_sampletime(original_times[0])
            new_stop = closest_sampletime(original_times[-1])
            # TODO + 1?
            new_num_samples = int(round((new_stop - new_start) / sampling_rate))
            new_times = np.linspace(new_start, new_stop, new_num_samples)
            '''
            print 'original time range (w/ min + max):', original_times.min(), original_times.max()
            print 'original_start, original_stop, new_start, new_stop, new_num_samples'
            print original_times[0], original_times[-1], new_start, new_stop, new_num_samples
            print 'range of new_times:', new_times[0], new_times[-1]
            '''
            new_x_positions = f(new_times)
            interp_time.append(new_times)
            interp_position.append(new_x_positions)
        
        # TODO check all of these make sense together
        old_min_time = min([np.min(a[0,:]) for a in time_speed])
        old_max_time = max([np.max(a[0,:]) for a in time_speed])
        min_time = min([np.min(a) for a in interp_time])
        max_time = max([np.max(a) for a in interp_time])

        begin_offset = []
        end_offset = []
        for i in range(num_trajecs):
            interp_section = interp_time[i]
            begin = int(((interp_section[0] - min_time)/sampling_rate))
            begin_offset.append(begin)
            end = int(((max_time - interp_section[-1])/sampling_rate))
            end_offset.append(end)

        final_aligned = []
        total_num_samples = int(round((max_time - min_time) / sampling_rate))
        
        for i in range(num_trajecs):
            aligned_interp = np.empty(total_num_samples) * np.nan
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
        return final_aligned


