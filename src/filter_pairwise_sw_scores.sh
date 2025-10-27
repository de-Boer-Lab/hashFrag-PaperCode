#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -N bkFILTERSW
#$ -l s_vmem=16G
#$ -l arm
#$ -pe def_slot 1
#$ -j y
#$ -o qsub_files

source $HOME/setenv/miniconda_arm.sh

SW_PATH=$1
CANDIDATES_PATH=$2

python filter_pairwise_sw_scores.py -s $SW_PATH -c $CANDIDATES_PATH