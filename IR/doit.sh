#!/bin/bash

# In order to run this setup, you have to have an optimized geometry and figured out all your convergences.
# It is assumed that you are starting this SCF with an already sorted sample.

mpirun.openmpi -np 6 -x OMP_NUM_THREADS=1 pw.x < Lizardite.scf | tee Lizardite.scf.out
mpirun.openmpi -np 6 -x OMP_NUM_THREADS=1 ph.x < Lizardite.ph | tee Lizardite.ph.out
mpirun.openmpi -np 6 -x OMP_NUM_THREADS=1 dynmat.x < Lizardite.dynmat | tee Lizardite.dynmat.out
wget https://rruff.info/repository/sample_child_record_infrared/by_minerals/Lizardite__R060006-1__Infrared__Infrared_Data_Processed__841.txt
python PlotIR.py
