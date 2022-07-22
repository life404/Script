#!  /usr/bin/env python3

import argparse
from blast_performing import ERVs

def make_parse():
    parse = argparse.ArgumentParser()
    parse.add_argument("-t", "--host", dest="target", help = "host genome")
    parse.add_argument("-v", "--virus", dest = "query", help = "virus protein")
    parse.add_argument("-o", "--output", dest="output", help = "output dir")
    parse.add_argument("--threads", dest="threads", help = "threads", default=12)
    parse.add_argument("--fevalue", dest="fevalue", default=0.009, help="evalue")
    parse.add_argument("--flength", dest="flength", default=200, help = "length")
    parse.add_argument("--name", dest = "name", help = "the name of final output")
    args = parse.parse_args()
    return args


def main():
    args = make_parse()
    target = args.target 
    query = args.query
    output = args.output 
    threads = args.threads 
    fevalue = args.fevalue 
    flength = args.flength
    final_results = args.name
    
    ervs = ERVs(target, query, output)
    first_blast_seq,first_blast_cor = ervs.first_blast(threads, fevalue, flength)
#    ervs.rbh(first_blast_seq, first_blast_cor, final_results)
    
if __name__ == "__main__":
    main()