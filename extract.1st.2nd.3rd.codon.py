#! /usr/bin/env python3

import argparse

parse = argparse.ArgumentParser()
parse.add_argument("-i", "--input", help = "input file")
parse.add_argument("-l", "--location", choices=["1st", "2nd", "3rd", "1st+2nd"], help = "location")
args = parse.parse_args()

with open (args.input, "r") as file:
    for line in file:
        line = line.strip()
        if ">" in line:
            print(line)
        else:
            if args.location == "1st":
                print(line[0:len(line):3])
            elif args.location == "2nd":
                print(line[1:len(line):3])
            elif args.location == "3rd":
                print(line[2:len(line):3])
            elif args.location == "1st+2nd":
                first = line[0:len(line):3]
                second = line[1:len(line):3]
                print("".join([a+b for a, b in zip(first, second)]))
            else:
                print("wrong location")
                exit



