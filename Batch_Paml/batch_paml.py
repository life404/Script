#! /usr/bin/env python3

import os
import subprocess
import argparse
import time
import shutil

def make_parse():
    parse = argparse.ArgumentParser()
    parse.add_argument("--input", "-i", help = "input dirtory contained phylip file (end with .phy or .phylip), or  single phylip file")
    parse.add_argument("--output", "-o", help = "output dirtory")
    parse.add_argument("--config", "-c", help = "path of config file")
    parse.add_argument("--tree", "-t", help = "tree file, wheather root or unroot dempends on the parameter in config file")
#    parse.add_argument("--process", "-p", default=4, help = "threads")
    args = parse.parse_args()
    return args

def run_processes(cmd_dicts, nproc=4, wait=5):
    proc_pool = []
    for idx, cmd_dict in enumerate(cmd_dicts):
        print(f'[Proc {idx}]', cmd_dict['args'])
        proc_pool.append(subprocess.Popen(**cmd_dict))
        while sum([x.poll() != 0 for x in proc_pool]) >= nproc:
            time.sleep(wait)
    while sum([x.poll() != 0 for x in proc_pool]) > 0:
        time.sleep(wait)


def main():
    args = make_parse()
    in_dir = args.input
    out_dir = args.output
    tree_file = args.tree
#    threads = int(args.process)
    config = args.config
    
    codeml_str = open(os.path.abspath(config), "r").read()

    if os.path.isdir(in_dir):
        fasta_list = sorted([
            x for x in os.listdir(in_dir)
            if x.endswith('.phy') or x.endswith('.phylip')
        ])
        cmd_dicts = []
        for fasta_file in fasta_list:
            pref = '.'.join(fasta_file.split('.')[:-1])
            gene_out_dir = f'{out_dir}/{pref}'
            if os.path.exists(gene_out_dir):
                shutil.rmtree(gene_out_dir)
#                subprocess.call(['rm -rf', gene_out_dir])
                subprocess.call(['mkdir', gene_out_dir])
            else:
                subprocess.call(['mkdir', gene_out_dir])
            gene_codeml_str = codeml_str.replace('SEQZ', os.path.abspath(f'{in_dir}/{fasta_file}'))
            gene_codeml_str = gene_codeml_str.replace('TREEZ', os.path.abspath(tree_file))
            with open(f'{gene_out_dir}/codeml.ctl', 'w') as f:
                print(gene_codeml_str, file=f)
#            cmd_dicts.append({
#                'args': ['codeml',],
#                'cwd': os.path.abspath(gene_out_dir),
#                # 'stdout': open(f'{gene_out_dir}/log', 'w')
#            })
#        run_processes(cmd_dicts, nproc=threads, wait=3)
            print("cd %s;%s" %(os.path.abspath(gene_out_dir), "codeml"))
    elif os.path.isfile(in_dir):
        cmd_dicts = []
        pref = '.'.join(in_dir.split('.')[:-1])
        gene_out_dir = f'{out_dir}/{pref}'
        if os.path.exists(gene_out_dir):
            shutil.rmtree(gene_out_dir)
#            subprocess.call(['rm -rf', gene_out_dir])
            subprocess.call(['mkdir', gene_out_dir])
        else:
            subprocess.call(['mkdir', gene_out_dir])
        gene_codeml_str = codeml_str.replace('SEQZ', os.path.abspath(f'{in_dir}'))
        gene_codeml_str = gene_codeml_str.replace('TREEZ', os.path.abspath(tree_file))
        with open(f'{gene_out_dir}/codeml.ctl', 'w') as f:
            print(gene_codeml_str, file=f)

        print("cd %s;%s" %(os.path.abspath(gene_out_dir), "codeml"))
#        cmd_dicts.append({
#            'args': ['codeml',],
#            'cwd': os.path.abspath(gene_out_dir),
#            # 'stdout': open(f'{gene_out_dir}/log', 'w')
#        })
#        run_processes(cmd_dicts, nproc=1, wait=0)

    else:
        print("input a fasta file or directory contain fasta files")


if __name__ == "__main__":
    main()
