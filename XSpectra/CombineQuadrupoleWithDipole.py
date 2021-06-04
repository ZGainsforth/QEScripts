import numpy as np
import matplotlib.pyplot as plt

BaseName = 'Run202'

Polarizations = [('e_100', 'xk010', 'xk001'), 
                 ('e_010', 'xk100', 'xk001'), 
                 ('e_001', 'xk100', 'xk010')]

IsotropicDipoleSpectra = None
IsotropicQuadrupoleSpectra = None
IsotropicCombinedSpectra = None

for i, p in enumerate(Polarizations):
    # In this case, spinel is isotropic so we just sum one direction and it is the isotropic spectrum.
    dipole = np.genfromtxt(f'../dipole/{BaseName}-Sum_{p[0]}.txt')
    quadrupolex = np.genfromtxt(f'../quadrupole_{p[1]}/{BaseName}-Sum_{p[0]}.txt')
    quadrupoley = np.genfromtxt(f'../quadrupole_{p[2]}/{BaseName}-Sum_{p[0]}.txt')

    combined = dipole.copy()
    combined[:,1] += quadrupolex[:,1]
    combined[:,1] += quadrupoley[:,1]

    quadrupole = quadrupolex.copy()
    quadrupole[:,1] += quadrupoley[:,1]

    # If this is our first spectrum, then initialize with it.
    if IsotropicDipoleSpectra is not None:
        IsotropicDipoleSpectra[:,1] += dipole[:,1]
    else:
        IsotropicDipoleSpectra = dipole

    # If this is our first spectrum, then initialize with it.
    if IsotropicQuadrupoleSpectra is not None:
        IsotropicQuadrupoleSpectra[:,1] += quadrupole[:,1]
    else:
        IsotropicQuadrupoleSpectra = quadrupole

    np.savetxt(f'{BaseName}-Sum_{p[0]}_dipole.txt', dipole, header='# eV  sigma')
    np.savetxt(f'{BaseName}-Sum_{p[0]}_quadrupole.txt', quadrupole, header='# eV  sigma')
    np.savetxt(f'{BaseName}-Sum_{p[0]}_dipoleplusquadrupole.txt', combined, header='# eV  sigma')

    fig,ax = plt.subplots(figsize=(12,8))
    ax.plot(dipole[:,0], dipole[:,1], label='Dipole')
    ax.plot(quadrupolex[:,0], quadrupolex[:,1], label='Quadrupole x')
    ax.plot(quadrupoley[:,0], quadrupoley[:,1], label='Quadrupole y')
    ax.plot(combined[:,0], combined[:,1], label='Dipole + Quadrupole')
    plt.legend(loc='upper left')
    plt.xlabel('eV')
    plt.ylabel('$\sigma$')
    plt.title(f'Sum spectrum {p[0]}')
    plt.savefig(f'{BaseName}-Sum_{p[0]}_dipoleplusquadrupole.png', dpi=300)

IsotropicDipoleSpectra[:,1] /= len(Polarizations)
IsotropicQuadrupoleSpectra[:,1] /= len(Polarizations)

IsotropicCombinedSpectra = IsotropicDipoleSpectra.copy()
IsotropicCombinedSpectra[:,1] += IsotropicQuadrupoleSpectra[:,1]

np.savetxt(f'{BaseName}-Isotropic_dipole.txt', IsotropicDipoleSpectra, header='# eV  sigma')
np.savetxt(f'{BaseName}-Isotropic_quadrupole.txt', IsotropicQuadrupoleSpectra, header='# eV  sigma')
np.savetxt(f'{BaseName}-Isotropic_dipoleplusquadrupole.txt', IsotropicCombinedSpectra, header='# eV  sigma')

fig,ax = plt.subplots(figsize=(12,8))
ax.plot(IsotropicDipoleSpectra[:,0], IsotropicDipoleSpectra[:,1], label='Dipole')
ax.plot(IsotropicQuadrupoleSpectra[:,0], IsotropicQuadrupoleSpectra[:,1], label='Quadrupole')
ax.plot(IsotropicCombinedSpectra[:,0], IsotropicCombinedSpectra[:,1], label='Dipole + Quadrupole')
plt.legend(loc='upper left')
plt.xlabel('eV')
plt.ylabel('$\sigma$')
plt.title(f'Isotropic spectrum')
plt.savefig(f'{BaseName}-Isotropic_dipoleplusquadrupole.png', dpi=300)
plt.show()

