# pytrim2
> pytrim2 searches adapter sequences in nanopore reads, trims the adapter sequences and demultiplexes reads. The program is memory friendly and able to process very large files with economic ram usage.


## Install

`pip install pytrim2`

## How to use

`pytrim2.demultiplex(input_file, input_file_type, primer_file, primer_file_type, output_folder, max_distance, max_alignments)`

## Example

`pytrim2.demultiplex("test_data/test.fasta", "fasta", "test_data/test_primer.fasta", "fasta", "test_out", 200, 5)`
