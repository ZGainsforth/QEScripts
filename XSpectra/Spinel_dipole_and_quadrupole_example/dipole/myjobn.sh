#!/bin/bash -l
# Job name:
#SBATCH --job-name=IW-1_XSPEC
#
# Partition:
#SBATCH --partition=vulcan
#
# Account:
#SBATCH --account=nano
#
# Wall clock limit:
#SBATCH --time=1-12:00:00
#
# Processors
#SBATCH --ntasks=72
#
# Mail type:
#SBATCH --mail-type=all
#
# Mail user:
#SBATCH --mail-user=zgainsforth@lbl.gov
#
# Exclude nodes that have produced the infiniband error in the past.
#SBATCH --exclude=n0245.vulcan0
#
## Run command
source loadmyqe
cd $SLURM_SUBMIT_DIR;

./runallscf.sh
./runallxspectra.sh

