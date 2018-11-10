import numpy as np

import matplotlib.pyplot as plt

def main():
   lx=512
   lz=512
   xi=15.0
   eps=20.0
   kappa=0.5
   fct=1 #1 Gaussian, 2 exponential
   psdf=np.zeros((lx,lz),dtype=np.complex128)
   np.random.seed(43)
   if fct==1:
      rand=gauss(lx,lz,xi,eps)
      label="Gaussian random field"
   if fct==2:
      rand=exponential(lx,lz,xi,eps)
      label="Exponential random field"

   im=plt.imshow(rand, cmap=plt.cm.jet)
   plt.colorbar(im)
   plt.title(label)
   plt.show()


def gauss(lx,lz,xi,eps):
   psdf=np.zeros((lx,lz),dtype=np.complex128)
   for i in range(0,lx/2):
      for j in range(0,lz/2):
         kr2=(i*2*np.pi/lx)**2+(j*2*np.pi/lz)**2
         psdfi=eps**2*np.pi*(xi)**2*np.exp(-kr2*(xi)**2/4)
         random=2*np.pi*(np.random.rand()-0.5)
         psdf[i,j]=np.sqrt(psdfi)*np.exp(1.j*random)
         psdf[i,lz-j-1]=-np.conjugate(np.sqrt(psdfi)*np.exp(1.j*random))
         psdf[lx-i-1,j]=-np.conjugate(np.sqrt(psdfi)*np.exp(1.j*random))
   rand=np.real((np.fft.ifft2(psdf)))
   return rand

def exponential(lx,lz,xi,eps):
   psdf=np.zeros((lx,lz),dtype=np.complex128)
   for i in range(0,lx/2):
      for j in range(0,lz/2):
         kr2=(i*2*np.pi/lx)**2+(j*2*np.pi/lz)**2
         psdfi=eps**2*np.pi*(xi)**2/(1.+kr2*xi**2)**1.5
         random=2*np.pi*(np.random.rand()-0.5)
         psdf[i,j]=np.sqrt(psdfi)*np.exp(1.j*random)
         psdf[i,lz-j-1]=-np.conjugate(np.sqrt(psdfi)*np.exp(1.j*random))
         psdf[lx-i-1,j]=-np.conjugate(np.sqrt(psdfi)*np.exp(1.j*random))
   rand=np.real((np.fft.ifft2(psdf)))
   return rand

    
if __name__=='__main__':
    main()
