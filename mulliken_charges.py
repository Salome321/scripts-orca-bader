import numpy as np
import pandas as pd
import re
import sys
import os.path


#help function accessible via python mullikencharge_check.py --help (or -h) 
import argparse
parser = argparse.ArgumentParser(description='Pull Bader Charges from Output and Visualize in VMD file.')
parser.add_argument('ACF', type=str,
                    help='path to ACF.dat file')
parser.add_argument('GEOMETRY_PATH', type=str, 
                    help='path to GEO_OPT.xyz file')
args = parser.parse_args()

#input files check
ACF = args.ACF
if not (os.path.isfile(ACF)):
    print('\nERROR: Path to ACF.dat file does not exist.')
    print('Please check path: '+ACF)
    exit()

GEOMETRY = args.GEOMETRY_PATH
if not (os.path.isfile(GEOMETRY)):
    print('\nERROR: Path to GEO_OPT.xyz file does not exist.')
    print('Please check input path: '+GEOMETRY)
    exit()

#extract number of system atoms from geometry xyz

with open(GEOMETRY, 'r') as f:
    for count, line in enumerate(f):
        pass
    print(count)
    with open(ACF, 'r') as acf:
        with open('full_charges.txt', 'w') as charges:
            lines = acf.readlines()
            for line in lines:
                for iline in range(1,1+count):
                    charges.write(lines[iline])
                    print(iline)
charges.close()
acf.close()
f.close()
with open('full_charges.txt','r') as row_charges:
    with open('charges.txt','w') as column_charges:
        with open('labels.txt','w') as labels:
            lines =  row_charges.readlines()
            for line in lines[1:]:
                line = line.strip()
                columns = line.split()
                num = columns[0]
                atom = columns[1]
                labels.write(num)
                labels.write(atom)
                labels.write(' ')
                qa = columns[4]
                column_charges.write(qa)
                column_charges.write(' ')

labels.close()
column_charges.close()
row_charges.close()

vmdscript = open('vmdscript.txt','w')
vmdscript.write('#script to be run in vmd directly using an output file from a ACF.dat file and an geo_opt.xyz geometry file. To run in vmd use the command line command "source vmdscript.txt" during an open session of vmd within the directory which contains the relevant output and geometry files.\n')
vmdscript.write('mol new geo_opt.xyz\n')
vmdscript.write('set mol 0\n')
vmdscript.write('mol representation Lines 9\n')
vmdscript.write('set sel [atomselect $mol all]\n')
vmdscript.write('set nf [molinfo $mol get numframes]\n')
vmdscript.write('set fp [open charges.txt r]\n')
vmdscript.write('set line ""\n')
vmdscript.write('for { set i 0} { $i < $nf} {incr i} {\n')
vmdscript.write('  gets $fp line\n')
vmdscript.write('  $sel frame $i\n')
vmdscript.write('  $sel set beta $line\n')
vmdscript.write('} \n')
vmdscript.write('sleep 20\n')
vmdscript.write('close $fp \n')
vmdscript.write('set mol 0\n')
vmdscript.write('set i 0\n')
vmdscript.write('set all [atomselect $mol "all"]\n')
vmdscript.write('foreach atom [$all list] {\n')
vmdscript.write('  label add Atoms "$mol/$atom"\n')
vmdscript.write('  label textformat Atoms $i "%i%e:%b" \n')
vmdscript.write('  incr i\n')
vmdscript.write('} \n')
vmdscript.write('mol delrep 0 0\n')
vmdscript.write('mol color beta\n')
vmdscript.write('mol addrep top\n')
vmdscript.write('mol selupdate 0 top 1\n')
vmdscript.write('mol colupdate 0 top 1\n')
vmdscript.write('color scale method BWR\n')
vmdscript.write('mol scaleminmax top 0 -1 1\n')
vmdscript.write('color Display Background black\n')
vmdscript.write('color Labels Atoms white\n')
vmdscript.write('axes location off\n')

acf.close()
charges.close()
vmdscript.close()

#print output message
print('------')
print('text file with Bader charges by atom in a single line for vmd is written in:')
print('\tcharges.txt')
print('------')
print('text file with vmd script for visualizing Bader charges in a molecule. Please check to see if you need to manually adjust the file paths in this text script:')
print('\tvmdscript.txt')
