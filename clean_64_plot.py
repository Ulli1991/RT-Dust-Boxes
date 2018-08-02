import h5py as h5py
import numpy as np
import gadget
import math
import matplotlib.pyplot as plt
import random
from astropy.io import fits
from matplotlib.colors import LogNorm

path1 = '/panfs/ds08/hopkins/uli/RDI_dust_spectrum/HR/s.k05N4.HR/output_dust_grid_gas_grid'

path = path1

biases = []
data = []
steps = np.arange(0,200.1,1).astype('int')

cyls = []
ncyls = 32
dust_norm = 0.011983339715927964*2.


bins = np.linspace(0, 1, 32)
cbins = (bins[1:] + bins[:-1]) / 2

xm, ym = np.meshgrid(cbins, cbins)

# steps=[0]
plt.figure()

for s in steps:
    print s
    dust=gadget.readsnap(path, s, 3)
    gas=gadget.readsnap(path, s, 0)
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
    weight_dust = dust_mass**(2./3)
    weight_gas=gas_mass
    #
    h_dust=np.histogram2d(x_dust,y_dust,bins=bins, weights=weight_dust)[0]
    h_gas=np.histogram2d(x_gas, y_gas, bins=bins, weights=weight_gas)[0]
    plt.clf()
    plt.subplot(221)
    plt.imshow(np.log10(h_gas), vmin=np.log10(0.0008), vmax=np.log10(0.0013))
    plt.title('%.1d'%(0.1*s))
    plt.axis('off')
    plt.subplot(222)
    plt.imshow(np.log10(h_dust), vmin=np.log10(0.007), vmax=np.log10(0.02))
    circle = plt.Circle((15, 15), 0.1*32, color='r', fill=False)
    plt.gca().add_artist(circle)
    plt.axis('off')
    temp = []
    for xc in [0.2, 0.4, 0.6, 0.8]:
        for yc in [0.2, 0.4, 0.6, 0.8]:
            filt = ((xm-xc)**2 + (ym-yc)**2)<0.1**2
            temp.append(-np.log(1.0-np.mean(1.0 - np.exp( - h_dust[filt] / dust_norm))))
    cyls.append(temp)
    #
    mean_dust_density=np.mean(h_dust)
    mean_gas_density=np.mean(h_gas)
    h_dust = (h_dust-mean_dust_density)/mean_dust_density
    h_gas = (h_gas-mean_gas_density)/mean_gas_density
    print s
    print np.mean(h_dust)
    print np.mean(h_gas)
    print 'bias=', np.median(h_gas/h_dust)
    biases.append(np.median(h_gas/h_dust))
    data.append([h_gas, h_dust])
    plt.subplot(223)
    plt.imshow(h_gas/h_dust, vmin=-3, vmax=3, cmap='bwr')
    plt.axis('off')
    plt.subplot(224)
    plt.hist2d(h_gas.flatten(), h_dust.flatten(), bins=np.linspace(-1,1,32), norm=LogNorm())
    plt.xlabel('gas overdensity')
    plt.ylabel('dust overdensity')
    plt.savefig('/home/kaurov/%03d.png'%s)

# command to convert frames into video
# ffmpeg -framerate 10 -i %03d.png -vcodec libx264 video.mp4

x = np.linspace(0,20,201)
plt.subplot(211)
plt.plot(x, np.array(cyls), alpha=0.5)
m = np.array(cyls).mean(1)
s = np.array(cyls).std(1)
plt.plot(x, m, 'k')
plt.fill_between(x, m-s, m+s, alpha=0.5)
plt.ylabel(r'$\tau$')
plt.subplot(212)
plt.plot(x, biases)
plt.ylabel('$b$')
plt.xlabel('$t$')
plt.show()
