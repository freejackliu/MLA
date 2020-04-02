#!/usr/bin/env python

import sys
import os
import shutil
from ase.io import *



def make_empty_dir(path, dirname):
    newdirpath = path + dirname
    if not os.path.exists(newdirpath):
        os.mkdir(newdirpath)
    else:
        shutil.rmtree(newdirpath)
        os.mkdir(newdirpath)
    return newdirpath
    

def main():
    vasp_input_path = '/vol7/home/ann/users/huanr/ann_envirset/vasp_input'
    opt_path        = os.getcwd()
    structure_name  = '/%s_structure'%opt_path.split('/')[-1]
    xsf_name        = '/correlation-xsfs'
    structure_path  = make_empty_dir(opt_path, structure_name)
    xsf_path        = make_empty_dir(opt_path, xsf_name)
    make_empty_dir(opt_path, '/%s_xsfs'%opt_path.split('/')[-1])

    get_xsf = open(opt_path + '/get_xsf.sh', 'w')
    get_xsf.write('#!/bin/bash\n')
    global xsf_index
    xsf_index = 0

    cmd = open(opt_path + '/auto.sh', 'w')
    cmd.write('#!/bin/bash\n')
    cmd.write('#SBATCH -p work -n 80 -J GaN-%s\n'%opt_path.split('/')[-1])
    cmd.write("EXE='yhrun vasp'\n")

    def read_traj_to_xsfs(itraj_file):
        confs = read(opt_path + '/traj/' + itraj_file, ':')
        for index, atoms in enumerate(confs):
            if index:
                global xsf_index
                traj_name = traj_file.split('.traj')[0] + '-%i'%index
                a_path = make_empty_dir(structure_path, '/' + traj_name)
                shutil.copy(vasp_input_path + '/INCAR', a_path)
                shutil.copy(vasp_input_path + '/POTCAR', a_path)
                shutil.copy(vasp_input_path + '/xml2xsfs', a_path)
                atoms.write(a_path+'/POSCAR', format = 'vasp')
                cmd.write('cd %s\n'%a_path)
                cmd.write("echo \" %i In directory: $PWD\"\n"%xsf_index)
                get_xsf.write('cd %s\n'%a_path)
                get_xsf.write("echo \" %i In directory: $PWD\"\n"%xsf_index)
                cmd.write('$EXE\n')
                get_xsf.write('xml2xsfs vasprun.xml\n')
                get_xsf.write('mv struct_00000.xsf %s' % xsf_path + '/%s.xsf\n' % traj_name)
                xsf_index += 1
                cmd.write('cd ..\n')
                get_xsf.write('cd ..\n')
    
    traj_files = os.listdir(opt_path + '/traj')
    for traj_file in traj_files:
        read_traj_to_xsfs(traj_file)


    os.system('chmod +x ./auto.sh')
    os.system('chmod +x ./get_xsf.sh')





if __name__ == "__main__":
    sys.exit(main())
