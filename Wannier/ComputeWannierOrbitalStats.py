
import sys, os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from ReadXSFVolume import ReadXSFVolume
from skimage.external.tifffile import imsave 

# Normalize wavefunction.
def NormPsi(Psi):
    UnNorm = np.sum(np.real(np.conj(Psi)*Psi))
    Psi /= np.sqrt(UnNorm)
    return Psi

# Psi squared
def Integrate(Psi):
    return(np.sum(np.real(np.conj(Psi)*Psi)))

# Expectation value of the electron radius.
def IntegrateMomentR(Psi, meshR):
    return(np.sum(np.real(np.conj(Psi)*meshR*Psi)))

def Plot3Planes(mesh, title=''):
    fig, (ax1, ax2, ax3) = plt.subplots(1,3)
    im = ax1.imshow(mesh[:,:,mesh.shape[2]//2].T, cmap='gray')
    fig.colorbar(im, ax=ax1, fraction=0.046, pad=0.04)
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_title('xy-plane (z-axis)')
    
    im = ax2.imshow(mesh[:,mesh.shape[1]//2,:].T, cmap='gray')
    fig.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
    ax2.set_xlabel('x')
    ax2.set_ylabel('z')
    ax2.set_title(title + '\nxz-plane (y-axis)')
    
    im = ax3.imshow(mesh[mesh.shape[0]//2,:,:].T, cmap='gray')
    fig.colorbar(im, ax=ax3, fraction=0.046, pad=0.04)
    ax3.set_xlabel('y')
    ax3.set_ylabel('z')
    ax3.set_title('yz-plane (x-axis)')
    plt.tight_layout()
    
def PlotOrbital(mesh, OrbitalName=''):

    Plot3Planes(np.real(np.conj(Psi)*Psi), OrbitalName + '<Psi|Psi>')
    Plot3Planes(np.real(Psi), OrbitalName + '<1|Psi>')
    Plot3Planes(np.imag(Psi), OrbitalName + '<i|Psi>')
    
    # from tifffile import imsave
    # imsave(OrbitalName+'.tif', np.real(np.conj(Psi)*Psi).astype('float32'))

def ShowWaveFuncStats(Psi, meshX, meshY, meshZ, dx, meshR, meshT, meshP):
    # Assume a charge of 1 at the nucleus.
    Z=1

    print(f'<Psi|Psi> = {Integrate(Psi)}')
    print(f'<Psi|R|Psi> = {IntegrateMomentR(Psi, meshR)} Bohr')

    # Laplacian on Psi.
    p = np.gradient(Psi,dx)
    p00 = np.gradient(p[0],dx)
    p11 = np.gradient(p[1],dx)
    p22 = np.gradient(p[2],dx)
    p2 = p00[0] + p11[1] + p22[2]
    # Kinetic energy
    E = np.conj(Psi)*(-p2)/2
    # Potential energy
    U = np.conj(Psi)*(-Z)/meshR*Psi
    TotalE = E+U
    
    # Output the energies.  
    # (Output the imaginary parts too just as a sanity check.  They should be 0.)
    print(f'Ereal = {np.sum(np.real(E)):0.4g} Hartrees')
    print(f'Eimag = {np.sum(np.imag(E)):0.4g} Hartrees')
    print(f'Ureal = {np.sum(np.real(U)):0.4g} Hartrees')
    print(f'Uimag = {np.sum(np.imag(U)):0.4g} Hartrees')
    print(f'Total Energy = {np.sum(np.real(TotalE)):0.4g} Hartrees')

    # Draw the energy 
    Plot3Planes(np.real(TotalE), '<Psi|H|Psi>')
    
    # Compute the orbital angular momentum.
    # Make p vector, p = -i*grad(psi)
    p = np.gradient(Psi,dx)
    px = -1j*p[0].astype('complex128')
    py = -1j*p[1].astype('complex128')
    pz = -1j*p[2].astype('complex128')

    # L = r x p
    Lx = meshY*pz - meshZ*py
    Ly = meshX*pz - meshZ*px
    Lz = meshX*py - meshY*px

    # L squared
    L2 = np.conj(Lx)*Lx + np.conj(Ly)*Ly + np.conj(Lz)*Lz

    print(f'<L|L> = {np.sum(np.real(L2)):0.4g} hbar (L**2)')

    # Projection of L onto z axis for mz
    zdotL = np.sqrt(np.sum(np.real(Lz)**2)) - np.sqrt(np.sum(np.imag(Lz)**2))
    print(f'<z|L> = {zdotL:0.4g} hbar (mz)')
    print('Note the z component only works if the WF is oriented so the z direction is along the z axis, obviously.')

    # We can draw the angular momentum too.
    # Typically the values are real, or complex, not both.  So we just mix them for drawing.
    Plot3Planes(np.real(Lz) + np.imag(Lz), 'Lz - real+imag')
    #Plot3Planes(np.imag(Lz), 'Lz - imag')


def ComputeWannierOrbitalStats(xsfFileName=None, WFOffset=(0,0,0), Cutoff=0.0, MaxR=100):

    # Read the XSF file.  Note that we expect the z axis to line up correctly at present.
    print('Loading XSF.')
    X,Y,Z,V = ReadXSFVolume(xsfFileName, verbose=False, WFOffset=WFOffset, Cutoff=Cutoff)

    # # Rotate the axes is desired.
    # XYZ = np.stack((X,Y,Z), axis=0)
    # Rz = 89
    # RotX = np.array([[1, 0, 0],
    #                  [0, np.cos(np.radians(Rz)),  -np.sin(np.radians(Rz))],
    #                  [0, np.sin(np.radians(Rz)),  np.cos(np.radians(Rz))]])
    # RotY = np.array([[np.cos(np.radians(Rz)),  0,  np.sin(np.radians(Rz))],
    #                  [0,                       1,  0],
    #                  [-np.sin(np.radians(Rz)), 0,  np.cos(np.radians(Rz))]])
    # RotZ = np.array([[np.cos(np.radians(Rz)), -np.sin(np.radians(Rz)), 0],
    #                  [np.sin(np.radians(Rz)),  np.cos(np.radians(Rz)), 0],
    #                  [0,                       0,                      1]])
    # whatsit = np.array([[1,2,0], [0,1,0], [0,0,0]])
    # XYZ2 = np.einsum('ij,jklm ->iklm', RotZ,XYZ)
    # print(XYZ2.shape)
    # print(X.shape)
    # print(np.sum(Y - XYZ2[1,:,:,:]))
    # X,Y,Z = XYZ2[0,:,:,:], XYZ2[1,:,:,:], XYZ2[2,:,:,:]

    meshX = X.copy()
    meshY = Y.copy()
    meshZ = Z.copy()
    Psi = V.copy()
    # imshow(Psi[Psi.shape[0]//2,:,:])
    # imshow(Psi[:,Psi.shape[1]//2,:])
    # imshow(Psi[:,:,Psi.shape[2]//2])

    # The meshes are in A but need to be in bohr.
    meshX /= 0.529177249
    meshY /= 0.529177249
    meshZ /= 0.529177249

    # Switch to spherical coordinates.
    meshR = np.sqrt(meshX**2 + meshY**2 + meshZ**2)
    meshT = -np.arccos(meshZ/meshR) + np.pi
    meshP = np.arctan(meshY/meshX)
    meshP[meshX<0] += np.pi
    meshP += np.pi/2
    dx = meshX[1,0,0] - meshX[0,0,0]

    # Trim the wavefunction at some radius to eliminate noise in the Wannier function at high distance, or select a portion.
    Psi[meshR > MaxR] = 0

    # Normalize the wavefunction.
    Psi = NormPsi(Psi)

    imsave(xsfFileName+'_V.tif', V.astype('float32'))
    imsave(xsfFileName+'_X.tif', meshX.astype('float32'))
    imsave(xsfFileName+'_Y.tif', meshY.astype('float32'))
    imsave(xsfFileName+'_Z.tif', meshZ.astype('float32'))
    imsave(xsfFileName+'_Psi.tif', Psi.astype('float32'))

    # Compute all the relevant parameters about the wavefunction and display them.
    ShowWaveFuncStats(Psi, meshX, meshY, meshZ, dx, meshR, meshT, meshP)

    # Note the above function will make plots but they won't be shown unless the caller shows them.

    return

if __name__ == '__main__':

    if len(sys.argv) < 1:
        print('Please give an XSF filename of a wannier function.')

    # ComputeWannierOrbitalStats('NiO_00001.xsf')
    ComputeWannierOrbitalStats('NiO_00001.xsf', MaxR=4)
    # ComputeWannierOrbitalStats('NiO_00001.xsf')
    # ComputeWannierOrbitalStats('NiO_00006.xsf', WFOffset=(2.0664296, -2.0664296, -2.0664296), MaxR = 4)
    # ComputeWannierOrbitalStats('NiO_00001.xsf')
    # ComputeWannierOrbitalStats('NiO_00001.xsf')
    # ComputeWannierOrbitalStats('NiO_00001.xsf')
    # ComputeWannierOrbitalStats(sys.argv[1], WFOffset=(0,0,3.5945353), Cutoff=0.0001)
    #plt.show()
