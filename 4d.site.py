#! /usr/bin/env python3

import argparse

parse = argparse.ArgumentParser()
parse.add_argument("-i", "--input", help = "input file")
args = parse.parse_args()


_4d_codon = ["GCT", "GCC", "GCA", "GCG",
            "CGT", "CGC", "CGA", "CGG",
             "GGT", "GGC", "GGA", "GGG",
            "CTT", "CTC", "CTA", "CTG",
            "CCT", "CCC", "CCA", "CCG",
            "TCT", "TCC", "TCA", "TCG",
            "ACT", "ACC", "ACA", "ACG",
            "GTT", "GTC", "GTA", "GTG"]


with open (args.input, "r") as file:
    for line in file:
        line = line.strip()
        if ">" in line:
            print(line)
        else:
            if len(line) % 3 == 0:
                _4d_site = []
                for i in range(0,len(line),3):
                    codon = line[i:i+3]
                    if codon in _4d_codon:
                        _4d_site.append(codon[-1])
                    else:
                        _4d_site.append("-")
                print("".join(_4d_site))
            else:
                print("your sequence isnot the multiple of three")
                exit


