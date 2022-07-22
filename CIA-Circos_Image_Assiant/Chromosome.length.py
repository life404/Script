#! /usr/bin/env python3

import argparse
from Bio import SeqIO
import os


def make_parse():
    parse = argparse.ArgumentParser()
    parse.add_argument("--input", "-i", type = str, help = "The fasta file of genome")
    parse.add_argument("--out", "-o", default = os.path.join(os.getcwd(), "ideogram.input"), 
                       required=False, type = str,
                       help = "The output file is the ideogram input of Circos")
    args = parse.parse_args()
    return args

def parse_fasta(fasta):
    seq_info = {}
    with open (fasta, "r") as fasta_tmp:
        for seq in SeqIO.parse(fasta_tmp, "fasta"):
            seq_info[seq.id] = len(seq)

    return seq_info

def writeout(output, seq_info):
    
    with open (output, "w") as file:
        chr_num = 1
        for key, value in seq_info.items():
            file.write("chr - chr%s %s 0 %s chr%s\n" %(chr_num, key, value, chr_num))
            chr_num += 1

def main():
    args = make_parse()
    fasta = args.input
    output = args.out

    seq_info = parse_fasta(fasta)
    writeout(output, seq_info)


if __name__ == "__main__":
    main()
