#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -j y
#$ -o qsub_files
#$ -N bkCORR
#$ -pe def_slot 1
#$ -l s_vmem=40G
#$ -l arm

source $HOME/setenv/miniconda_arm.sh

HITS_PATH=$1
SW_PATH=$2

HITS_DIR=$( dirname $HITS_PATH )
OUT_DIR=$HITS_DIR/correlation_analysis
mkdir -p $OUT_DIR

LABEL=$( basename -s ".pairwise_comparisons.batch.txt.gz" $SW_PATH )
OUTPUT_PATH=$OUT_DIR/${LABEL}.sw_blast_correlation_analysis.csv.gz

echo "Top BLAST hits path: ${HITS_PATH}"
echo "Smith-Waterman path: ${SW_PATH}"
echo "Output path:         ${OUTPUT_PATH}"

python correlation_sw_blast_analysis.py \
-i $HITS_PATH \
-s $SW_PATH \
-o $OUTPUT_PATH
