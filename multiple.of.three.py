#! /usr/bin/env python3

import argparse


parse = argparse.ArgumentParser()
parse.add_argument("-i", "--input", help = "fasta file")
args = parse.parse_args()



bases = "TCAG"
codons = [a+b+c for a in bases for b in bases for c in bases]
amino_acids = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
codon_table = dict(zip(codons, amino_acids))

with open (args.input, "r") as file:
    for line in file:
        line = line.strip()
        if ">" in line:
            print(line)
        else:
            length = len(line)
            tail = length % 3
            if tail!=0:
                seq1 = line[0:(length-tail)]
                seq2 = line[tail:length]

                AA_num1 = 0
                for i in range(0, len(seq1), 3):
                    codon = seq1[i:i+3]
                    if codon in codon_table.keys():
                        if codon_table[codon] != "*":
                            AA_num1 += 1
                        else:
                            continue
                    else:
                        continue

                AA_num2 = 0
                for i in range(0, len(seq1), 3):
                    codon = seq2[i:i+3]
                    if codon in codon_table.keys():
                        if codon_table[codon] != "*":
                            AA_num2 += 1
                        else:
                            continue
                    else:
                        continue


                if AA_num1 > AA_num2:
                    print(seq1)
                elif AA_num2 > AA_num1:
                    print(seq2)
                else:
                    print("can't decide which seq was be used")
                    print(seq1)
                    print("-"*80)
                    print(seq2)

            else:
                print(line)





