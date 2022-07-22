#! /usr/bin/env python3

from Bio import AlignIO
import argparse

parse = argparse.ArgumentParser()
parse.add_argument("--input","-i", help = "Input file, must fasta type")
parse.add_argument("--outtype", "-ot", help = "The type of output, should be one in `stockholm, fasta, phylip, phylip-relaxed, clustal`")
args = parse.parse_args()

fasta = args.input
outtype = args.outtype

alignment = AlignIO.read(fasta, "fasta")
AlignIO.write(alignment, fasta+"."+outtype, outtype)



