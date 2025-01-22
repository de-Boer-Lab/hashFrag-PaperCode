import os
import gzip
from glob import glob
from itertools import combinations_with_replacement
from argparse import ArgumentParser
from utils import *

def parse_arguments():
    parser = ArgumentParser(description="")
    parser.add_argument('-i','--input_path',type=str,required=True,help="")
    parser.add_argument('-p','--partition_size',type=int,required=True,help="")
    parser.add_argument('-o','--out_dir',type=str,required=True,help="")
    return parser.parse_args()

def partition_dataset():
    """
    Divides a dataset into partitions of specified size and generates a list of all combinations
    of partition pairs. Outputs compressed partition files and a file listing the combinations.
    """

    # Parse command-line arguments
    args       = parse_arguments()
    # Extract the base name of the dataset file (without extension)
    dataset = os.path.splitext(os.path.basename(args.input_path))[0]

    # Load sequences into a dictionary from the input file
    fasta_dict = {}
    with open(args.input_path,"r") as handle:
        handle.readline() # Skip the header line
        for line in handle:
            entries = line.strip().split()
            seqid, seq= entries[0], entries[1]  ## Extract sequence ID and sequence; change the indices if the position of seqid and seq are different
            fasta_dict[seqid] = seq
    
    # Get the total number of sequences and their IDs
    n   = len(fasta_dict)
    ids = list(fasta_dict.keys())

    # Create the output directory if it does not exist
    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
    
    # Partition the dataset into chunks of specified size
    for p,i in enumerate(range(0,n,args.partition_size)):
        part_label = f"part_{p+1:0>3}"
        part_ids   = ids[i:i+args.partition_size]
        outpath    = os.path.join(args.out_dir,f"{dataset}.{part_label}.fa.gz")

        with gzip.open(outpath,"wt") as handle:
            for seqid in part_ids:
                handle.write(f">{seqid}\n{fasta_dict[seqid]}\n")
    
    # Generate the combinations of partition pairs
    files_path     = os.path.join(args.out_dir,"filepaths.txt")
    fasta_pathlist = sorted(glob(os.path.join(args.out_dir,"*.fa.gz")))
    n_partitions   = len(fasta_pathlist)
    with open(files_path,"w") as handle:
        for i,j in combinations_with_replacement(range(n_partitions),2):
            part_i = os.path.basename(fasta_pathlist[i]).replace(".fa.gz","").split(".")[1]
            part_j = os.path.basename(fasta_pathlist[j]).replace(".fa.gz","").split(".")[1]
            handle.write(f"{dataset}.{part_i}.{part_j}.txt.gz,{fasta_pathlist[i]},{fasta_pathlist[j]}\n")

    print("Done!",flush=True)

if __name__ == "__main__":
    partition_dataset()

# Example usage:
# python src/partition_dataset.py -i data/K562.tsv -p 10000 -o data/partitioned