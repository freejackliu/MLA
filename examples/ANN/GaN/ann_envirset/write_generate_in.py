#!/usr/bin/env python
# -*- coding: gbk -*-

import sys
import os
import shutil
import numpy as np


elements = ['Ga', 'N']
alloy = 'GaN'
energy = [-2.01360100, -7.82805860]


def rename_xsf(index):
    xsf_name = 'STRUCTURE_' + '%05d.xsf' % index
    return xsf_name


def compute_squared_edm(x):
    x = np.abs(x)
    m, n = x.shape
    g = np.dot(x.T, x)
    h = np.tile(np.diag(g), (n, 1))
    return h + h.T - 2*g


def rmin_del(info):
    with open(info, 'r') as fr:
        if os.path.getsize(info):
            corxyz = []
            for line in fr:
                line = line.split()
                if line:
                    corxyz_add = []
                    for c_1 in elements:
                        if line[0] == c_1:
                            coor = line[1:4]
                            for cor in coor:
                                corxyz_add.append(float(cor))
                    if len(corxyz_add) != 0:
                        corxyz.append(corxyz_add)
            corxyz = np.array(corxyz)
            corxyz = corxyz.T
            r_2 = compute_squared_edm(corxyz)
            elmflag = 1
            for m in range(len(r_2) - 1):
                for n in range(m + 1, len(r_2)):
                    if r_2[m][n] <= 0.9:
                        elmflag = 0
            return elmflag
        else:
            return 0


def combine_xsfs(path,newpath,xi):

    path_array = os.listdir(path)
    
    xsf_index  = xi
    for i in range(len(path_array)):
        path_mayxsf = path + '/' + path_array[i]
        print("*********************************************************")
        print("In directory:%s" % path_mayxsf)
        if not os.system('cd %s' % path_mayxsf):
            path_mayxsf_s = path_array[i].split('_')
            if path_mayxsf_s[0] and (path_mayxsf_s[-1]=='xsfs' or path_mayxsf_s[-1]=='xsf'):
                print("Source XSF dir found")
                path_real = os.listdir(path_mayxsf)
                for j in range(len(path_real)):
                    info_path = os.path.join(path_mayxsf, path_real[j])
                    if path_real[j].split('.')[-1] == 'xsf' and rmin_del(info_path):
                        newname_xsf = rename_xsf(xsf_index)
                        shutil.copy(path_mayxsf + '/' + path_real[j], newpath + '/Xsfs/' + newname_xsf)
                        xsf_index += 1
            else:
                print("Not a XSF dir")
    return xsf_index


xsf_index    = 1
xsf_path     = os.getcwd()
ann_index    = int((xsf_path.split('/')[-1]).split('_00')[-1])+1
new_ann_path = xsf_path.replace('ann_%03d'%(ann_index-1),'ann_%03d'%ann_index)


if not os.path.exists(new_ann_path):
    os.mkdir(new_ann_path)
else:
    shutil.rmtree(new_ann_path)
    os.mkdir(new_ann_path)


if not os.path.exists(new_ann_path + '/Xsfs'):
    shutil.copytree(xsf_path + '/new_xsfs',new_ann_path + '/Xsfs')
else:
    shutil.rmtree(new_ann_path + '/Xsfs')
    shutil.copytree(xsf_path + '/new_xsfs',new_ann_path + '/Xsfs')

'''
for xsf_ori in os.listdir(xsf_path+'/new_xsfs'):
    shutil.copy(xsf_path+'/new_xsfs/'+xsf_ori,new_ann_path + '/Xsfs')
'''

f = os.listdir(xsf_path+'/04-ase')
tmp_path = []
index_li = []
for dirname in f:
    if dirname.split('md')[0] != dirname or dirname.split('opt')[0] != dirname:
        tmp_path.append(xsf_path+'/04-ase/'+dirname)
        index_li.append(0)
index_li.append(0)
index_li[0] = len(os.listdir(xsf_path+'/new_xsfs'))+1


for ind, pth in enumerate(tmp_path):
    index_li[ind+1] = combine_xsfs(pth,new_ann_path,index_li[ind])
   
print(index_li)

generate = open(new_ann_path + '/generate.in', 'w')
generate.write('OUTPUT %s.train\n' % alloy)
generate.write('\n')
generate.write('TYPES\n')
generate.write('%d\n' % len(elements))
generate.write('%-3s' % elements[0] + '%.8f' % energy[0] + '  | eV\n')
generate.write('%-3s' % elements[1] + '%.8f' % energy[1] + '  | eV\n')
generate.write('\n')
generate.write('SETUPS\n')
generate.write('%-3s' % elements[0] + '%3s.fingerprint.stp\n' % elements[0])
generate.write('%-3s' % elements[1] + '%3s.fingerprint.stp\n' % elements[1])
generate.write('\n')
generate.write('FILES\n')
generate.write('%d\n' % (index_li[-1]-1))
for i in range(index_li[-1]-1):
    generate.write('../Xsfs/STRUCTURE_' + '%05d.xsf\n' % (i+1))




