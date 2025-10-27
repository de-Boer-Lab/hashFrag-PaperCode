#!/bin/bash

FASTAS_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/fastas
for SAMPLE_FASTA_PATH in $FASTAS_DIR/K562_clean.subsample_*.fa.gz
do
    echo $SAMPLE_FASTA_PATH
    qsub pairwise_sw_comparisons_all_all.sh $SAMPLE_FASTA_PATH
done