#!/bin/bash

for WORD_SIZE in 7 11 4 5 6 8 9 10
do
    qsub blastn_complete_dataset.sh $WORD_SIZE
done