import h5py as h5py
import numpy as np
import gadget
import math
import matplotlib.pyplot as plt
import random
from astropy.io import fits
from scipy.stats import gaussian_kde


dust=gadget.readsnap('/panfs/ds08/hopkins/phopkins/data2/RDI_dust_spectrum/HR/s.k05N4.HR/output/', 50, 3)
gas=gadget.readsnap('/panfs/ds08/hopkins/phopkins/data2/RDI_dust_spectrum/HR/s.k05N4.HR/output/', 50, 0)
#dust=gadget.readsnap('/panfs/ds08/hopkins/uli/RDI_dust_spectrum/LR/output_4HR/', 0, 3)

dust_pos=dust['p']
grainsize=dust['GrainSize']
dust_mass=dust['m']
x_dust=dust_pos[:,0]
y_dust=dust_pos[:,2]

gas_pos=gas['p']
x_gas=gas_pos[:,0]
y_gas=gas_pos[:,2]
gas_mass=gas['m']

min_grain=np.min(grainsize)
max_grain=np.max(grainsize)

values=np.percentile(grainsize, 25)
#id1=np.where(np.logical_and(grainsize >= 1*max_grain/5., grainsize <= 2*max_grain/5.))
id1=np.where(grainsize <= values)
x_dust1=x_dust[id1]
y_dust1=y_dust[id1]

x_gas1=x_gas
y_gas1=y_gas

bins=np.linspace(0,1,128)
weight_dust=dust_mass/(1/128. * 1/128.)
weight_dust1=weight_dust[id1]
weight_gas=gas_mass/(1/128. * 1/128.)

cbins=(bins[:1]+bins[:-1])/2

h_dust=np.histogram2d(x_dust1,y_dust1,bins=bins, weights=weight_dust1)[0]
h_gas=np.histogram2d(x_gas1, y_gas1, bins=bins, weights=weight_gas)[0]

mean_dust_density=np.mean(h_dust)
mean_gas_density=np.mean(h_gas)
h_dust=(h_dust-mean_dust_density)/mean_dust_density
h_gas=(h_gas-mean_gas_density)/mean_gas_density

print h_dust
print h_gas

#xy = np.vstack([h_gas,h_dust])
#z = gaussian_kde(xy)(xy)

#idx = z.argsort()
#h_gas, h_dust, z = h_gas[idx], h_dust[idx], z[idx]

#fig, ax = plt.subplots()
#ax.scatter(h_gas, h_dust, c=z, s=100, edgecolor='')
#plt.show()

plt.plot(h_gas, h_dust, 'b.')
plt.show()

  #print np.median(h_dust)
  #print np.median(h_gas)

 # print 'bias =', np.median(h_gas/h_dust) 

#  bias_out[i] = np.median(h_gas/h_dust)

#hdu = fits.PrimaryHDU()
#hdu.data=bias_out
#hdu.writeto('s.sims_bias_xy_2_over_5_grains.fits')

#plt.imshow(h_gas)
#plt.show()

#case of constant grainszes
#print 0.01*sum(grainsize2*grainsize2)/sum(mass2)*(mass2[0]/(4./3.*0.15**3))

#case of non constant grainsizes
#print 0.01*sum(grainsize2*grainsize2*mass2/(4./3.*grainsize2**3)) /sum(mass2)

#grainsize/=np.max(grainsize)
#print np.max(grainsize)
#physical_mass=4./3. * np.pi * 2 * (grainsize*0.0001)**3
#print physical_mass
#print mass

#N=mass/physical_mass

#print np.mean(N)

#calculates grainsize in microns
#grainsize/=np.max(grainsize)
#grainsize in solar radii
#grainsize*=(1/6.957e14)

#x_dust=pos_dust[:,0]
#y_dust=pos_dust[:,1]
#z_dust=pos_dust[:,2]

#print 'shifting coordinate system done...'

#optical_depth_total=1/np.mean(N) * math.pi*sum(grainsize*grainsize)*0.01/sum(mass)

#print optical_depth_total

