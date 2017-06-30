# ---------------------------------------------------------------------
#  Filename: convert_extended_MOMENT.py
#  Purpose : prepare input files (moment) for extended-source model of 
#  SEM3D code of Ecole Centrale Paris
#  Author  : Elif ORAL
#  Email   : elif.oral@centralesupelec.fr 
#
# ---------------------------------------------------------------------

# Librairies necessaires #
import matplotlib.pyplot as plt
import numpy 			 as np
import h5py
from   INTFORTRAN 		 import trapezoid
from   elfolib           import read_moment_rate_RIK, vecteurs

#####################################################################
### PROGRAMME ###													#
#####################################################################
# Ce programme cree les fichiers d'entree necessaires pour le 		#
# modele de source etendue a employer dans le code SEM3D a partir du#
# modele de RIK (Gallovic, 2016) 									#
#																	#
# This script prepares input files for SEM3D extended source block  #
# Input data is taken from RIK model of Gallovic (2016) for this    #
# example.															#
#     																#
#####################################################################


# Plot moment vs time graph for all point sources on the fault plan 
plot_figure     = True
# Figure name
figurename = 'Moment_vs_time_Napa_bedrock_model.png'

# Filename for SEM3D coordinates of all point sources on the fault plan
coord_file_name = 'Coordinates_Niigata_Depth14km.dat'

# Filename of coordinate data of all point sources on the fault plan
RIK_slipfile = 'RIK_model_data/slipdistribution.dat'

# Filename of moment-time history of all point sources on the fault plan
mrfile  	 = 'RIK_model_data/ELIF_MomentRate.dat'


# Number of point on fault plan (along strike)
NL = 150
# Number of point on fault plan (along dip)
NW = 100

# Strike, dip and rake angles
strike = 155.0
dip    = 82.0
rake   = -172.0

# Coordinates of hypocenter in RIK model  (in meters)
RIK_hypocenter = np.array([0.0, 12.5, 10.0]) * 1e3  # Y_RIK, X_RIK, DEPTH (DOWNWARD POSITIVE)

# Coordinates of hypocenter in SEM model  (in meters)
SEM_hypocenter = np.array([0.0,  0.0,-10.0]) * 1e3  # EST,   NORD,  UPWARD

# Input files for SEM3D
# Fault data
kinefile_out  = h5py.File('Napa_kine.hdf5', 'w')
# Moment data
slipfile_out  = h5py.File('Napa_moment.hdf5','w')
#
# Moment vs time history
# Time duration
T_total = 21.25
# Time step
dt      = 0.025



#####################################################################

kinefile_out.attrs['Ns']     = NL 
kinefile_out.attrs['Nd']     = NW


# Les angles en radian
aS    = np.pi/180.0* strike
aR    = np.pi/180.0* rake
aD    = np.pi/180.0* dip



print 'Rotation matrix: '
# Ce matrice utilise [E,N,Z] et
# sort aussi [E,N,Z]
#
MatMesh = np.zeros((3,3))
MatMesh[0,0] = -np.cos(aS)* np.cos(aD)
MatMesh[0,1] = np.sin(aS)
MatMesh[1,0] = np.sin(aS)* np.cos(aD)
MatMesh[1,1] = np.cos(aS)
MatMesh[2,2] =  -1


for i in np.arange(3):
	for j in np.arange(3):
		if abs(MatMesh[i,j]) < 1e-15:
			MatMesh[i,j] = 0.0

print MatMesh[0,:]
print MatMesh[1,:]
print MatMesh[2,:]



# Vecteurs du normale et du slip
vecteurs(aD,aS,aR,kinefile_out)



# Coordonnees des points dans le repere SEM3D
xgrid = kinefile_out.create_dataset('x', (NL, NW), chunks=(1, 1))
ygrid = kinefile_out.create_dataset('y', (NL, NW), chunks=(1, 1))
depth = kinefile_out.create_dataset('z', (NL, NW), chunks=(1, 1))

xgrid[:,:] = 0.0
ygrid[:,:] = 0.0
depth[:,:] = 0.0




# x,y koordinatlari (RIK) - metre
print '*********'
print 'Hypocenter of RIK model:'
print RIK_hypocenter[0], RIK_hypocenter[1], RIK_hypocenter[2]

print 'Hypocenter of SEM model:'
print SEM_hypocenter[0], SEM_hypocenter[1], SEM_hypocenter[2]




# RIK model - Les coordonnees de x et y
RIK_xcoord   = np.genfromtxt(RIK_slipfile, usecols=1)  # Y_RIK
RIK_ycoord   = np.genfromtxt(RIK_slipfile, usecols=0)  # X_RIK


print 'Total point number in fault plane: ', NL*NW
n = 0
for j in np.arange(NW):
	for i in np.arange(NL):

		# en kilometres
		if (NL*NW > 1):
			xgrid[i,j] = RIK_xcoord[n]
			ygrid[i,j] = RIK_ycoord[n]
		else:
			print 'ATTENTION: CHANGE THIS FOR MODELS WITH MORE THAN 1 POINT'
			xgrid[i,j] = RIK_xcoord
			ygrid[i,j] = RIK_ycoord

		depth[i,j] = (RIK_hypocenter[2]/1e3+ np.sin(aD)* (RIK_hypocenter[0]/1e3-xgrid[i,j]))


		# en metres
		xgrid[i,j] = xgrid[i,j]* 1e3
		ygrid[i,j] = ygrid[i,j]* 1e3
		depth[i,j] = depth[i,j]* 1e3

		n = n+1



# ATTENTION: Once rotate edip sonra farkina bakiyorum
fark  = np.dot(MatMesh,RIK_hypocenter) 	
fark  = (SEM_hypocenter-fark)

# print 'fark', fark
print


# Opening file to save SEM3D coordinates of grid points
coord_file = open (coord_file_name, 'w')

# Burada rotation yapiyorum
n = 0 
for j in np.arange(NW):
	for i in np.arange(NL):
		n = n+ 1

		print 'Point ',n,		
		print

		# print 'COORDONNEES SELON LE REPERE DE RIK'
		# Rotasyon uyguluyorum
		coord = np.array([xgrid[i,j], ygrid[i,j], depth[i,j]])
		dum   = np.dot(MatMesh,coord)
	
		# print 'COORDONNEES SELON LE REPERE DE SEM - ROTATION'
		# Aradaki farki ekliyorum; boylelikle translate ediyor
		xgrid[i,j] = dum[0]+ fark[0]
		ygrid[i,j] = dum[1]+ fark[1]
		depth[i,j] = dum[2]+ fark[2]

		# print 'COORDONNEES SELON LE REPERE DE SEM - ROTATION + TRANSLATION'

		# Writing out the cordinates
		coord_file.write('%s \t %s \t %s \t %s \n' %  (str(n), str(xgrid[i,j]), str(ygrid[i,j]), str(depth[i,j])))
		print '***'
#
coord_file.close()





# ### ### ### ### ###
# # MOMENT vs TIME


NT      = T_total/dt
MR      = read_moment_rate_RIK (mrfile,(NL,NW,NT))
time    = np.linspace(0.0, T_total, NT)


# Attribuer les proprietes temporelles
kinefile_out.attrs['Nt']     = NT
kinefile_out.attrs['dt']     = time[1]-time[0]

# Creer le matrice hdf5 pour le temps
slipfile_out.create_dataset('time', data=time)

# Creer le matrice hdf5 pour le moment
Moment = slipfile_out.create_dataset('moment', (NL, NW, NT), chunks=(1, 1, NT))


# Integration pour calculer le moment
print 'INTEGRATION'
n = 0
for i in range(0, NL):
	for j in range(0, NW):
		n = n+ 1
		Moment[i,j,:] = trapezoid(NT, dt, MR[i,j,:])
		print NT, dt, '  --->  Point ', n
#



if plot_figure:
	### PLOTTING ###
	fig = plt.figure(figsize=(12,10))
	ax  = fig.add_subplot(111)

	# ax.set_xlim([0,1])

	# #
	n = 0
	for i in range(0, NL):
		for j in range(0, NW):
			n = n+1
			ax.plot(time, Moment[i,j,:], label='Point '+str(n),color='Gray')
	# #

	ax.set_xlabel('Time [s]'    ,fontsize=20)
	ax.set_ylabel('Moment [Nm]' ,fontsize=20)
	# ax.legend()
	plt.show()
	fig.savefig(figurename,dpi=300)
#


print ''
print 'Min and max values on East   direction:   ',   xgrid[:,:].min(), xgrid[i,j].max()
print 'Min and max values on North  direction:   ',   ygrid[:,:].min(), ygrid[i,j].max()
print 'Min and max values on Upward direction:   ',   depth[:,:].min(), depth[i,j].max()



# Fermeture des fichiers hdf5
kinefile_out.close()
slipfile_out.close()
#