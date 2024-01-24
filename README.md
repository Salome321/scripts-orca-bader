# Scripts for Orca and Bader
Scripts to operate Orca and initiate Bader charge calculations. Orca is used to perform the geometry optimiations of molecules, and calculate the single point energy of their anion, cation and neutral forms. Bader is used to show the distribution of the extra electron aquired by the anion associated with each atom in the molecule.

## 1. split.sh
This script splits a txt file of coordinates into individual txt files with the coordinates of each molecules, by using the separator $$$$ between the coordinates in the original file\
Run ./split.sh <name of coordinate file>
Splits coordinates into 4 parts (part1 part2 part3 part4 directories), inside each directory is one fourth of the coordinates files, named file1.xyz, file2.xyz, file10.xyz etc.\
The coordinate files end with .xyz, you might need to remove the .xyz ending that has been added to some other files (eg. inner_run.sh.xyz)

## 2. outer_run.sh
This script creates directories for each coordinate files (file1 file2 file10 etc.) directories), copies the relevant scripts inside and runs inner_run.sh\
Make sure all xyz files you would like to run in a batch are in the same directory (eg. part1 directory)\
Edit relevant file paths in outer_run.sh\
Run ./outer_run.sh

## 3. inner_run.sh
This script automates the geometry optimisation and single point calculations of neutral, anion, cation with Orca. It also adds these values to the all_energies.txt in the parent directory.\
This script is run in a directory countaining only one xyz coordinate file. Make sure that geo_opt.inp, sp_neutral.inp, sp_anion.inp, sp_cation.inp are also copied in the directory (this is already done if outer_run.sh was run).

## 4. cube_density.sh
This scrpit should be run outside the coordinate files directories.\
Edit relevant file path.\
It automates bader and local_charges.py:\
It uses an *out.cube file as an input for bader charges calculations.\
It copies bader in each directory and runs bader charges on this out.cube file.\
It copies local_charges.py in each directory and runs it to create scripts for visualisation of Bader and Mulliken charges in vmd.

### 4.1. bader 
This program developed by Henkelman Group outputs the total charge associated with each atom, and the zero flux surfaces defining the Bader volumes.
Calculates bader charges.\
Run ./bader -c bader <cube file> -v\
Returns ACF.dat, AVF.dat and BCF.dat files
- W. Tang, E. Sanville, and G. Henkelman A grid-based Bader analysis algorithm without lattice bias, J. Phys.: Condens. Matter 21, 084204 (2009).

### 4.2. local_charges.py
This scripts creates visualisation vmd scripts for Bader and Mulliken.\
Run python local_charges.py <sp file with Mulliken charges eg. sp_enutral.out> <dat file with Bader charges eg. ACF.dat> <coordinate file eg. geo_opt.xyz>\
Creates bader_vmdscript.txt. Visualise in vmd by typing source bader_vmdscript.txt.

