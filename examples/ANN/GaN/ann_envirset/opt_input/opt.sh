#!/bin/bash
#SBATCH -p work -n 20 -J GaN-opt
python opt_run.py
mv opt*.traj ./traj
mv slurm* ./opt.out
