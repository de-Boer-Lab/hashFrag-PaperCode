#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -j y
#$ -o qsub_files
#$ -N bkCROSS
#$ -pe def_slot 1
#$ -l s_vmem=64G
#$ -l arm

source $HOME/setenv/miniconda_arm.sh

INPUT_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/blast/K562_clean.complete.wordsize_7.work
OUTPUT_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/analysis/cross_fold_max_sw_analysis

DISTANCES_PATH=$1

echo $DISTANCES_PATH
echo $OUTPUT_DIR

python cross_fold_leakage_analysis.py \
-i $INPUT_DIR \
-d $DISTANCES_PATH \
-o $OUTPUT_DIR
