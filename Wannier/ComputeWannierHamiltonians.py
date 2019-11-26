import numpy as np
import numpy.linalg as linalg
import matplotlib.pyplot as plt
import sys, os
import glob2
import os, sys
from tabulate import tabulate

# Information specific to this computation. 
hr_filename = 'NiO_hr.dat'
out_suffix = '_hamiltonian.txt'
Efermi = 14.0853

# This reads the hamiltonian elements for a specific unit cell coordinate.  
# Wannier90 reports them by unit cell (x,y,z, i,j) where (1,0,0, 1,1) is the overlap of
# wavefunction 1 in the 0,0,0 cell with wavefunction 1 translated by one unit cell in the x direction.
def GetOneCell(x,y,z):
    hrtrim = hr[(hr[:,0]==x) & (hr[:,1]==y) & (hr[:,2]==z)]
    hrtrim = hrtrim[:,3:]
    H = np.zeros((num_MLWFs,num_MLWFs), dtype='complex')
    for r in hrtrim[:]:
        i = int(r[0])-1
        j = int(r[1])-1
        overlap = complex(r[2], r[3])
        H[i, j] = overlap
    return H

def PrintH(H):
    OutStr = ''
    for m in range(H.shape[0]):
        # for n in range(H.shape[1]):
        #     OutStr += f'({float(np.real(H[m,n])):+8.3f}{float(np.real(H[m,n])):+8.3f}j)    '
        for n in range(H.shape[1]):
            OutStr += f'{float(np.real(H[m,n])):+8.3f}  '
        OutStr += '\n'
        for n in range(H.shape[1]):
            OutStr += f'{float(np.imag(H[m,n])):+8.3f}j '
        OutStr += '\n\n'
    return OutStr

# Loop through all the subdirectories and proces all the hr_filename files.
G = glob2.glob('*/')
for g in G:

    os.chdir(g)

    print(f'Reading Hamiltonian in {g}')

    with open(hr_filename, 'r') as f:
        _ = f.readline() # The first line is just the date and time.
        num_MLWFs = int(f.readline())  # How many wannier functions in the hamiltonian basis.
        num_rpts =  int(f.readline()) # How many Wigner-Seitz grid-points (unit cells) are listed.
        # We will need to skip the first three lines plus the R points lines with 15 entries per line.
        hamiltonian_header_lines = int(np.ceil(num_rpts/15)) + 3 

    # First read in the Hamiltonian file data.
    hr = np.genfromtxt(hr_filename, skip_header=hamiltonian_header_lines)

    OutStr = ''

    # Print the eigenvalues for just the consideration of one unit cell.
    H = GetOneCell(0,0,0)
    OutStr += f'Single unit cell eigenvalues: \n{linalg.eig(H)[0]}'

    # Now do the same but considering the 6 nearest neighbors.
    H = GetOneCell(0,0,0)

    H += GetOneCell(1,0,0)
    H += GetOneCell(0,1,0)
    H += GetOneCell(0,0,1)
    H += GetOneCell(-1,0,0)
    H += GetOneCell(0,-1,0)
    H += GetOneCell(0,0,-1)

    OutStr += f'\n\nCenter unit cell + 6 neareast neighbors eigenvalues: \n{linalg.eig(H)[0]}'

    # Now build it using every element.
    H = np.zeros((num_MLWFs,num_MLWFs), dtype='complex')
    for r in hr[:]:
        x = int(r[0])
        y = int(r[1])
        z = int(r[2])
        i = int(r[3])-1
        j = int(r[4])-1
        overlap = complex(r[5], r[6])
        H[i, j] += overlap

    # Print out the energy levels from greatest to least, 
    # along with <psi_m|psi_n> so we can see what orbitals
    # they represent.
    E = linalg.eig(H)[0]
    psi = linalg.eig(H)[1]
    OutStr += '\n\nEigenvalues and eigenvectors across all cells:\n'
    for i in range(len(E)):
        OutStr += f'Energy = {float(np.real(E[i])):0.2f} eV\n'
        # OutStr += f'Energy = {np.real(E[i]):0.2f} eV'
        OutStr += f'psi=('
        normval=np.abs(psi[i]).sum()
        for j in range(len(E)):
            OutStr += f'{np.real(psi[i][j])/normval:0.2f}, '
        OutStr += ')\n'
    _ = plt.hist(np.real(E)-Efermi, orientation='horizontal', bins=10)
    plt.xlabel('Num States')
    plt.ylabel('E$_{Fermi}$ - E')
    plt.title('Eigenvalues')
    plt.savefig(os.path.split(g)[0] + '_Eigenvalues.png')

    OutStr += '\n\nUndiagonalized Hamiltonian Matrix:\n'
    OutStr += PrintH(H)

    print(OutStr)

    with open(os.path.split(g)[0] + out_suffix, 'w') as outfile:
        outfile.write(OutStr)
    
    os.chdir('..')
