#!/bin/bash
#SBATCH -p work -n 20 -J GaN_md
if [ ! -d traj ]; then
    mkdir traj
else
    rm -rf traj
    mkdir traj
fi
python ase_run.py
mv nvt* ./traj
