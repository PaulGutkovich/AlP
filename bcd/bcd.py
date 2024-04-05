import os
os.environ['OPENBLAS_NUM_THREADS'] = '8'
os.environ['MKL_NUM_THREADS'] = '8'




import numpy as np
import scipy
import matplotlib.pyplot as plt
import wannierberri as wberri
from wannierberri import calculators as calc
from wannierberri.smoother import FermiDiracSmoother
import sys



parallel = wberri.Parallel(num_cpus=4, progress_step_percent=10)


print('loading...')
system=wberri.System_w90("../w90/alp",berry=True)


err = 0.05
fermi = 5.0231
print(fermi)
efermi = np.linspace(fermi * (1 - err), fermi * (1 + err), 101, True)


kwargs = dict(
   Efermi=efermi,
   kwargs_formula={"external_terms": False},
   smoother=FermiDiracSmoother(efermi, T_Kelvin= 10, maxdE=8)
)


calculators = {
   'berry_dipole_fermi_sea': calc.static.BerryDipole_FermiSea(**kwargs),
   'cumdos': calc.static.CumDOS(Efermi=efermi,)
}


grid = wberri.Grid(system, NK=30, NKFFT=2)


result_irr_grid = wberri.run(
   system,
   grid=grid,
   calculators=calculators,
   # parallel=parallel,
   print_Kpoints = False,
   use_irred_kpt = True,
   adpt_num_iter=50
)


ir_string = ["D_xx", "D_yy", "D_zz"]


data = result_irr_grid.results['berry_dipole_fermi_sea'].data
cumdos = result_irr_grid.results['cumdos'].data


fig, axs = plt.subplots(1, 2)
axs[0].plot(efermi, (data**2).sum(axis = (1, 2)))
axs[0].plot(efermi, np.trace(data, axis1 = 1, axis2 = 2))
axs[1].plot(efermi, cumdos)
plt.savefig('result.pdf')