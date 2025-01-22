import gzip
import numpy as np
from argparse import ArgumentParser
from utils import *

def parse_arguments():
    parser = ArgumentParser(description="")
    parser.add_argument('-i','--fasta_path_i',type=str,required=True,help="")
    parser.add_argument('-j','--fasta_path_j',type=str,required=True,help="")
    parser.add_argument('-o','--outpath',type=str,required=True,help="")
    return parser.parse_args()

def batch_sequence_alignment_scores():
    """
    Compute and write pairwise Smith-Waterman alignment scores to a file.
    """
    print("\nBatch pairwise sequence alignment scores...", flush=True)

    args = parse_arguments()

    print("\nParsing partitioned FASTA files for sequence lists...", flush=True)

    # Read sequences from both FASTA files
    ids_i, seqs_i = parse_fasta(args.fasta_path_i)
    ids_j, seqs_j = parse_fasta(args.fasta_path_j)

    print("\nPairwise calculation of Smith-Waterman scores...", flush=True)
    # Compute Smith-Waterman scores between sequences in the two files
    sw_scores = compute_alignment_scores(seqs_i, seqs_j)

    print("Writing pairwise alignment scores to .txt.gz file...")
    # Write the computed scores to a compressed output file
    with gzip.open(args.outpath, "wt") as handle:
        handle.write(f"id_i,id_j,smith_waterman\n")
        for i in range(sw_scores.shape[0]):
            for j in range(sw_scores.shape[1]):
                handle.write(f"{ids_i[i]},{ids_j[j]},{sw_scores[i,j]}\n")

    print("Done!", flush=True)
if __name__ == "__main__":
    batch_sequence_alignment_scores()

# Example usage:

# python src/batch_sequence_alignment_combined.py -i data/partitioned/K562_clean.part_001.fa.gz -j data/partitioned/K562_clean.part_002.fa.gz -o data/001_002.txt.gz