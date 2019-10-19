import numpy as np
import re
import argparse 

p = argparse.ArgumentParser()
p.add_argument('FileRoot')
args = p.parse_args()
FileRoot = args.FileRoot

ReplaceAtomBase = 'O_'
ExcitedAtom = 'O_x'
GroundAtom = 'O'

with open(FileRoot, 'r') as f:
    FileBody = f.read()

for n in range(1,17):
    print(n)
    NewFileBody = re.sub('('+ReplaceAtomBase+str(n)+')  ', ExcitedAtom, FileBody)
    NewFileBody = re.sub('('+ReplaceAtomBase+'[0-9]{1,2})  ', GroundAtom, NewFileBody)
    # print(NewFileBody)
    # raw_input()
    with open(f'{FileRoot}.O{n}.in', 'w+') as g:
        g.write(NewFileBody)

# print(FileBody)

