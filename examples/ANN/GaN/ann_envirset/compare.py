#!usr/bin/env python 

import numpy as np
import matplotlib.pyplot as plt
import os
from math import *
from ase.io import *
from aenet.calculator import ANNCalculator

plot_xsf_path = "/vol7/home/ann/users/huanr/origin_ann/ann_002/03-predict/predict_GaN"
calc = ANNCalculator(potentials={"Ga": "Ga.10t-10t.nn", "N": "N.10t-10t.nn"})


def read_vasp_energy(ixsf_file_path):
    with open(ixsf_file_path, 'r') as xsf:
        a = xsf.readline()
        vasp_energy = float(a.split()[-2])
        return vasp_energy


def ase_calc_energy(ixsf_file_path):
    atoms = read(ixsf_file_path)
    atoms.set_calculator(calc)
    ann_energy = atoms.get_potential_energy()
    return ann_energy


def read_volume(ixsf_file_name):
    tmp = ixsf_file_name.split('.')
    if tmp[0] and tmp[-1]=="xsf":
        mp_code = tmp[0].split('-')[1]
        volume_scaled = float((ixsf_file_name.split('-')[-1]).split('.xsf')[0])
        return mp_code, volume_scaled


def plot_sorted(x,y):
    assert len(x)==len(y)
    dict = {}
    for i in range(len(x)):
        dict[x[i]]=y[i]
    x_new=sorted(x)
    y_new=y
    for i in range(len(x_new)):
        y_new[i]=dict[x_new[i]]
    return x_new, y_new

mp_code_selec     = []
volume_selec      = []; new_vo_selec = []
vasp_energy_selec = []; new_va_selec = []
ase_energy_selec  = []; new_ae_selec = []

xsf_file_names = os.listdir(plot_xsf_path)
for xsf_file_name in xsf_file_names:
    xsf_file_path = plot_xsf_path + "/" +xsf_file_name
    n, v = read_volume(xsf_file_name)
    if 0.5 <=v<= 1.5:
        mp_code_selec.append(n)
        volume_selec.append(v)
        va = read_vasp_energy(xsf_file_path)
        ae = ase_calc_energy(xsf_file_path)
        vasp_energy_selec.append(va)
        ase_energy_selec.append(ae)
mp_name = list(set(mp_code_selec))
for mp_n in mp_name:
    new_ae_selec.append([])
    new_va_selec.append([])
    new_vo_selec.append([])
    for i in range(len(mp_code_selec)):
        if mp_n == mp_code_selec[i]:
            new_ae_selec[-1].append(ase_energy_selec[i])
            new_vo_selec[-1].append(volume_selec[i])
            new_va_selec[-1].append(vasp_energy_selec[i])


m=2;n=2
assert m + n == len(mp_name)
plt.figure(figsize=(8,8))

plt.subplot(2,2,1)
plt.xlabel('volume(scaled)')
plt.ylabel('E/eV')
plot_x, plot_y = plot_sorted(new_vo_selec[0], new_va_selec[0])
plt.plot(plot_x, plot_y, label='mp'+mp_name[0]+' vasp data')
plt.scatter(new_vo_selec[0], new_ae_selec[0], marker='x', label='mp'+mp_name[0]+' ann predict')
plt.legend()

plt.subplot(2,2,2)
plt.xlabel('volume(scaled)')
plt.ylabel('E/eV')
plot_x, plot_y = plot_sorted(new_vo_selec[1], new_va_selec[1])
plt.plot(plot_x, plot_y, label='mp'+mp_name[1]+' vasp data')
plt.scatter(new_vo_selec[1], new_ae_selec[1], marker='x', label='mp'+mp_name[1]+' ann predict')
plt.legend()

plt.subplot(2,2,3)
plt.xlabel('volume(scaled)')
plt.ylabel('E/eV')
plot_x, plot_y = plot_sorted(new_vo_selec[2], new_va_selec[2])
plt.plot(plot_x, plot_y, label='mp'+mp_name[2]+' vasp data')
plt.scatter(new_vo_selec[2], new_ae_selec[2], marker='x', label='mp'+mp_name[2]+' ann predict')
plt.legend()

plt.subplot(2,2,4)
plt.xlabel('volume(scaled)')
plt.ylabel('E/eV')
plot_x, plot_y = plot_sorted(new_vo_selec[3], new_va_selec[3])
plt.plot(plot_x, plot_y, label='mp'+mp_name[3]+' vasp data')
plt.scatter(new_vo_selec[3], new_ae_selec[3], marker='x', label='mp'+mp_name[3]+' ann predict')
plt.legend()

plt.show()

