import bz2
import pickle
import os
import numpy as np
from argparse import ArgumentParser
from utils import *
###########################################################################

def parse_arguments():
    parser = ArgumentParser(description="")
    parser.add_argument('-m','--matrix_file',type=str,required=True,help="")
    parser.add_argument('-s','--seqid_file',type=str,required=True,help="")
    parser.add_argument('-t','--threshold',type=int,required=True,help="")
    parser.add_argument('-o','--out_dir',type=str,required=True,help="")
    return parser.parse_args()

def find_similar_seqs():
    """
    from an all by all similarity matrix, find all pair of sequences that share a similarity score above a certain threshold.
    """
    args = parse_arguments()
    matrix_file = args.matrix_file
    seqid_file= args.seqid_file

    with bz2.BZ2File(matrix_file, "rb") as handle:
        distarray = pickle.load(handle)

    with open(seqid_file, "r") as handle:
        idmap = handle.read().splitlines()

    sim_threshold = args.threshold

    row_indices, col_indices = np.tril_indices_from(distarray, k=-1)
    above_threshold_indices = distarray[row_indices, col_indices] >= sim_threshold

    filtered_row_indices = row_indices[above_threshold_indices]
    filtered_col_indices = col_indices[above_threshold_indices]

    sequence_pairs_with_distance = [
    (idmap[i], idmap[j], distarray[i, j])
    for i, j in zip(filtered_row_indices, filtered_col_indices)
    ]

    pairs_file = os.path.join(args.out_dir, f"sequence_pairs_with_alignment_above_threshold_{os.path.basename(matrix_file)}_{sim_threshold}.txt")
    with open(pairs_file, 'w') as handle:
        for seq1, seq2, dist in sequence_pairs_with_distance:
            handle.write(f'{seq1}\t{seq2}\t{dist}\n')
            
if __name__ == "__main__":
    find_similar_seqs()

# Example Usage 

# python src/find_similar_seqs_above_threshold.py \
# -m "data/smith_waterman.darray.pbz2" \
# -s "data/smith_waterman.seqids.txt" \
# -t 30 \
# -o "data/"