#!/bin/bash -l
# Job name:
#SBATCH --job-name=OPX_XCH_fast
#
# Partition:
#SBATCH --partition=vulcan
#
# Account:
#SBATCH --account=vulcan
#
# Wall clock limit:
#SBATCH --time=20:00:00
#
# Processors
#SBATCH --ntasks=144
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
module load gnu-parallel
echo $SLURM_JOB_NODELIST 
echo $SLURM_JOB_NODELIST |sed s/\,/\\n/g > hostfile
export JOBS_PER_NODE=2
parallel --delay 2 --jobs $JOBS_PER_NODE --slf hostfile --wd $SLURM_SUBMIT_DIR -a runallxspectra.sh
