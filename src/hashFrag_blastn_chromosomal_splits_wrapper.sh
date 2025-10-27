#!/bin/bash

CHROM_DIR=/home/brett/work/OrthogonalTrainValSplits/data/K562_clean/chrom_split

# TRAIN_FASTA_PATH=$CHROM_DIR/chr1.fa.gz
# TEST_FASTA_PATH=$CHROM_DIR/chr2.fa.gz
# qsub hashFrag_blastn_chromosomal_splits.sh $TRAIN_FASTA_PATH $TEST_FASTA_PATH xdrop_disabled

# TRAIN_FASTA_PATH=$CHROM_DIR/chr1.fa.gz
# TEST_FASTA_PATH=$CHROM_DIR/chr2.fa.gz
# qsub hashFrag_blastn_chromosomal_splits.sh $TRAIN_FASTA_PATH $TEST_FASTA_PATH xdrop_enabled

TRAIN_FASTA_PATH=$CHROM_DIR/chr1.fa.gz
TEST_FASTA_PATH=$CHROM_DIR/chr2.fa.gz
qsub hashFrag_blastn_chromosomal_splits.sh $TRAIN_FASTA_PATH $TEST_FASTA_PATH xdrop_enabled_high
