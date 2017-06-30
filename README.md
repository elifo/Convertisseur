Extended-source modeling in SEM3D starting from Ruiz's Integral Kinematic source model


We model near source effects using the spectral element method (SEM) including topographical 
effects of the 3D propagation medium. For the kinematic source modeling, the model developed 
by Ruiz et al. (2011) and further modified by Gallovic (2016) is used. This method allows 
taking into account frequency-dependent directivity effects. The asperities have a fractal 
distribution that may follow a given inverted slip distribution. We implement the extended 
fault model into SEM3D code of Ecole Centrale Paris to study 3D wave propagation.

The objective of this manual is to instruct the users how to use extended-source modeling 
in SEM3D code of Ecole Centrale Paris. 

It includes the folders of RIK_MODEL, CONVERTISSEUR and SEM3D for each step of the procedure.
	1) In RIK_model, the kinematic source model is generated for given seismic data. 
	2) In Convertisseur, necessary input files for SEM3D (hdf5 files) are created for simulations
	   of SEM3D code.
	3) In SEM3D, extended-source block is defined (in input.spec file) with created input files.  

For any further information, please contact Elif Oral by
elif.oral@centralesupelec.fr

#
