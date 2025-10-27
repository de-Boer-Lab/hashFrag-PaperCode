#!/bin/bash

DISTANCES_DIR=/home/brett/work/OrthogonalTrainValSplits/distances/K562_clean.smith_waterman.1121
OUTPUT_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/analysis/cross_fold_max_sw_analysis
for DISTANCES_PATH in $DISTANCES_DIR/*.txt.gz.pairwise_comparisons.batch.txt.gz
do
    LABEL=$( basename -s ".txt.gz.pairwise_comparisons.batch.txt.gz" $DISTANCES_PATH )
    CHROM_OUTPUT_PATH=$OUTPUT_DIR/${LABEL}.chromosomal.max_sw_score.csv.g
    HASHFRAG_OUTPUT_PATH=$OUTPUT_DIR/${LABEL}hashFrag.max_sw_score.csv.gz
    if [ ! -f "$CHROM_OUTPUT_PATH" ] || [ ! -f "$HASHFRAG_OUTPUT_PATH" ]
    then
        qsub cross_fold_leakage_analysis.sh $DISTANCES_PATH
    fi
done
