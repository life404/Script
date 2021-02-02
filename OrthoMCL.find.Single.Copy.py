#! /usr/bin/env python3

import argparse

def mcl_parse(mcl_groups):
    group_count = {}
    with open (mcl_groups) as file:
        for line in file:
            line = line.strip()
            group_id = line.split(":")[0].strip()
            group_terms = line.split(":")[1].strip()
            #print(group_terms.split(" "))
            group_count[group_id] = [i.split("|")[0] for i in group_terms.split(" ")]
    return group_count

def stdout(group_count):
    colnames = []
    for value in group_count.values():
        colnames+=value
    colnames = set(colnames)
    print("groups" + "\t" + "\t".join(colnames))

    for key, value in group_count.items():
        print("%s" %key, end = "")
        for i in colnames:
            print(" %s" %(value.count(i)), end = "")
        print("\n")

def stdout_single(group_count):
    colnames = []
    for value in group_count.values():
        colnames+=value
    colnames = set(colnames)
    print("groups" + "\t" + "\t".join(colnames))

    for key, value in group_count.items():
        single_copy = []
        for i in colnames:
            single_copy.append(value.count(i))
        if list(set(single_copy))[0] == 1 and len(set(single_copy)) == 1:
            print("%s " %key, end = "")
            print(" ".join([str(i) for i in single_copy]))

    

            


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("-i", "--input", help = "input file")
    parse.add_argument("-s", "--single", action="store_true", help = "weather or not print single copy groups")
    args = parse.parse_args()
    
    single = args.single
    mcl_groups = args.input
    group_count = mcl_parse(mcl_groups)

    if single:
        stdout_single(group_count)
    else:
        stdout(group_count)

if __name__ == "__main__":
    main()





