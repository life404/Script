#! /usr/bin/env python3
from Bio import AlignIO
import os
import sys
import argparse


class toPhylip:
    'translate input file to Phylip of PAML'

    def __init__(self, msa_file, type, output):
        self.type = type
        self.msa = msa_file
        self.output = output

    def open_file(self):
        alignments = AlignIO.read(open(self.msa), self.type)

        return alignments
    
    def phy_path(self):
        phy_path = os.path.join(self.output, os.path.splitext(os.path.split(self.msa)[-1])[0] + ".phy")
        return phy_path

    def writePhylip(self):
        alignments = self.open_file()

        phy_file = self.phy_path() 
        phy = open(phy_file, "w")

        phy.writelines("%s\t%s\n" % (len(list(alignments)),
                                     alignments.get_alignment_length()))
        for record in alignments:
            phy.writelines(record.id)
            phy.writelines("\n")

            phy.writelines(record.seq)
            phy.writelines("\n")
        phy.close()


def make_parse():
    parse = argparse.ArgumentParser()
    parse.add_argument("-i", "--input", help = "input")
    parse.add_argument("-t", "--type", default = "fasta", help = "the type of input file")
    parse.add_argument("-o", "--output", help = "output dirtory")
    args = parse.parse_args()
    return args

def main():
    args = make_parse()
    msa_file = args.input
    type = args.type
    output = args.output

    Phy_object = toPhylip(msa_file, type, output)
    Phy_object.writePhylip()

if __name__ == "__main__":
    main()
        
