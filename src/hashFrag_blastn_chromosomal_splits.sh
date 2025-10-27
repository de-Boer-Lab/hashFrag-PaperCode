#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -j y
#$ -o qsub_files
#$ -N bkBLASTN
#$ -pe def_slot 16
#$ -l s_vmem=2G

# qsub blastn_complete_dataset.sh 4

THREADS=16

source $HOME/setenv/miniconda.sh

TRAIN_FASTA_PATH=$1
TEST_FASTA_PATH=$2
DIR_LABEL=$3

TRAIN_LABEL=$( basename -s ".fa.gz" $TRAIN_FASTA_PATH )
TEST_LABEL=$( basename -s ".fa.gz" $TEST_FASTA_PATH )
LABEL=hashFrag_blast.train_${TRAIN_LABEL}.test_${TEST_LABEL}

BLAST_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/blast/blastn.xdrop_analysis.work/${DIR_LABEL}
mkdir -p $BLAST_DIR

# hashFrag blastn_module \
# --train_fasta_path $TRAIN_FASTA_PATH \
# --test_fasta_path $TEST_FASTA_PATH \
# -w 4 \
# -m 50000 \
# -e 50000 \
# --xdrop_ungap 0 \
# --xdrop_gap 0 \
# --xdrop_gap_final 0 \
# --force \
# -d no \
# -T $THREADS \
# --blastdb_label $LABEL \
# -o $BLAST_DIR

# hashFrag blastn_module \
# --train_fasta_path $TRAIN_FASTA_PATH \
# --test_fasta_path $TEST_FASTA_PATH \
# -w 4 \
# -m 50000 \
# -e 50000 \
# --force \
# -d no \
# -T $THREADS \
# --blastdb_label $LABEL \
# -o $BLAST_DIR

hashFrag blastn_module \
--train_fasta_path $TRAIN_FASTA_PATH \
--test_fasta_path $TEST_FASTA_PATH \
-w 4 \
-m 50000 \
-e 50000 \
--xdrop_ungap 50000 \
--xdrop_gap 50000 \
--xdrop_gap_final 50000 \
--force \
-d no \
-T $THREADS \
--blastdb_label $LABEL \
-o $BLAST_DIR
