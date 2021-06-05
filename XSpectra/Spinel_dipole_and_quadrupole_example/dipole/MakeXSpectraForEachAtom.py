import numpy as np
import re
import argparse 

FileBase = 'IW-1'
ReplaceAtomBase = 'V_'
ExcitedAtom = 'V_x'
GroundAtom = 'V'
Atoms = [1,]
Polarizations = ['e_001', 'e_010', 'e_100'] # These must have a format of e_xxx or e_xxx_k_xxx
SCFRunCommand = 'mpirun -np 72 -x OMP_NUM_THREADS=1 pw.x < {prefix}.in | tee {prefix}.out\n'
XSPECTRARunCommand = 'mpirun -np 72 -x OMP_NUM_THREADS=1 xspectra.x < {prefix}.{Polarization}.in | tee {prefix}.{Polarization}.out\n'

# First read in the scf file.
with open(FileBase+'.scf', 'r') as f:
    SCFFileBody = f.read()

# Read in the xspectra file.
with open(FileBase+'.xspectra', 'r') as f:
    XSPECTRAFileBody = f.read()

# We will have two files with commands to run all the processes.
RunallSCF = ''
RunallXSPECTRA = ''

# Now loop through all the atoms we need to substitute.
for n in Atoms:
    print(f'Creating SCF for {ReplaceAtomBase}{n}')
    prefix = f'{FileBase}.{ReplaceAtomBase}{n}'

    # First we edit the scf file
    # Replace the one atom we are working on now with the excited atom pseudo.
    NewFileBody = re.sub('('+ReplaceAtomBase+str(n)+')  ', ExcitedAtom, SCFFileBody)
    # Replace all the other numbered atoms with the ground state pseudo.
    NewFileBody = re.sub('('+ReplaceAtomBase+'[0-9]{1,2})  ', GroundAtom, NewFileBody)
    # Replace the prefix for the calculation with a unique string.
    NewFileBody = re.sub(r'(prefix\s*=\s*[\'"])(.*)([\'"])', f'\g<1>{prefix}\g<3>', NewFileBody)
    # Write out the result.
    with open(f'{prefix}.in', 'w+') as g:
        g.write(NewFileBody)

    # Add this file to the runall.
    RunallSCF += SCFRunCommand.format(prefix=prefix)

    # Make xspectra files for each polarization now.
    for Polarization in Polarizations:
        print(f'Creating XSPECTRA for {prefix}.{Polarization}')

        # Get numerical values for the polarization.
        if 'k' in [Polarization]:
            print('Quadrupole not implemented yet.')
        assert Polarization[:2] == 'e_', 'Polarization string must have format e_xxx or e_xxx_k_xxx'
        ex = int(Polarization[2])
        ey = int(Polarization[3])
        ez = int(Polarization[4])
        print(ex, ey, ez)
        
        # Replace the prefix for the calculation with a unique string.
        NewFileBody = re.sub(r'(prefix\s*=\s*[\'"])(.*)([\'"])', f'\g<1>{prefix}\g<3>', XSPECTRAFileBody)
        # Replace the polarization cards with correct values.
        NewFileBody = re.sub(r'(xepsilon\(1\)\s*=\s*)([0-9.]*)', f'\g<1>{ex}', NewFileBody)
        NewFileBody = re.sub(r'(xepsilon\(2\)\s*=\s*)([0-9.]*)', f'\g<1>{ey}', NewFileBody)
        NewFileBody = re.sub(r'(xepsilon\(3\)\s*=\s*)([0-9.]*)', f'\g<1>{ez}', NewFileBody)
        # Change the names of the output files to be unique.
        NewFileBody = re.sub(r'xanes.sav', f'{prefix}.{Polarization}.sav', NewFileBody)
        NewFileBody = re.sub(r'xanes.dat', f'{prefix}.{Polarization}.dat', NewFileBody)

        # Write out the result.
        with open(f'{prefix}.{Polarization}.in', 'w+') as g:
            g.write(NewFileBody)

        # Add this file to the runall.
        RunallXSPECTRA += XSPECTRARunCommand.format(prefix=prefix, Polarization=Polarization)

# Write out runall files.
with open(f'runallscf.sh', 'w+') as g:
    g.write(RunallSCF)
with open(f'runallxspectra.sh', 'w+') as g:
    g.write(RunallXSPECTRA)


