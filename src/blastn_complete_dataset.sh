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

FASTA_PATH=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/fastas/K562_clean.fa.gz
WORD_SIZE=$1
MAX_TARGET_SEQS=226253
EVALUE=226253
DUST=no

LABEL=$( basename -s ".fa.gz" $FASTA_PATH )
BLAST_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/blast/${LABEL}.complete.wordsize_${WORD_SIZE}.xdrop_test.work
OUTPUT_PATH=$BLAST_DIR/${LABEL}.blastn.out

hashFrag blastn_module \
-f $FASTA_PATH \
-w $WORD_SIZE \
-m $MAX_TARGET_SEQS \
-e $EVALUE \
--xdrop_ungap 0 \
--xdrop_gap 0 \
--xdrop_gap_final 0 \
--force \
-d $DUST \
-T $THREADS \
-o $OUTPUT_PATH
