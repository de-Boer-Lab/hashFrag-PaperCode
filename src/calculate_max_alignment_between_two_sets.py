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
import bz2
import pickle
from utils import *

###########################################################################

def parse_arguments():
    parser = ArgumentParser(description="")
    parser.add_argument('-m','--matrix_file',type=str,required=True,help="")
    parser.add_argument('-set1','--set1_indices_file',type=str,required=True,help="")
    parser.add_argument('-set2','--set2_indices_file',type=str,required=True,help="")
    parser.add_argument('-o','--out_path',type=str,required=True,help="")
    return parser.parse_args()

def max_similarity_two_sets():

    """
    pull sequence alignment scoers between two sets of sequences from an all by all precalculated score matrix to report the maximum alignmnet scores
    """
    args = parse_arguments()

    matrix_file= args.matrix_file

    with bz2.BZ2File(matrix_file, "rb") as handle:
        distarray = pickle.load(handle)

    with open(args.set1_indices_file, 'r') as file:
        set1_indices = [int(line.strip()) for line in file]
    with open(args.set2_indices_file, 'r') as file:
        set2_indices = [int(line.strip()) for line in file]

    max_scores = np.zeros(len(set2_indices))

    for i, set2_index in enumerate(set2_indices):
        set2_row = distarray[set2_index]
        set1_scores = set2_row[set1_indices]
        max_scores[i] = np.max(set1_scores)

    np.save(args.out_path, max_scores)
    
if __name__ == "__main__":
    max_similarity_two_sets()

# Example Usage 

# python src/calculate_max_alignment_between_two_sets.py \
# -m "data\smith_waterman.darray.pbz2" \
# -set1 "data/train_indices.txt" \
# -set2 "data/test_indices.txt" \
# -o "data/max_sw.npy"