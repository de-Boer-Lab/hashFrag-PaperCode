import gzip
import pandas as pd
from argparse import ArgumentParser

def parse_arguments():
    parser = ArgumentParser(description="")
    parser.add_argument('-s','--sw_path',type=str,required=True,help="")
    parser.add_argument('-c','--candidates_path',type=str,required=True,help="")
    parser.add_argument('-t','--threshold',type=int,default=30,help="")
    return parser.parse_args()

def load_candidates_list(path):
    with gzip.open(path,"rt") as handle:
        candidates = handle.read().splitlines()
    return candidates

def filter_pairwise_sw_scores():
    args = parse_arguments()

    df = pd.read_csv(args.sw_path,compression="gzip")
    candidates = load_candidates_list(args.candidates_path)
    df["candidate"] = candidates
    df = df[df["sw"] >= 30]

    outpath = args.sw_path.replace(".txt.gz",".filter30.txt.gz")
    df.to_csv(outpath,compression="gzip",index=False)
    print("Done!",flush=True)

if __name__ == "__main__":
    filter_pairwise_sw_scores()