from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ipdb

sampling_interval = 1
#plt.plot(b[:, 0], color = 'blue')
#plt.plot(b[:, 1], color = 'green')
#ax = sns.tsplot(data=b)
#ax = sns.tsplot(data=b[:,1], err_style='ci_bars')
plt.ylabel('flies')
plt.xlabel('frames')
lf_edge= 0
rt_edge= (1/sampling_interval)*60*2
#ax = sns.tsplot(data=b[:, 0])
#ax = sns.tsplot(data=b[:, 1])
times = []
for i in range (46):
        lf_edge= lf_edge + (1/sampling_interval)*60*30
        times.append(lf_edge)
        rt_edge= rt_edge + (1/sampling_interval)*60*30
        plt.axvspan(lf_edge, rt_edge, alpha=0.5, color= 'yellow')

times = times[0: -1: 2]
points = np.arange(23)
points = points +1
plt.xticks(times, points)
plt.savefig('/home/lab/analysis_graphs/aserajesr.png')

