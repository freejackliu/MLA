#!/usr/bin/env python

import sys
import os
from math import *
import numpy as np
import matplotlib.pyplot as plt
import shutil

elements=['Ga', 'N']

def get_g_parameters(raw):
    rawsp = raw.split()
    #print(rawsp)
    if len(rawsp):
        if rawsp[0] == 'G=2':
            g2_pa = [[],0,0,0,0]
            g2_pa[0] = [rawsp[1].replace("type2=", "")]
            g2_pa[1] = float(rawsp[2].replace("eta=", ""))
            g2_pa[2] = float(rawsp[3].replace("Rs=", ""))
            g2_pa[3] = float(rawsp[4].replace("Rc=", ""))
            return g2_pa
        elif rawsp[0] == 'G=4':
            g4_pa = [[],0,0,0,0]
            g4_pa[0] = [rawsp[1].replace("type2=", ""),
                        rawsp[2].replace("type3=", "")]
            g4_pa[1] = float(rawsp[3].replace("eta=", ""))
            g4_pa[2] = float(rawsp[5].replace("lambda=", ""))
            g4_pa[3] = float(rawsp[7].replace("zeta=", ""))
            g4_pa[4] = float(rawsp[8].replace("Rc=", ""))
            return g4_pa


def read_stp(ipath = os.getcwd()):
    para = {}
    for name in os.listdir(ipath):
        for element in elements:
            if name.split('.')[-1] == 'stp' and name.split('.')[0] == element:
                with open(ipath + '/' + name, 'r') as stp:
                    gp = [get_g_parameters(line) for line in stp]
                    gp = np.delete(gp, range(13))
                    para[element] = gp
    return para


def read_xsf(ipath):
    with open(ipath, 'r') as xsf:
        print(ipath)
        corxyz   = []
        elem_add = []
        for line in xsf:
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
        corxyz = np.array(corxyz)
        corxyz = corxyz.T
        return corxyz, elem_add


def coscal(r1, r2, r3):
    # r1(r2) stands the distance between center atom and neighbor atom
    # r3 stands the distance between the two neighbor atoms
    cosval = (r1*r1 + r2*r2 - r3*r3)/(2*r1*r2)
    return cosval


def compute_squared_edm(x):
    x = np.abs(x)
    m, n = x.shape
    g = np.dot(x.T, x)
    h = np.tile(np.diag(g), (n, 1))
    return h + h.T - 2*g


def compute_g2(ir_2, ipara, icenter, ielem, rcmin=0.75):
    g2     = []
    iir_2  = np.zeros((len(ir_2), len(ir_2)))
    elem   = ipara[0][0]
    eta_g2 = ipara[1]
    rs     = ipara[2]
    rc     = ipara[3]
    for j_1 in range(len(ir_2)):
        if ielem[j_1] == icenter:
            for j_2 in range(len(ir_2)):
                if rcmin * rcmin <= ir_2[j_1][j_2] <= rc * rc and ielem[j_2] == elem:
                    ya = sqrt(ir_2[j_1][j_2])
                    x = 1 - ya / rc
                    iir_2[j_1][j_2] = tanh(x) * tanh(x) * tanh(x) * exp(-eta_g2 * (ya - rs) * (ya - rs))
            g2.append(iir_2[j_1].sum())
    return g2


def compute_g4(ir_2, ipara, icenter, ielem, rcmin=0.75):
    g4     = []
    iir_2  = np.tile(ir_2, 1)
    elem   = ipara[0]
    eta_g4 = ipara[1]
    lamda  = ipara[2]
    kec    = ipara[3]
    rc     = ipara[4]
    for j_1 in range(0, len(ir_2)):
        if ielem[j_1] == icenter:
            x = []
            # get fixed components
            for j_2 in range(0, len(ir_2)):
                if rcmin * rcmin <= ir_2[j_1][j_2] <= rc * rc:
                    a = sqrt(ir_2[j_1][j_2])
                    x.append([a, j_2])
                    iir_2[j_1][j_2] = \
                        tanh(1 - a / rc) * tanh(1 - a / rc) * tanh(1 - a / rc) * exp(-eta_g4 * ir_2[j_1][j_2])
                else:
                    iir_2[j_1][j_2] = 0
            # neighbors
            if len(x) > 1:
                r_add = np.zeros((len(x) * (len(x) - 1) // 2, 3))
                g_add = np.zeros((len(x) * (len(x) - 1) // 2, 3))
                im = 0
                flag = 0
                while im != len(x) - 1:
                    if ielem[x[im][1]] == elem[0]:
                        for j_2 in range(im, len(x) - 1):
                            if ielem[x[j_2 + 1][1]] == elem[1]:
                                atem = sqrt(ir_2[x[j_2 + 1][1]][x[im][1]])
                                if  rcmin < atem < rc:
                                    r_add[flag, :] = [x[im][0], x[j_2 + 1][0], atem]
                                    g_add[flag, :] = [iir_2[j_1][x[j_2 + 1][1]], iir_2[j_1][x[im][1]],
                                                      tanh(1 - atem / rc) * tanh(1 - atem / rc) * tanh(
                                                          1 - atem / rc) * exp(
                                                          -eta_g4 * ir_2[x[j_2 + 1][1]][x[im][1]])]
                                    flag += 1
                    im += 1
                # delete redundant rows in array
                if flag < len(r_add):
                    r_add = np.delete(r_add, range(flag, len(r_add)), 0)
                    g_add = np.delete(g_add, range(flag, len(g_add)), 0)
                cosceta = coscal(r_add[:, 0], r_add[:, 1], r_add[:, 2])
                fin = g_add[:, 0] * g_add[:, 1] * g_add[:, 2] * pow(2, (1 - kec)) * np.power(1 + lamda * cosceta, kec)
                km = fin.sum()
                g4.append(km)
            else:
                g4.append(0)
    return g4


def elem_global_fingerprint(ig2,ig4):
    ig = np.concatenate((ig2.sum(axis=1), ig4.sum(axis=1)))
    return ig



def main():
    p = read_stp('/vol7/home/ann/users/huanr/ann_fingerprint')

    xsf_path = os.getcwd()+'/04-ase/md/correlation-xsfs'
    xsf_ori_path = os.getcwd()+'/04-ase/md_input_xsf'
    xsf_output_path = os.getcwd()+'/04-ase/md/md_xsfs'
    xsf_ori_names = os.listdir(xsf_ori_path)
    xsf_files = os.listdir(xsf_path)
    xsf_total_number = len(xsf_files)
    xsf_ori_number = len(xsf_ori_names)
    xsf_unit = int(xsf_total_number/xsf_ori_number)+1 

    gf_cov_se = []
    for xsf_ori_name in xsf_ori_names:
        xsf_cor_app = [xsf_ori_name]*xsf_unit
        for i in range(xsf_unit):
            if i:
                xsf_cor_app[i]=xsf_path+'/nvt_'+xsf_cor_app[i].split('.xsf')[0]+'-%i.xsf'%i
            else:
                xsf_cor_app[i]=xsf_ori_path+'/'+xsf_cor_app[i]
        gf_dict = {}
        for xsf in range(len(xsf_cor_app)):
            xyz, atoms_elems = read_xsf(xsf_cor_app[xsf])
            r_2 = compute_squared_edm(xyz)
            r = np.sqrt(r_2)
            # print(r)
            # print('**************************************')
            global_finger = []
            for elem in elements:
                ps_xsf = p[elem]
            #   print(elem)
                g2 = []
                g4 = []
                for p_xsf in ps_xsf:
                    if len(p_xsf[0]) == 1:
                        g2.append(compute_g2(r_2, p_xsf, elem, atoms_elems))
                    else:
                        g4.append(compute_g4(r_2, p_xsf, elem, atoms_elems))
                g2 = np.array(g2)
                g4 = np.array(g4)
                global_finger.append(elem_global_fingerprint(g2, g4))
            for iin in range(len(global_finger) - 1):
                gf = np.concatenate((global_finger[iin], global_finger[iin + 1]))
            # print(gf)
            gf_dict[xsf] = gf
            # print('\n')

        xsf_number = xsf_unit
        gf_sorted = np.zeros((len(gf), xsf_number))
        for ii in range(xsf_number):
            gf_sorted[:, ii] = gf_dict[ii]
        '''
        covmat = np.cov(gf_sorted, rowvar=False)
        gf_cov = np.zeros(xsf_number)
        for j in range(len(covmat)):
            gf_cov[j] = covmat[0][j] / sqrt(covmat[0][0]) / sqrt(covmat[j][j])
        gf_cov_se.append(gf_cov)
        '''
        gf_cov = np.zeros(xsf_number)
        gf_mean = np.mean(gf_sorted,axis=0)
        gf_std = np.std(gf_sorted,axis=0)
        gf_tmp = gf_sorted - gf_mean

        for i in range(xsf_number):
            gf_sum = 0 
            for j in range(len(gf_sorted)):
                gf_sum += gf_tmp[:,0][j]*gf_tmp[:,i][j]
            gf_cov[i] = gf_sum/len(gf_sorted)/gf_std[0]/gf_std[i]
            if gf_cov[i] < 0.85:
                shutil.copy(xsf_cor_app[i],xsf_output_path)
        gf_cov_se.append(gf_cov)
    '''    
    d_line = np.zeros(xsf_unit)
    for j in range(xsf_unit):
        d_line[j] = j*0.4
    fig = plt.figure(figsize=(6,6))
    ax = plt.subplot(111)
    for index, cov_line in enumerate(gf_cov_se):
        ax.scatter(d_line,cov_line,label='%s'%(xsf_ori_names[index].split('.xsf')[0]))
    plt.xlabel('MD Time/ps')
    plt.ylabel('Correlation')
    plt.legend()
    plt.savefig('correlation_new.png')
    plt.show()
    '''



if __name__ == "__main__":
    sys.exit(main())
