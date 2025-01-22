import bz2
import pickle
import pandas as pd
from argparse import ArgumentParser
from utils import *
###########################################################################
def parse_arguments():
    parser = ArgumentParser(description="")
    parser.add_argument('-m','--matrix_file',type=str,required=True,help="")
    parser.add_argument('-s','--seqid_file',type=str,required=True,help="")
    parser.add_argument('-tr','--train_indices_file',type=str,required=True,help="")
    parser.add_argument('-te', '--test_indices_file',type=str,required=True,help="")
    parser.add_argument('-o','--out_file', type=str, help="")
    return parser.parse_args()

def calculate_similarity_stats():
    """
    calculate similarity statistics between the training and test set.
    """
    args = parse_arguments()
    with bz2.BZ2File(args.matrix_file,"rb") as handle:
       distarray = pickle.load(handle)
    with open(args.seqid_file,"r") as handle:
        idmap = handle.read().splitlines()

    with open(args.train_indices_file, 'r') as file:
        training_set_indices = [int(line.strip()) for line in file]

    with open(args.test_indices_file, 'r') as file:
        test_set_indices = [int(line.strip()) for line in file]

    similarity_stats_test = [
    list_of_statistics(
        distarray[idx, training_set_indices]) for idx in test_set_indices
        ]
    seq_ids_test = [idmap[i] for i in test_set_indices]
    similarity_df_test = pd.DataFrame(similarity_stats_test)
    similarity_df_test['Seq_ID'] = seq_ids_test
    similarity_df_test['Set'] = "Test"

    similarity_stats_training = [
    list_of_statistics(
        distarray[idx, training_set_indices]) for idx in training_set_indices
        ]
    seq_ids_training = [idmap[i] for i in training_set_indices]
    similarity_df_training = pd.DataFrame(similarity_stats_training)
    similarity_df_training['Seq_ID'] = seq_ids_training
    similarity_df_training['Set'] = 'Train'
    all_sequences_df = pd.concat([similarity_df_training, similarity_df_test], ignore_index=True)

    all_sequences_df.reset_index(drop=True, inplace=True)
    all_sequences_df.to_csv(f"data/{args.out_file}.csv", index=False)

if __name__ == "__main__":
    calculate_similarity_stats()

# Example Usage

# python calculate_similarity_stats.py \
# -m "data/smith_waterman.darray.pbz2" \
# -s "data/smith_waterman.seqids.txt" \
# -tr "data/train_indices.txt" \
# -te "data/test_indices.txt" \ 
# -o "sw_stats"

