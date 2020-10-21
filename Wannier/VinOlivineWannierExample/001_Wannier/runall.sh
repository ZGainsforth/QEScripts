echo scf V_1
mpirun -np 6 -x OMP_NUM_THREADS=1 pw.x < Mg2SiO4.V_1.scf | tee Mg2SiO4.V_1.scf.out

echo nscf V_1
mpirun -np 6 -x OMP_NUM_THREADS=1 pw.x < Mg2SiO4.V_1.nscf | tee Mg2SiO4.V_1.nscf.out

echo wannier pp V_1
wannier90.x -pp Mg2SiO4.V_1 | tee Mg2SiO4.V_1.pp.wout

echo pw2wannier90 V_1
mpirun -np 6 -x OMP_NUM_THREADS=1 pw2wannier90.x < Mg2SiO4.V_1.pw2wan | tee Mg2SiO4.V_1.pw2wan.out

echo wannier V_1
wannier90.x Mg2SiO4.V_1 | tee Mg2SiO4.V_1.wout

# ---------------------------------

echo scf V_5
mpirun -np 6 -x OMP_NUM_THREADS=1 pw.x < Mg2SiO4.V_5.scf | tee Mg2SiO4.V_5.scf.out

echo nscf V_5
mpirun -np 6 -x OMP_NUM_THREADS=1 pw.x < Mg2SiO4.V_5.nscf | tee Mg2SiO4.V_5.nscf.out

echo wannier pp V_5
wannier90.x -pp Mg2SiO4.V_5 | tee Mg2SiO4.V_5.pp.wout

echo pw2wannier90 V_5
mpirun -np 6 -x OMP_NUM_THREADS=1 pw2wannier90.x < Mg2SiO4.V_5.pw2wan | tee Mg2SiO4.V_5.pw2wan.out

echo wannier V_5
wannier90.x Mg2SiO4.V_5 | tee Mg2SiO4.V_5.wout
