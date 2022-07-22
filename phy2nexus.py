#! /usr/bin/env python3

from Bio import SeqIO
import argparse


def make_parse():
    parse = argparse.ArgumentParser()
    parse.add_argument("-i", "--phylip", help = "phylip input file")
    parse.add_argument("-o", "--nexus", help = "nexus output file")
    args = parse.parse_args()
    return args


def main():
    args = make_parse()
    phylip = args.phylip
    nexus = args.nexus

    records = SeqIO.parse(phylip, "phylip")
    count = SeqIO.write(records, nexus, "nexus")
    print("Converted %i records" % count)

if __name__ == "__main__":
    main()
