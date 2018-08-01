import h5py as h5py
import numpy as np
import gadget
import math
import matplotlib.pyplot as plt
import random
from astropy.io import fits

star_list=[0.01, 0.02, 0.04, 0.08, 0.1]
time=np.linspace(0,20, 40)


hdulist1 = fits.open('0.04Size_of_Star_clever.fits')
hdu1=hdulist1[0]

hdulist2 = fits.open('0.06Size_of_Star_clever.fits')
hdu2=hdulist2[0]

hdulist3 = fits.open('0.08Size_of_Star_clever.fits')
hdu3=hdulist3[0]

hdulist4 = fits.open('0.1Size_of_Star_clever.fits')
hdu4=hdulist4[0]

hdulist5 = fits.open('0.2Size_of_Star_clever.fits')
hdu5=hdulist5[0]

hdulist6 = fits.open('0.3Size_of_Star_clever.fits')
hdu6=hdulist6[0]

hdulist7 = fits.open('0.4Size_of_Star_clever.fits')
hdu7=hdulist7[0]

optical_depth1=hdu1.data
optical_depth2=hdu2.data
optical_depth3=hdu3.data
optical_depth4=hdu4.data
optical_depth5=hdu5.data
optical_depth6=hdu6.data
optical_depth7=hdu7.data
#np.set_printoptions(threshold='nan')
standard1=np.zeros(200)
standard2=np.zeros(200)
standard3=np.zeros(200)
standard4=np.zeros(200)
standard5=np.zeros(200)
standard6=np.zeros(200)
standard7=np.zeros(200)

print optical_depth1[:,0]

for i in range(0,200, 5):
  #print optical_depth1[:,i]
  standard1[i]=-np.log(np.mean(np.exp(-optical_depth1[:,i])))
  standard2[i]=-np.log(np.mean(np.exp(-optical_depth2[:,i])))
  standard3[i]=-np.log(np.mean(np.exp(-optical_depth3[:,i])))
  standard4[i]=-np.log(np.mean(np.exp(-optical_depth4[:,i])))
  standard5[i]=-np.log(np.mean(np.exp(-optical_depth5[:,i])))
  standard6[i]=-np.log(np.mean(np.exp(-optical_depth6[:,i])))
  standard7[i]=-np.log(np.mean(np.exp(-optical_depth7[:,i])))
  #print standard

id1=np.where(standard1 > 0.0)
id2=np.where(standard2 > 0.0)
id3=np.where(standard3 > 0.0)
id4=np.where(standard4 > 0.0)
id5=np.where(standard5 > 0.0)
id6=np.where(standard6 > 0.0)
id7=np.where(standard7 > 0.0)
standard11=standard1[id1]
standard12=standard2[id2]
standard13=standard3[id3]
standard14=standard4[id4]
standard15=standard5[id5]
standard16=standard6[id6]
standard17=standard7[id7]

#test1=optical_depth1[:,10]
#test2=optical_depth1[:,100]
#test3=optical_depth1[:,150]

#print test1
#print test2
#print test3

#plt.plot(time, standard11, label='0.04 $L_{Box}$')
plt.plot(time, standard12, label='0.06 $L_{Box}$')
plt.plot(time, standard13, label='0.08 $L_{Box}$')
plt.plot(time, standard14, label='0.1 $L_{Box}$')
plt.plot(time, standard15, label='0.2 $L_{Box}$')
#plt.plot(time, standard16, label='0.3 $L_{Box}$')
#plt.plot(time, standard17, label='0.4 $L_{Box}$')
plt.xlabel('time [i.u.]')
plt.ylabel(r'$\tau$')
plt.legend(loc='lower right')
#plt.yscale('log')
plt.show()

#plt.hist([test1, test2, test3], alpha=1.0, bins=1000, cumulative=True, histtype='step')

#print standard1
