import gzip
import numpy as np
import pandas as pd
from collections import defaultdict
from argparse import ArgumentParser

def parse_arguments():
    parser = ArgumentParser(description="")
    parser.add_argument('-b','--blast_path',type=str,required=True,help="")
    parser.add_argument('-s','--score_path',type=str,required=True,help="")
    parser.add_argument('-c','--candidates_path',type=str,required=True,help="")
    parser.add_argument('-r','--recall_path',type=str,required=True,help="")
    return parser.parse_args()

blast_columns = [
    "qseqid","sseqid","pident","length","mismatch",
    "gapopen","qstart","qend","sstart","send","evalue",
    "bitscore","uncorrected_blast_score","positive","gaps"
]

def recall_analysis():
    args = parse_arguments()

    # blast_columns = ["qseqid","sseqid","pident","length","mismatch","gapopen","qstart","qend","sstart","send","evalue","bitscore"]
    # blast_df = pd.read_csv(args.blast_path,compression="gzip",header=None,sep="\t",names=blast_column_labels)

    score_df = pd.read_csv(args.score_path,compression="gzip")

    candidate_dict = defaultdict(set)
    # blast_columns = ["qseqid","sseqid","pident","length","mismatch","gapopen","qstart","qend","sstart","send","evalue","bitscore","score","positive","gapextend"]
    for chunk_df in pd.read_csv(args.blast_path,header=None,sep="\t",names=blast_columns,chunksize=100_000):
        for _,row in chunk_df.iterrows():
            candidate_dict[row["qseqid"]].add(row["sseqid"])
    
    n_candidates = np.sum([len(g) for g in candidate_dict.values()])
    print(f"Number of candidates: {n_candidates}",flush=True)

    candidates = []
    for idx,row in score_df.iterrows():
        id_i = row["id_i"]
        id_j = row["id_j"]
        candidates.append(int((id_i in candidate_dict[id_j]) or (id_j in candidate_dict[id_i])))

    with gzip.open(args.candidates_path,"wt") as handle:
        handle.write("\n".join([str(seq_id) for seq_id in candidates])+"\n")

    score_df["candidate"] = candidates

    results_dict = {
        "threshold":[],
        "TP":[],
        "FP":[],
        "TN":[],
        "FN":[],
        "recall":[],
        "FPR":[]
    }

    min_score = score_df["sw"].min()
    max_score = score_df["sw"].max()
    for threshold in np.arange(min_score,max_score+1,1):
        above_threshold = score_df["sw"] >= threshold
        below_threshold = score_df["sw"] < threshold
        tp = np.sum(above_threshold & (score_df["candidate"] == 1))  # True Positives: number of hits LSH captures
        fn = np.sum(above_threshold & (score_df["candidate"] == 0))  # False Negatives: number of hits LSH misses
        fp = np.sum(below_threshold & (score_df["candidate"] == 1))  # False Positives: number of non-hits LSH successfully misses
        tn = np.sum(below_threshold & (score_df["candidate"] == 0))  # True Negatives:  number of non-hits that LSH detects
        results_dict["threshold"].append(threshold)
        results_dict["TP"].append(tp)
        results_dict["FN"].append(fn)
        results_dict["FP"].append(fp)
        results_dict["TN"].append(tn)
        results_dict["recall"].append(tp/(tp+fn) if (tp+fn) > 0 else 0)
        results_dict["FPR"].append(fp/(fp+tn) if (fp+tn) > 0 else 0)

    results_df = pd.DataFrame(results_dict)
    results_df.to_csv(args.recall_path,compression="gzip",index=False)

    print("Done!",flush=True)

if __name__ == "__main__":
    recall_analysis()