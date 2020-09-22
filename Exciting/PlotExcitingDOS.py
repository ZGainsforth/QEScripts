import numpy as np
import matplotlib.pyplot as plt
import sys, os

Fermi=np.genfromtxt('EFERMI.OUT')
print(Fermi)
x = np.genfromtxt('TDOS.OUT')
plt.plot(x[:,0]-Fermi, x[:,1])

# GWFermi=np.genfromtxt('EFERMI_GW.OUT')
# print(GWFermi)
# Fermi=0
# g0w0 = np.genfromtxt('TDOS-QP.OUT')
# plt.plot(x[:,0]-Fermi, x[:,1], g0w0[:,0]-Fermi, g0w0[:,1])
# plt.legend(['Ground', 'G0W0'])

plt.savefig('TDOS.png', dpi=300)
# os.system('display TDOS.png')
plt.show()
