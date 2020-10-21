import matplotlib.pyplot as plt
import numpy as np
V2 = np.genfromtxt('V2+_D4h_2p_XAS_iso.spec', skip_header=5)
V3 = np.genfromtxt('V3+_D4h_2p_XAS_iso.spec', skip_header=5)

np.savetxt('V2+LedgeM1_Olivine_Crispy.txt', np.stack((V2[:,0]+517.0, V2[:,2]), axis=1))
np.savetxt('V3+LedgeM1_Olivine_Crispy.txt', np.stack((V3[:,0]+517.0, V3[:,2]), axis=1))

plt.plot(V2[:,0], V2[:,2])
plt.plot(V3[:,0], V3[:,2])
plt.legend(['V2+', 'V3+'])
plt.show()

