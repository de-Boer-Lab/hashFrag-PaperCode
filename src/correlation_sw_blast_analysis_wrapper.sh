#!/bin/bash

INPUT_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/blast/K562_clean.complete.wordsize_screen
SW_DIR=/home/brett/work/OrthogonalTrainValSplits/distances/K562_clean.smith_waterman.1121

for HITS_PATH in $INPUT_DIR/*.work/K562_clean.blastn.out/K562_clean.top_blast_hits_dict.pbz2
do
    echo $HITS_PATH
    for SW_PATH in $SW_DIR/K562_clean.part_*.part_*.pairwise_comparisons.batch.txt.gz
    do
        LABEL=$( basename -s ".pairwise_comparisons.batch.txt.gz" $SW_PATH )
        OUTPUT_PATH=$OUT_DIR/${LABEL}.sw_blast_correlation_analysis.csv.gz
        echo $LABEL
        if [ ! -f "$OUTPUT_PATH" ]
        then
            qsub correlation_sw_blast_analysis.sh $HITS_PATH $SW_PATH
        fi
    done
done