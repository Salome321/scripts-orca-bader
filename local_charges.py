import numpy as np
import pandas as pd
import re
import sys
import os.path


#help function accessible via python charges_check.py --help (or -h)
#input files are: sp_neutral.out (or anion/cation) ACF.dat geo_opt.xyz (or other geometry files)
import argparse
parser = argparse.ArgumentParser(description='Pull Mulliken and Bader Charges from Output and Visualize in VMD.')
parser.add_argument('SP_OUT', type=str,
                    help='path to SINGLE POINT OUTPUT file')
parser.add_argument('BADER_OUT', type=str,
                    help='path to BADER CHARGE OUTPUT file')
parser.add_argument('GEOMETRY_PATH', type=str, 
                    help='path to INPUT.xyz file')
args = parser.parse_args()

#input files check
SP_OUT = args.SP_OUT
if not (os.path.isfile(SP_OUT)):
    print('\nERROR: Path to SINGLE POINT OUTPUT file does not exist.')
    print('Please check path: '+SP_OUT)
    exit()

BADER_OUT = args.BADER_OUT
if not (os.path.isfile(BADER_OUT)):
    print('\nERROR: Path to BADER CHARGE OUTPUT file does not exist.')
    print('Please check path: '+BADER_OUT)
    exit()

GEOMETRY = args.GEOMETRY_PATH
if not (os.path.isfile(GEOMETRY)):
    print('\nERROR: Path to INPUT.xyz file does not exist.')
    print('Please check input path: '+GEOMETRY)
    exit()

#extract number of system atoms from geometry xyz

with open(GEOMETRY, 'r') as f:
    for count, line in enumerate(f):
        pass
    print(count)
    with open(SP_OUT, 'r') as sp_out:
        with open('full_mulliken_charges.txt', 'w') as m_charges:
            lines = sp_out.readlines()
            for line in lines:
                if line.find('ATOM       NA') != -1:
                    i = lines.index(line)
                    for iline in range(i,i+count):
                        m_charges.write(lines[iline])
                        print(iline)
    with open(BADER_OUT, 'r') as bader_out:
        with open('full_bader_charges.txt','w') as b_charges:
            lines = bader_out.readlines()
            for line in range(0,count+1):
                b_charges.write(lines[line])
                print(line)
            
b_charges.close()
m_charges.close()
sp_out.close()
f.close()
with open('full_mulliken_charges.txt','r') as m_row_charges:
    with open('mulliken_charges.txt','w') as m_column_charges:
        lines =  m_row_charges.readlines()
        for line in lines[1:]:
            line = line.strip()
            columns = line.split()
            qa = columns[4]
            m_column_charges.write(qa)
            m_column_charges.write(' ')
m_column_charges.close()
m_row_charges.close()

with open('full_bader_charges.txt','r') as b_row_charges:
    with open('bader_charges.txt','w') as b_column_charges:
        lines = b_row_charges.readlines()
        for line in lines[2:]:
            line = line.strip()
            columns = line.split()
            bq = columns[4]
            b_column_charges.write(bq)
            b_column_charges.write(' ')
b_column_charges.close()
b_row_charges.close()

vmdscript = open('mulliken_vmdscript.txt','w')
vmdscript.write('#script to be run in vmd directly using an output file from a single point calculation and an geo_opt.xyz geometry file. To run in vmd use the command line command "source vmdscript.txt" during an open session of vmd within the directory which contains the relevant output and geometry files.\n')
vmdscript.write('mol new geo_opt.xyz\n')
vmdscript.write('set mol 0\n')
vmdscript.write('mol representation Lines 9\n')
vmdscript.write('set sel [atomselect $mol all]\n')
vmdscript.write('set nf [molinfo $mol get numframes]\n')
vmdscript.write('set fp [open mulliken_charges.txt r]\n')
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

b_vmdscript = open('bader_vmdscript.txt','w')
b_vmdscript.write('#script to be run in vmd directly using an output file from a single point calculation and an geo_opt.xyz geometry file. To run in vmd use the command line command "source vmdscript.txt" during an open session of vmd within the directory which contains the relevant output and geometry files.\n')
b_vmdscript.write('mol new geo_opt.xyz\n')
b_vmdscript.write('set mol 0\n')
b_vmdscript.write('mol representation Lines 9\n')
b_vmdscript.write('set sel [atomselect $mol all]\n')
b_vmdscript.write('set nf [molinfo $mol get numframes]\n')
b_vmdscript.write('set fp [open bader_charges.txt r]\n')
b_vmdscript.write('set line ""\n')
b_vmdscript.write('for { set i 0} { $i < $nf} {incr i} {\n')
b_vmdscript.write('  gets $fp line\n')
b_vmdscript.write('  $sel frame $i\n')
b_vmdscript.write('  $sel set beta $line\n')
b_vmdscript.write('} \n')
b_vmdscript.write('sleep 20\n')
b_vmdscript.write('close $fp \n')
b_vmdscript.write('set mol 0\n')
b_vmdscript.write('set i 0\n')
b_vmdscript.write('set all [atomselect $mol "all"]\n')
b_vmdscript.write('foreach atom [$all list] {\n')
b_vmdscript.write('  label add Atoms "$mol/$atom"\n')
b_vmdscript.write('  label textformat Atoms $i "%i%e:%b" \n')
b_vmdscript.write('  incr i\n')
b_vmdscript.write('} \n')
b_vmdscript.write('mol delrep 0 0\n')
b_vmdscript.write('mol color beta\n')
b_vmdscript.write('mol addrep top\n')
b_vmdscript.write('mol selupdate 0 top 1\n')
b_vmdscript.write('mol colupdate 0 top 1\n')
b_vmdscript.write('color scale method BWR\n')
b_vmdscript.write('mol scaleminmax top 0 -0.01 0.2\n')
b_vmdscript.write('color Display Background black\n')
b_vmdscript.write('color Labels Atoms white\n')
b_vmdscript.write('axes location off\n')


sp_out.close()
bader_out.close()
vmdscript.close()
b_vmdscript.close()
#print output message
print('------')
print('text file with Mulliken charges by atom written in:')
print('\tmulliken_charges.txt')
print('------')
print('text file with vmd script for visualizing Mulliken charges in a molecule. Please check to see if you need to manually adjust the file paths in this text script:')
print('\tmulliken_vmdscript.txt')
print('------')
print('text file with Bader charges by atom written in:')
print('\tbader_charges.txt')
print('------')
print('text file with vmd script for visualizing Bader charges in a molecule. Please check to see if you need to manually adjust the file paths in this text script:')
print('\tbader_vmdscript.txt')
