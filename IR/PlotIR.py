import numpy as np
import matplotlib.pyplot as plt
from GetChunkFromTextFile import GetChunkFromTextFile

# modes = np.genfromtxt('Lizardite.modes.txt', skip_header=1)
modes = GetChunkFromTextFile('Lizardite.dynmat.out', '#', '\n\n', skip_header=1)
scaling=0.01
exper = np.genfromtxt('Lizardite__R060006-1__Infrared__Infrared_Data_Processed__841.txt', skip_header=10, skip_footer=1, delimiter=',')
print(exper)

cm = np.linspace(0, 4000, 4001)

def Gaussian(x, A, x0, sigma):
    return A*np.exp(-(x-x0)**2 / (2*sigma**2))

y = np.zeros(len(cm))
for i in range(modes.shape[0]):
    y += Gaussian(cm, modes[i,3]*scaling, modes[i,1], 30)

plt.plot(cm, y, label='DFT')
plt.plot(exper[:,0], exper[:,1], label='RRUFF')
plt.legend()
plt.savefig('IRSpectrum.png', dpi=300)
plt.show()

