import numpy as np
import matplotlib.pyplot as plt
import copy
import os
import sys
import shutil
import linecache
from math import *
from ase import Atoms
from ase.io import *
from ase.calculators.emt import EMT
from aenet.calculator import ANNCalculator

onu = 5
xsf_path = os.getcwd()+'/new_xsfs'
ase_input_path = os.getcwd()+'/04-ase/'
elements = ['Ga', 'N']
calc = ANNCalculator(potentials={"Ga": "Ga.10t-10t.nn", "N": "N.10t-10t.nn"})


def make_empty_dir(path,dirname):
    newdirpath = path + dirname
    if not os.path.exists(newdirpath):
        os.mkdir(newdirpath)
    else:
        shutil.rmtree(newdirpath)
        os.mkdir(newdirpath)
    return newdirpath



def read_vasp_energy(ixsf_file_path):
    atoms_number = int(linecache.getline(ixsf_file_path, 9).split()[0])
    with open(ixsf_file_path, 'r') as xsf:
        a = xsf.readline()
        vasp_energy = float(a.split()[-2])
        return vasp_energy, atoms_number


def ase_calc_energy(ipos_file_path):
    struc_from_file = read(ipos_file_path)
    struc_from_file.set_calculator(calc)
    ann_energy = struc_from_file.get_potential_energy()
    return ann_energy


def gan_select(ixsf_path):
    with open(ixsf_path,'r') as fr:
        elem_add = []
        ga_nu = 0
        n_nu = 0
        for line in fr:
            line = line.split()
            if line:
                for c_1 in elements:
                    if line[0] == c_1:
                        elem_add.append(c_1)
        for elem in elem_add:
            if elem == elements[0]:
                ga_nu += 1
            else:
                n_nu += 1
        return (n_nu != len(elem_add) and ga_nu != len(elem_add))


def main():
    xsf_files = os.listdir(xsf_path)
    # ee = np.zeros(len(xsf_files))
    emax = [0]*onu
    epath = {}
    target_file_path = make_empty_dir(ase_input_path,'opt_input_xsf')
    for i in range(len(xsf_files)):
        xsf_file_path = os.path.join(xsf_path,xsf_files[i])
        print(xsf_file_path)
        ve = read_vasp_energy(xsf_file_path)
        ae = ase_calc_energy(xsf_file_path)
        ee = abs(ve[0]-ae)/ve[1]
        if ee > emax[0] and gan_select(xsf_file_path):
            epath[ee] = xsf_file_path
            etemp = copy.copy(emax)
            etemp.append(ee)
            etemp = sorted(etemp)
            emax = etemp[1:]
    print(emax)
            
    for ie in emax:
        shutil.copy(epath[ie],target_file_path)
    plt.figure(figsize=(6,6))
    plt.hist(ee, bins=30, range=[0,0.1])
    plt.xlabel("energy error(eV/atom)")
    plt.show()

if __name__ == '__main__':
    sys.exit(main())
