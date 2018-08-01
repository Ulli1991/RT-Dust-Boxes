import h5py as h5py
import numpy as np
import gadget
import math
import matplotlib.pyplot as plt
import random
from astropy.io import fits


biases = []
data = []
steps = np.arange(0,200.1,5).astype('int')
for s in steps:
    dust=gadget.readsnap('/panfs/ds08/hopkins/phopkins/data2/RDI_dust_spectrum/HR/s.k05N4.HR/output/', s, 3)
    gas=gadget.readsnap('/panfs/ds08/hopkins/phopkins/data2/RDI_dust_spectrum/HR/s.k05N4.HR/output/', s, 0)
    #dust=gadget.readsnap('/panfs/ds08/hopkins/uli/RDI_dust_spectrum/LR/output_4HR/', 0, 3)
    #
    dust_pos=dust['p']
    grainsize=dust['GrainSize']
    dust_mass=dust['m']
    x_dust=dust_pos[:,0]
    y_dust=dust_pos[:,2]
    #
    gas_pos=gas['p']
    x_gas=gas_pos[:,0]
    y_gas=gas_pos[:,2]
    gas_mass=gas['m']
    #
    bins=np.linspace(0,1,32)
    weight_dust=dust_mass/(1/64. * 1/64.)
    weight_gas=gas_mass/(1/64. * 1/64.)
    #
    h_dust=np.histogram2d(x_dust,y_dust,bins=bins, weights=weight_dust)[0]
    h_gas=np.histogram2d(x_gas, y_gas, bins=bins, weights=weight_gas)[0]
    #
    cbins=(bins[:1]+bins[:-1])/2
    #
    mean_dust_density=np.mean(h_dust)
    mean_gas_density=np.mean(h_gas)
    h_dust = (h_dust-mean_dust_density)/mean_dust_density
    h_gas = (h_gas-mean_gas_density)/mean_gas_density
    print s
    print np.mean(h_dust)
    print np.mean(h_gas)
    print 'bias=', np.mean(h_gas/h_dust)
    biases.append(np.mean(h_gas/h_dust))
    data.append([h_gas, h_dust])


plt.plot(steps, biases)
plt.show()


for i in [-1]:#len(data):
    plt.figure(figsize=(8,8))
    plt.subplot(221)
    plt.imshow(data[i][0])
    plt.axis('off')
    plt.subplot(222)
    plt.imshow(data[i][1])
    plt.axis('off')
    plt.subplot(223)
    plt.imshow(data[i][0]/data[i][1])
    print(np.mean(data[i][0]/data[i][1]), np.median(data[i][0]/data[i][1]))
    plt.axis('off')


plt.show()

biases_med = []
for i in range(len(data)):
    biases_med.append(np.median(data[i][0] / data[i][1]))

plt.plot(steps/10., biases_med)
plt.ylabel('bias = median($\delta_g / \delta_d$)')
plt.xlabel('t')
plt.ylim([-0.05, 0.1])
plt.show()

import h5py as h5py
import numpy as np
import gadget
import math
import matplotlib.pyplot as plt
import random
from astropy.io import fits

bins=np.linspace(0,1,64)
s=120

p = '/panfs/ds08/hopkins/phopkins/data2/RDI_dust_spectrum/HR/s.k05N4.HR/output/'

dust=gadget.readsnap(p, s, 3)
gas=gadget.readsnap(p, s, 0)
#dust=gadget.readsnap('/panfs/ds08/hopkins/uli/RDI_dust_spectrum/LR/output_4HR/', 0, 3)
#
dust_pos=dust['p']
grainsize=dust['GrainSize']
dust_mass=dust['m']
x_dust=dust_pos[:,0]
y_dust=dust_pos[:,2]
#
gas_pos=gas['p']
x_gas=gas_pos[:,0]
y_gas=gas_pos[:,2]
gas_mass=gas['m']

h_dust = np.histogram2d(x_dust, y_dust, bins=bins, )[0]

h_gas = np.histogram2d(x_gas, y_gas, bins=bins,)[0]


plt.imshow(h_gas)
plt.show()


#hdu = fits.PrimaryHDU()
#hdu.data=array
#hdu.writeto('s.sims_200.fits')

#plt.imshow(h)
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

