import numpy as np
import matplotlib.pyplot as plt

# Atom name
AtomName = 'V'
# Input file names.
FileName = 'ld1.dlog'
FileNamePseudo = 'ld1ps.dlog'

AEld = np.genfromtxt('ld1.dlog')
PSld = np.genfromtxt('ld1ps.dlog')

plt.figure()
for i in range(AEld.shape[1]-1):
    plt.plot(AEld[:,0], AEld[:,i+1], label='AE_ld%d'%(i+1))
    plt.plot(PSld[:,0], PSld[:,i+1], '.', label='PS_ld%d'%(i+1))
plt.ylim([-5,5])
plt.ylabel('Log Deriv')
plt.xlabel('a.u.')
plt.legend()
plt.savefig('PlotLogDerivs.png', dpi=300)
plt.show()
