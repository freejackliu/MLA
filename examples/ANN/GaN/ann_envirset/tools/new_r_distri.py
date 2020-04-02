#!/usr/bin/env python

import os
import numpy as np
import matplotlib.pyplot as plt


ipath = os.getcwd()+'/new_xsfs'
elements = ['Ga', 'N']
number = 200
interval = 0.1
range_list = []
d_line = np.zeros(number)
gaga_line = np.zeros(number)
gan_line = np.zeros(number)
nn_line = np.zeros(number)

for i in range(number):
    d_line[i] = i*interval+0.05
    range_add = [i*interval,(i+1)*interval]
    range_list.append(range_add)


def compute_squared_edm(x):
    x = np.abs(x)
    m, n = x.shape
    g = np.dot(x.T, x)
    h = np.tile(np.diag(g), (n, 1))
    return h + h.T - 2*g


def r_distribution(r,ir_d):
    for index, nu in enumerate(range_list):
        if nu[0] < r <= nu[1]:
            ir_d[index] += 1


filenames = os.listdir(ipath)
for filename in filenames:
    file_path = ipath + '/'+filename
    with open(file_path, 'r') as fr:
        print(file_path)
        elem_add = []
        corxyz = []
        ga_nu = 0
        n_nu = 0
        for line in fr:
            line = line.split()
            if line:
                corxyz_add = []
                for c_1 in elements:
                    if line[0] == c_1:
                        coor = line[1:4]
                        elem_add.append(c_1)
                        for cor in coor:
                            corxyz_add.append(float(cor))
                if len(corxyz_add) != 0:
                    corxyz.append(corxyz_add)
        for elem in elem_add:
            if elem == elements[0]:
                ga_nu += 1
            else:
                n_nu += 1
        if n_nu != len(elem_add) and ga_nu != len(elem_add):
          corxyz = np.array(corxyz)
          corxyz = corxyz.T
          r_2 = compute_squared_edm(corxyz)
          r_2 = np.sqrt(r_2)
    
          for m in range(len(r_2)-1):
            for n in range(m+1,len(r_2)):
                if elem_add[m] == elements[0] and elem_add[n] == elements[0]:
                    r_distribution(r_2[m][n], gaga_line)
                elif (elem_add[m] == elements[0] and elem_add[n] == elements[1]) or (elem_add[m] == elements[1] and elem_add[n] == elements[0]):
                    r_distribution(r_2[m][n], gan_line)
                elif elem_add[m] == elements[1] and elem_add[n] == elements[1]:
                    r_distribution(r_2[m][n], nn_line)

for i in range(number):
    gaga_line[i] = 100*gaga_line[i]/np.sum(gaga_line)
    gan_line[i] = 100*gan_line[i]/np.sum(gan_line)
    nn_line[i] = 100*nn_line[i]/np.sum(nn_line)


plt.figure(figsize=(6, 6))
ax=plt.subplot(111)
ax.plot(d_line, gaga_line, label='Ga-Ga')
ax.plot(d_line, gan_line, label='Ga-N')
ax.plot(d_line, nn_line, label='N-N')
plt.xlabel('R')
plt.ylabel('Frequency of occurrence(%)')
plt.legend()
plt.savefig('r_distribution.png')
plt.show()
