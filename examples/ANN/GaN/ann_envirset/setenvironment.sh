#!/bin/bash

mkdir '01-generate'
mkdir '02-train'
mkdir '03-predict'
mkdir '04-ase'
mkdir './04-ase/opt'
mkdir './04-ase/md'
mkdir 'new_xsfs'

cp ../../ann_fingerprint/Ga.fingerprint.stp ../../ann_fingerprint/N.fingerprint.stp ./01-generate

cp ../../ann_envirset/train.in ../../ann_envirset/nga.py ../../ann_envirset/job-train.sh ./02-train

cp ../../ann_envirset/write_generate_in.py ./
cp ../../ann_envirset/get_energy_err.py ./
cp ../../ann_envirset/compare.py ./03-predict

cp ../../ann_envirset/traj2poscar.py ./04-ase/opt
cp ../../ann_envirset/traj2poscar.py ./04-ase/md

cp ../../ann_envirset/ase_input/ase_run.py ./04-ase/md
cp ../../ann_envirset/ase_input/ase.sh ./04-ase/md

cp ../../ann_envirset/opt_input/opt_run.py ./04-ase/opt
cp ../../ann_envirset/opt_input/opt.sh ./04-ase/opt

cp ../../ann_envirset/high_ene_namelist.py ./02-train

mkdir './04-ase/md_input_xsf'
mkdir './04-ase/opt_input_xsf'
cp ../../ann_envirset/ase_input_random_choose.py ./
