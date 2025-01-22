import os
from argparse import ArgumentParser
import bz2
import pickle
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from utils import *
###########################################################################

def parse_arguments():
    parser = ArgumentParser(description="")
    parser.add_argument('-m','--matrix_file',type=str,required=True,help="")
    parser.add_argument('-s','--seqid_file',type=str,required=True,help="")
    parser.add_argument('-set1','--set1_file_path',type=str,required=True,help="")
    parser.add_argument('-set2','--set2_file_path',type=str,required=True,help="")
    parser.add_argument('-mx','--max_val',type=int,required=True,help="")
    parser.add_argument('-mn','--min_val',type=int,required=True,help="")
    parser.add_argument('-o','--out_dir',type=str,required=True,help="")
    return parser.parse_args()
    
def clustermap():
    """
    given an all by all similarity matrix, for two sets of sequences perform Hierarchical clustering to generate a heatmap to visualize similarity
    """
        
    args = parse_arguments()

    with bz2.BZ2File(args.matrix_file,"rb") as handle:
        distarray = pickle.load(handle)
    
    with open(args.seqid_file,"r") as handle:
        idmap = handle.read().splitlines()

    with open(args.set1_file_path, 'r') as file:
        set1_indices = [int(line.strip()) for line in file]
    with open(args.set2_file_path, 'r') as file:
        set2_indices = [int(line.strip()) for line in file]

    distarray_subset = distarray[set1_indices][:,set2_indices]
 
    plt.figure(figsize=(8, 8), dpi=300)
    g = sns.clustermap(distarray_subset, cmap="viridis", vmin=args.min_val, vmax=args.max_val,
                    xticklabels=False, yticklabels=False)
    g.ax_row_dendrogram.set_visible(False)
    g.ax_col_dendrogram.set_visible(False)
    g.cax.set_visible(False)
    row_indices = g.dendrogram_row.reordered_ind
    col_indices = g.dendrogram_col.reordered_ind

    np.save(os.path.join(args.out_dir, f"row_indices.npy"), row_indices)
    np.save(os.path.join(args.out_dir, f"col_indices.npy"), col_indices)

    plt.savefig(os.path.join(args.out_dir, f"clustermap.png"), 
                dpi=300, bbox_inches='tight')
    plt.close()

    np.save(os.path.join(args.out_dir, f"arr.npy"), distarray_subset)

if __name__ == "__main__":
    clustermap()

# Example Usage

# python src/clustermap.py \
# -m "data/smith_waterman.darray.pbz2" \
# -s "data/smith_waterman.seqids.txt" \
# -set1 "data/train_indices.txt" \
# -set2 "data/test_indices.txt" \
# -o "data/"
