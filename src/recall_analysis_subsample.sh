#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -j y
#$ -o qsub_files
#$ -N bkRECALL
#$ -pe def_slot 1
#$ -l s_vmem=16G
#$ -l arm

source $HOME/setenv/miniconda_arm.sh

BLAST_PATH=$1
SCORE_PATH=$2
CANDIDATES_PATH=$3
RECALL_PATH=$4

echo "Blastn path: ${BLAST_PATH}"
echo "Score (SW) path: ${SCORE_PATH}"
echo "Candidates (out)path: ${CANDIDATES_PATH}"
echo "Recall (out)path: ${RECALL_PATH}"

python recall_analysis_subsample.py \
-b $BLAST_PATH \
-s $SCORE_PATH \
-c $CANDIDATES_PATH \
-r $RECALL_PATH

echo "Done!"
