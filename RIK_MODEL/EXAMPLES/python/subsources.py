# Script to plot 3 subplots in a row

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import pylab as p
import numpy as np
import sys
import os 
from collections import OrderedDict 
# from matplotlib.patches import Polygon
import matplotlib.patches as patches

from matplotlib.collections import PatchCollection
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.cm import ScalarMappable
import scipy.interpolate
from matplotlib import ticker

from   matplotlib.colors   import LogNorm
from   matplotlib.image    import NonUniformImage
from   matplotlib.ticker   import LogFormatter
import matplotlib.colors   as mcolors
from   sys                 import exit

import matplotlib.lines as mlines
from matplotlib.patches import Circle


# Colormap

def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)



###

def readfile (NSR, filename):

	xgrid = np.zeros((NSR))
	ygrid = np.zeros((NSR))
	slip  = np.zeros((NSR))


	f = open (filename, 'r')
	print 'Reading the file', filename
	print '...'

	for i in np.arange(NSR):
		string   = f.readline()
		degerler = [float(j) for j in string.split()]

		xgrid[i] = degerler[0]
		ygrid[i] = degerler[1]
		slip [i] = degerler[2]


	return xgrid, ygrid, slip

###

 
def plotsubsources(x,y,radius,kaydet,figname,nucx,nucy):

	# Making a colormap
	c    = mcolors.ColorConverter().to_rgb
	cc = ['#ffffff', '#dfe6ff', '#a5b5da', '#516b8e', '#c5ce9b',
	      '#fcab6c', '#f50000']

	#cc1 = np.logspace(np.log10(0.25),np.log10(0.95),6)
	cc1 = np.linspace(0,1,6)

	cmap = make_colormap([c(cc[0]), c(cc[1]), cc1[0],
	                      c(cc[1]), c(cc[2]), cc1[1],
	                      c(cc[2]), c(cc[3]), cc1[2],
	                      c(cc[3]), c(cc[4]), cc1[3],
	                      c(cc[4]), c(cc[5]), cc1[4],
	                      c(cc[5]), c(cc[6]), cc1[5],
	                      c(cc[6])])


	# Figure parameters
	sns.set_style('whitegrid')
	fig = p.figure(figsize=(18,10))

	p.subplots_adjust(hspace=0.35)

	# #
	ax = fig.add_subplot(111)

	ax.set_xlabel('Along strike [km]', fontsize=17)
	ax.set_ylabel('Along up-dip [km]', fontsize=17)

	ax.set_xlim([0,15.0])
	ax.set_ylim([-0.2,10.0])


	i = 0
	for xx,yy in zip(x,y):
	    circ = Circle((xx,yy),radius[i], fill=False, lw=1)
	    ax.add_patch(circ)	
	    
	    i = i+1


	topname  = 'Total number of subsources = '+ '%d' % Nsub
	plt.title(topname+'\n', fontsize=20)

	ax.plot(nucx,nucy, marker='o', color='red',markersize=20)

	plt.xticks(fontsize=17)
	plt.yticks(fontsize=17)


	if kaydet:
		fig.savefig(figname, dpi=300)
	else:
		plt.show()

###




### PROGRAM 

# Input data
Nsub = 3724


filename = '../NAPA_ROCHER/subsources.dat'
x, y, radius = readfile (Nsub, filename)



plotsubsources(x,y,radius,True,'15000points_Napa_rocher_circles.png',12.5,0.0)





print '*** Done ***'
#