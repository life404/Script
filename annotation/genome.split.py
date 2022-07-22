#! /usr/bin/env python3

import argparse
from Bio import SeqIO
import os

def fasta_info(faidx):
    genome_info = {}
    with open (faidx) as file:
        for line in file:
            array = line.strip().split("\t")
            seq_id = array[0]
            seq_len = array[1]
            genome_info[seq_id] = int(seq_len)

    return genome_info

def write_fasta(seq, file_num, start, end):
    file_name = "_genome.fa" + "{:0>3d}".format(file_num)
    seq_id = str(seq.id) + "_" + "{:0>3d}".format(file_num)
    seq_seq = seq.seq[start:end]
    seq_record = SeqIO.SeqRecord(seq_seq)
    seq_record.id = seq_id
    SeqIO.write(seq_record, file_name, "fasta")


def split_fasta(genome_info, fasta, split_len):
    split_info = open("split.info", "w")
    sequence = SeqIO.parse(fasta, "fasta")
    file_num = 0
    for seq in sequence:
        if split_len >= genome_info[seq.id]:
            file_name = "_genome.fa" + "{:0>3d}".format(file_num)
            SeqIO.write(seq, file_name, "fasta")
            file_num += 1
            split_info.write("%d\t%d\t%s\t%s\n" %(start, end, seq.id, file_name))
        else:
            start=0
            end=split_len
            write_fasta(seq, file_num, start, end)
            split_info.write("%d\t%d\t%s\t%s\n" %(start, end, seq.id, "_genome.fa" + "{:0>3d}".format(file_num)))

            file_num += 1

            while end < genome_info[seq.id]:
                start = end - 50000
                end += split_len
                write_fasta(seq, file_num, start, end)
                split_info.write("%d\t%d\t%s\t%s\n" %(start, end, seq.id, "_genome.fa" + "{:0>3d}".format(file_num)))
                
                file_num += 1
                end += split_len

            start = end - split_len - 50000
            end = genome_info[seq.id]
            write_fasta(seq, file_num, start, end)
            split_info.write("%d\t%d\t%s\t%s\n" %(start, end, seq.id, "_genome.fa" + "{:0>3d}".format(file_num)))
    split_info.close()

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("--faidx", type = str, dest = "faidx", help = "faidx of genome")
    parse.add_argument("--genome", type = str, dest = "geno", help = "genome fasta file")
    parse.add_argument("--len", type = int, dest = "length", default = 5000000, help = "the length of split, default = 5000000")
    args = parse.parse_args()
    faidx = args.faidx
    fasta = args.geno
    split_len = args.length

    genome_info = fasta_info(faidx)
    split_fasta(genome_info, fasta, split_len)

if __name__ == "__main__":
    main()
