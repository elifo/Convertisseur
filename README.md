# Extended-source modeling in SEM3D starting from Ruiz's Integral Kinematic source model

* This repository includes the files necessary to prepare a finite source model that can be used as input for the 3D spectral element code of SEM3D (of Ecole Centrale Paris, IPGP and CEA).

* For the kinematic source modeling, we use the RIK model developed by Ruiz et al. (2011) and further modified by Gallovic (2016). The asperities (or seismic sub-sources) have a fractal distribution that can be adjusted to a pre-defined slip inversion data. 

* More details in [Manual](https://github.com/elifo/Convertisseur/blob/master/DOC/manual.pdf)

## Content
* The kinematic source model generation in [RIK_MODEL](https://github.com/elifo/Convertisseur/tree/master/RIK_MODEL)
* Conversion of RIK model outputs for SEM3D format (hdf5 files) in [Convertisseur](https://github.com/elifo/Convertisseur/tree/master/CONVERTISSEUR)
* Example for extended-source definition in SEM3D input file (`input.spec`) in [SEM3D](https://github.com/elifo/Convertisseur/tree/master/SEM3D)


## Related publication
* Oral, E., Gatti, F. and Lopez‐Caballero, F., 2018, June. 3d spectral element modeling of near source effects including kinematic rupture and finite-fault effects.


For any questions, you can write to me; Check out my email address [here](https://elifo.github.io).

