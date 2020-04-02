#!usr/bin/env python

import os
import shutil
import random

elements = ['Ga','N']
ann_path = os.getcwd()
xsf_path = ann_path + '/new_xsfs'
md_input_path = ann_path + '/04-ase/md_input_xsf'
xsf_names = os.listdir(xsf_path)
xsf_number = len(xsf_names)

rate = 0.02
cn = int(xsf_number*rate)

random_choices = random.sample(range(1,xsf_number+1),cn)

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


for rc in random_choices:
    if gan_select(xsf_path + '/STRUCTURE_%05d.xsf'%rc):
        shutil.copy(xsf_path + '/STRUCTURE_%05d.xsf'%rc, md_input_path + '/STRUCTURE_%05d.xsf'%rc)
