#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -j y
#$ -o qsub_files
#$ -N bkTOPBLAST
#$ -pe def_slot 1
#$ -l s_vmem=64G

source $HOME/setenv/miniconda.sh

BLAST_PATH=$1

echo "BLAST path: ${BLAST_PATH}"

python collect_top_blast_hits_dict.py -b $BLAST_PATH
