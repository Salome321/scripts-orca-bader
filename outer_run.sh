#!/bin/bash

for f in /scratch/salome/metabolites_orca/scripts_for_orca//*xyz
do
	(mkdir "${f%.xyz}"
	cp inner_run.sh "${f%.xyz}"
	cp *.inp "${f%.xyz}"
	cp $f "${f%.xyz}"/input.xyz
	cd "${f%.xyz}"
	./inner_run.sh
	)
done

