#! /usr/bin/env python3

import argparse
from Bio import SeqIO
import math
import numpy as np
import gzip


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("--input", type = str, help = "input file")
    args = parse.parse_args()

    input = args.input
    # with gzip.open (input, "rt") as fastq:
    #     records = SeqIO.parse(fastq, "fastq-illumina")
    # seq_length = []
    # for record in records:
    #     seq_length.append(len(records[record].seq))
    
    seq_length = []
    with gzip.open (input, "rt") as handle:
        for r in SeqIO.parse(handle, "fastq"):
            seq_length.append(len(r))

    print("begin")
    all_length = sum(seq_length)
    seq_length.sort(reverse=True)
    Nx0 = 0
    start = 1
    for i in seq_length:
        Nx0 = Nx0 + i
        distri = float(Nx0/all_length)*100
        if start == int(distri)+0.01:
            continue
        else:
            for percent in np.arange(start,int(distri)+0.01, 0.01):
                print("%f\t%d" %(percent, i))
            start = int(distri)+0.01

            


if __name__ == "__main__":
    main()
