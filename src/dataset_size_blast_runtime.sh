#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -j y
#$ -o qsub_files
#$ -N bkHF_BLAST
#$ -pe def_slot 16
#$ -l s_vmem=2G

THREADS=16

source $HOME/setenv/miniconda.sh

FASTA_PATH=$1
WORD_SIZE=$2

LABEL=$( basename -s ".fa.gz" $FASTA_PATH )
BLAST_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/blast/dataset_sizes
OUTPUT_DIR=$BLAST_DIR/${LABEL}.wordsize_${WORD_SIZE}.blastn.removing_extension_heuristics.work

echo $FASTA_PATH
echo $WORD_SIZE

/usr/bin/time -f "%M,KB,%e,sec," hashFrag blastn_module \
-f $FASTA_PATH \
-w $WORD_SIZE \
-m 226253 \
-e 226253 \
# --xdrop_ungap 0.01 \
# --xdrop_gap 0.01 \
# --xdrop_gap_final 0.01 \
--force \
-T $THREADS \
-o $OUTPUT_DIR
