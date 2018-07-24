import numpy as np
import h5py as h5py

def makeIC_box(DIMS=3, N_1D=256, Ngrains_Ngas=1,
        fname='dustywind_3d_H1_N256.hdf5', Lbox=1., rho_desired=1., mode_dust='grid', mode_gas='grid'):

    # make a regular 1D grid for particle locations (with N_1D elements and unit
#length)
    x0=np.arange(-0.5,0.5,1./N_1D); x0+=0.5*(0.5-x0[-1]);
    N_1D_dust = np.round((1.*N_1D)*((1.*Ngrains_Ngas)**(1./(1.*DIMS)))).astype('int')
    x0d=np.arange(-0.5,0.5,1./N_1D_dust); x0d+=0.5*(0.5-x0d[-1]);
    x0d+=0.5/(1.*N_1D_dust)+0.5*(1./(1.*N_1D)-1./(1.*N_1D_dust)); x0d[x0d>0.5]-=1.
    
    if DIMS == 3:
        if mode_gas == 'grid':
            xv_g, yv_g, zv_g = np.meshgrid(x0, x0, x0, sparse=False, indexing='xy')
        elif mode_gas == 'wn':
            xv_g = np.random.random(N_1D**3)
            yv_g = np.random.random(N_1D**3)
            zv_g = np.random.random(N_1D**3)
        else:
            raise 'Undefined mode_gas'

        if mode_dust == 'grid':
            xv_d, yv_d, zv_d = np.meshgrid(x0d, x0d, x0d, sparse=False, indexing='xy')
        elif mode_dust == 'wn':
            xv_d = np.random.random(N_1D_dust ** 3)
            yv_d = np.random.random(N_1D_dust ** 3)
            zv_d = np.random.random(N_1D_dust ** 3)
        else:
            raise 'Undefined mode_dust'
    else:
        if mode_gas == 'grid':
            xv_g, yv_g = np.meshgrid(x0, x0, sparse=False, indexing='xy')
        elif mode_gas == 'wn':
            xv_g = np.random.random(N_1D**3)
            yv_g = np.random.random(N_1D**3)
        else:
            raise 'Undefined mode_gas'
        zv_g = 0.0*xv_g

        if mode_dust == 'grid':
            xv_d, yv_d = np.meshgrid(x0d, x0d, sparse=False, indexing='xy')
        elif mode_dust == 'wn':
            xv_d = np.random.random(N_1D_dust ** 3)
            yv_d = np.random.random(N_1D_dust ** 3)
        else:
            raise 'Undefined mode_dust'
        zv_d = 0.0*xv_d

    Ngas = xv_g.size
    Ngrains = xv_d.size
    xv_g = xv_g.flatten()*Lbox; yv_g = yv_g.flatten()*Lbox; zv_g = zv_g.flatten()*Lbox;
    xv_d = xv_d.flatten()*Lbox; yv_d = yv_d.flatten()*Lbox; zv_d = zv_d.flatten()*Lbox;

    m_target_gas = rho_desired/((1.*Ngas)/(Lbox*Lbox*Lbox))

    file = h5py.File(fname,'w') 
    npart = np.array([Ngas,0,0,Ngrains,0,0]) # we have gas and particles we will set
#for type 3 here, zero for all others
    h = file.create_group("Header");
    h.attrs['NumPart_ThisFile'] = npart; # npart set as above - this in general
#should be the same as NumPart_Total, it only differs 
    h.attrs['NumPart_Total'] = npart; # npart set as above
    h.attrs['NumPart_Total_HighWord'] = 0*npart; # this will be set automatically
#in-code (for GIZMO, at least)
    h.attrs['MassTable'] = np.zeros(6); # these can be set if all particles will
#have constant masses for the entire run. however since 
    h.attrs['Time'] = 0.0;  # initial time
    h.attrs['Redshift'] = 0.0; # initial redshift
    h.attrs['BoxSize'] = 1.0; # box size
    h.attrs['NumFilesPerSnapshot'] = 1; # number of files for multi-part snapshots
    h.attrs['Omega0'] = 1.0; # z=0 Omega_matter
    h.attrs['OmegaLambda'] = 0.0; # z=0 Omega_Lambda
    h.attrs['HubbleParam'] = 1.0; # z=0 hubble parameter (small 'h'=H/100 km/s/Mpc)
    h.attrs['Flag_Sfr'] = 0; # flag indicating whether star formation is on or off
    h.attrs['Flag_Cooling'] = 0; # flag indicating whether cooling is on or off
    h.attrs['Flag_StellarAge'] = 0; # flag indicating whether stellar ages are to be
#saved
    h.attrs['Flag_Metals'] = 0; # flag indicating whether metallicity are to be saved
    h.attrs['Flag_Feedback'] = 0; # flag indicating whether some parts of
#springel-hernquist model are active
    h.attrs['Flag_DoublePrecision'] = 0; # flag indicating whether ICs are in
#single/double precision
    h.attrs['Flag_IC_Info'] = 0; # flag indicating extra options for ICs
    
    # start with particle type zero. first (assuming we have any gas particles)
#create the group 
    p = file.create_group("PartType0")
    q=np.zeros((Ngas,3)); q[:,0]=xv_g; q[:,1]=yv_g; q[:,2]=zv_g;
    p.create_dataset("Coordinates",data=q)
    p.create_dataset("Velocities",data=np.zeros((Ngas,3)))
    p.create_dataset("ParticleIDs",data=np.arange(1,Ngas+1))
    p.create_dataset("Masses",data=(0.*xv_g+m_target_gas))
    p.create_dataset("InternalEnergy",data=(0.*xv_g+1.))

    p = file.create_group("PartType3")
    q=np.zeros((Ngrains,3)); q[:,0]=xv_d; q[:,1]=yv_d; q[:,2]=zv_d;
    p.create_dataset("Coordinates",data=q)
    p.create_dataset("Velocities",data=np.zeros((Ngrains,3)))
    p.create_dataset("ParticleIDs",data=np.arange(Ngas+1,Ngrains+Ngas+1))
    p.create_dataset("Masses",data=(0.*xv_d+m_target_gas))
    file.close()
