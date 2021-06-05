import numpy as np
import matplotlib.pyplot as plt
import glob2 as glob

# Basic data about the set of files which we will combine to make spectra.
BaseName = 'IW-1'
Atoms = [1,]
Polarizations = ['e_001', 'e_010', 'e_100']

# We will have one spectrum for each polarization.
SumSpectra = [None]*len(Polarizations)

def Despike(S):
    # For some reason XSpectra is returning a big spike on the first negative value on the energy axis.
    # We are going to just make the value the average of the nearest neighbors.
    # Energy axis:
    E = np.copy(S[:,0])
    # Ignore any positive energies (by dropping them to the most negative value around.
    E[E>=0] = np.min(E)
    # The least negative energy is now the maximum value.
    i = np.argmax(E)
    S[i,1] = (S[i-1,1] + S[i+1,1]) / 2
    return S

# Loop through each polarization
for i, p in enumerate(Polarizations):
    # Get all the filenames for this polarization.
    Files = glob.glob(f'{BaseName}*{p}*.dat')
    Files.sort()

    print(f'Polarization: {p}')

    # Figure 1 is going to be redrawn for each spectrum.
    plt.figure(1)
    plt.clf() 
    # Figure 2 is the combination of all atoms in the current polarization.
    plt.figure(2)
    plt.clf() # Clear out the figure only at the start of the polarization.

    for j, g in enumerate(Files):
        print(f'\tAdding {g}')
        # Get the raw data.
        x = np.genfromtxt(g)
        x = Despike(x) # Get rid of the funky spike just below zero on the energy axis.
        # And save a plot
        plt.figure(1)
        plt.clf() # We are reusing this figure for each file.
        plt.plot(x[:,0], x[:,1], label=g)
        plt.ylabel('$\sigma$')
        plt.xlabel('eV')
        plt.title(g)
        # plt.legend()
        plt.savefig(g + '.png', dpi=300)

        # Also add this to the sum polarization plot.
        plt.figure(2)
        plt.plot(x[:,0], x[:,1], '--', label=f'Atom {j+1}')

        # If this is our first spectrum, then initialize with it.
        if SumSpectra[i] is not None:
            # print(SumSpectra[i][:,0], x[:,0])
            # assert SumSpectra[i][:,0] == x[:,0], f"{g} energy axis doesn't match other spectra in this polarization."
            SumSpectra[i][:,1] += x[:,1]
        else:
            SumSpectra[i] = x

    # Renormalize the sum so it has the right amplitude.  For now, we assume equal weighting.
    SumSpectra[i][:,1] /= len(Files)

    # Save a file with the sum polarization.
    np.savetxt(f'{BaseName}-Sum_{p}' + '.txt', SumSpectra[i], header='eV                      sigma')

    # Now we draw two plots.  One shows the polarization sum along with all the components that went into it (messy).
    plt.figure(2)
    plt.plot(SumSpectra[i][:,0], SumSpectra[i][:,1], label=f'Sum of polarization {p}')
    plt.ylabel('$\sigma$')
    plt.xlabel('eV')
    plt.title(f'Polarizations: {p}')
    plt.legend(fontsize=6)
    plt.savefig(f'{BaseName}-Sum_{p}_with_components' + '.png', dpi=300)

    # And now just the sum for a clean plot.
    plt.clf()
    plt.plot(SumSpectra[i][:,0], SumSpectra[i][:,1], label=f'Sum of polarization {p}')
    plt.ylabel('$\sigma$')
    plt.xlabel('eV')
    plt.title(f'Sum of polarization {p}')
    plt.savefig(f'{BaseName}-Sum_{p}' + '.png', dpi=300)

# Finally we make an isotropic spectrum which is the sum of the three polarizations.
IsoSpectrum = None
plt.figure(2)
plt.clf()
for i, p in enumerate(Polarizations):
    # If this is the first polarization component, then use it to initialize the isotropic spectrum.
    if IsoSpectrum is None:
        IsoSpectrum = SumSpectra[i]
    else:
        IsoSpectrum[:,1] += SumSpectra[i][:,1]

    # Draw a plot which shows the isotropic alongside the individual components.
    plt.plot(SumSpectra[i][:,0], SumSpectra[i][:,1], label=f'Sum of polarization {p}')

# Renormalize the sum so it has the right amplitude.  For now, we assume equal weighting.
IsoSpectrum[:,1] /= len(Polarizations)

# Save the isotropic spectrum.
np.savetxt(f'{BaseName}-Isotropic' + '.txt', IsoSpectrum, header='eV                      sigma')

# And finalize the plot
plt.plot(IsoSpectrum[:,0], IsoSpectrum[:,1], label=f'Isotropic Spectrum')
plt.ylabel('$\sigma$')
plt.xlabel('eV')
plt.title(f'Isotropic spectrum with polarization components')
plt.legend(fontsize=6)
plt.savefig(f'{BaseName}-Isotropic_with_polarizations' + '.png', dpi=300)

# Now one final plot with just the isotropic spectrum without components to avoid clutter.
plt.clf()
plt.plot(IsoSpectrum[:,0], IsoSpectrum[:,1], label=f'Isotropic Spectrum')
plt.ylabel('$\sigma$')
plt.xlabel('eV')
plt.title(f'Isotropic spectrum with polarization components')
# plt.legend(fontsize=6)
plt.savefig(f'{BaseName}-Isotropic' + '.png', dpi=300)
