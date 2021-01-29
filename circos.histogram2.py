#! /usr/bin/env python3

import os
import argparse
import multiprocessing
import shutil


def split_chromosome_into_bin(ideogram, split_len):
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


def split_gff(gff3):
    if not os.path.exists("./tmp"):
        os.mkdir("./tmp")
    else:
        shutil.rmtree("./tmp")
        os.mkdir("./tmp")

    file_num = 1
    line_num = 0
    LIMIT = 10000
    content = []
    with open(gff3, "r") as file:
        for line in file:
            line_num += 1
            if line_num < LIMIT:
                content.append(line)
            else:
                tmp_file = os.path.join("./tmp", ('tmp%s' % file_num))
                tmp = open(tmp_file, "w")
                for line in content:
                    tmp.write(line)
                tmp.close()
                content = []
                line_num = 0
                file_num += 1

def remove_duplicate(gff3):
    rd_result = open (os.path.join("./tmp", '%s.rd'%gff3), "w")
    chromosome_name = ''
    with open (os.path.join("./tmp", gff3), "r") as file:
        for line in file:
            line = line.strip()
            array = line.split("\t")
            if array[0] != chromosome_name:
                real_start = float('inf')
                real_end = float('inf')
                TE_name = []
                if int(array[4]) < real_start:
                    if real_start != float('inf') and real_end != float(inf)
                        rd_result.write('\t'.join([chromosome_name, str(real_start), str(real_end), ';'.join(TE_name)]))
                        rd_result.write("\n")
                    real_start = int(array[3])
                    real_end = int(array[4])
                    TE_name = []
                    TE_name.append(array[8].split(";")[0])
                else:
                    real_start = int(array[3])
                    TE_name.append(array[8].split(";")[0])
    rd_result.close()

            


def analysis_gff(chromosome_bin, tmp_file):
    print("Begin analysis " + tmp_file)
    result_file = '%s.out' % (tmp_file)
    result = open(os.path.join('./tmp', result_file), "w")
    content = ''
    with open(os.path.join('./tmp', tmp_file), "r") as file:
        for line in file:
            line = line.strip()
            array = line.split("\t")
            chromosome_name = array[0]
            TE_start = int(array[3])
            TE_end = int(array[4])
            TE_name = array[8].split(";")[0]
            previout_end = 0
            if chromosome_name in chromosome_bin.keys():
                for i in range(0, len(chromosome_bin[chromosome_name])-1):
                    if TE_start >= chromosome_bin[chromosome_name][i] and TE_end <= chromosome_bin[chromosome_name][i+1]:
                        TE_len = TE_end - TE_start
                        content = ":".join([chromosome_name, 
                                            str(chromosome_bin[chromosome_name][i]), 
                                            str(chromosome_bin[chromosome_name][i+1])]) + "\t" + str(TE_len) + "\t" + TE_name
                        result.write(content)
                        result.write("\n")
                        previout_end = TE_end

                    elif TE_start < chromosome_bin[chromosome_name][i] and TE_end in range(chromosome_bin[chromosome_name][i], chromosome_bin[chromosome_name][i+1]):
                        TE_len = TE_end - chromosome_bin[chromosome_name][i]
                        content = ":".join([chromosome_name, 
                                            str(chromosome_bin[chromosome_name][i]), 
                                            str(chromosome_bin[chromosome_name][i+1])]) + "\t" + str(TE_len) + "\t" + TE_name
                        result.write(content)
                        result.write("\n")

                    elif TE_start in range(chromosome_bin[chromosome_name][i], chromosome_bin[chromosome_name][i+1]) and TE_end > chromosome_bin[chromosome_name][i+1]:
                        TE_len= chromosome_bin[chromosome_name][i+1] - TE_start
                        content = ":".join([chromosome_name, 
                                            str(chromosome_bin[chromosome_name][i]), 
                                            str(chromosome_bin[chromosome_name][i+1])]) + "\t" + str(TE_len) + "\t" + TE_name
                        result.write(content)
                        result.write("\n")
            else:
                continue
                
    result.close()
    print("Finish analysis " + tmp_file)

def multip_computation(thread, chromosome_bin):
    tmp_files = os.listdir("./tmp/")
    pool = multiprocessing.Pool(thread)
    for tmp_file in tmp_files:
        pool.apply_async(analysis_gff, args = (chromosome_bin, tmp_file))
    pool.close()
    pool.join()

def merge_result():
    print("Merging Result.....")
    result_file = []
    for file in os.listdir("./tmp"):
        if 'out' in file:
            result_file.append(file)
    
    final_file = os.path.join("./", "circos.histogram.input")
    merge_file = os.path.join("./", "circos.mergeed")
    final_result = open (final_file, "w")
    merge_result = open (merge_file, "w")
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
    print("Finish")

    for key, value in TE_all.items():
        array = key.split(":")
        percent = float(int(value)/(int(array[2])-int(array[1])))*100
        final_result.write('\t'.join([array[0], array[1], array[2], '%.2f%%'%(percent)]))
        final_result.write('\n')
    final_result.close()

def make_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ideogram", type = str, help = "path of ideogram file")
    parser.add_argument("-g", "--gff", type = str, help = "path of gff3 file")
    parser.add_argument("-s", "--split", type = int, default = 100000, help = "split length")
    parser.add_argument("-t", "--threads", type = int, default = 1, help = "threads number")
    args = parser.parse_args()
    return args
                

def main():
    args = make_args()
    ideogram = args.ideogram
    gff3 = args.gff
    split_len = args.split
    thread = args.threads
    #chromosome_bin = split_chromosome_into_bin(ideogram, split_len)
    #print(chromosome_bin)
    #split_gff(gff3)
    tmp_file = 'tmp1'
    remove_duplicate(tmp_file)
    #analysis_gff(chromosome_bin, tmp_file)
    #multip_computation(thread, chromosome_bin)
    #merge_result()


if __name__ == "__main__":
    main()
