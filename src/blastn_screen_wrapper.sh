#!/bin/bash

FASTAS_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/fastas
BLAST_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/blast
for SAMPLE_BLAST_DIR in $BLAST_DIR/*.work
do
    LABEL=$( basename -s ".work" $SAMPLE_BLAST_DIR )
    echo $LABEL
    FASTA_PATH=$FASTAS_DIR/${LABEL}.fa.gz
    INPUT_PATH=$FASTAS_DIR/${LABEL}.fa
    gunzip -c $FASTA_PATH > $INPUT_PATH

    BLASTDB_PATH=$SAMPLE_BLAST_DIR/${LABEL}.blastdb

    for WORD_SIZE in 5 7 11 16 20
    do
        for MAX_TARGET_SEQS in 500 1000 5000 10000
        do
            for EVALUE in 10 50 100
            do
                for DUST in yes no
                do
                    OUTPUT_PATH=$SAMPLE_BLAST_DIR/${LABEL}.wordsize_${WORD_SIZE}.maxtargetseqs_${MAX_TARGET_SEQS}.evalue_${EVALUE}.dust_${DUST}.blastn.out
                    qsub blastn_call.sh $INPUT_PATH $BLASTDB_PATH $WORD_SIZE $MAX_TARGET_SEQS $EVALUE $DUST $OUTPUT_PATH 
                done
            done
        done
    done
done