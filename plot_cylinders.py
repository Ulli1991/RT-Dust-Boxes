import h5py as h5py
import numpy as np
import gadget
import matplotlib.pyplot as plt

#gas=gadget.readsnap('/panfs/ds08/hopkins/phopkins/data2/RDI_dust_spectrum/HR/c.k05N4.HR/output/', 0, 0)
dust=gadget.readsnap('/panfs/ds08/hopkins/phopkins/data2/RDI_dust_spectrum/HR/s.k05N4.HR/output/', 200, 3)


#print dust
#pos_gas=gas['p']
pos_dust=dust['p']
grainsize=dust['GrainSize']

#calculates grainsize in microns
grainsize/=np.max(grainsize)

y_dust=pos_dust[:,1]
bins=np.logspace(np.log10(np.min(grainsize)), np.log10(np.max(grainsize)), 16)
N=81
res = np.zeros([N, len(bins)-1])

#defines unit of grainsize to be in microns
#grainsize*=np.max(grainsize) 

for i in range(9):
  x_dust=pos_dust[:,0]-i*0.1 + 0.1
  for j in range(9):
    z_dust=pos_dust[:,1]-j*0.1 + 0.1

    radius=np.sqrt(x_dust*x_dust + z_dust*z_dust)
    id=np.where(radius <= 0.01)
    grainsize2=grainsize[id]
    H, X = np.histogram(grainsize2, bins = bins)
    print 9*i+j
    print H
    res[9*i+j,:] = H
print ''
print len(X)
print len(res)
print len(H)
print ''
x_centers = np.sqrt((X[1:]+X[:-1])/2.)
print 'x_centers', x_centers
mean_hist = res.mean(0)
std_hist = res.std(0)
print len(x_centers)
print len(mean_hist)
print len(std_hist)

plt.fill_between(x_centers, mean_hist-std_hist, mean_hist+std_hist, alpha = 0.5, facecolor='green')
plt.plot(x_centers, mean_hist, '--g')
plt.xlabel('x_centers')
plt.ylabel('mean_hist')
plt.xscale('log')

    #plt.hist(grainsize2, bins=bins, alpha=0.5, color='blue', histtype='step')
#plt.xlabel('grainsize [$\mu$m]')
#plt.ylabel('Number of grains')
#plt.title('grainsize distribution')
#plt.xscale('log')
#plt.tight_layout()
plt.show()
