import numpy as np
import matplotlib
import mpl_toolkits.mplot3d
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size

import math
from ase import Atoms
from ase.calculators.emt import EMT
from aenet.calculator import ANNCalculator

N=1000
d_line = np.linspace(0.,6.5,N)
e_line_1=np.linspace(0.,6.5,N)
e_line_2=np.linspace(0.,6.5,N)
e_line_3=np.linspace(0.,6.5,N)
#e_line_4=np.linspace(0.,6.5,N)
calc=ANNCalculator(potentials={"Ga":"Ga.10t-10t.nn","N":"N.10t-10t.nn"})
#calc=ANNCalculator(potentials={"O":"O.15t-15t.nn"})

for i in range(N):
    molecule = Atoms('NGa', positions=[(0., 0., 0.), (0., 0., d_line[i])])
    molecule.set_calculator(calc)
    e_line_1[i]= molecule.get_potential_energy()
for i in range(N):
    molecule = Atoms('GaGa', positions=[(0., 0., 0.),(0., 0., d_line[i])])
    molecule.set_calculator(calc)
    e_line_2[i]= molecule.get_potential_energy()
for i in range(N):
    molecule = Atoms('NN', positions=[(0., 0., 0.),(0., 0., d_line[i])])
    molecule.set_calculator(calc)
    e_line_3[i]= molecule.get_potential_energy()
'''
for i in range(N):
    molecule = Atoms('GaN', positions=[(0., 0., 0.),(0., 0., d_line[i])])
    molecule.set_calculator(calc)
    e_line_4[i]= molecule.get_potential_energy()
'''
#plt.switch_backend("agg")
fig=plt.figure(figsize=(6,6))
ax=plt.subplot(111)
ax.plot(d_line,e_line_1,label='NGa')
ax.plot(d_line,e_line_2,label='GaGa')
ax.plot(d_line,e_line_3,label='NN')
#ax.plot(d_line,e_line_4,label='GaN')
plt.ylim((-18,5))
plt.xlabel('R')
plt.ylabel('E/eV')
plt.legend()
plt.show()

