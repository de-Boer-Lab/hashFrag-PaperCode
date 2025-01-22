import os
from argparse import ArgumentParser
import pandas as pd
from utils import *
###########################################################################

def parse_arguments():
    parser = ArgumentParser(description="")
    parser.add_argument('-i','--input_file',type=str,required=True,help="")
    parser.add_argument('-mx','--max',type=int,required=True,help="")
    parser.add_argument('-mn','--min',type=int,required=True,help="")
    parser.add_argument('-bw','--bin_width',type=int,required=True,help="")
    parser.add_argument('-p','--perc',type=float,required=True,help="")
    parser.add_argument('-n','--nn',type=int,required=True,help="")
    parser.add_argument('-tr','--train_file',type=str,required=True,help="")
    parser.add_argument('-te','--test_file',type=str,required=True,help="")
    return parser.parse_args()
    
def overfitNN():
    """
    for sequences in the test set, use the most similar sequences from the test set to make expression prediction.
    """
        
    args = parse_arguments()
    distance_ranges = [(i, i - args.bin_width) for i in range(args.max, args.min-1, -args.bin_width)]
    sw_percentage_range = args.perc
    n=args.nn
        
    df=pd.read_csv(args.input_file, sep='\t', header = None)
    df.columns=['id_i','id_j','sw']

    df_train = pd.read_csv(args.train_file, sep='\t')
    df_test = pd.read_csv(args.test_file, sep='\t')

    train_ids = set(df_train['seq_id'])
    test_ids = set(df_test['seq_id'])

    def determine_source(seq_id):
        if seq_id in train_ids:
            return 'train'
        elif seq_id in test_ids:
            return 'test'
        
    def filter_and_aggregate(group):
        max_sw = group['sw'].max()
        threshold = max_sw * (1 - sw_percentage_range)
        filtered_group = group[group['sw'] >= threshold]
        return pd.Series({
            'id_i': ', '.join(filtered_group['id_i']),
            'sw': filtered_group['sw'].mean(),
            # 'collisions': filtered_group['collisions'].max(),
            'id_i_source': filtered_group['id_i_source'].iloc[0],
            'id_j_source': filtered_group['id_j_source'].iloc[0],
            'id_i_mean_value': filtered_group['id_i_mean_value'].mean(),
            'id_j_mean_value': filtered_group['id_j_mean_value'].mean()
        })

    df['id_i_source'] = df['id_i'].apply(determine_source)
    df['id_j_source'] = df['id_j'].apply(determine_source)
    
    df = df[(
        ((df['id_i_source'].isin(['train'])) & (df['id_j_source'] == 'test')) |
        ((df['id_i_source'] == 'test') & (df['id_j_source'].isin(['train'])))
    )]
    df = df.apply(swap_train_test, axis=1)
    df_sorted = df.sort_values(by=['id_j', 'sw'], ascending=[True, False])
    df_top_n = df_sorted.groupby('id_j').head(n)
    correlations = []

    for idx, (upper, lower) in tqdm(enumerate(distance_ranges)):
        filtered_df = df_top_n[(df_top_n['sw'] < upper) & (df_top_n['sw'] >= lower)]
        temp_df_1 = filtered_df.merge(df_train[['seq_id', 'mean_value']], left_on='id_i', right_on='seq_id', how='left')
        temp_df_1.rename(columns={'mean_value': 'id_i_mean_value'}, inplace=True)
        temp_df_1.drop(columns=['seq_id'], inplace=True)
        temp_df_2 = filtered_df.merge(df_test[['seq_id', 'mean_value']], left_on='id_j', right_on='seq_id', how='left')
        temp_df_2.rename(columns={'mean_value': 'id_j_mean_value'}, inplace=True)
        temp_df_2.drop(columns=['seq_id'], inplace=True)
        temp_df = temp_df_1.merge(temp_df_2, how='left')
        temp_df = temp_df.groupby('id_j').apply(filter_and_aggregate)
        pearson_correlation = temp_df['id_i_mean_value'].corr(temp_df['id_j_mean_value'])
        correlations.append(pearson_correlation)
    
    print(correlations)
    return correlations

if __name__ == "__main__":
    overfitNN()

# Example Usage

# python src/overfitNN.py \
# -i "data/top_10.txt" \ 
# -max 30 \ 
# -min 10 \
# -bw 5 \
# -p 0.1 \ 
# -n 10 \
# -tr "data/train.txt" \
# -te "data/test.txt"