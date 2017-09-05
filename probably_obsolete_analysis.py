import numpy as np
import multi_tracker_analysis as mta
import matplotlib.pyplot as plt

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
        np.unique(pd.objid)
        self.pd.keys()
        self.dataset = mta.read_hdf5_file_to_pandas.Dataset(pd, path = path)
        self.dataset.load_keys()
        self.position = []
        min_frame = None
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

    def interpolate(self, time_position):
        interp_position_x = []
        interp_position_y = []
        interp_position_total = []
        for i in range (time_position.shape[0]):
            x_y = time_position[i]
            x_y = np.array(x_y)
            x = x_y[:, 0]
            y = x_y[:, 1]
            f = interpolate.interp1d(x, y)
            xnew = np.arange(x[0],x[-1], .1)
            ynew = f(xnew)
            interp_position_x.append(xnew)
            interp_position_y.append(ynew)
        interp_position_total.append([interp_position_x, interp_position_y])
        return interp_position_total

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

    def occupancy_indiv(self):
        indiv_position = []
        for i in range (len(np.unique(self.pd.objid))):
    	    trajec = self.dataset.trajec(self.dataset.keys[i])
    	    aligned_position = []
    	    for ii in range (self.beginning_offsets[i]):
    		    aligned_position.append(None)
    	    aligned_position.extend(trajec.position_x)
    	    for ii in range (self.ending_offsets[i]):
    		    aligned_position.append(None)
    	    indiv_position.append(aligned_position)
        indiv_position = np.asarray(indiv_position)
        print indiv_position.shape
        plt.plot(indiv_position)
        plt.xlabel('time')
        plt.ylabel('x-position')
        lf_edge= 0
        rt_edge= self.frame_rate*2*60
        for i in range ((self.max_frame/(self.frame_rate*30*60))+1):
                lf_edge= lf_edge+ self.frame_rate*1680
                rt_edge= rt_edge+ self.frame_rate*1680
                plt.axvspan(lf_edge, rt_edge, alpha=0.5, color= 'yellow')
        plt.show()
        return self.position

    def walkspeed(self):
        speed = []
        for i in range (len(np.unique(self.pd.objid))):
            aligned_speed = []
            trajec = self.dataset.trajec(self.dataset.keys[i])
            for ii in range (self.beginning_offsets[i]):
        		aligned_speed.append(0.0000000000000000000000001)
            aligned_speed.extend(trajec.speed)
            for ii in range (self.ending_offsets[i]):
        		aligned_speed.append(0.0000000000000000000000001)
            speed.append(aligned_speed)
        speed = np.array(speed)
        speedy = None
        walking_speed = []
        for i in range(speed.shape[1]):
        	flies = float(np.sum(speed[:, i]!=0.0000000000000000000000001))
        	if flies != None:
        		speedy = sum(speed[:, i])/flies
        		walking_speed.append(speedy)
        	else:
        		walking_speed.append(None)
        plt.plot(walking_speed)
        plt.xlabel('time')
        plt.ylabel('average walking speed')
        lf_edge= 0+ 6.666666666*self.frame_rate
        rt_edge= self.frame_rate*2*60+ 6.666666666*self.frame_rate
        for i in range ((self.max_frame/(self.frame_rate*30*60))+1):
                lf_edge= lf_edge+ self.frame_rate*1680
                rt_edge= rt_edge+ self.frame_rate*1680
                plt.axvspan(lf_edge, rt_edge, alpha=0.5, color= 'yellow')
        plt.show()
        return walking_speed
