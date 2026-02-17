#!/bin/bash
#SBATCH --job-name=sieve
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128
#SBATCH --time=96:00:00
#SBATCH --partition=msismall
#SBATCH --output=slurm-%j.out

module load python

srun python ~/code/msi-examples/worker.py
