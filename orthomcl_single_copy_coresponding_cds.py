#! /usr/bin/env python3

import argparse
from Bio import SeqIO
import os
import re




def make_parse():
    parse = argparse.ArgumentParser()
    parse.add_argument("-i", "--input", type = str, help = "OG dir")
    parse.add_argument("-d", "--dir2", type = str, help = "CDS dir")
    args = parse.parse_args()

    return args

def main():
    args = make_parse()
    input = args.input
    CDS_dir = args.dir2

    OG_ID = {}
    with open (input, "r") as file:
        for line in file:
            if ">" in line:
                line = line.strip(">").strip()
                OG_ID[line.split("|")[0]] = line.split("|")[1]

    for key, value in OG_ID.items():
        records = SeqIO.parse(os.path.join(CDS_dir, key+".CDS"), "fasta")
        for record in records:
            if key == "IaIo":
                if value == record.id:
                    print(">%s|%s_CDS" %(key, value))
                    print(record.seq)
            else:  
                if value == re.search(r"protein_id=[A-Z]*_[0-9]+.[0-9]+", record.description)[0].split("=")[1]:
                    print(">%s|%s_CDS" %(key, value))
                    print(record.seq)



if __name__ == "__main__":
    main()