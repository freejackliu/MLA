import numpy as np
import os
import shutil
import sys
from mpi4py import MPI
from ase.io import *
from ase.io.trajectory import Trajectory
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution, Stationary
from ase.md.npt import NPT
from ase.md.langevin import Langevin as NVT
from ase.md.logger import MDLogger
from ase.units import fs, kB, GPa
from aenet.calculator import ANNCalculator

def make_empty_dir(path, dirname):
    newdirpath = path + dirname
    if not os.path.exists(newdirpath):
        os.mkdir(newdirpath)
    else:
        shutil.rmtree(newdirpath)
        os.mkdir(newdirpath)
    return newdirpath
      

def md_run(origin_poscar_path, index):
    print('%d'%index+' In directory : %s'%origin_poscar_path)
    atoms = read(origin_poscar_path)

    calc = ANNCalculator(potentials={"Ga": "Ga.10t-10t.nn", "N": "N.10t-10t.nn"})
    atoms.set_calculator(calc)

    MaxwellBoltzmannDistribution(atoms, 1200*kB)
    Stationary(atoms)

    md = NVT(atoms, timestep=2*fs, temperature=1000*kB, friction=0.05)
    logger = MDLogger(md, atoms, '-', stress=True)
    md.attach(logger, interval=1)
    traj = Trajectory("nvt_%s.traj"%(origin_poscar_path.split('/')[-1].split('.xsf')[0]), "w", atoms)
    md.attach(traj.write, interval=200)

    md.run(40000)


def main():
    poscar_path  = os.getcwd().replace('/'+os.getcwd().split('/')[-1],'') + '/md_exp_input_xsf/'
    traj_path    = os.getcwd() + '/'
    poscar_files = os.listdir(poscar_path)
    for index, poscar_file in enumerate(poscar_files):
        poscar_file_path = poscar_path + poscar_file
        md_run(poscar_file_path, index)

    

if __name__ =="__main__":
    sys.exit(main())
    

