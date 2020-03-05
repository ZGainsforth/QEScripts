import numpy as np
import matplotlib.pyplot as plt
import re
import sys, os
from pprint import pprint
import pdb;

# This script will generate and run the files necessary to plot a band structure.  
# The sequence:
#
# Preliminary:
# 1) You have an SCF calculation completed.
# 2) Create a kpath file using XCrysDen and a text editor (description below).
#
# Prepare calculation
# 3) Run this script using the SCF and kpath as inputs.
# 4) This script will produce a pw.x input file using the 'bands' calculation.
# 5) This script will produce a bands.x intput file for post processing.
#
# Do calculation
# 6) This script will run pw.x.
# 7) This script will run bands.x.s
#
# Process results
# 8) This script will parse the outputs and produce plots.

# Steps to produce kpath file which is similar to the format QE will want:
# Go to bilbao crystallographic server and load space group, kvec, enter space group number.
# Use XCrysDen to click on the kpath and write it to a kpf file.
# Edit the kpf file into a kpath file where you add the number of steps for each path, comment out the description, and add the KPOINTS line and the line with how many lines.  You should wind up with something like:
# K_POINTS crystal
#     9
#    0.0000000000     0.0000000000     0.0000000000   1   $\Gamma$ 
#    0.5000000000     0.0000000000     0.0000000000   10  X
#    0.0000000000     0.0000000000     0.5000000000   10  Z
#    0.5000000000     0.0000000000     0.5000000000   10  U
#    0.0000000000     0.5000000000     0.0000000000   10  Y
#    0.5000000000     0.5000000000     0.0000000000   10  S
#    0.0000000000     0.5000000000     0.5000000000   10  T
#    0.5000000000     0.5000000000     0.5000000000   10  R
#    0.0000000000     0.0000000000     0.0000000000   10  $\Gamma$
# 
# Note that last one needs to have only one point.
# Each line has: x, y, z, number of points in this leg, name of symmetry point at beginning of leg.
# There must be at least two legs.
# Notice that the names of the gamma points are passed straight to matplotlib.  So if you want a fancy Gamma you can do that.

def PrepCalc(EnvironmentVars):

    print(f'Preparing band structure calculation from {EnvironmentVars["SCFName"]} and {EnvironmentVars["KPathName"]}')

    # Read in the kpath file.
    with open(EnvironmentVars['KPathName'], 'r') as f:
        KPathLines = f.readlines()

    # We want to verify a header line so we don't accidentally read a wrong file.
    assert 'K_POINTS crystal' in KPathLines[0], "Invalid KPath file.  See comment in this script to see how to produce it."
    # The second line is how many lines in the rest of the file to read -- one line for each high symmetry point.
    NumKPathLegs = int(KPathLines[1]) # The second line of the file is how many legs there are in this band strucutre.
    # We are going to generate a list of k-points from the list of high symmetry points.
    # One text line for each and every kpoint.
    KPoints = [] 
    # We also want to keep track of names and positions of the high symmetry points for plotting later.
    KPathSymmetryPointNames = [] # Names of the high symmetry points.  Should be the same as NumKPathLegs
    KPathSymmetryPointIndexes = [] # Index into KPoints where this symmetry point is.  

    # Read one line from the file and turn it into meaningful numbers and a name for the symmetry point.
    def ParseKPathLine(line):
        SymPoint = line.split() 
        h = float(SymPoint[0])
        k = float(SymPoint[1])
        l = float(SymPoint[2])
        NumPoints = int(SymPoint[3]) # How many points in this leg.
        SymName = SymPoint[4]
        
        return h, k, l, NumPoints, SymName

    # Generate a line that will be written to the output file for pw.x.
    def WriteKPoint(h, k, l):
        KPoints.append(f'\t{h:0.6f}\t{k:0.6f}\t{l:0.6f}\t1.0\n') # The last entry is the weight for this k-point.

    # Get the first high symmetry point and write it to the list of kpoints.
    h, k, l, NumPoints, SymName = ParseKPathLine(KPathLines[2]) # Real data begins on the third line.
    WriteKPoint(h, k, l)
    # Note this starting position as a high symmetry point with index zero (the first position in KPoints.)
    KPathSymmetryPointIndexes.append(0)
    KPathSymmetryPointNames.append(SymName)

    # Now loop through each following high symmetry point and produce a series of kpoints from the last (or first) symmetry point to this one.
    for i in range(NumKPathLegs-1): # -1 because we already loaded the first.
        # The next high symmetry point is...
        h2, k2, l2, NumPoints2, SymName2 = ParseKPathLine(KPathLines[3+i])
        # There will be NumPoints kpoints between the last high symmetry point (h,k,l) and this one (h2,k2,l2)
        for j in range(1, NumPoints+1):
            # Create an even grid of points from h to h2 with NumPoints steps.
            # For example, if h = 0, h2 = 1, and NumPoints = 4, then we loop over 4 j values (1 indexed):
            # j * (h2 - h)/NumPoints + h = 1/4
            # 1 * (1  - 0)/4         + 0 = 1/4
            # j=2 -> 1/2, j=3 -> 3/4 and finally j=4 -> 1.
            hj = j*(h2-h)/NumPoints + h
            kj = j*(k2-k)/NumPoints + k
            lj = j*(l2-l)/NumPoints + l
            WriteKPoint(hj, kj, lj)
        # After the last point we have to note the position of this high symmetry point for plotting later.
        KPathSymmetryPointIndexes.append(len(KPoints)-1)
        KPathSymmetryPointNames.append(SymName2)
        # And set the current high symmetry point as the last one for the next loop around.
        h = h2; k = k2; l = l2 
        NumPoints = NumPoints2
        SymName = SymName2

    print(f'There are {len(KPoints)} k-points in this calculation.')

    EnvironmentVars['KPoints'] = KPoints
    EnvironmentVars['KPathSymmetryPointIndexes'] = KPathSymmetryPointIndexes
    EnvironmentVars['KPathSymmetryPointNames'] = KPathSymmetryPointNames

    # Generate the text we will drop into the scf file
    KPointText = '\t%d\n'%(len(KPoints)) + ''.join(KPoints)

    # Contents for the new file that will be the pwbands file -- i.e. the pw.x input file for the 'bands' calculation.
    PWBandsLines = []

    # Read in the scf file line by line...
    with open(EnvironmentVars['SCFName'], 'r') as f:
        SCFLines = f.readlines()
    # ... and replace the calculation name and KPOINTS sections.
    for i, line in enumerate(SCFLines):
        # Change the scf calculation to bands
        if "'scf'" in line:
            SCFLines[i] = line.replace("'scf'", "'bands'")
        # If this is the K_POINT section, then replace it with our new section.
        # For now, we only support replacing a 2-line K_POINT section where it makes a grid automatically.
        if 'K_POINTS' in line:
            SCFLines[i] = 'K_POINTS crystal\n' # New header to the K_POINTS section
            SCFLines[i+1] = KPointText # And the full text of it.

    # Finally, write the updated pwbands file out.
    with open(EnvironmentVars['PWBandsFileName'], 'w') as f:
        f.writelines(SCFLines)
    print(f'Wrote {EnvironmentVars["PWBandsFileName"]}. To run, execute: ')
    print('    ' + EnvironmentVars["PWBandsCommand"])

    # Now we need to generate the bands file for bands.x
    BandsxLines = ['&BANDS\n']
    for line in SCFLines:
        if any(x in line for x in ['prefix', 'outdir']):
            BandsxLines.append(line)
    BandsxLines.append('\tfilband="%s'%EnvironmentVars['BandsxFileName']+'.dat"\n') # Remember, there can't be a space between filband and the =.  *eyeroll*
    BandsxLines.append('/')
    with open(EnvironmentVars['BandsxFileName'], 'w') as f:
        f.writelines(BandsxLines)
    print(f'Wrote {EnvironmentVars["BandsxFileName"]}. To run, execute: ')
    print('    ' + EnvironmentVars['BandsxCommand'])

def DoCalc(EnvironmentVars):
    print('Running Quantum Espresso.')
    # Now run pw.x with the pwbands file
    os.system(EnvironmentVars['PWCommand'])
    os.system(EnvironmentVars['BandsxCommand'])

def ProcessCalc(EnvironmentVars):
    print('Plotting band structure.')

    # Get the Fermi level
    with open(EnvironmentVars['SCFName']+'.out', 'r') as f:
        SCFOutText = f.read()
    m = re.search('\s*the Fermi energy is \s*([-0-9.]*) ev\s*', SCFOutText)
    EFermi = float(m[1])

    # The .gnu file has the easiest to read number format.  It is a two column block with the values for the first band, a blank line, then another 2 column block etc through all bands.
    Bands = np.genfromtxt(EnvironmentVars['BandsxFileName']+'.dat.gnu')

    # However, to parse the gnu file, we need to know the number of bands so we know how long to loop.  We get this from the header of the .dat file.
    # It also gives a good consistency check.
    with open(EnvironmentVars['BandsxFileName']+'.dat', 'r') as f:
        BandsDatText = f.read()
    m = re.search('\s*\&plot\s*nbnd=\s*([0-9]*),\s*nks=\s*([0-9]*)\s*', BandsDatText)
    NumBands = int(m[1])
    NumKs = int(m[2])
    assert NumKs == len(EnvironmentVars['KPoints']), "Band structure path produced by bands.x has a different number of k-points than the original path input to pw.x.  Likely your calculation did not complete successfully."

    # Draw the plot, one band at a time.
    plt.figure()
    for i in range(NumBands):
        # Reconstruct the values for this band by slicing out the values for this band across all the k-points.
        ThisBand = Bands[i*NumKs:(i+1)*NumKs]
        plt.plot(ThisBand[:,0], ThisBand[:,1]-EFermi, alpha=EnvironmentVars['PlotAlpha'])
        kmax = ThisBand[-1,0]

    # # plt.ylim([-10,10])
    plt.xlabel('kpoint')
    plt.ylabel('eV')
    plt.ylim([EnvironmentVars['PlotMinEnergy'], EnvironmentVars['PlotMaxEnergy']])
    plt.xticks(ThisBand[EnvironmentVars['KPathSymmetryPointIndexes'],0], EnvironmentVars['KPathSymmetryPointNames'])
    # plt.xticks(np.array([0.*kmax, 14.*kmax, 22.*kmax, 30.*kmax, 39.*kmax])/39., ['$\Gamma$', 'X', 'Z', 'U', 'Y', 'S', 'T', 'R', '$\Gamma$'])
    plt.title(EnvironmentVars['RootName'])
    plt.savefig(EnvironmentVars['RootName']+'.bands.png', dpi=300)
    plt.show()

if __name__ == '__main__':

    # pdb.set_trace()

    # INPUTS
    EnvironmentVars = dict()
    #You must have an scf file, and you must have a kpath file.
    EnvironmentVars['RootName'] = 'Forsterite'  # Name of the computation
    EnvironmentVars['SCFName'] = 'Forsterite.scf' # SCF file to be used as the source of the bands files
    EnvironmentVars['KPathName'] = 'Forsterite.kpath' # Kpoint path file, see below for comment on how to produce this.
    EnvironmentVars['PlotMinEnergy'] = -2 # eV relative to EFermi
    EnvironmentVars['PlotMaxEnergy'] = 10 # eV relative to EFermi

    # Usually the default values for these environment variables are OK and don't need to be edited.
    EnvironmentVars['PWBandsFileName'] = EnvironmentVars['RootName']+'.pwbands'
    EnvironmentVars['PWBandsCommand'] = 'mpirun -np 6 -x OMP_NUM_THREADS=1 pw.x < %s | tee %s.out'%(EnvironmentVars['PWBandsFileName'],EnvironmentVars['PWBandsFileName'])
    EnvironmentVars['BandsxFileName'] = EnvironmentVars['RootName']+'.bandsx'
    EnvironmentVars['BandsxCommand'] = 'bands.x < %s | tee %s.out'%(EnvironmentVars['BandsxFileName'], EnvironmentVars['BandsxFileName'])
    EnvironmentVars['PlotAlpha'] = 1 # Sometimes it is useful to have alpha < 1 so the plotted lines are a little transparent.  It helps to see overlapping bands.  Usually, we want solid colors though.

    print('------------------------------ START ------------------------------')

    # Create the input files that will be needed by pw.x and bands.x.
    # Do steps 3-5 in the list above.
    PrepCalc(EnvironmentVars)

    # Run quantum espresso.
    # Do steps 6 and 7 in the list above.
    # DoCalc(EnvironmentVars)

    # Read and parse the outputs from quantum espresso and produce plots.
    # Do step 8 in the list above.
    ProcessCalc(EnvironmentVars)

    print('------------------------------ DONE ------------------------------')
