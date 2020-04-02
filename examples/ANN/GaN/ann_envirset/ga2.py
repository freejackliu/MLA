import numpy as np
import matplotlib
import mpl_toolkits.mplot3d
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size

import math
from ase import Atoms
from ase.calculators.emt import EMT
from aenet.calculator import ANNCalculator

N=200
d_line = np.linspace(0,6.5,N)
e_line=np.linspace(0,6.5,N)


calc=ANNCalculator(potentials={"Ga":"Ga.10t-10t.nn","N":"N.10t-10t.nn"})
#calc=ANNCalculator(potentials={"O":"O.15t-15t.nn"})

for i in range(N):
    molecule = Atoms('2Ga', positions=[(0., 0., 0.), (0., 0., d_line[i])])

    molecule.set_calculator(calc)
    e_line[i]= molecule.get_potential_energy()


#plt.switch_backend("agg")
fig=plt.figure(figsize=(6,6))
ax=plt.subplot(111)
ax.plot(d_line,e_line,label='Ga-Ga')
plt.legend()
plt.xlabel('r/A')
plt.ylabel('E/eV')
plt.show()
