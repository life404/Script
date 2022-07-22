#! /usr/bin/env python3

from Bio import SeqIO
import argparse

def make_args():
    parse = argparse.ArgumentParser()
    parse.add_argument("-i", "--input", help = "input file")
    parse.add_argument("-t", "--threshod", default = "0.5", type = float, help = "the threshod of gap percent")
    args = parse.parse_args()

    return args

def main():
    args = make_args()
    fasta = args.input
    threshod = args.threshod

    for record in SeqIO.parse(fasta, "fasta"):
        seq = record.seq
        count = seq.count("-")
        percent = float(count/len(seq))

        if percent < threshod:
            print(">%s %s" %(record.id, percent))
            print("%s" %(seq))

if __name__ == "__main__":
    main()
