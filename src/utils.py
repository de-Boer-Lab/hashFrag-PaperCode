from pyfastx import Fasta
import numpy as np
from tqdm import tqdm
from Bio import pairwise2
import random

def parse_fasta(path):
    """
    Reads sequences from a FASTA file and returns their IDs and sequences.
    Args:
        path (str): Path to the FASTA file.
    Returns:
        ids (list): List of sequence IDs.
        seqs (list): List of corresponding sequences.
    """
    ids  = []
    seqs = []
    for seqid,seq in Fasta(path,build_index=False):
        ids.append(seqid)
        seqs.append(seq)
    return ids,seqs

def list_of_statistics(similarities):
    """
    Calculate statistics from a list of similarity scores.
    
    Args:
        similarities: Array of similarity scores.

    Returns:
        dict: A dictionary containing similarity statistics.
    """
    return {
        'max_similarity': np.max(similarities),
        'median_similarity': np.median(similarities)
    }

def compute_alignment_scores(seqs_i, seqs_j):
    """
    Computes pairwise Smith-Waterman alignment scores between two sets of sequences.
    Args:
        seqs_i (list): List of sequences from the first FASTA file.
        seqs_j (list): List of sequences from the second FASTA file.
    Returns:
        np.ndarray: 2D array of alignment scores.
    """
    # Define scoring parameters for the Smith-Waterman algorithm
    match_score = 1
    mismatch_score = -1
    open_gap_score = -2
    extend_gap_score = -1
    scores_sw = []

    # Iterate over each pair of sequences from the two lists and compute alignment score
    for seq_i in seqs_i:
        for seq_j in tqdm(seqs_j):
            sw_score = pairwise2.align.localms(seq_i, seq_j, match_score, mismatch_score, open_gap_score, extend_gap_score, score_only = True)
            scores_sw.append(sw_score)

    # Reshape the list of scores into a 2D array (len(seqs_i) x len(seqs_j))
    return np.array(scores_sw).reshape(len(seqs_i), len(seqs_j))

def swap_train_test(row):
    if row['id_i_source'] == 'test' and row['id_j_source'] == 'train':
        row['id_i'], row['id_j'] = row['id_j'], row['id_i']
        row['id_i_source'], row['id_j_source'] = row['id_j_source'], row['id_i_source']
    return row

def dinucleotide_shuffle(seq):
    dinucleotides = [seq[i:i+2] for i in range(len(seq) - 1)]
    random.shuffle(dinucleotides)
    
    shuffled_seq = dinucleotides[0]
    for dinucleotide in dinucleotides[1:]:
        if shuffled_seq[-1] == dinucleotide[0]:
            shuffled_seq += dinucleotide[1]
        else:
            candidates = [d for d in dinucleotides if d[0] == shuffled_seq[-1] and d != dinucleotide]
            if candidates:
                choice = random.choice(candidates)
                shuffled_seq += choice[1]
                dinucleotides.remove(choice)
            else:
                shuffled_seq += dinucleotide
    
    return shuffled_seq

def mononucleotide_shuffle(seq):
    nucleotides = list(seq)
    random.shuffle(nucleotides)
    shuffled_seq = ''.join(nucleotides)
    return shuffled_seq

def random_dna_sequence_gc_matched(length):
    nucleotides = 'ATGC'
    weights = [0.3, 0.3, 0.2, 0.2]  # A and T (30% each), G and C (20% each) to simulate ~40% GC content
    return ''.join(random.choices(nucleotides, weights, k=length))

def random_dna_sequence(length):
    nucleotides = 'ATGC'
    weights = [0.25, 0.25, 0.25, 0.25]
    return ''.join(random.choices(nucleotides, weights, k=length))