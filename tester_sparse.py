from __future__ import division
import numpy as np
import multi_tracker_analysis as mta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy import sparse
from scipy import stats
import seaborn as sns
import os

import ipdb

class Analysis:
    def __init__(self, pd, dataset, hdf5_filename, path, sampling_interval):
        self.hdf5_filename = hdf5_filename
        self.path = path
        self.pd, config = mta.read_hdf5_file_to_pandas.load_and_preprocess_data(self.hdf5_filename)
        self.pd.keys()
        self.dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
        self.dataset.load_keys()
        self.sampling_interval = sampling_interval

    def time_position(self):
        """
        Returns a list of numpy arrays of shape (2, num_samples),
        where num_samples can vary across trajectories.
        """
        time_position = []
        min_time_len = None
        for i in range (len(np.unique(self.pd.objid))):
            trajec = self.dataset.trajec(self.dataset.keys[i])
            times = trajec.time_epoch_secs + trajec.time_epoch_nsecs / 1e9
            time_pos = np.vstack([times, trajec.position_x])
            time_position.append(time_pos)
            if min_time_len == None:
                min_time_len = len(times)
            elif min_time_len > len(times):
                min_time_len = len(times)
        print min_time_len
        return time_position

    def interpolate_and_align(self, time_position):
        """
        Parameters:
        time_position (list): contains numpy arrays of (2, num_samples)
                              where dimension 0 is time and 1 is x position
        """

        num_trajecs = len(time_position)
        rows = []
        cols = []
        data = []
        missing_trajecs = 0
        def closest_sampletime(t):
            return round(float(t) / self.sampling_interval) * self.sampling_interval

        interp_position = []
        interp_time = []
        for i in range(len(time_position)):
        # TODO last indices were swapped here before? is this wrong?
        # did i screw something else up?
            print self.hdf5_filename
            original_times = time_position[i][0,:]
            original_x_positions = time_position[i][1,:]
            # TODO maybe consider using ceil / floor in calculating closest sample time
            # and getting rid of the fill_value='extrapolate' argument
            if (len(original_times)>1 and len(original_x_positions)>1):
                f = interpolate.interp1d(original_times, original_x_positions, fill_value='extrapolate')
                new_start = closest_sampletime(original_times[0])
                new_stop = closest_sampletime(original_times[-1])
            # TODO + 1?
                new_num_samples = int(round((new_stop - new_start) / self.sampling_interval))
                ipdb.set_trace()
                new_times = np.linspace(new_start, new_stop, new_num_samples)
                new_x_positions = f(new_times)
            if (len(new_times)> 0 and len(new_x_positions) > 0):
                interp_time.append(new_times)
                interp_position.append(new_x_positions)
                data.extend(new_x_positions)
                row =np.ones(len(new_times))*i
                rows.extend(row)
            else:
                print "THROWING OUT STUFF BC NOT ENOUGH TIME & POSITION VALUES"
                missing_trajecs += 1



        print "END OF FOR LOOP"
        '''
        print 'original time range (w/ min + max):', original_times.min(), original_times.max()
        print 'original_start, original_stop, new_start, new_stop, new_num_samples'
        print original_times[0], original_times[-1], new_start, new_stop, new_num_samples
        print 'range of new_times:', new_times[0], new_times[-1]
        '''
        # TODO check all of these make sense together
        #old_min_time = min([np.min(a[0,:]) for a in time_position])
        #old_max_time = max([np.max(a[0,:]) for a in time_position])

        min_time = min([np.min(a) for a in interp_time])
        max_time = max([np.max(a) for a in interp_time])

        print max_time - min_time
        total_num_samples = int(round((max_time - min_time) / self.sampling_interval))
        max_end_idx = None
        for i in range(num_trajecs - missing_trajecs):
            #aligned_interp = np.empty(total_num_samples) * np.nan
            start_idx = int(round((interp_time[i][0] - min_time) / self.sampling_interval))
            end_idx = start_idx + len(interp_time[i])
            cols.extend(np.arange(start_idx, end_idx))
            if max_end_idx==None:
                max_end_idx = end_idx
            elif max_end_idx< end_idx:
                max_end_idx = end_idx
        mtx = sparse.coo_matrix((data, (rows, cols)), shape = (len(time_position), max_end_idx))
        print max_end_idx*self.sampling_interval
        final_aligned = mtx.tocsc()



        return final_aligned

        '''
        # TODO check all of these make sense together
        old_min_time = min([np.min(a[0,:]) for a in time_position])
        old_max_time = max([np.max(a[0,:]) for a in time_position])
        min_time = min([np.min(a) for a in interp_time])
        max_time = max([np.max(a) for a in interp_time])

        begin_offset = []
        end_offset = []
        print "end of for loop"
        total_num_samples = int(round((max_time - min_time) / self.sampling_interval))
        #final_aligned = []
        print "DID IT GET HERE???"
        final_aligned = np.empty([num_trajecs, total_num_samples])

        print "GET HERE?"
        for i in range(num_trajecs):
            print i/num_trajecs
            #aligned_interp = np.empty(total_num_samples) * np.nan
            start_idx = int(round((interp_time[i][0] - min_time) / self.sampling_interval))
            end_idx = start_idx + len(interp_time[i])
            #aligned_interp[start_idx:end_idx] = interp_position[i]
            final_aligned[i,start_idx:end_idx] = interp_position[i]
            #final_aligned.append(aligned_interp)

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

        final_aligned = np.array(final_aligned)
        print final_aligned.shape
        return final_aligned
        '''
    def occupancy(self, interp_position_total):
        plt.figure(figsize = (40,6))
        num_of_trajectories = []
        num_frames_shape = interp_position_total.get_shape()
        num_frames = num_frames_shape[1]
        b = []
        flies = 0
        lf = 0
        rt = 0
        for i in range (num_frames):
            column = interp_position_total[:, i]
            flies = (column>0.0).sum()
            num_of_trajectories.append(flies)
            lf = (column >920.0).sum()
            rt = flies-lf
            b.append([lf,rt])
            # unnecessary
            rt =0
            lf =0
            flies = 0
        b = np.array(b)
        print b.shape
        plt.plot(b[:, 0], color = 'blue')
        plt.plot(b[:, 1], color = 'red')
        #ax = sns.tsplot(data=b[:,0])
        #ax = sns.tsplot(data=b[:,1])
        plt.ylabel('flies')
        plt.xlabel('frames')
        lf_edge= 0
        rt_edge= (1/self.sampling_interval)*60*2
        for i in range (46):
                lf_edge= lf_edge + (1/self.sampling_interval)*60*30
                rt_edge= rt_edge + (1/self.sampling_interval)*60*30
                plt.axvspan(lf_edge, rt_edge, alpha=0.5, color= 'yellow')
        os.chdir('/home/lab/analysis_graphs')
        os.getcwd()
        #os.mkdir(self.hdf5_filename[18:36])
        plt.savefig('/home/lab/analysis_graphs/' + self.hdf5_filename[18: 36] + '/occupancy.png')
        return b

    def occupancy_percent(self, occupancy_original):
        plt.figure(figsize = (40,6))
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
        lf_edge= 0
        rt_edge= (1/self.sampling_interval)*60*2
        for i in range (46):
                lf_edge= lf_edge + (1/self.sampling_interval)*60*30
                rt_edge= rt_edge + (1/self.sampling_interval)*60*30
                plt.axvspan(lf_edge, rt_edge, alpha=0.5, color= 'yellow')

        plt.savefig('/home/lab/analysis_graphs/' + self.hdf5_filename[18:36] + '/occupancy_percent.png')
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
            time_speedy = np.vstack([times, trajec.speed])
            time_speed.append(time_speedy)
        return time_speed

    def walkspeed(self, time_speed):
        """
        Parameters:
        time_position (list): contains numpy arrays of (2, num_samples)
                              where dimension 0 is time and 1 is x position
        """
        speed = []

        num_trajecs = len(time_speed)
        rows = []
        cols = []
        data = []
        missing_trajectories = 0
        def closest_sampletime(t):
            return round(float(t) / self.sampling_interval) * self.sampling_interval

        interp_speed = []
        interp_time = []
        for i in range(len(time_speed)):
        # TODO last indices were swapped here before? is this wrong?
        # did i screw something else up?
            original_times = time_speed[i][0,:]
            original_speeds = time_speed[i][1,:]
            # TODO maybe consider using ceil / floor in calculating closest sample time
            # and getting rid of the fill_value='extrapolate' argument
            if (len(original_times)>1 and len(original_speeds)>1):
                f = interpolate.interp1d(original_times, original_speeds, fill_value='extrapolate')
                new_start = closest_sampletime(original_times[0])
                new_stop = closest_sampletime(original_times[-1])
                # TODO + 1?
                new_num_samples = int(round((new_stop - new_start) / self.sampling_interval))
                ipdb.set_trace()
                new_times = np.linspace(new_start, new_stop, new_num_samples)
                new_speeds = f(new_times)
            if (len(new_times)>0 and len(new_speeds>0)):
                interp_time.append(new_times)
                interp_speed.append(new_speeds)
                data.extend(new_speeds)
                row =np.ones(len(new_times))*i
                rows.extend(row)
            else:
                print "THROWING OUT STUFF BC NOT ENOUGH TIME & POSITION VALUES"
                missing_trajectories += 1



        print "END OF FOR LOOP"
        '''
        print 'original time range (w/ min + max):', original_times.min(), original_times.max()
        print 'original_start, original_stop, new_start, new_stop, new_num_samples'
        print original_times[0], original_times[-1], new_start, new_stop, new_num_samples
        print 'range of new_times:', new_times[0], new_times[-1]
        '''
        # TODO check all of these make sense together
        #old_min_time = min([np.min(a[0,:]) for a in time_position])
        #old_max_time = max([np.max(a[0,:]) for a in time_position])
        min_time = min([np.min(a) for a in interp_time])
        max_time = max([np.max(a) for a in interp_time])

        print max_time - min_time
        total_num_samples = int(round((max_time - min_time) / self.sampling_interval))
        max_end_idx = None
        for i in range(num_trajecs - missing_trajectories):
            #aligned_interp = np.empty(total_num_samples) * np.nan
            start_idx = int(round((interp_time[i][0] - min_time) / self.sampling_interval))
            end_idx = start_idx + len(interp_time[i])
            cols.extend(np.arange(start_idx, end_idx))
            if max_end_idx==None:
                max_end_idx = end_idx
            elif max_end_idx< end_idx:
                max_end_idx = end_idx
        mtx = sparse.coo_matrix((data, (rows, cols)), shape = (len(time_speed), max_end_idx))
        print max_end_idx*self.sampling_interval
        final_aligned = mtx.tocsc()

        avg = []
        num_frames_shape = final_aligned.get_shape()
        num_frames = num_frames_shape[1]
        plt.figure(figsize = (40,6))
        for i in range (num_frames):
            column = final_aligned[:, i]
            flies = (column>0).sum()
            total_speed = column.sum()
            avg_speed = total_speed/flies
            avg.append(avg_speed)
        plt.plot(avg)
        avg = np.array(avg)

        #ax = sns.tsplot(data=avg)

        std_err = np.empty(final_aligned.shape[1])
        for i in range(final_aligned.shape[1]):
            std_err[i] = stats.sem(final_aligned[:, i].data, nan_policy='omit')
        std_err = np.array(std_err)
        x = np.arange(len(avg))
        y = avg
        plt.errorbar(x,y, yerr= std_err, color = 'y')
        plt.xlabel('time')
        plt.ylabel('percent occupancy')
        lf_edge= 0
        rt_edge= (1/self.sampling_interval)*60*2
        for i in range (46):
                lf_edge= lf_edge + (1/self.sampling_interval)*60*30
                rt_edge= rt_edge + (1/self.sampling_interval)*60*30
                plt.axvspan(lf_edge, rt_edge, alpha=0.5, color= 'yellow')
        plt.savefig('/home/lab/analysis_graphs/' + self.hdf5_filename[18: 36] + '/walking_speed.png')
        return final_aligned

    def num_trajecs_histogram(self, interp_position_total):
        #plot differently
        #seaborn error thing
        num_of_trajectories = []
        num_frames_shape = interp_position_total.get_shape()
        num_frames = num_frames_shape[1]
        flies = 0
        for i in range (num_frames):
            column = interp_position_total[:, i]
            flies = (column>0.0).sum()
            num_of_trajectories.append(flies)
        plt.hist(num_of_trajectories, 60*5/self.sampling_interval, normed = 0)
        plt.xlabel('number of trajectories')
        plt.ylabel('frequency')
        plt.show()
