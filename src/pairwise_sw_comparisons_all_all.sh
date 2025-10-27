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

SAMPLE_FASTA_PATH=$1
SW_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/smith_waterman

LABEL=$( basename -s ".fa.gz" $SAMPLE_FASTA_PATH )
OUTPATH=$SW_DIR/${LABEL}.smith_waterman.csv.gz

python pairwise_smith_waterman_comparisons.py \
-i $SAMPLE_FASTA_PATH \
-n $CPU \
-o $OUTPATH
