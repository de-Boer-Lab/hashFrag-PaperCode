import os
import gzip

import numpy as np
import pandas as pd
from argparse import ArgumentParser

def parse_arguments():
    parser = ArgumentParser(description="")
    parser.add_argument('-i','--input-dir',type=str,required=True,help="")
    parser.add_argument('-d','--distances-path',type=str,required=True,help="")
    parser.add_argument('-o','--output-dir',type=str,required=True,help="")
    return parser.parse_args()

def cross_fold_leakage_analysis():
    args = parse_arguments()

    chrom_folds_path = os.path.join(args.input_dir,"control.10_chromosomal_folds.tsv.gz")
    hashfrag_folds_path = os.path.join(args.input_dir,"hashFrag.10_orthogonal_folds.tsv.gz")
    chrom_folds_df = pd.read_csv(chrom_folds_path,sep="\t")
    hashfrag_folds_df = pd.read_csv(hashfrag_folds_path,sep="\t")

    chrom_fold_map = {}
    for seq_id,fold in zip(chrom_folds_df["id"],chrom_folds_df["fold"]):
        chrom_fold_map[seq_id] = fold

    hashfrag_fold_map = {}
    for seq_id,fold in zip(hashfrag_folds_df["id"],hashfrag_folds_df["fold"]):
        hashfrag_fold_map[seq_id] = fold

    n_chrom_folds = chrom_folds_df["fold"].nunique()
    n_hashfrag_folds = hashfrag_folds_df["fold"].nunique()
    chrom_arr = np.zeros(shape=(n_chrom_folds,n_chrom_folds))
    hashfrag_arr = np.zeros(shape=(n_hashfrag_folds,n_hashfrag_folds))

    with gzip.open(args.distances_path,"rt") as handle:
        handle.readline()
        for line in handle:
            id_i,id_j,d = line.strip().split(",")
            d = float(d)
            try:
                i = chrom_fold_map[id_i]
                j = chrom_fold_map[id_j]
                chrom_arr[i,j] = max(chrom_arr[i,j],d)
                chrom_arr[j,i] = max(chrom_arr[j,i] ,d)
            except:
                pass
            
            try:
                i = hashfrag_fold_map[id_i]
                j = hashfrag_fold_map[id_j]
                hashfrag_arr[i,j] = max(hashfrag_arr[i,j],d)
                hashfrag_arr[j,i] = max(hashfrag_arr[j,i],d)
            except:
                pass

    label = os.path.basename(args.distances_path).replace(".txt.gz.pairwise_comparisons.batch.txt.gz","")
    chrom_output_path = os.path.join(args.output_dir,f"{label}.chromosomal.max_sw_score.csv.gz")
    hashfrag_output_path = os.path.join(args.output_dir,f"{label}.hashFrag.max_sw_score.csv.gz")
    chrom_output_df = pd.DataFrame(chrom_arr)
    hashfrag_output_df = pd.DataFrame(hashfrag_arr)
    chrom_output_df.to_csv(chrom_output_path,compression="gzip",index=True,header=True)
    hashfrag_output_df.to_csv(hashfrag_output_path,compression="gzip",index=True,header=True)

    print("Done!",flush=True)

if __name__ == "__main__":
    cross_fold_leakage_analysis()