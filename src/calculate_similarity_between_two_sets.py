from multiprocessing import Pool
from Bio import pairwise2
import random
from argparse import ArgumentParser
import numpy as np
from tqdm import tqdm
import random
import os
from argparse import ArgumentParser
import pandas as pd
from utils import *
###########################################################################

def parse_arguments():
    parser = ArgumentParser(description="")
    parser.add_argument('-set1','--set1_file',type=str,required=True,help="")
    parser.add_argument('-set2','--set2_file',type=str,required=True,help="")
    parser.add_argument('-s','--seq_type',type=str,required=True,help="")
    parser.add_argument('-t','--num_threads',type=int,required=True,help="")
    parser.add_argument('-o','--out_path',type=str,required=True,help="")
    return parser.parse_args()

def align_sequences(pair):
    seq1, seq2, match_score, mismatch_score, open_gap_score, extend_gap_score = pair
    return pairwise2.align.localms(seq1, seq2, match_score, mismatch_score, open_gap_score, extend_gap_score, score_only=True)


def similarity_two_sets():

    # random.seed(42)

    """
    calculate the pairwise sequence alignment between two sets of sequences or their shuffled versions.
    remove the adapters from your sequence library if there are any.
    """
    args = parse_arguments()

    match_score = 1
    mismatch_score = -1
    open_gap_score = -2
    extend_gap_score = -1

    set1=pd.read_csv(args.set1_file, sep='\t')
    set2=pd.read_csv(args.set2_file, sep='\t')

    set1_sequences = set1['seq']
    set2_sequences = set2['seq']

    if args.seq_type == "genomic":
        set1_sequences = [seq for seq in set1_sequences]
        set2_sequences = [seq for seq in set2_sequences]

    elif args.seq_type == "dinucleotide_shuffle":
        set1_sequences = [seq for seq in set1_sequences]
        set2_sequences = [seq for seq in set2_sequences]
        set1_sequences = [dinucleotide_shuffle(seq) for seq in tqdm(set1_sequences)]
        set2_sequences = [dinucleotide_shuffle(seq) for seq in tqdm(set2_sequences)]

    elif args.seq_type == "mononucleotide_shuffle":
        set1_sequences = [seq for seq in set1_sequences]
        set2_sequences = [seq for seq in set2_sequences]
        set1_sequences = [mononucleotide_shuffle(seq) for seq in tqdm(set1_sequences)]
        set2_sequences = [mononucleotide_shuffle(seq) for seq in tqdm(set2_sequences)]

    pairs = [(set1_sequences[i], set2_sequences[j], match_score, mismatch_score, open_gap_score, extend_gap_score)
            for i in tqdm(range(len(set1_sequences))) for j in range(len(set2_sequences))]

    with Pool(processes=args.num_threads) as pool:
        scores_sw = list(tqdm(pool.imap(align_sequences, pairs), total=len(pairs)))

    sw_matrix = np.array(scores_sw).reshape((len(set1_sequences), len(set2_sequences)))
    np.save(args.out_path, sw_matrix)
    
if __name__ == "__main__":
    similarity_two_sets()

# Example Usage 

# python src/calculate_similarity_between_two_sets.py \
# -set1 "data/train.txt" \
# -set2 "data/test.txt" \
# -s "genomic" \
# -o "data/sw.npy"