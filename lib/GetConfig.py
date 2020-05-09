#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymatgen import MPRester
from itertools import combinations as cb
import os
import copy
import argparse


class GetConfig:
    def __init__(self,symbols):
        self.symbols = symbols
        self.filenames = []
        self.m = MPRester()
        self.pathnow = os.getcwd()
    
     
    def write_to(self,source_list,source_tag):        
        for index,struct in enumerate(source_list):
            struct.to(filename=source_tag+'/'+self.filenames[index])

    
    def get_structure_list(self, *args):
        structures = []       
        # single-element
        if not args[0]:
            for symbol in self.symbols:
                sg_structures = self.m.get_structures(symbol)
                self.filenames.extend(_getFileNameFromList(len(sg_structures),symbol))
                structures.extend(sg_structures)
        # compound
        if len(self.symbols) > 1:
            for i in range(len(self.symbols)):
                if i>=1:
                    i_combs = list(cb(self.symbols,i+1))
                    for index,comb in enumerate(i_combs):
                        chem_str = '-'.join(list(comb))
                        cp_structures = self.m.get_structures(chem_str)
                        self.filenames.extend(_getFileNameFromList(len(cp_structures),chem_str))
                        structures.extend(cp_structures)                      
        return structures


def _getFileNameFromList(listlen,symbol_comb):
    namelist = []
    for iindex in range(listlen):
        namelist.append(symbol_comb+'%03d'%iindex+'.cif')
    return namelist
    

def mkEmptyDir(path): 
    pathcopy = copy.copy(path)       
    if not os.path.exists(path):
        os.mkdir(path)
        print('Files will be stored at %r'%path)
        return path
    else:
        ic = 1
        while os.path.exists(pathcopy):
            pathcopy = path+'(%i)'%ic
            ic += 1
        os.mkdir(pathcopy)
        print('Files will be stored at %r'%path)
        return pathcopy
    
                        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="""Get original structures from Materials Project""",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--symbols','-s',required=True,nargs='+',help='Arguments for elements. e.g., python GetConfig.py -s Cu Zr')
    parser.add_argument('--onlycompound','-oc',action='store_true',help='With this flag,the code only gets structures of compounds')
    args = parser.parse_args()
    symbols = args.symbols
    oc_flag = args.onlycompound    
    path = os.getcwd()+'/'+''.join(symbols)
    newpath = mkEmptyDir(path)
    InitialConfig = GetConfig(symbols)
    structures = InitialConfig.get_structure_list(oc_flag)
    InitialConfig.write_to(structures,newpath)
    
    