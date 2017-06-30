# Script to plot 3 subplots in a row

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import pylab as p
import numpy as np
import sys
import os 
from collections import OrderedDict 
from matplotlib.patches import Polygon
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

 
def plotslip(nrows,ncols,slip,kaydet,figname,nucx,nucy):

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

	vmin = slip.min()
	vmax = slip.max()

	print vmin,vmax
	# print xgrid.min(), xgrid.max(), ygrid.min(), ygrid.max()


	grid 		 = slip.reshape((nrows, ncols))


	im = plt.imshow(grid, extent=(0.0,15.0,0.0,10.0), interpolation='bilinear', cmap=cmap, origin='lower')

	formatter = LogFormatter(10, labelOnlyBase=False)
	cb        = fig.colorbar(im, shrink=0.5, aspect=10, pad=0.01, ticks=np.arange(vmin,vmax,1), format=formatter)
	cb.set_label('Slip [m]', labelpad=20, y=0.5, rotation=90, fontsize=17)

	p.setp(cb.ax.yaxis.get_ticklabels(), fontsize=16)


	ax.plot(nucx,nucy, marker='o', color='black',markersize=20)

	plt.xticks(fontsize=17)
	plt.yticks(fontsize=17)


	topname  = 'Max slip = '+ '% .4f' % max(slip)
	plt.title(topname+'\n', fontsize=20)


	if kaydet:
		fig.savefig(figname, dpi=300)
	else:
		plt.show()

###




### PROGRAM 

# Input data
Lgrid   = 150
Wgrid   = 100
NSR 	= Wgrid*Lgrid


filename = '../NAPA_ROCHER/slipdistribution.dat'
x, y, slip = readfile (NSR, filename)

# Attention a l'ordre de W et L #
plotslip (Wgrid,Lgrid,slip,True,'15000points_Napa_rocher_slip.png',12.5,0.0)

print '*** Done ***'
#