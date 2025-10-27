#!/bin/bash

FASTA_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/fastas/dataset_sizes
for FASTA_PATH in $FASTA_DIR/*.fa.gz
do
    for WORD_SIZE in 4 5 6 7 8 9 10 11
    do
        qsub dataset_size_blast_runtime.sh $FASTA_PATH $WORD_SIZE
    done
done