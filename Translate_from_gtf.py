#! /usr/bin/env python

import sys
import subprocess
import argparse
import collections
import re
from Bio.Seq import Seq


def reverse_commend(line):
    seq = Seq(line)
    return seq.reverse_complement()

def get_cds_from_gtf(fasta_file, gtf_file):
    bed_file = open("tmp.bed", "w")
    with open (gtf_file, "r") as files:
        for line in files:
            line_list = line.strip().split("\t")
            try:
                if "mRNA" in line_list[2] or "transcript" in line_list[2]:
                    tag = re.search(r'gene_id ["\w.]*', line.strip()).group().split(" ")[1] + \
                        "|" + re.search(r'transcript_id ["\w.]*', line.strip()).group().split(" ")[1] + "|" + line_list[6]
                elif "CDS" in line_list[2]:
                    chromosome_name = line_list[0]
                    start = str(int(line_list[3])-1)
                    end = line_list[4]
                    bed_info = "\t".join([chromosome_name, start, end, tag])
                    bed_file.write(bed_info)
                    bed_file.write("\n")
            except IndexError:
                continue
    bed_file.close()
    command = " ".join(["bedtools", "getfasta", "-fi", fasta_file, "-bed" , "tmp.bed", "-fo", "tmp.fasta", "-name"])
    print(command)
    subprocess.call(command, shell=True)

def get_cds_from_gff(fasta_file, gtf_file):
    bed_file = open("tmp.bed", "w")
    with open (gtf_file, "r") as files:
        for line in files:
            line_list = line.strip().split("\t")
            try:
                if "mRNA" in line_list[2] or "transcript" in line_list[2]:
                    tag = re.search(r'gene_id=["\w.]*', line.strip()).group().split("=")[1] + \
                        "|" + re.search(r'transcript_id=["\w.]*', line.strip()).group().split("=")[1].strip("\"") + "|" + line_list[6]
                    #print(tag)
                elif "CDS" in line_list[2]:
                    chromosome_name = line_list[0]
                    start = str(int(line_list[3])-1)
                    end = line_list[4]
                    bed_info = "\t".join([chromosome_name, start, end, tag])
                    #print(bed_info)
                    bed_file.write(bed_info)
                    bed_file.write("\n")
            except IndexError:
                continue
    bed_file.close()
    command = " ".join(["bedtools", "getfasta", "-fi", fasta_file, "-bed" , "tmp.bed", "-fo", "tmp.fasta", "-name"])
    print(command)
    subprocess.call(command, shell=True)


def get_seq():
    mRNA_seq = collections.OrderedDict()
    #mRNA_seq = {}
    with open ("tmp.fasta", "r") as file:
        for line in file:
            line = line.strip()
            if ">" in line:
                tag = line.split("::")[0]
            else:
                if tag in mRNA_seq.keys():
                    if "+" in tag:
                        mRNA_seq[tag].append(Seq(line))
                    elif "-" in tag:
                        mRNA_seq[tag].append(reverse_commend(line))
                elif tag not in mRNA_seq.keys() :
                    if "+" in tag:
                        mRNA_seq[tag] = []
                        mRNA_seq[tag].append(Seq(line))
                    elif "-" in tag:
                        mRNA_seq[tag] = []
                        mRNA_seq[tag].append(reverse_commend(line))
    #for key in mRNA_seq.keys():
    #    if "-" in key:
    #        print(key, mRNA_seq[key])
    return mRNA_seq

def translate_seq_to_protein(mRNA_seq, code_table):
    print("Total " + str(len(mRNA_seq.keys())) + " protein sequences")
    protein_seq = collections.OrderedDict()
    for key in mRNA_seq.keys():
        coding_dna = Seq("")
        for seq in mRNA_seq[key]:
            coding_dna += seq
            coded_protein = coding_dna.translate(table = code_table)
            protein_seq[key] = str(coded_protein)
    return protein_seq


def defined_paramter():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fasta", type = str, help="The fasta input file")
    parser.add_argument("--gtf", type = str,  help = "The gtf formate file of annotation file")
    parser.add_argument("--code", type = int, default = 1, help = """The translation table from NCBI \n 1\tThe Standard Code (default)\n\
                                                                2\tThe Vertebrate Mitochondrial Code\n\
                                                                3\tThe Yeast Mitochondrial Code\n\
                                                                4\tThe Mold, Protozoan, and Coelenterate Mitochondrial Code and the Mycoplasma/Spiroplasma Code\n\
                                                                5\tThe Invertebrate Mitochondrial Code\n\
                                                                6\tThe Ciliate, Dasycladacean and Hexamita Nuclear Code\n\
                                                                9\tThe Echinoderm and Flatworm Mitochondrial Code\n\
                                                                10\tThe Euplotid Nuclear Code\n \
                                                                11\tThe Bacterial, Archaeal and Plant Plastid Code\n\
                                                                12\tThe Alternative Yeast Nuclear Code\n\
                                                                13\tThe Ascidian Mitochondrial Code\n\
                                                                14\tThe Alternative Flatworm Mitochondrial Code\n\
                                                                16\tChlorophycean Mitochondrial Code\n\
                                                                21\tTrematode Mitochondrial Code\n\
                                                                22\tScenedesmus obliquus Mitochondrial Code\n\
                                                                23\tThraustochytrium Mitochondrial Code\n\
                                                                24\tRhabdopleuridae Mitochondrial Code\n\
                                                                25\tCandidate Division SR1 and Gracilibacteria Code\n\
                                                                26\tPachysolen tannophilus Nuclear Code\n\
                                                                27\tKaryorelict Nuclear Code\n\
                                                                28\tCondylostoma Nuclear Code\n\
                                                                29\tMesodinium Nuclear Code\n\
                                                                30\tPeritrich Nuclear Code\n\
                                                                31\tBlastocrithidia Nuclear Code\n\
                                                                33\tCephalodiscidae Mitochondrial UAA-Tyr Code""")
    args = parser.parse_args()
    return args

def main():
    args = defined_paramter()
    fasta_file = args.fasta
    gtf_file = args.gtf
    code_table = args.code
    print("Getting CDS sequence......")
    if "gff" in gtf_file:
        get_cds_from_gff(fasta_file, gtf_file)
    elif "gtf" in gtf_file:
            get_cds_from_gtf(fasta_file, gtf_file)

    print("CDS sequences were saved in tmp.fasta")

    print("Translate DNA to protein sequence")
    mRNA_seq = get_seq()
    print("Translation table is\t" + str(code_table))
    protein_seq = translate_seq_to_protein(mRNA_seq, code_table)
    translation_file = open("translation_protein.fasta", "w")
    for key in protein_seq.keys():
        translation_file.write(key)
        translation_file.write("\n")
        translation_file.write(protein_seq[key])
        translation_file.write("\n")
    translation_file.close()
    

if __name__ == "__main__":
    main()


    
