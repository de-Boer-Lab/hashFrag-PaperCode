import os
import bz2
import gzip
import pickle
import numpy as np
from glob import glob
from pyfastx import Fasta
from argparse import ArgumentParser

def parse_arguments():
    parser = ArgumentParser(description="")
    parser.add_argument('-i','--partition_dir',type=str,required=True,help="")
    parser.add_argument('-d','--alignments_dir',type=str,required=True,help="")
    parser.add_argument('-m','--metric',type=str,required=True,help="")
    parser.add_argument('-o','--outpath',type=str,required=True,help="")
    return parser.parse_args()

def batch_matrix_construction():
    """
    Constructs an all-by-all alignment matrix based on pairwise sequence alignment calculations.
    The matrix is saved in a compressed binary format, and sequence IDs are written to a separate file.
    """
    print("\nAll-all matrix construction of batched pairwise sequence comparisons.\n",flush=True)
    args = parse_arguments()

    # Step 1: Extract sequence IDs from the partitioned FASTA files
    print("Extracting complete list of sequence ids...",flush=True)
    ids     = []
    pattern = os.path.join(args.partition_dir,"*.fa.gz")
    for fasta_path in sorted(glob(pattern)):
        for seqid,seq in Fasta(fasta_path,build_index=False):
            ids.append(seqid)
    n     = len(ids)
    idmap = { seqid:idx for idx,seqid in enumerate(ids) } # map sequence id to alignment array index

    print("Constructing all-all alignment matrix...",flush=True)

    # Step 2: Initialize the alignment matrix based on the specified metric
    arr = np.zeros(shape=(n,n),dtype=np.float16)
    
    # Step 3: Populate the alignment matrix from batched pairwise alignment files

    pattern = os.path.join(args.alignments_dir,"*.txt.gz")
    alignments_pathlist = sorted(glob(pattern)) # List of batched alignment files
    for x,alignments_path in enumerate(alignments_pathlist):
        print(f"\t{os.path.basename(alignments_path)} ({x+1}/{len(alignments_pathlist)})",flush=True)
        with gzip.open(alignments_path,"rt") as handle:
            header = handle.readline()
            try:
                disidx = int(header.strip().split(",").index(args.metric))
            except:
                raise ValueError(f"The specified alignment metric, {args.metric}, could not be found in the batch alignments file {args.alignments_dir}")
            for line in handle:
                entry    = line.strip().split(",")
                id_i     = entry[0] # Sequence ID 1
                id_j     = entry[1] # Sequence ID 2
                i        = idmap[id_i] # Index for ID 1
                j        = idmap[id_j] # Index for ID 2
                d        = entry[disidx] # Alignment value
                arr[i,j] = d # Populate matrix (i, j)
                arr[j,i] = d # Symmetric assignment (j, i)

    # Step 4: Save the alignment matrix to a compressed binary file
    print("Writing alignment array.",flush=True)
    with bz2.BZ2File(args.outpath,"wb") as handle:
        pickle.dump(arr,handle)
    
    # Step 5: Save the sequence ID list to a separate file
    print("Writing sequence ID list.",flush=True)
    seqid_outpath = args.outpath.replace(".darray.pbz2",".seqids.txt")
    with open(seqid_outpath,"w") as handle:
        handle.write("\n".join(ids)+"\n")

    print("Done!",flush=True)

if __name__ == "__main__":
    batch_matrix_construction()

# Example usage

# python batch_matrix_construction.py \
# -i data/partitioned \
# -d data/batch_alignments \
# -m smith_waterman \
# -o data/smith_waterman.darray.pbz2