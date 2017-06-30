import matplotlib        
import numpy              as np
import pylab              as p
from   math               import *




def faxis(x,dt):
   n  = len(x)
   df = 1.0 / (n*dt)
   f  = []
   for i in range( n ):
      f.append( df*i )

   return f
#

def fourier(x,dtoutput):
   # Tapering the data

   # FFT
   print 'dt', dtoutput
   s = np.abs( dtoutput * np.fft.fft(x,n=4096) )
   f = faxis(s,dtoutput)
   print 'df', f[1]-f[0]
   print 

   return f[:2049], s[:2049]
#


def ko(y,dx,bexp):
  nx      = len(y)
  fratio  = 10.0**(2.5/bexp)
  ylis    = range( nx )
  ylis[0] = y[0]

  for ix in range( 1,nx ):
     fc  = float(ix)*dx
     fc1 = fc/fratio
     fc2 = fc*fratio
     ix1 = int(fc1/dx)
     ix2 = int(fc2/dx) + 1
     if ix1 <= 0:  ix1 = 1
     if ix2 >= nx: ix2 = nx
     a1 = 0.0
     a2 = 0.0
     for j in range( ix1,ix2 ):
        if j != ix:
           c1 = bexp*log10(float(j)*dx/fc)
           c1 = (sin(c1)/c1)**4
           a2 = a2+c1
           a1 = a1+c1*y[j]
        else:
           a2 = a2+1.0
           a1 = a1+y[ix]
     ylis[ix] = a1 / a2

  for ix in range( nx ):
     y[ix] = ylis[ix]

  return y
#



# Subroutines #

def vecteurs(aD,aS,aR,output):
  ''' Calcul du vecteur normal Vnormal sur le plan de faille, et du vecteur unitaire
  de glissement Vslip dans le repere de reference et les attribuer dans le fichier 
  output de hdf5 '''

  # ELIF
  # En supposant que (puisque l'on multiplie avec MatMesh)
  # x ----> EST
  # y ----> NORD
  # z ----> UP

  Vnormal = np.array([ np.sin(aD)*np.cos(aS),
                      -np.sin(aD)*np.sin(aS),
                       np.cos(aD)])


  Vslip   = np.array([-np.sin(aR)*np.cos(aD)*np.cos(aS) + np.cos(aR)*np.sin(aS),
                      +np.sin(aR)*np.cos(aD)*np.sin(aS) + np.cos(aR)*np.cos(aS),
                      +np.sin(aR)*np.sin(aD)])



  output.attrs['Vnormal'] = Vnormal
  output.attrs['Vslip']   = Vslip
  print "Vector normal to the fault : ", Vnormal
  print "Vector of the slip         : ", Vslip

  ###
  M = np.zeros((3,3))
  for i in np.arange(3):
    for j in np.arange(3):
      M[i,j] = Vnormal[i]*Vslip[j]+Vnormal[j]*Vslip[i]
  print 'Moment matrix of SEM3D code: '
  print M[0,:]
  print M[1,:]
  print M[2,:]  
#

def read_moment_rate_RIK(dosya,dim):
  ''' Lire la vitesse de moment par un fichier dosya et 
  l'assigner a l'array de dimension dim '''

  Mrate = np.zeros((dim[0]*dim[1], dim[2]))

  print 'Reading moment rate of all points...'
  f = open (dosya, 'r')
  # Pour tous les points
  for i in np.arange(dim[0]*dim[1]):
    # Histoire temporelle
    for t in np.arange(dim[2]):
      string = f.readline()

      dagit  = string.rsplit()
      Mrate[i,t] = float(dagit[1])

    f.readline(); f.readline()

  Mratenew = np.reshape(Mrate, dim, order='F')
  return Mratenew
#


# Subroutines #
def calculer_force_dm(Q,X,Y,v,a,d,L,tau,time):

  DM = np.zeros(len(time))
  for t in np.arange(len(time)):
    DM[t] = Q*Y/2*((X)**(((v*(time[t]-tau)-a)**2/d**2))+(X)**(((v*(time[t]-tau)-a-L)**2/d**2)))

  return DM
# 