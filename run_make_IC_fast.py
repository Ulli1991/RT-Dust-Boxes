import make_IC_box

#def makeIC_box(DIMS=3, N_1D=256, Ngrains_Ngas=1,
        #fname='dustywind_3d_H1_N256.hdf5', Lbox=1., rho_desired=1.):

make_IC_box.makeIC_box(DIMS = 3, # number of particles across box x-axis
		    N_1D = 64, # number of dimensions
		        Ngrains_Ngas= 4, # vertical height of box (in code units)
<<<<<<< Updated upstream
			    fname = '64_N4.hdf5', # number of dust particles, relative to gas
			        Lbox=1., # output filename
				    rho_desired=1.,
					   mode_dust='wn',
					   mode_gas='grid')
=======
			    fname = '064_N4_wn_dust_wn_gas.hdf5', # number of dust particles, relative to gas
			        Lbox=1., # output filename
				    rho_desired=1.,
					mode_dust='wn', 
					     mode_gas='wn')
>>>>>>> Stashed changes
