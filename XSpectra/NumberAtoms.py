# Written by Matthew Marcus 2019
# Numbers atoms in a QE input file within the ATOMIC_POSITIONS section so they can be processed
# by the MakeXSpectraForEachAtom.py script.

import re

# Inputs, edit these.
FileBase = 'OPX_XCH'
ReplacedBase = 'OPX_XCH_numbered'
ReplaceAtomBase = '^\s*O\s'
Replace_with = 'O_'

# First read in the scf file.
with open(FileBase+'.scf', 'r') as f:
    lines = f.readlines()
with open(ReplacedBase+'.scf','w') as g:
    count = 0
    PastAtomicPositions = False
    for line in lines:
        if 'ATOMIC_POSITIONS' in line:
            PastAtomicPositions = True
        if PastAtomicPositions == False:
            g.write(line)
            continue
        numstr = str(count+1)
        s = re.subn(ReplaceAtomBase,Replace_with+str(numstr),line)
        if s[1]:
            line = s[0]
            count += 1
        g.write(line)

