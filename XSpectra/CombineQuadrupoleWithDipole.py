import numpy as np
import matplotlib.pyplot as plt

rootname = 'VMetal-Sum_e_001'
dipole = np.genfromtxt(rootname+'_dipole.txt')
quadrupole = np.genfromtxt(rootname+'_quadrupole.txt')

combined = dipole.copy()
combined[:,1] += quadrupole[:,1]

np.savetxt(rootname+'_dipoleplusquadrupole.txt', combined, header='# eV  sigma')

fig,ax = plt.subplots()
ax.plot(dipole[:,0], dipole[:,1], label='Dipole')
ax.plot(quadrupole[:,0], quadrupole[:,1], label='Quadrupole')
ax.plot(combined[:,0], combined[:,1], label='Dipole + Quadrupole')
plt.legend(loc='upper left')
plt.xlabel('eV')
plt.ylabel('$\sigma$')
plt.savefig(rootname+'_dipoleplusquadrupole.png', dpi=300)
plt.show()

