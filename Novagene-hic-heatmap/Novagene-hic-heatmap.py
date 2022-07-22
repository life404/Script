#! /usr/bin/env python3

import argparse

def make_parse():
    parse = argparse.ArgumentParser()
    parse.add_argument("--fai", help = "samtools faidx results of genome fasta")
    parse.add_argument("--metrics", help = "the metrics file export from Juicebox")
    args = parse.parse_args()
    return args

def chrom_break(fai, metrics):
    total = 0
    with open (fai, "r") as file:
        for line in file:
            total = total + int(line.strip().split("\t")[1])
    
    line_num = 0
    with open (metrics) as file:
        for line in file:
            line_num += 1
            if line_num <= 2:
                resolution = int(line.split("\t")[1])
            else:
                break
    print(resolution)

    mapinput = open ("tmp", "w")
    with open (metrics, "r") as file:
        for line in file:
            array = line.strip().split("\t")
            if int(array[0]) != 0 and int(array[0]) != int(array[1]):
                mapinput.write("%d\t%d\t%s\n" %(int(array[0])/resolution, int(array[1])/resolution, array[2]))
                mapinput.write("%d\t%d\t%s\n" %(int(array[1])/resolution, int(array[0])/resolution, array[2]))










def main():
    args = make_parse()
    fai = args.fai
    metrics=args.metrics
    chrom_break(fai, metrics)


if __name__ == "__main__":
    main()
