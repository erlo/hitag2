#!/bin/bash

######################################################
#
# Usage: ./checkLFSR <fichier1> <fichier2> <nbbits>
#
# Recherche des lignes qui ont les mêmes <nbbits>
# en commun entre 2 fichiers
#
######################################################

f1=$1
f2=$2
nbbits=$3

cat $f1 | cut -c1-${nbbits} | sort | uniq > ${f1}.temp
cat $f2 | cut -c1-${nbbits} | sort | uniq > ${f2}.temp
for code in $(comm -12 ${f1}.temp ${f2}.temp)
do
    echo "----- RESULTAT -----"
    echo -n "Fichier $f1: "
    grep -r $code $f1 | cut -d "|" -f 2
    echo -n "Fichier $f2: "
    grep -r $code $f2 | cut -d "|" -f 2
done
rm -f ${f1}.temp ${f2}.temp
