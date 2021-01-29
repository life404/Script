#! /usr/bin/env python3

import os
import multiprocessing
import argparse
import time
from Bio import SeqIO

def remove_duplicate_region(input_path, gff3):
    begin = 0
    end = 0
    output_file = os.path.join(input_path, '%s.absulote'%gff3)
    output_content = open (output_file, "w")
    with open (os.path.join(input_path, gff3), "r") as file:
        for line in file:
            line = line.strip()
            array = line.split("\t")
            if int(array[3]) > end:
                output_content.write(line)
                output_content.write('\n')
                begin = int(array[3])
                end = int(array[4])
            else:
                if int(array[3]) >= begin:
                    if int(array[4]) <= end:
                        continue
                    else:
                        output_content.write('\t'.join(array[0:3]) + '\t' + str(end) + '\t' +'\t'.join(array[4:]))
                        output_content.write('\n')
                        begin = end
                        end = int(array[4])
                else:
                    continue
    output_content.close()

def split_ideogram_into_bin(ideogram, split_len):
    chromosome_bin = {}
    with open(ideogram, "r") as file:
        for line in file:
            line = line.strip()
            array = line.split(" ")
            chromosome_name = array[3]
            chromosome_bin[chromosome_name] = []
            length = int(array[5])
            start = 0
            end = 0
            split_bin = range(0, length, split_len)
            for i in range(1, len(split_bin)):
                if i < (len(split_bin)-1):
                    end = split_bin[i]
                else:
                    end = length

                chromosome_bin[chromosome_name].append(start)
                chromosome_bin[chromosome_name].append(end)
                start = end + 1
    return chromosome_bin

def count(input_path, tmp_file, chromosome_bin):
    print("Analysising " + tmp_file)
    result_file = '%s.out' % (tmp_file)
    result = open(os.path.join(input_path, result_file), "w")
    content = ''
    with open(os.path.join(input_path, tmp_file), "r") as file:
        for line in file:
            line = line.strip()
            array = line.split("\t")
            chromosome_name = array[0]
            TE_start = int(array[3])
            TE_end = int(array[4])
            TE_name = array[8].split(";")[0]

            for i in range(0, len(chromosome_bin[chromosome_name])-1, 2):
                start = chromosome_bin[chromosome_name][i]
                end   = chromosome_bin[chromosome_name][i+1]
                if TE_start >= start and TE_end <= end:
                    TE_len = TE_end - TE_start
                    content = ":".join([chromosome_name, 
                                        str(start), 
                                        str(end)]) + "\t" + str(TE_len) + "\t" + TE_name
                    result.write(content)
                    result.write("\n")

                if TE_start < start and TE_end in range(start, end):
                    TE_len = TE_end - start
                    content = ":".join([chromosome_name, 
                                        str(start), 
                                        str(end)]) + "\t" + str(TE_len) + "\t" + TE_name
                    result.write(content)
                    result.write("\n")

                if TE_start in range(start, end) and TE_end > end:
                    TE_len= end - TE_start
                    content = ":".join([chromosome_name, 
                                        str(start), 
                                        str(end)]) + "\t" + str(TE_len) + "\t" + TE_name
                    result.write(content)
                    result.write("\n")

                
    result.close()
    print("Finish analysising " + tmp_file)

def analysis_GC_percent(chromosome_bin, fasta):
    GC_file = os.path.join("./", 'GC.desinity')
    GC_content = open (GC_file, "w")
    record = SeqIO.parse(fasta, "fasta")
    record = SeqIO.to_dict(record)
    for ID in list(record.keys()):
        print('ANALYSIS' + ID)
        if ID in chromosome_bin.keys():
            ID2 = "chr" + str(int(ID.split('_')[-1])+1)
            positions = chromosome_bin[ID]
            print(positions)
            for i in range(0, len(positions)-1, 2):
                start = int(positions[i])
                end = int(positions[i+1])
                sequence = record[ID][start:end].seq
                GC = float((sequence.count("G") + sequence.count("C"))/len(sequence))*100
                GC_content.write(' '.join([ID2, str(start), str(end), '%.2f'%GC]))
                GC_content.write("\n")
    GC_content.close()



def merge_result(input_path, out_prefix):
    print("START MERGING......")
    result_file = []
    for file in os.listdir(input_path):
        if 'tmp.absulote.out' in file:
            result_file.append(file)
    
    final_file = os.path.join("./", "%s.density"%out_prefix)
    merge_file = os.path.join("./", "%s.count"%out_prefix)
    circos_input = os.path.join("./", "%s.circos.histogram.input"%out_prefix)
    final_result = open (final_file, "w")
    merge_result = open (merge_file, "w")
    circos_result = open (circos_input, "w")
    TE_all = {}
    for file in result_file:
        with open (os.path.join('./tmp', file), "r") as file:
            for line in file:
                merge_result.write(line)
                line = line.strip()
                array = line.split("\t")
                if array[0] in TE_all.keys():
                    TE_all[array[0]] += int(array[1])
                else:
                    TE_all[array[0]] = 0
                    TE_all[array[0]] += int(array[1])
    merge_result.close()

    for key, value in TE_all.items():
        array = key.split(":")
        percent = float(int(value)/(int(array[2])-int(array[1])))*100
        final_result.write('\t'.join([array[0], array[1], array[2], '%.2f%%'%(percent)]))
        final_result.write('\n')
    final_result.close()

    for key, value in TE_all.items():
        array = key.split(":")
        percent = float(int(value)/(int(array[2])-int(array[1])))*100
        ID = "chr"+str(int(array[0].split("_")[-1])+1)
        circos_result.write(' '.join([ID, array[1], array[2], '%.2f'%(percent)]))
        circos_result.write('\n')
    circos_result.close()

    print("FINISH......")

def multiprocessing_analysis(thread, input_path):
    pool = multiprocessing.Pool(thread)
    for input_file in os.listdir(input_path):
        pool.apply_async(remove_duplicate_region, args = (input_path, input_file))
    pool.close()
    pool.join()

def multiprocessing_analysis2(thread, input_path, chromosome_bin):
    pool = multiprocessing.Pool(thread)
    absolute_files = []
    for input_file in os.listdir(input_path):
        if 'absulote' in input_file:
            absolute_files.append(input_file)
    for absolute_file in absolute_files:
        pool.apply_async(count, args = (input_path, absolute_file, chromosome_bin))
    pool.close()
    pool.join()


def make_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default='./tmp', help = "The path of input")
    parser.add_argument("--ideogram", type=str, help = "The path of ideogram file")
    parser.add_argument('--thread', type=int, default=40, help = "The number of threads")
    parser.add_argument('--split', type=int, default=1048576, help = "The length of split")
    parser.add_argument('--output', type=str, help = "The prefix of output file")
    parser.add_argument('--type', type=str, default=' ', help = "The type of analysis")
    parser.add_argument('--fasta', type=str, help = "The path of fasta")
    args = parser.parse_args()
    return args
    
def main():
    args = make_args()
    split_len = args.split
    ideogram = args.ideogram
    type = args.type
    chromosome_bin = split_ideogram_into_bin(ideogram, split_len)
    if type != "GC":
        input_path = args.input
        thread = args.thread
        out_prefix = args.output
        multiprocessing_analysis(thread, input_path)
        multiprocessing_analysis2(thread, input_path, chromosome_bin)
        merge_result(input_path, out_prefix)
    if type == "GC":
        fasta = args.fasta
        analysis_GC_percent(chromosome_bin, fasta)



if __name__ == "__main__":
    main()
