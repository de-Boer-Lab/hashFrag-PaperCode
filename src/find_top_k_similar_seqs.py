import bz2
import pickle
import os
import sys
import numpy as np
from argparse import ArgumentParser
###########################################################################

def parse_arguments():
    parser = ArgumentParser(description="")
    parser.add_argument('-m','--matrix_file',type=str,required=True,help="")
    parser.add_argument('-s','--seqid_file',type=str,required=True,help="")
    parser.add_argument('-k','--top_k',type=int,required=True,help="")
    parser.add_argument('-o','--out_file',type=str,required=True,help="")
    return parser.parse_args()

def find_top_k_similar_seqs():
    """
    from an all by all similarity matrix, find top k similar sequences for each sequence.
    """
    args=parse_arguments()

    with bz2.BZ2File(args.matrix_file, "rb") as handle:
        distarray = pickle.load(handle)

    with open(args.seqid_file, "r") as handle:
        idmap = handle.read().splitlines()

    num_matches = args.top_k
    filename = args.out_file

    with open(filename, 'w') as outfile:
        for i, row in enumerate(distarray):
            top_indices = np.argsort(row)[-(num_matches+1):-1]  # Exclude the last one (self-similarity if it's a similarity matrix)
            for j in top_indices:
                outfile.write(f"{idmap[i]}\t{idmap[j]}\t{distarray[i, j]}\n")
            
if __name__ == "__main__":
    find_top_k_similar_seqs()

# Example Usage 

# python src/find_top_k_similar_seqs.py \
# -m "data/smith_waterman.darray.pbz2" \
# -s "data/smith_waterman.seqids.txt" \
# -k 10 \
# -o "data/top_10.txt"
