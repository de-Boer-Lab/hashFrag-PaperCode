#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -N bkSW
#$ -l s_vmem=8G
#$ -l arm
#$ -pe def_slot 16
#$ -j y
#$ -o qsub_files

CPU=16

source $HOME/setenv/miniconda_arm.sh

SUBSAMPLED_FASTA_PATH=$1
OUT_DIR=$2

LABEL=$( basename -s ".fa.gz" $SUBSAMPLED_FASTA_PATH )
OUTPATH=$OUT_DIR/${LABEL}.pairwise_comparisons.all_all.csv.gz

python pairwise_comparisons.py \
-i $SUBSAMPLED_FASTA_PATH \
-n $CPU \
-o $OUTPATH
