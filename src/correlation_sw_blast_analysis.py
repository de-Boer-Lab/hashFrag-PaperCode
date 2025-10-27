import bz2
import pickle
import pandas as pd
from argparse import ArgumentParser

def parse_arguments():
    parser = ArgumentParser(description="")
    parser.add_argument('-i','--hits_path',type=str,required=True,help="")
    parser.add_argument('-s','--sw_path',type=str,required=True,help="")
    parser.add_argument('-o','--output_path',type=str,required=True,help="")
    return parser.parse_args()

def correlation_sw_blast_analysis():
    args = parse_arguments()

    with bz2.BZ2File(args.hits_path,"rb") as handle:
        max_blast_score_dict = pickle.load(handle)

    score_df = pd.read_csv(args.sw_path)
    score_df['pair'] = score_df[['id_i','id_j']].apply(lambda x: tuple(sorted(x)),axis=1)
    score_df = score_df[score_df.pair.isin(max_blast_score_dict)]
    score_df["corrected_blast_score"] = [max_blast_score_dict[pair] for pair in score_df["pair"]]
    score_df = score_df[["id_i","id_j","corrected_blast_score","sw"]]
    score_df.to_csv(args.output_path,compression="gzip",index=False)

    print("Done!",flush=True)

if __name__ == "__main__":
    correlation_sw_blast_analysis()