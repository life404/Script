#! /usr/bin/env python3

from Bio import SeqIO
import argparse

parse = argparse.ArgumentParser()
parse.add_argument("-b", "--bed", help = "bed file", dest="bed")
parse.add_argument("-g", "--genome", help = "genome fasta file", dest = "genome")
args = parse.parse_args()

bed = args.bed
genome = args.genome


sequences = SeqIO.parse(genome, "fasta")
seq_dic = {}
for sequence in sequences:
    seq_dic[sequence.id] = sequence.seq

with open (bed, "r") as file:
    for line in file:
        line = line.strip()
        array = line.split("\t")
        seq = str(seq_dic[array[0]][int(array[1]):int(array[2])]).upper()
        gc = float((seq.count("G") + seq.count("C"))/(int(array[2])-int(array[1])))
        print("%s\t%f" %(line,gc))
