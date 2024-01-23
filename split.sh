#!/bin/bash

file_1=$1

awk '/\$$$$/{close(f); f="file" ++c;next} {print>f;}' $1

find . -type f -exec mv '{}' '{}'.xyz \; 

mkdir 0_2
mkdir 3_4
mkdir 5_7
mkdir 8_9

mv file*0.xyz 0_2
mv file*1.xyz 0_2
mv file*2.xyz 0_2

mv file*3.xyz 3_4
mv file*4.xyz 3_4

mv file*5.xyz 5_7
mv file*6.xyz 5_7
mv file*7.xyz 5_7

mv file*8.xyz 8_9
mv file*9.xyz 8_9

mv ${1}.xyz $1
mv split.sh.xyz split.sh
