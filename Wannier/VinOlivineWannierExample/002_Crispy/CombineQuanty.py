import matplotlib.pyplot as plt
import numpy as np
import os, sys

V2M1 = np.genfromtxt(os.path.join('M1', 'V2+LedgeM1_Olivine_Crispy.txt'), skip_header=1)
V2M2 = np.genfromtxt(os.path.join('M2', 'V2+LedgeM2_Olivine_Crispy.txt'), skip_header=1)
V3M1 = np.genfromtxt(os.path.join('M1', 'V3+LedgeM1_Olivine_Crispy.txt'), skip_header=1)
V3M2 = np.genfromtxt(os.path.join('M2', 'V3+LedgeM2_Olivine_Crispy.txt'), skip_header=1)

# Create spectra that are the combined M1 and M2 sites.
V2 = V2M1.copy()
V2[:,1] += V2M2[:,1]
V2[:,1] /= 2

V3 = V3M1.copy()
V3[:,1] += V3M2[:,1]
V3[:,1] /= 2

np.savetxt('V2+Ledge_Olivine_Crispy.txt', V2)
np.savetxt('V3+Ledge_Olivine_Crispy.txt', V3)

plt.plot(V2[:,0], V2[:,1])
plt.plot(V3[:,0], V3[:,1])
plt.legend(['V2+', 'V3+'])
plt.show()

