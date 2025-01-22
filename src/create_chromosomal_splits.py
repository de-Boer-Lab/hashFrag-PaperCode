import os
from argparse import ArgumentParser
import pandas as pd

###########################################################################

def parse_arguments():
    parser = ArgumentParser(description="")
    parser.add_argument('-i','--input_file',type=str,required=True,help="")
    parser.add_argument('-tr','--train_chrom_list',type=str,required=True,help="")
    parser.add_argument('-o','--out_dir',type=str,required=True,help="")    
    return parser.parse_args()

def create_chromosomal_splits():

    args = parse_arguments()
    df=pd.read_csv(args.input_file, sep='\t')

    chroms = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19', 'chr20', 'chr21', 'chr22', 'chrX', 'chrY']
    # Read training chromosome list from file
    with open(args.train_chrom_list, 'r') as f:
        train_chroms = [line.strip() for line in f]
    # Determine test chromosomes as those not in training list
    test_chroms = [x for x in chroms if x not in train_chroms]

    tr_df = df[df['chrom'].isin(train_chroms)]
    test_df = df[df['chrom'].isin(test_chroms)]

    tr_df.to_csv(os.path.join(args.out_dir, 'train.txt'), index=False, sep='\t')
    test_df.to_csv(os.path.join(args.out_dir, 'test.txt'), index=False, sep='\t')

    # Save training and test indices to files
    tr_indices = tr_df.index.tolist()
    test_indices = test_df.index.tolist()

    with open(os.path.join(args.out_dir, 'train_indices.txt'), 'w') as f:
        f.writelines(f"{idx}\n" for idx in tr_indices)

    with open(os.path.join(args.out_dir, 'test_indices.txt'), 'w') as f:
        f.writelines(f"{idx}\n" for idx in test_indices)

if __name__ == "__main__":
    create_chromosomal_splits()

# Example Usage

# python create_chromosomal_splits.py \
# -i "full_data/K562.tsv" \
# -tr "full_data/train_chrom_list.txt" \
# -o "data/"