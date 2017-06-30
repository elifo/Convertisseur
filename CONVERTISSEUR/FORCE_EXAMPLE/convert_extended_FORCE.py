# ---------------------------------------------------------------------
#  Filename: convert_extended_FORCE.py
#  Purpose : prepare input files (force) for extended-source model of 
#  SEM3D code of Ecole Centrale Paris
#  Author  : Elif ORAL
#  Email   : elif.oral@centralesupelec.fr 
#
# ---------------------------------------------------------------------

# Librairies necessaires #
import matplotlib.pyplot as plt
import numpy 			 as np
import h5py
from   elfolib           import calculer_force_dm


#####################################################################
### PROGRAM ###
#####################################################################
# Ce programme cree les fichiers d'entree necessaires dans le 		#
# modele de source etendue pour les cas ou on insere la source par  #
# Force en temps 													#
#
#####################################################################

# Grille de points
NL = 1
NW = 3

# Creation des fichiers d'entree pour SEM
kinefile_out  = h5py.File('essai_ppts.hdf5', 'w')
slipfile_out  = h5py.File('essai_force.hdf5','w')

# Save the figure into 
figurename = 'Force_3point.png'

# Ppts de temps
T_total = 0.3
dt      = 0.001

# DM parameter tau
tau 	  = np.zeros((NL, NW))

# POINT 1
tau [0,0] = 0.0016666666666666666
# POINT 2
tau [0,1] = 0.03166666666666661
# POINT 3
tau [0,2] = 0.06166666666666658

# Vecteur directionnel (pareil pour tous les points)
Dir = np.array([1.0, 1.0, 0.0])

# Coordonnees des points dans le repere SEM3D
xgrid = kinefile_out.create_dataset('x', (NL, NW), chunks=(1, 1))
ygrid = kinefile_out.create_dataset('y', (NL, NW), chunks=(1, 1))
depth = kinefile_out.create_dataset('z', (NL, NW), chunks=(1, 1))

xgrid[:,:] = 0.0
ygrid[:,:] = 0.0
depth[:,:] = 0.0

# Coordinates of 3 point sources
# POINT 1
xgrid[0,0] = 0.0
ygrid[0,0] = 0.0
depth[0,0] = 0.0

# POINT 2
xgrid[0,1] = 0.0
ygrid[0,1] = 100.0
depth[0,1] = 0.0

# POINT 3
xgrid[0,2] = -150.0
ygrid[0,2] = 0.0
depth[0,2] = 0.0
#


#########################################################################################
ndir  = (Dir[0])**2+ (Dir[1])**2+ (Dir[2])**2
ndir  = ndir** 0.5
Dir   = Dir/ndir 
kinefile_out.attrs['Dir'] = Dir



kinefile_out.attrs['Ns']     = NL 
kinefile_out.attrs['Nd']     = NW


# ### ### ### ### ###
# # FORCE vs TIME
# Calculer et ecrire la force
NT      = T_total/dt
time    = np.linspace(0.0, T_total, NT)

kinefile_out.attrs['dt']     = dt 
kinefile_out.attrs['Nt']     = NT



# Creer le matrice hdf5 pour le temps (data 1d)
slipfile_out.create_dataset('time', data=time)

# Creer le matrice hdf5 pour le moment
Force = slipfile_out.create_dataset('moment', (NL, NW, NT), chunks=(1, 1, NT))

n = 0
for i in range(0, NL):
	for j in range(0, NW):
		n = n+ 1

		Q = 6250.0
		X = 0.7158
		Y = 2.0
		v = 90.0
		a = 3.0
		L = 3.0
		d = 0.6

		DM_point     = calculer_force_dm(Q,X,Y,v,a,d,L,tau[i,j],time)
		Force[i,j,:] = DM_point

		print NT, dt, '  --->  Point ', n
#





### PLOTTING ###
fig = plt.figure(figsize=(12,10))
# sns.set_style('whitegrid')
ax  = fig.add_subplot(111)
# ax.set_xlim([0,1])

# #
n=0
for i in range(0, NL):
	for j in range(0, NW):
		ax.plot(time, Force[i,j,:]/1e3, label='Point '+str(n+1))
		n=n+1
# #

ax.set_xlabel('Time [s]'    ,fontsize=20)
ax.set_ylabel('Force [kN]' ,fontsize=20)
ax.legend()
plt.show()
fig.savefig(figurename,dpi=300)
#





# Fermeture des fichiers hdf5
kinefile_out.close()
slipfile_out.close()
#