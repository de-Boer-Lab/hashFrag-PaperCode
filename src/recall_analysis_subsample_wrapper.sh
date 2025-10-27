#!/bin/bash

FASTAS_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/fastas
BLAST_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/blast
SCORE_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/smith_waterman
RECALL_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/analysis/recall

for SAMPLE_FASTA_PATH in $FASTAS_DIR/K562_clean.subsample_*.fa.gz
do
    LABEL=$( basename -s ".fa.gz" $SAMPLE_FASTA_PATH )
    SAMPLE_BLAST_DIR=$BLAST_DIR/${LABEL}.work
    SCORE_PATH=$SCORE_DIR/${LABEL}.smith_waterman.csv.gz
    for SAMPLE_BLAST_PATH in $SAMPLE_BLAST_DIR/${LABEL}.*.blastn.out.gz
    do
        echo $SAMPLE_BLAST_PATH
        COMPLETE_LABEL=$( basename -s ".out.gz" $SAMPLE_BLAST_PATH )
        CANDIDATES_PATH=$RECALL_DIR/${COMPLETE_LABEL}.candidates.txt.gz
        RECALL_PATH=$RECALL_DIR/${COMPLETE_LABEL}.recall.csv.gz
        if [ ! -f "$RECALL_PATH" ]
        then
            echo $SAMPLE_BLAST_PATH
            # qsub recall_analysis_subsample.sh $SAMPLE_BLAST_PATH $SCORE_PATH $CANDIDATES_PATH $RECALL_PATH
        fi
    done
done