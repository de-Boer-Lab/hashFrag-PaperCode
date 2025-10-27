#!/bin/bash

SW_DIR=/home/brett/work/OrthogonalTrainValSplits/distances/K562_clean.smith_waterman.1121
RECALL_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/analysis/recall/complete/K562_clean.complete.wordsize_7.recall
for SW_PATH in $SW_DIR/K562_clean.*.pairwise_comparisons.batch.txt.gz
do
    LABEL=$( basename -s ".pairwise_comparisons.batch.txt.gz" $SW_PATH | sed 's/K562_clean.//g' )
    CANDIDATES_PATH=$RECALL_DIR/K562_clean.complete.wordsize_7.${LABEL}.candidates.txt.gz
    qsub filter_pairwise_sw_scores.sh $SW_PATH $CANDIDATES_PATH
done