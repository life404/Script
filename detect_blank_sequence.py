#! /usr/bin/env python3 

from Bio import SeqIO
import sys


sequences = SeqIO.parse(sys.argv[1], "fasta")

for sequence in sequences:
    if len(sequence.seq) == 0:
        print(sequence.id)


