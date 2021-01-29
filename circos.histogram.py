#! /usr/bin/env python3

import argparse
import os
import multiprocessing
import shutil


def split_chromosome_into_bin(ideogram, split_length, chromosome_bin):
    with open (ideogram, "r") as file:
        for line in file:
            line = line.strip()
            array = line.split(" ")
            chrosome = array[3]
            length = array[5]
            start = 0
            end = 0
            split_bin = range(0, int(length), split_length)
            for i in range(1, len(split_bin)):
                if i<len(split_bin)-1:
                    end = split_bin[i]
                else:
                    end = length
                
                bin_name = ''.join([chrosome,":",str(start),":",str(end)])
                chromosome_bin[bin_name] = 0
                start = int(split_bin[i])

def read_gff3(gff3, chromosome_bin):
    print("Begin analysis " + gff3)
    with open (gff3, "r") as file:
        for line in file:
            #print (line)
            line = line.strip()
            array = line.split("\t")
            TE_name = array[0]
            TE_start = int(array[3])
            TE_end = int(array[4])
            TE_len = int(array[4]) - int(array[3]) + 1
            for location in chromosome_bin.keys():
                if TE_name == location.split(":")[0]:
                    if TE_start >= int(location.split(":")[1]) and TE_end <= int(location.split(":")[2]):
                        #lock.acquire()
                        base_num = chromosome_bin[location]
                        base_num += TE_len
                        chromosome_bin[location] = base_num
                        #lock.release()
                    elif TE_start >= int(location.split(":")[1]) and TE_start <= int(location.split(":")[2]):
                        if TE_end > int(location.split(":")[2]):
                            TE_len = int(location.split(":")[2]) - int(TE_start)
                            #lock.acquire()
                            base_num = chromosome_bin[location]
                            base_num += TE_len
                            chromosome_bin[location] = base_num
                            #lock.release()
                    elif TE_end >= int(location.split(":")[1]) and TE_end <= int(location.split(":")[2]):
                        if TE_start < int(location.split(":")[1]):
                            TE_len = TE_end - int(location.split(":")[1])
                            #lock.acquire()
                            base_num = chromosome_bin[location]
                            base_num += TE_len
                            chromosome_bin[location] = base_num
                            #lock.release()
                    else:
                        continue
                else:
                    continue
    print("Finish " + gff3)

def split_file(gff3):
    if not os.path.exists("./tmp/"):
        os.mkdir("./tmp")
    else:
        shutil.rmtree("./tmp")
        os.mkdir("./tmp")

    line_num = 0
    file_num = 1
    LIMIT = 10000
    tmp_content = []
    test = 0
    with open (gff3, "r") as bigfile:
        for line in bigfile:
            test += 1
            line_num += 1
            if line_num < LIMIT:
                tmp_content.append(line)
            
            else:
                tmp_content.append(line)
                tmp_file = os.path.join("./tmp", 'tmp%s'%str(file_num))
                tmp = open(tmp_file, "w")
                for line in tmp_content:
                    tmp.write(line)
                tmp.close()
                tmp_content = []
                line_num = 0
                file_num += 1
    #print(len(tmp_content))
    #print(test)
    if tmp_content:
        tmp_file = os.path.join("./tmp", 'tmp%s'%str(file_num))
        tmp = open(tmp_file, "w")
        for line in tmp_content:
            tmp.write(line)
        tmp.close()

def make_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ideogram", type = str, help = "The ideogram file of circos")
    parser.add_argument("--split_len", type = int, help = "The length of bin ")
    parser.add_argument("--gff", type = str, help = "The TE annotation files in GFF3 format")
    parser.add_argument("--threads", type = int, default=20, help = "The number of threads")
    args = parser.parse_args()
    return args

def main():
    chromosome_bin = multiprocessing.Manager().dict()
    #lock = multiprocessing.Lock()
    args = make_args()
    ideogram = args.ideogram
    split_length = args.split_len
    gff3 = args.gff
    thread = args.threads

    split_chromosome_into_bin(ideogram, split_length, chromosome_bin)
    split_file(gff3)

    pool = multiprocessing.Pool(thread)
    tmp_files = os.listdir("./tmp")
    for tmp_file in tmp_files:
        pool.apply_async(read_gff3, args=(os.path.join('./tmp/', tmp_file), chromosome_bin))
    #pool.apply_async(read_gff3, args=(os.path.join('./tmp/tmp1'), chromosome_bin, lock))
    pool.close()
    pool.join()

    for key, value in chromosome_bin.items():
        if value != 0:
            print(key, "\t", value)
    

if __name__ == "__main__":
    main()



            

