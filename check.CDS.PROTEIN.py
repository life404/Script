#! /usr/bin/env python3

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import argparse
import os


def open_CDS_file (CDS_file):
    cds_records = SeqIO.parse(CDS_file, "fasta")
    return cds_records

def open_PROTEIN_file (PEP_file):
    protein_records = SeqIO.parse(PEP_file, "fasta")
    return protein_records

def clean_PROTEIN(protein_records):
    clean_protein = []
    for record in protein_records:
        if str(record.seq)[-1] == "*":
            record.seq = Seq(str(record.seq).strip("*"))
            clean_protein.append(record)
        else:
            clean_protein.append(record)
    
    return clean_protein


def check(cds_records, clean_protein):
    cds = list(cds_records)
    protein = list(clean_protein)
#    print(len(cds), len(protein))
    if len(cds) == len(protein):
        for i in range(0, len(cds)):
            check1 = cds[i]
            check2 = protein[i]
            

            if len(check1.seq) >= len(check2.seq)*3:

                remainder = len(check1.seq) % 3

                if remainder == 0:
                    print(">%s" % check1.id)
                    print(check1.seq)

                else:
                    splited = SeqRecord(Seq(str(check1.seq)[0:-remainder]), id = check1.id)
                    coding = str(splited.translate().seq).strip("*")

                    if coding.replace("*", "X") == str(check2.seq):
                        print(">%s" % splited.id)
                        print(splited.seq)
                
                    else:
                        splited = SeqRecord(Seq(str(check1.seq)[remainder:]), id = check1.id)
                        coding = str(splited.translate().seq).strip("*")

                        if coding.replace("*", "X") == str(check2.seq):
                            print(">%s" % splited.id)
                            print(splited.seq)

                        else:
                            print("please check %s" % splited.id)
            else:
                remainder = (len(check2.seq)*3-len(check1.seq)) % 3
                print(">%s" % check1.id)
                print(str(check1.seq)[0:-(3-remainder)])
                    

def make_args():
    parse = argparse.ArgumentParser()
    parse.add_argument("-i", "--input", type = str, help = "input file cds")
    parse.add_argument("-I", "--INPUT", type = str, help = "input file protein")
    args = parse.parse_args()

    return args

def main():
    args = make_args()
    CDS_file = args.input
    PEP_file = args.INPUT

    cds_records = open_CDS_file(CDS_file)
    protein_records = open_PROTEIN_file(PEP_file)
    clean_protein = clean_PROTEIN(protein_records)

    check(cds_records, clean_protein)


if __name__ == "__main__":
    main()
