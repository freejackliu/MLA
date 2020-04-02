#!usr/bin/env python

import shutil

real_index = 1
with open('GaN.train.asc','r') as f:
    for line in f:
        if line.split('.xsf')[0] != line:
            shutil.copy(line.replace('\n',''),'../new_xsfs/STRUCTURE_%05d.xsf'%real_index)
            real_index += 1

