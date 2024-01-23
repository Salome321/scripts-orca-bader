#!/bin/bash

#this sets the comman to quit the run entirely if there is a non-zero exit code at any point
set -e

#loading orca path
module load openmpi/4.0.1/gcc-8.3.0

export ORCA_PATH=/share/lcbcsrv5/lcbcdata/antalik/programs/orca_5.0.3_rel/

#run first geo optimizations and then the three single points
$ORCA_PATH/orca geo_opt.inp > geo_opt.out
wait
$ORCA_PATH/orca sp_neutral.inp > sp_neutral.out
wait
$ORCA_PATH/orca sp_anion.inp > sp_anion.out
wait
$ORCA_PATH/orca sp_cation.inp > sp_cation.out
wait

#grab the id of each molecule and the single point energies
sed -n '2,2'p input.xyz > id
grep "FINAL SINGLE POINT" sp_neutral.out > energy_n
grep "FINAL SINGLE POINT" sp_anion.out > energy_a
grep "FINAL SINGLE POINT" sp_cation.out > energy_c
wait

awk '{print $5}' energy_n > final_energy_n
awk '{print $5}' energy_a > final_energy_a
awk '{print $5}' energy_c > final_energy_c
wait

#paste id and energies into one line 
paste -d "," id final_energy_n final_energy_a final_energy_c > final_energies
mv final_energies "$(cat id)_final_energies"
cat "$(cat id)_final_energies" >> ../all_energies

mv neutral.cube "$(cat id)_neutral.cube"
mv anion.cube "$(cat id)_anion.cube" 
mv cation.cube "$(cat id)_cation.cube"
