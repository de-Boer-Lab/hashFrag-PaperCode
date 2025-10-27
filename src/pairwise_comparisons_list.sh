#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -N bkSW
#$ -l s_vmem=8G
#$ -l arm
#$ -pe def_slot 8
#$ -j y
#$ -o qsub_files

CPU=8

source $HOME/setenv/miniconda_arm.sh

FASTA_PATH=$1
PAIRWISE_PATH=$2
OUT_DIR=$3

# K562_clean.complete.256perms_11mer_256trees.partition001.comparisons_list.txt.gz
LABEL=$( basename -s ".comparisons_list.txt.gz" $PAIRWISE_PATH )

OUTPATH=$OUT_DIR/${LABEL}.pairwise_sw_scores.csv.gz

python pairwise_comparisons.py \
-i $FASTA_PATH \
-p $PAIRWISE_PATH \
-n $CPU \
-o $OUTPATH
