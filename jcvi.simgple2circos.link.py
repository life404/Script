#! /usr/bin/env python3

import argparse

def make_args():
    parse = argparse.ArgumentParser()
    parse.add_argument("-i", "--input", type = str, help = "simple file")
    parse.add_argument("-b", "--bed", type = str, help = "bed file")
    parse.add_argument("-t", "--type", type = str, default = "intra", choices=["intra", "extra"], help = "type, intra or extra ")
    args = parse.parse_args()
    return args

def intra(simple, bed):
    query_dict = {line.split("\t")[3]:line.split("\t")[0:3] for line in open (bed)}

    with open (simple, "r") as file:
        for line in file:
            line = line.strip()
            array = line.split("\t")
            source_chro = query_dict[array[0]][0]
            source_start = query_dict[array[0]][1]
            source_end = query_dict[array[1]][2]
            target_chro = query_dict[array[2]][0]
            target_start = query_dict[array[2]][1]
            target_end = query_dict[array[3]][2]
            print("%s\t%s\t%s\t%s\t%s\t%s" %(source_chro, source_start, source_end, target_chro,
                target_start, target_end))

def main():
    args = make_args()
    simple = args.input
    bed = args.bed
    t = args.type

    if t == "intra":
        intra(simple, bed)

    else:
        print("right type")

if __name__ == "__main__":
    main()







    
