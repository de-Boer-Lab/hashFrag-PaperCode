#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -j y
#$ -o qsub_files
#$ -N bkSW_BATCH
#$ -pe def_slot 16
#$ -l s_vmem=4G
#$ -l arm

source $HOME/setenv/miniconda_arm.sh

# FASTA_FILEPATHS=$HOME/work/OrthogonalTrainValSplits/data/K562_clean/K562_clean_filepaths.txt
# OUT_DIR=/home/brett/work/OrthogonalTrainValSplits/hashClust/tutorial/sw
PAIRED_FASTAS_PATH=$1
OUT_DIR=$2

PAIRWISE_INFO=$( sed -n ${SGE_TASK_ID}p $PAIRED_FASTAS_PATH )
LABEL=$( echo $PAIRWISE_INFO | cut -d "," -f 1 )
FASTA_PATH_i=$( echo $PAIRWISE_INFO | cut -d "," -f 2 )
FASTA_PATH_j=$( echo $PAIRWISE_INFO | cut -d "," -f 3 )
OUTPATH=$OUT_DIR/${LABEL}.pairwise_comparisons.batch.txt.gz

python pairwise_comparisons.py \
-i $FASTA_PATH_i \
-j $FASTA_PATH_j \
-n 16 \
-o $OUTPATH
