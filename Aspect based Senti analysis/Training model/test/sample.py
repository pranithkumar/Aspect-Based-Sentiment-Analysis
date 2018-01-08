x = [3, 0, 1, 2, 2, 0, 1, 3, 3, 3, 4, 1, 4, 3, 0]
y = [1, 0, 4, 3, 2, 1, 4, 0, 3, 0, 4, 2, 3, 3, 1]

import matplotlib.pyplot as plt
import numpy as np

x = np.array(x)
y = np.array(y)

hist, xbins,ybins = np.histogram2d(y,x, bins=range(6))
X,Y = np.meshgrid(xbins[:-1], ybins[:-1])
X = X[hist != 0]; Y = Y[hist != 0]
Z   = hist[hist != 0]


fig, ax = plt.subplots()
ax.scatter(x,y, s=49, alpha=0.4)

for i in range(len(Z)):
    ax.annotate(str(int(Z[i])), xy=(X[i],Y[i]), xytext=(4,0), 
                textcoords="offset points" )

plt.show()