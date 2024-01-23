#!/bin/bash

for dir in /scratch/salome/metabolites_orca/scripts_for_orca/metabolites/file*/
do
    cd $dir
    cp ../cube_density.py .
    python cube_density.py
    wait
    cp ../bader .
    ./bader -c bader *_out.cube -v
    wait
    cp ../local_charges.py .
    python local_charges.py sp_neutral.out ACF.dat geo_opt.xyz
done

