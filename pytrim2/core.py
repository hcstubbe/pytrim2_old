# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['findAlingments', 'align_barcodes', 'decide_barcode_id', 'trim_record', 'sort_records_to_file', 'pytrim2']

# Cell

# Import dependencies
from Bio import SeqIO
from Bio import Align
from Bio.Seq import Seq
import numpy as np

# Cell

# Find alignments for each primer in a sequence record
def findAlingments(seq_record, primer_dict, inward_end, max_alignments):

    primer_keys = list(primer_dict.keys())

    aligner = Align.PairwiseAligner()
    aligner.match_score = 1.0
    aligner.mismatch_score = 0
    aligner.gap_score = -2
    aligner.mode = "local"

    n_sequences = len(primer_keys)

    array_cols = max_alignments + 3
    al_array = np.zeros( (n_sequences, array_cols) )

    for i in list(range(0, n_sequences, 1)):
        al = []
        seq = primer_dict[primer_keys[i]].seq
        alignments = aligner.align(seq_record[0:inward_end], seq)
        len_alignments = len(alignments)
        if(len_alignments <= max_alignments):
            score = alignments.score
            al = [j.aligned for j in alignments]
            len_al = len(al)
            for k in range(0, len_al):
                al[k] = (al[k][0][0][1])
            al_array[i, 0:len(al)] = al # ends of each alignment
            al_array[i, -3] = max(al) # maximum posistion of each alignment
            al_array[i, -2] = len_alignments # number of alingments
            al_array[i, -1] = np.around(alignments.score/len(seq)*100, 0) # normalized local alingnment score

    return(al_array)



# Cell

# Aligne all barcodes in a list of seq records
def align_barcodes(primer_dict, record_dict, inward_end, max_alignments):

    record_keys = list(record_dict.keys())
    n_sequences = len(record_keys)

    alingments = list( range(0, n_sequences) )
    for i in list(range(0, n_sequences, 1)):
        seq_i = record_dict[record_keys[i]].seq

        alingments[i] = findAlingments(seq_i, primer_dict, inward_end, max_alignments)
    return(alingments)

# Cell

# Decide which barcode is best hit; remove if tie
def decide_barcode_id(alginment_arrays):
    id_array = np.zeros((np.shape(alginment_arrays)[0],2), dtype=np.int64)
    for i in range(0, np.shape(alginment_arrays)[0]):
        array_i = alginment_arrays[i]
        id_i = np.where(array_i[:,-1] == np.max(array_i[:,-1]))[0]
        if len(id_i) == 1:
            id_array[i,0] = id_i
            id_array[i,1] = array_i[id_i,-3]
        elif len(id_i) >= 1:
            id_array[i,0] =  -1
            id_array[i,1] = 0

    return(id_array)

# Cell

# Trim barcodes of sequence
def trim_record(seq_record, primer_end_position):
    x = seq_record
    x.seq =  x.seq[primer_end_position:]
    return(x)

# Cell

# Sort records into new files based on barcodes and name files after barcodes
def sort_records_to_file(record_dict, primer_dict, output_folder, alginment_arrays):

    seq_barcode_res = decide_barcode_id(alginment_arrays)
    seq_barcode_ids = seq_barcode_res[:,0]
    seq_barcode_end_pos = seq_barcode_res[:,1]
    primer_keys = list(primer_dict.keys())
    record_keys = list(record_dict.keys())
    record_numbers = range(0, len(record_keys))

    for k in range(0, len(primer_dict)):
        seq_iterator_k = (trim_record(record_dict[record_keys[i]], seq_barcode_end_pos[i]) for i in record_numbers if seq_barcode_ids[i] == k)
        SeqIO.write(seq_iterator_k, output_folder + "/" + primer_dict[primer_keys[k]].name + "_seqs.fasta", "fasta")



# Cell

# Run the program
def pytrim2(input_file, input_file_type, primer_file, primer_file_type, output_folder):
    primer_dict = SeqIO.index(primer_file, primer_file_type)
    record_dict = SeqIO.index(input_file, input_file_type)
    alginment_arrays = align_barcodes(primer_dict, record_dict, 200, 10)
    sort_records_to_file(record_dict, primer_dict, output_folder, alginment_arrays)