#! /usr/bin/env python3

import argparse
import os
import make_config_file as mcf
import make_file_dir as mfd
import toPhylip as tp
from Bio import Phylo
import subprocess
import multiprocessing
import shutil

def make_parse():
    parse = argparse.ArgumentParser()
    parse.add_argument("-i", "--msa", type=str, help="msa file directory")
    parse.add_argument("-t", "--tree", help="tree file")
    parse.add_argument("-o", "--output", default=os.getcwd(),
                       type=str, help="output dir")
    parse.add_argument("-f", "--formate", default="fasta",
                       help="formate of msa")
    parse.add_argument(
        "-sm", "--site", default="M0:M1a:M2a:M3:M7:M8:M8a", help="sites model")
    parse.add_argument("-bm", "--branch",
                       default="Mbm:Mbm0", help="branch model")
    parse.add_argument("-bsm", "--branch_site",
                       default="Ma:Man", help="branch-sites model")
    parse.add_argument("--threads", type=int, default=40, help="The threads")
    parse.add_argument("--noisy", type=str, default="9", help="noisy")
    parse.add_argument("--verbose", type=str, default="0", help="verbose")
    parse.add_argument("--getSE", type=str, default="0", help="getSE")
    parse.add_argument("--RateAncestor", type=str,
                       default="0", help="RateAncestor")
    parse.add_argument("--runmode", type=str, default="0", help="runmode")
    parse.add_argument("--fix_blength", type=str,
                       default="0", help="fix_blength")
    parse.add_argument("--seqtype", type=str, default="1", help="seqtype")
    parse.add_argument("--CodonFreq", type=str, default="2", help="CodonFreq")
    parse.add_argument("--cleandata", type=str, default="1", help="cleandata")
    parse.add_argument("--ndata", type=str, default="1", help="ndata")
    parse.add_argument("--clock", type=str, default="0", help="clock")
    parse.add_argument("--Mgene", type=str, default="0", help="Mgene")
    parse.add_argument("--icode", type=str, default="0", help="icode")
    parse.add_argument("--Small_Diff", type=str,
                       default=".45e-6", help="Small_Diff")
    parse.add_argument("--model", type=str, default="0", help="model")
    parse.add_argument("--aaRatefile", type=str,
                       default="", help="aaRatefile")
    parse.add_argument("--aaDist", type=str, default="0", help="aaDist")
    parse.add_argument("--NSsites", type=str, default="0", help="NSsites")
    parse.add_argument("--fix_alpha", type = str, default = "1", help = "fix_alpha")
    parse.add_argument("--alpha", type=str, default="0", help="alpha")
    parse.add_argument("--Malpha", type=str, default="0", help="Malpha")
    parse.add_argument("--ncatG", type=str, default="3", help="ncatG")
    parse.add_argument("--fix_kappa", type=str, default="0", help="fix_kappa")
    parse.add_argument("--kappa", type=str, default="2", help="kappa")
    parse.add_argument("--fix_omega", type=str, default="0", help="fix_omega")
    parse.add_argument("--omega", type=str, default="2", help="omega")
    parse.add_argument("--method", type=str, default="0", help="method")
    parse.add_argument("--parallel", type = str, default = os.path.join(os.getcwd(), "parallel.jobs"), help = "GNU parallel jobs file")
    args = parse.parse_args()
    return args

def operation(output, models, msa, formate, args, tree, label_tree):
    directory = mfd.make_file_dir(output, models, msa)
    directory.make_dir()
    dir_first_path = directory.get_first_dir()
    Phylip = tp.toPhylip(os.path.join(args.msa, msa), formate, dir_first_path)
    Phylip.writePhylip()
    phy_path = Phylip.phy_path()

    dir_second_path = directory.get_second_dir()
    for directory in dir_second_path:
        config_value = {
            "noisy": args.noisy,
            "verbose": args.verbose,
            "getSE": args.getSE,
            "RateAncestor": args.RateAncestor,
            "runmode": args.runmode,
            "fix_blength": args.fix_blength,
            "seqtype": args.seqtype,
            "CodonFreq": args.CodonFreq,
            "cleandata": args.cleandata,
            "ndata": args.ndata,
            "clock": args.clock,
            "Mgene": args.Mgene,
            "icode": args.icode,
            "Small_Diff": args.Small_Diff,
            "model": args.getSE,
            "aaRatefile": args.aaRatefile,
            "aaDist": args.aaDist,
            "NSsites": args.NSsites,
            "fix_alpha": args.fix_alpha,
            "alpha": args.alpha,
            "Malpha": args.Malpha,
            "ncatG": args.ncatG,
            "fix_kappa": args.fix_kappa,
            "kappa": args.kappa,
            "fix_omega": args.fix_omega,
            "omega": args.omega,
            "method": args.method
        }
        if os.path.split(directory)[-1] == "M0":
            config_file = mcf.make_config_file(
                phy_path, tree, directory, config_value)
            config_file.write_config()
        elif os.path.split(directory)[-1] == "M1a":
            config_value["NSsites"] = "1"
            config_file = mcf.make_config_file(
                phy_path, tree, directory, config_value)
            config_file.write_config()
        elif os.path.split(directory)[-1] == "M2a":
            config_value["NSsites"] = "3"
            config_file = mcf.make_config_file(
                phy_path, tree, directory, config_value)
            config_file.write_config()
        elif os.path.split(directory)[-1] == "M3":
            config_value["NSsites"] = "3"
            config_file = mcf.make_config_file(
                phy_path, tree, directory, config_value)
            config_file.write_config()
        elif os.path.split(directory)[-1] == "M7":
            config_value["NSsites"] = "7"
            config_file = mcf.make_config_file(
                phy_path, tree, directory, config_value)
            config_file.write_config()
        elif os.path.split(directory)[-1] == "M8":
            config_value["NSsites"] = "8"
            config_file = mcf.make_config_file(
            phy_path, tree, directory, config_value)
            config_file.write_config()
        elif os.path.split(directory)[-1] == "M8a":
            config_value["NSsites"] = "8"
            config_value["fix_omega"] = "1"
            config_value["omega"] = "1"
            config_file = mcf.make_config_file(
                phy_path, tree, directory, config_value)
            config_file.write_config()
        elif os.path.split(directory)[-1] == "Ma":
            config_value["model"] = "2"
            config_value["NSsites"] = "2"
            config_file = mcf.make_config_file(
                phy_path, label_tree, directory, config_value)
            config_file.write_config()
        elif os.path.split(directory)[-1] == "Man":
            config_value["model"] = "2"
            config_value["NSsites"] = "2"
            config_value["fix_omega"] = "1"
            config_value["omega"] = "1"
            config_file = mcf.make_config_file(
                phy_path, label_tree, directory, config_value)
            config_file.write_config()
        elif os.path.split(directory)[-1] == "Mbm":
            config_value["model"] = "2"
            config_file = mcf.make_config_file(
                phy_path, label_tree, directory, config_value)
            config_file.write_config()
        elif os.path.split(directory)[-1] == "Mbm0":
            config_file = mcf.make_config_file(
                phy_path, label_tree, directory, config_value)
            config_file.write_config()
        

def run_codeml(directory):
    os.chdir(directory)
    subprocess.run("codeml codeml.ctl", shell=True, stdout=subprocess.PIPE)
    print("CODEML %s in %s FINISH" % (os.path.split(directory)[-1], directory))

def write_parallel(all_codeml_dir, args):
    parallel = open(args.parallel, "w")
    for msa in all_codeml_dir:
        command = "cd "+ msa + ";"+"codeml codeml.ctl"
        parallel.write(command)
        parallel.write("\n")
    parallel.close()


def main():
    args = make_parse()
    
    output = os.path.abspath(args.output)
    if len(os.listdir(output)) != 0:
        print("The output directory is not  empty.")
        choice = input("Do you want to clear EXISTING RESULTS [Y]es/[N]o:")
        if choice == "Y":
            for dir in os.listdir(output):
                shutil.rmtree(os.path.join(output, dir))
        elif choice == "N":
                exit(0)
        else:
            exit(0)
        
    models = ":".join([args.site, args.branch, args.branch_site]).strip(":")
    msa_file = [msa for msa in os.listdir(
        args.msa) if ".fa" == os.path.splitext(msa)[-1]]
    formate = args.formate
    
    tree = args.tree
    read_tree = Phylo.read(tree, "newick")
    Phylo.draw_ascii(read_tree)
    
    label_tree = os.path.join(os.path.split(tree)[0], "labeled.tree")
    label_file = open(label_tree, "w")
    label = input("Label:")
    with open(tree, "r") as file:
        for line in file:
            if label in line:
                label_file.write(line.replace(label, label + " #1"))
            else:
                print("Please input correct label")
                exit(0)
    label_file.close()
    
    all_codeml_dir = []
    
    pool = multiprocessing.Pool(args.threads)
    for msa in msa_file:
        pool.apply_async(operation, args=(
            output, models, msa, formate, args, tree, label_tree))
    pool.close()
    pool.join()

#    for msa in msa_file:
#        operation(output, models, msa, formate, args, tree, label_tree)

    for first_dir in os.listdir(output):
        for second_dir in os.listdir(os.path.join(output, first_dir)):
            codeml_dir = os.path.join(output, first_dir, second_dir)
            if os.path.isdir(codeml_dir):
                all_codeml_dir.append(codeml_dir)

#    print(all_codeml_dir)
    write_parallel(all_codeml_dir, args)

#    pool = multiprocessing.Pool(args.threads)
#    pool.map_async(run_codeml, all_codeml_dir)
#    pool.close()
#    pool.join()


if __name__ == "__main__":
    main()
