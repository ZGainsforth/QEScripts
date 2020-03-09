import numpy as np
import matplotlib.pyplot as plt
# import pdb; pdb.set_trace()

# Atom name
AtomName = 'F'
# Input file name.
FileName = 'ld1.wfc'
# Orbitals to plot
OrbitalNames = ('1S', '2S', '2P', '2P')
Multiplicity = [2,    2,    3, 2]
# Plot settings
xlim = [0,2]
print(OrbitalNames)
print(f'Total number of electrons to plot is {np.sum(Multiplicity)}')


# Load the Kohn-Sham wavefuncs that were output by ld1
# First just get the column names.
wfc = np.genfromtxt(FileName, names=True)
Names = wfc.dtype.names
# Note that the wavefunctions are from the highest (column 1) to the lowest (last column) in the wfc file.  So we have to read backwards through the columns and compare against the expected inputs.
for i, Name in enumerate(Names[-1:0:-1]):
    if '_' in Name:
        Name, _ = Name.split('_')
    assert Name == OrbitalNames[i], 'Input orbital names does not equal the orbitals in the file.'
# Now get the raw data.
wfc = np.genfromtxt(FileName, skip_header=1)

# The first column is the radius from the nucleus.  The wavefunctions need to be normalized and dr is not constant.  So we need to diff and recenter our r vector.  We will do this with the psi**2 also.
r = wfc[:,0]
dr = np.diff(r)
r = r[:-1] + dr/2
print(np.mean(dr))

# Dictionary to hold each psi**2.
WaveFuncs = {}
# SumFunc is the sum(4*pi*r**2 * psi**2) for all electrons.
SumFunc = np.zeros(r.shape)
# The total number of electrons is the same / 4 pi r**2
SumElectrons = 0

# Per Dal Corso's lecture  on materialscloud, 4 pi r**2 rho(r) = sum(multiplicity * psi(r)**2
# So the wavefunction is being reported in a spherical basis already.

# We will plot the wavefuncs as we compile them.
plt.figure()
for i, Name in enumerate(Names[-1:0:-1]):
    # Get this one wavefunc.
    w = wfc[:,-(i+1)]
    # Recenter it so the axis matches r.
    w = w[:-1] + np.diff(w)/2
    # Square it.
    w = w**2 
    # And get a total electron charge density by multiplying by the multiplicity
    w *= Multiplicity[i]
    # To make it density we have to multiply by the shell area, remember it is already in spherical coords.
    psisq = (w * dr)
    # Save it.
    WaveFuncs[Name] = w
    # Add this to the total charge density.
    SumFunc += w
    SumElectrons += np.sum(psisq)
    # Plot it.
    plt.plot(r, w, label=Name+f'({Multiplicity[i]} e$^-$)')
    print(f'{Name}: {np.sum(w)}')
plt.xlim(xlim)
plt.ylabel('Radial distribution')
plt.xlabel('a.u.')
plt.title(AtomName)
plt.legend()
plt.savefig('PlotIndividualWaveFuncRadialDistribution.png')

# Plot the psi**2 for everything as a radial distribution.
plt.figure()
plt.plot(r, SumFunc)
plt.xlim(xlim)
plt.ylabel('Radial distribution')
plt.xlabel('a.u.')
plt.title(AtomName)
plt.legend(['$4 \pi r^2 \\rho(r)$'])
plt.savefig('PlotTotalRadialDistribution.png')

# Generate the coulomb potential, which is basically just psi**2 / r.
Coulomb = SumFunc / (r * r * 4 * np.pi) /r

# Let's fit a Yukawa potential to that.
from scipy.optimize import curve_fit

def Yukawa(x, Amp, Decay):
    return Amp*np.exp(-Decay*x)/x

YukawaParams = [1,1]
# Fit only in the region where r>1 since we will have essentially one Yukawa potential for each energy shell.depending on the orbitals.
rmin = 4
rmax = 30
YukawaParams, pcov = curve_fit(Yukawa, r[(r>rmin) & (r<rmax)], Coulomb[(r>rmin) & (r<rmax)], p0=YukawaParams)

# Plot the psi**2 as a coulomb potential.
plt.figure()
plt.semilogy(r, Coulomb)
plt.semilogy(r, YukawaParams[0]*np.exp(-r*YukawaParams[1])/r)
# plt.semilogy(r, 0.4*np.exp(-r*1.25)/r)
plt.xlim([0,10])
plt.ylim([1e-8,1e6])
plt.ylabel('Charge density')
plt.xlabel('a.u.')
plt.title(AtomName)
plt.legend(['$\\rho(r)/r$', 'Arbitrary Yukawa: %0.2f $\\frac{e^{-%0.2f r}}{r}$'%(YukawaParams[0], YukawaParams[1])])
plt.savefig('PlotTotalChargeDensity.png')
Curve=np.stack((r,SumFunc / (r * r * 4 * np.pi)/r)).T
np.savetxt('ChargeDensity.txt', Curve)

print(f'Total number of electrons in charge density is: {SumElectrons}')

plt.show()
