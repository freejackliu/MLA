#!usr/bin/env python

import os
import shutil

energy = [-2.01360100, -7.82805860]
elements = ['Ga','N']
alloy = 'GaN'
xsf_paths = ['','']
xsf_paths[0] = '/vol7/home/ann/users/huanr/origin_ann/ann_005/04-ase/2md/2md_xsfs'
xsf_paths[1] = '/vol7/home/ann/users/huanr/origin_ann/ann_005/revasp/revasp_xsfs'
xsf_output_path = '/vol7/home/ann/users/huanr/origin_ann/ann_006/Xsfs'
generate_in_path = '/vol7/home/ann/users/huanr/origin_ann/ann_006/01-generate'

xsf_index = 1
for xsf_path in xsf_paths:
    if xsf_path != xsf_output_path:
        file_names = os.listdir(xsf_path)
        for file_name in file_names:
            shutil.copy(xsf_path+'/'+file_name,xsf_output_path+'/STRUCTURE_%05d.xsf'%xsf_index)
            xsf_index += 1
    else:
        file_names  = os.listdir(xsf_path)
        for file_name in file_names:
            shutil.move(xsf_path+'/'+file_name,xsf_output_path+'/STRUCTURE_%05d.xsf'%xsf_index)
            xsf_index += 1

generate = open(generate_in_path+'/generate.in','w')
generate.write('OUTPUT %s.train\n'%alloy)
generate.write('\n')
generate.write('TYPES\n')
generate.write('%d\n'%len(elements))
generate.write('%-3s' % elements[0] + '%.8f' % energy[0] + '  | eV\n')
generate.write('%-3s' % elements[1] + '%.8f' % energy[1] + '  | eV\n')
generate.write('\n')
generate.write('SETUPS\n')
generate.write('%-3s' % elements[0] + '%3s.fingerprint.stp\n' % elements[0])
generate.write('%-3s' % elements[1] + '%3s.fingerprint.stp\n' % elements[1])
generate.write('\n')
generate.write('FILES\n')
generate.write('%d\n' % (xsf_index-1))
for i in range(xsf_index-1):
    generate.write('../Xsfs/STRUCTURE_%05d.xsf\n'%(i+1))

