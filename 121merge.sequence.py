#! /usr/bin/env python3


import argparse
import os
from Bio import SeqIO
import multiprocessing

def merge_sequence(fasta_file, input_path, individual):
    sequence = ""
    records = SeqIO.parse(os.path.join(input_path, fasta_file), "fasta")
    for record in records:
        #print(record.seq)
        if record.id.split("|")[0] == individual:
            sequence = "%s"%(record.seq)
    return sequence

def get_individual_name(fasta):
    records = SeqIO.parse(fasta, "fasta")
    individual_name = []
    for record in records:
        individual_name.append(record.id.split("|")[0])
    return individual_name

def make_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type = str, help = "The path of input")
    parser.add_argument("--thread", type = int, default = 40, help = "The number of threads")
    args = parser.parse_args()
    return args

def main():
    args = make_args()
    input_path = args.input
    fasta_files = []
    for fasta_file in os.listdir(input_path):
        if 'gb' == fasta_file.split("-")[-1]:
            if 0 not in [len(record.seq) for record in SeqIO.parse(fasta_file, "fasta")]:
                fasta_files.append(fasta_file)
    individual_name = get_individual_name(os.path.join(input_path, fasta_files[0]))
    parsition_num = 1
    partition_num = 1
    for individual in individual_name:
        print("ANALYSIZING " + individual + " ......")
        partitioned_file = os.path.join(input_path, "partitioned_file")
        partitioned_content = open (partitioned_file, "w")
        partitioned_content.write("#nexus" + "\n")
        partitioned_content.write("begin sets;" + "\n")
        
        
        individual_file = os.path.join(input_path, "%s.indivudal.fa"%individual)
        individual_content = open (individual_file, "w")
        individual_content.write(">"+individual+"\n")
        for fasta_file in fasta_files:
            sequence = merge_sequence(fasta_file, input_path, individual)
            individual_content.write(str(sequence))
            parsition_num_end = len(str(sequence))+parsition_num-1
            partitioned_content.write("\tcharset part%s = %s-%s;"%(str(partition_num), str(parsition_num), str(parsition_num_end)))
            partitioned_content.write("\n")
            partitioned_content.write("#%s"%fasta_file)
            partitioned_content.write("\n")
            parsition_num = parsition_num_end+1
            partition_num += 1
        parsition_num = 1
        partition_num = 1
        individual_content.write("\n")
        individual_content.close()
        partitioned_content.close()
    
if __name__ == "__main__":
    main()
    






        
