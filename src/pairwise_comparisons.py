import gzip
import multiprocessing as mp
from functools import partial
from itertools import combinations
from argparse import ArgumentParser

import utils.helper_functions as helper

def parse_arguments():
    parser = ArgumentParser(description="")
    parser.add_argument('-i','--fasta_path_i',type=str,required=True,help="")
    parser.add_argument('-j','--fasta_path_j',type=str,default=None,help="")
    parser.add_argument('-p','--pairwise_path',type=str,default=None,help="")
    parser.add_argument('-m','--match',type=int,default=1,help="")
    parser.add_argument('-x','--mismatch',type=int,default=1,help="")
    parser.add_argument('-g','--gap_open',type=int,default=2,help="")
    parser.add_argument('-e','--gap_extend',type=int,default=1,help="")
    parser.add_argument('-n','--n_processes',type=int,default=1,help="")
    parser.add_argument('-o','--outpath',type=str,required=True,help="")
    return parser.parse_args()

def pairwise_smith_waterman_scores():
    args = parse_arguments()

    if args.fasta_path_j is not None:
        print("Computing pairwise SW scores between the two sequence files provided.",flush=True)
        print(f"  FASTA file i: {args.fasta_path_i}",flush=True)
        print(f"  FASTA file j: {args.fasta_path_j}",flush=True)
        print(f"  CPUs: {args.n_processes}",flush=True)
        print(f"  Output path: {args.outpath}",flush=True)
        pairs = helper.pairwise_generator_from_fastas(args.fasta_path_i,args.fasta_path_j)


    elif args.pairwise_path is not None:
        print("Computing pairwise SW scores from a list of paired sequence IDs.",flush=True)
        print(f"  FASTA file i: {args.fasta_path_i}",flush=True)
        print(f"  File with paired sequence IDs: {args.pairwise_path}",flush=True)
        print(f"  CPUs: {args.n_processes}",flush=True)
        print(f"  Output path: {args.outpath}",flush=True)
        pairs = helper.pairwise_generator_from_pairwise_list(args.pairwise_path,args.fasta_path_i)

    else:
        print("Computing all-all SW scores for the provided sequence file.",flush=True)
        print(f"  FASTA file: {args.fasta_path_i}",flush=True)
        print(f"  CPUs: {args.n_processes}",flush=True)
        print(f"  Output path: {args.outpath}",flush=True)
        seqs  = helper.parse_fasta_to_generator(args.fasta_path_i)
        pairs = combinations(seqs,2)

    with mp.Pool(args.n_processes) as p:
        compute_sw_score_partial = partial(
            helper.compute_sw_score,
            match=args.match,
            mismatch=args.mismatch,
            gap_open=args.gap_open,
            gap_extend=args.gap_extend
        )
        results = p.map(compute_sw_score_partial,pairs)

    with gzip.open(args.outpath,"wt") as handle:
        handle.write("id_i,id_j,sw\n")
        for (id_i,id_j,sw) in results:
            handle.write(f"{id_i},{id_j},{sw}\n")

    print("Done!",flush=True)

if __name__ == "__main__":
    pairwise_smith_waterman_scores()