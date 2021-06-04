#!/bin/bash

FileBase=Run202

# Some files are simply copied over.
for quad in quadrupole_xk001 quadrupole_xk010 quadrupole_xk100
do
    mkdir $quad
    #cp dipole/MakeXSpectraForEachAtom.py $quad
    #cp dipole/PlotXSpectraXANES.py $quad # We edit this via sed as we copy it over
    cp dipole/myjobn.sh $quad
    cp dipole/myjob.sh $quad
    cp dipole/doit.sh $quad
    cp dipole/$FileBase.scf $quad
    # cp dipole/$FileBase.xspectra $quad # This is handled via sed because we have to change xkvec
    cp dipole/*.core $quad
    cp -r dipole/pseudo $quad
    cp -r dipole/calcdir $quad
done

# Now we do the files that require special attention.

# We need to remove the polarization that can't be plotted (k and e have to be othogonal.
sed -e "s/'e_001', //" dipole/MakeXSpectraForEachAtom.py > quadrupole_xk001/MakeXSpectraForEachAtom.py
sed -e "s/'e_010', //" dipole/MakeXSpectraForEachAtom.py > quadrupole_xk010/MakeXSpectraForEachAtom.py
sed -e "s/'e_100', //" dipole/MakeXSpectraForEachAtom.py > quadrupole_xk100/MakeXSpectraForEachAtom.py

# We need to remove the polarization that can't be plotted (k and e have to be othogonal.
sed -e "s/'e_001', //" dipole/PlotXSpectraXANES.py > quadrupole_xk001/PlotXSpectraXANES.py
sed -e "s/'e_010', //" dipole/PlotXSpectraXANES.py > quadrupole_xk010/PlotXSpectraXANES.py
sed -e "s/'e_100', //" dipole/PlotXSpectraXANES.py > quadrupole_xk100/PlotXSpectraXANES.py

# We copy over the xspectra file while changing the polarization momentum vector.
sed -e "s/xanes_dipole/xanes_quadrupole/" -e "s/\(xkvec(3)[ \t]*=[ \t]*\)[0-9.]*/\11.0/" dipole/$FileBase.xspectra >  quadrupole_xk001/$FileBase.xspectra 
sed -e "s/xanes_dipole/xanes_quadrupole/" -e "s/\(xkvec(2)[ \t]*=[ \t]*\)[0-9.]*/\11.0/" dipole/$FileBase.xspectra >  quadrupole_xk010/$FileBase.xspectra 
sed -e "s/xanes_dipole/xanes_quadrupole/" -e "s/\(xkvec(1)[ \t]*=[ \t]*\)[0-9.]*/\11.0/" dipole/$FileBase.xspectra >  quadrupole_xk100/$FileBase.xspectra 

# Finally go run all the python scripts.
for quad in quadrupole_xk001 quadrupole_xk010 quadrupole_xk100
do
    cd $quad
    python MakeXSpectraForEachAtom.py
    chmod +x *.sh
    cd ..
done

echo Remember to edit your myjob or runall scripts to exclude the scf part if it has already been done in the dipole calc.
