#! /usr/bin/env python3

import argparse
import subprocess
import os

def make_argparse():
    parse = argparse.ArgumentParser()
    parse.add_argument("--input", type = str, help = "The input file include the path of mat file and fasta file")
    parse.add_argument("--output", type = str, help = "the output dir")
    parse.add_argument("--threads", default= 40, type = int, help = "threads")
    args = parse.parse_args()
    return args

def parse_input(input_file):
    input_list = []
    with open (input_file) as file:
        for line in file:
            line = line.strip()
            input_list.append(line)

    return input_lt

def split_fasta(fasta):
    if os.path.exists(fasta):
        split_command = " ".join(["/disk/tools/seqkit", "split", "-i", "-o tmp.split", fasta])

