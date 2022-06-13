# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['findAlingments']

# Cell
# Import dependencies
from Bio import SeqIO
from Bio import Align
from Bio.Seq import Seq
import numpy as np

# Cell

def findAlingments(record_dict, barcode_primer, inward_end, max_alignments):

    record_keys = list(record_dict.keys())

    aligner = Align.PairwiseAligner()
    aligner.match_score = 1.0
    aligner.mismatch_score = 0
    aligner.gap_score = -2
    aligner.mode = "local"

    n_sequences = len(record_keys)

    array_cols = max_alignments + 2
    al_array = np.zeros( (n_sequences, array_cols) )

    for i in list(range(0, n_sequences, 1)):
        al = []
        seq = record_dict[record_keys[i]].seq[0:inward_end]
        alignments = aligner.align(seq, barcode_primer)
        len_alignments = len(alignments)
        if(len_alignments <= max_alignments):
            score = alignments.score
            al = [j.aligned for j in alignments]
            len_al = len(al)
            for k in range(0, len_al):
                al[k] = (al[k][0][0][1])
            al_array[i, 0:len(al)] = al # ends of each alignment
            al_array[i, -2] = len_alignments # number of alingments
            al_array[i, -1] = np.around(alignments.score/len(barcode_primer)*100) # normalized local alingnment score

    return(al_array)

