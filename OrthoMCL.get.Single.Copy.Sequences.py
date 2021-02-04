#! /usr/bin/env python3

import argparse
from Bio import SeqIO
from Bio import Seq
import subprocess
import os

def make_args():
    parse = argparse.ArgumentParser()
    parse.add_argument("-i", "--input", type = str, help = "input file of single copy groups")
    parse.add_argument("-d", "--dir", type = str, help = "the dir include sequences file, which were be used in OrthoMCL analysis")
    parse.add_argument("-p", "--pattern", type = str, default = ".fasta", help = "the same pattern of sequences file")
    parse.add_argument("-o", "--output", type = str, default = os.getcwd(), help = "the output director, default is current dir")
    args = parse.parse_args()
    return args

def parse_single_copy_groups(single_copy_groups):
    single_copy_dic = {}
    with open (single_copy_groups, "r") as file:
        for line in file:
            line = line.strip()
            single_copy_dic[line.split(":")[0]] = [i for i in line.split(":")[-1].strip().split(" ")]

    return single_copy_dic

def merge_fasta_file(sequences_dir, pattern):
    sequences_files = [file for file in os.listdir(sequences_dir) if pattern in file ]
    all_fa = open(os.path.join(sequences_dir, "tmp.all.fa"), "w")
    for file in sequences_files:
       all_fa.write(open(os.path.join(sequences_dir, file), "r").read())
    
    all_fa.close()

def filter_sequence(single_copy_dic, sequences_dir, output_dir):
    all_sequence = {}
    for record in SeqIO.parse(os.path.join(sequences_dir, "tmp.all.fa"), "fasta"):
        all_sequence[record.id] = str(record.seq)
    for key, value in single_copy_dic.items():
        single_copy_seq = open(os.path.join(output_dir, key+".fa"), "w")
        for i in value:
            single_copy_seq.write(">" + i)
            single_copy_seq.write("\n")
            single_copy_seq.write(all_sequence[i])
            single_copy_seq.write("\n")
        single_copy_seq.close()
    os.remove(os.path.join(sequences_dir, "tmp.all.fa"))

def main():
    args = make_args()
    single_copy_groups = args.input
    sequences_dir = args.dir
    pattern = args.pattern
    output_dir = args.output

    single_copy_dic = parse_single_copy_groups(single_copy_groups)

    merge_fasta_file(sequences_dir, pattern)

    filter_sequence(single_copy_dic, sequences_dir, output_dir)

if __name__ == "__main__":
    main()











