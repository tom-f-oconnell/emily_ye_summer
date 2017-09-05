import matplotlib.pyplot as plt
import numpy as np
plt.figure(figsize = (40,6))
a = [1,2,3,4,2,5,2,7,4,12,3,45,73,45,3, 34]
b = [1,2,3,7,4,2,4,6,5,77,7,5,6,7,5,32]
plt.plot(a,b)
plt.savefig('/home/lab/analysis_graphs/size.png')
