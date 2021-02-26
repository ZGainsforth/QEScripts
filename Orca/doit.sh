#!/bin/zsh

source loadmyorca

InputFile=FeCH

orca $InputFile.inp | tee $InputFile.out

orca_mapspc $InputFile.out SOCABS -eV -x0700 -x1740 -n500 -w0.5

streamlit run DrawSpec.py
