#!/bin/bash

# BLAST_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/blast
# RECALL_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/analysis/recall/complete
SCORE_DIR=/home/brett/work/OrthogonalTrainValSplits/distances/K562_clean.smith_waterman.1121

# for COMPLETE_BLAST_DIR in $BLAST_DIR/K562_clean.complete.wordsize_11.work
# do
#     LABEL=$( basename -s ".work" $COMPLETE_BLAST_DIR )
#     echo $COMPLETE_BLAST_DIR

#     OUT_DIR=$RECALL_DIR/${LABEL}.recall
#     mkdir -p $OUT_DIR

#     COMPLETE_BLAST_PATH=$COMPLETE_BLAST_DIR/K562_clean.blastn.out.gz
#     for PARTITIONED_SCORE_PATH in $SCORE_DIR/K562_clean.part_*.part_*.pairwise_comparisons.batch.txt.gz
#     do
#         PARTITIONED_LABEL=$( basename -s ".pairwise_comparisons.batch.txt.gz" $PARTITIONED_SCORE_PATH | sed 's/K562_clean.//g' )
#         CANDIDATES_PATH=$OUT_DIR/${LABEL}.${PARTITIONED_LABEL}.candidates.txt.gz
#         RECALL_PATH=$OUT_DIR/${LABEL}.${PARTITIONED_LABEL}.recall.csv.gz
#         qsub recall_analysis_complete_partitioned.sh $COMPLETE_BLAST_PATH $PARTITIONED_SCORE_PATH $CANDIDATES_PATH $RECALL_PATH
#     done
# done

BLAST_DIR=/home/brett/work/OrthogonalTrainValSplits/K562_orthoSplit/blast/K562_clean.complete.wordsize_screen
for COMPLETE_BLAST_DIR in $BLAST_DIR/K562_clean.complete.wordsize_*.work/K562_clean.blastn.out
do
    LABEL=$( basename -s ".work" $( dirname $COMPLETE_BLAST_DIR ) )
    WORD_SIZE=$( echo $LABEL | cut -d "." -f 3 | cut -d "_" -f 2 )
    if [ "$WORD_SIZE" = "5" ] || [ "$WORD_SIZE" = "6" ] || [ "$WORD_SIZE" = "4" ] # ||
    then
        echo $COMPLETE_BLAST_DIR
        RECALL_DIR=$( dirname $COMPLETE_BLAST_DIR )/recall
        mkdir -p $RECALL_DIR

        COMPLETE_BLAST_PATH=$COMPLETE_BLAST_DIR/K562_clean.blastn.out
        for PARTITIONED_SCORE_PATH in $SCORE_DIR/K562_clean.part_*.part_*.pairwise_comparisons.batch.txt.gz
        do
            PARTITIONED_LABEL=$( basename -s ".pairwise_comparisons.batch.txt.gz" $PARTITIONED_SCORE_PATH | sed 's/K562_clean.//g' )
            CANDIDATES_PATH=$RECALL_DIR/${LABEL}.${PARTITIONED_LABEL}.candidates.txt.gz
            RECALL_PATH=$RECALL_DIR/${LABEL}.${PARTITIONED_LABEL}.recall.csv.gz
            if [ ! -f "$RECALL_PATH" ] || [ ! -f $CANDIDATES_PATH ]
            then
                echo $PARTITIONED_SCORE_PATH
                qsub recall_analysis_complete_partitioned.sh $COMPLETE_BLAST_PATH $PARTITIONED_SCORE_PATH $CANDIDATES_PATH $RECALL_PATH
            fi
            # qsub recall_analysis_complete_partitioned.sh $COMPLETE_BLAST_PATH $PARTITIONED_SCORE_PATH $CANDIDATES_PATH $RECALL_PATH

        done
    fi
done

