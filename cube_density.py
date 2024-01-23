# %%
from QChemTool.QuantumChem.Classes.density import DensityGrid as density
import os

# %%
dens_anion= density(None,None,None,None)
dens_cation= density(None,None,None,None)
dens_neutral= density(None,None,None,None)

# %%
current_directory = os.getcwd()
for path, currentDirectory, files in os.walk(current_directory):
   for file in files:
       if file.endswith("_anion.cube"):
           dens_anion.import_cub(os.path.join(path, file))
           file_name = file
       if file.endswith("_neutral.cube"):
           dens_neutral.import_cub(os.path.join(path, file))

# %%
print(file_name)
file_name2 = file_name[:-11]
print(file_name2)
output_name = file_name2 + '_out.cube'
print(output_name)

# %%
dens_final = dens_anion.copy()
dens_final.data = dens_anion.data-dens_neutral.data

# %%
# os.chdir('../') save the cub the cube file in the parent directory
dens_final.output(output_name)

