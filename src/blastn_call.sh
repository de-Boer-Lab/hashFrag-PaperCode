#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -j y
#$ -o qsub_files
#$ -N bkBLASTN
#$ -pe def_slot 8
#$ -l s_vmem=2G

source $HOME/setenv/miniconda.sh

FASTA_PATH=$1
BLASTDB_PATH=$2
WORD_SIZE=$3
MAX_TARGET_SEQS=$4
EVALUE=$5
DUST=$6
OUTPUT_PATH=$7

echo "FASTA path: ${FASTA_PATH}" 
echo "BlastDB path: ${BLASTDB_PATH}"
echo "Word size: ${WORD_SIZE}"
echo "Max target seqs: ${MAX_TARGET_SEQS}"
echo "e-value: ${EVALUE}"
echo "Dust: ${DUST}"
echo "Output path: ${OUTPUT_PATH}.gz"

blastn \
-query $FASTA_PATH \
-db $BLASTDB_PATH \
-out $OUTPUT_PATH \
-word_size $WORD_SIZE \
-gapopen 2 \
-gapextend 1 \
-penalty -1 \
-reward 1 \
-max_target_seqs $MAX_TARGET_SEQS \
-evalue $EVALUE \
-dust $DUST \
-num_threads 8 \
-outfmt 6

gzip $OUTPUT_PATH

echo "Done!"
