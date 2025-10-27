import os
import gc
import bz2
import pickle
import pandas as pd
from argparse import ArgumentParser
from collections import defaultdict

def parse_arguments():
    parser = ArgumentParser(description="")
    parser.add_argument('-b','--blast_path',type=str,required=True,help="")
    return parser.parse_args()

def collect_top_blast_hits_dict():
    args = parse_arguments()

    blast_columns = [
        "qseqid","sseqid","pident","length","mismatch",
        "gapopen","qstart","qend","sstart","send","evalue",
        "bitscore","score","positive","gaps"
    ]

    reward    = 1
    penalty   = -1
    gapopen   = 2
    gapextend = 1

    print("Constructing max_blast_score_dict...",flush=True)
    max_blast_score_dict = defaultdict(float)
    for partial_blast_df in pd.read_csv(args.blast_path,names=blast_columns,sep="\t",chunksize=250_000):
        partial_blast_df["corrected_blast_score"] = (
            reward*partial_blast_df["positive"] +
            penalty*partial_blast_df["mismatch"] -
            gapopen*partial_blast_df["gapopen"] -
            gapextend*(partial_blast_df["gaps"] - partial_blast_df["gapopen"])
        )
        partial_blast_df['pair'] = partial_blast_df[['qseqid','sseqid']].apply(lambda x: tuple(sorted(x)),axis=1)
        partial_blast_df = partial_blast_df[["pair","corrected_blast_score"]]
        for pair,score in zip(partial_blast_df["pair"],partial_blast_df["corrected_blast_score"]):
            if score > max_blast_score_dict[pair]:
                max_blast_score_dict[pair] = score
        del partial_blast_df
        gc.collect()

    out_dir = os.path.dirname(args.blast_path)
    out_label = os.path.basename(args.blast_path).replace(".blastn.out","")
    outpath = os.path.join(out_dir,f"{out_label}.top_blast_hits_dict.pbz2")
    with bz2.BZ2File(outpath,"wb") as handle:
        pickle.dump(max_blast_score_dict,handle)

    print(outpath)
    print("Done!",flush=True)

if __name__ == "__main__":
    collect_top_blast_hits_dict()