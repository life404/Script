#! /usr/bin/env python3

import argparse
import os
import subprocess
import multiprocessing
import re
import time


def make_args():
    parse = argparse.ArgumentParser()
    parse.add_argument("-f", "--file", help="codeml result Dir")
    parse.add_argument("-p", "--pattern", default="OG",
                       help="the partern was be used to find the directory")
    parse.add_argument("-c", "--compare", default="Ma:Man",
                       help="the comparation between two group")
    parse.add_argument("-t", "--threads", type = int, default=40, help="the threads")
    parse.add_argument("--df", help="the df")
    args = parse.parse_args()

    return args


def chi2_calculate(directory, compare, df):
    lnL = 0
    for model in compare.split(":")[::-1]:
        path = os.path.join(directory, model, "mlc")
        command = " ".join(["grep", "-w", "\"lnL\"", path])
        result = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, encoding="utf-8").stdout
        #lnL = float(re.search(r'\):[ -0-9]+.[0-9]+',result)[0].split(" ")[-1]) - lnL
        lnL = float(result.split("):")[-1].strip().split(" ")[0])-lnL
    command = " ".join(["chi2", str(df), str(abs(lnL)*2)])
    significance = subprocess.run(command, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8").stdout
    print(significance.strip() + "\t" + os.path.split(directory)[-1])
    

def main():
    args = make_args()
    input = os.path.abspath(args.file)
    pattern = args.pattern
    compare = args.compare
    threads = args.threads
    df = args.df
    
    codeml_dir = []
    for dir in os.listdir(input):
        if pattern in dir:
            codeml_dir.append(os.path.join(input, dir))
    
    pool = multiprocessing.Pool(threads)
    for directory in codeml_dir:
        time.sleep(0.1)
        pool.apply_async(chi2_calculate, args=(directory, compare, df))
    pool.close()
    pool.join()
    
if __name__ == "__main__":
    main()
    
    
    
        
    
    
    
