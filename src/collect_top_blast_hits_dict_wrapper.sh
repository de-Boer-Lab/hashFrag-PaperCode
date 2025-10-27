#!/bin/bash

INPUT_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/blast/K562_clean.complete.wordsize_screen

for BLAST_PATH in $INPUT_DIR/*.work/K562_clean.blastn.out/K562_clean.blastn.out
do
    echo $BLAST_PATH   
    qsub collect_top_blast_hits_dict.sh $BLAST_PATH
done