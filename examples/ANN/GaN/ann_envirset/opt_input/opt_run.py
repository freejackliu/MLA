#!/usr/bin/env python

import sys
import os
import shutil
from mpi4py import MPI
from ase.io import *
from ase.io.trajectory import Trajectory
from ase.optimize import BFGS
from ase.constraints import UnitCellFilter
from aenet.calculator import ANNCalculator


def opt_run(ixsf_path, itraj_path, ixsf_file_name,index):
    print('%d'%index+' In directory : %s'%(ixsf_path + ixsf_file_name))
    atoms = read(ixsf_path + ixsf_file_name)
    calc = ANNCalculator(potentials={"Ga": "Ga.10t-10t.nn",
                                     "N": "N.10t-10t.nn"})

    atoms.set_calculator(calc)

    ucf = UnitCellFilter(atoms)
    opt = BFGS(ucf)
    traj = Trajectory(itraj_path + 'opt_%i.traj'%index, 'w', atoms)

    opt.attach(traj, interval=40)
    opt.run(fmax=0.05)
        
         
def make_empty_dir(path, dirname):
    if not os.path.exists(path+dirname):
        os.mkdir(path+ dirname)
    else:
        shutil.rmtree(path+dirname)
        os.mkdir(path+dirname)


def main():
    xsf_path  = os.getcwd().replace('/'+os.getcwd().split('/')[-1],'') + '/opt_input_xsf/'
    traj_path = os.getcwd() + '/'   #"/vol7/home/ann/users/huanr/origin_ann/ann_00*/04-ase/opt/"
    make_empty_dir(traj_path, 'traj')
    xsf_file_names = os.listdir(xsf_path)
    for i, xsf_file_name in enumerate(xsf_file_names):
        opt_run(xsf_path, traj_path, xsf_file_name, i)
            

if __name__ =="__main__":
    sys.exit(main())
