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

FASTA_PATH=$1
BLAST_PATH=$2
OUTPUT_PATH=$3

python pairwise_smith_waterman_comparisons.py \
-i $FASTA_PATH \
-b $BLAST_PATH \
-n $CPU \
-o $OUTPUT_PATH
