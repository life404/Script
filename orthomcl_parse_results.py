#! /usr/bin/env python3
from Bio import SeqIO
import pandas as pd
from pathlib import Path
import argparse

class orthomcl():
    def __init__(self, mclgroups, outdir):
        self.mclgroups = mclgroups
        self.outdir = outdir
    
    def mclcount(self):
        data = pd.read_csv(self.mclgroups, sep = " ", header=None, index_col=0, encoding='utf8', low_memory=False)
        count = data
        count = count.apply(lambda x: x.str.split("|").str.get(0))
        count = count.apply(lambda x: x.value_counts(), axis = 1)
        count = count.fillna(0).astype('int')
        count.to_csv(Path(self.outdir).joinpath('mclCount.csv'), sep='\t', index=True)
        
        single = count
        for i in single.columns:
            single = single[single[i]==1]
        single.to_csv(Path(self.outdir).joinpath('mclSingle.csv'), sep='\t', index=True)
        
        return data
    
    def sequences(self, records, data):
        seq_dir = Path(self.outdir).joinpath('Orthogroup_Sequences')
        Path.mkdir(seq_dir,exist_ok=True)
        
        records_list = {}
        for record in records:
            records_list[record.id] = record
        group = data
        group = group.apply(lambda x: x.str.split('|').str.get(1))
        
        
        for group in group.index:
            seqs = [records_list[i] for i in list(data.loc[group,:].astype('str')) if i!='nan']
            SeqIO.write(seqs, Path(seq_dir).joinpath('{group}.fa'.format(group=str(group).replace(":",""))), 'fasta')
        
    
def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('-i','--input', help='the groups file from orthomcl-pipeline in groups directory')
    parse.add_argument('-f','--fasta', help='the all fasta sequences used in analysis, you can use \'cat\' to merge all fasta files in \'compliant_fasta\' directory')
    parse.add_argument('-o','--output', help='the output directory')
    args = parse.parse_args()
    
    outdir = args.output
    
    if Path(outdir).exists():
        pass
    else:
        Path.mkdir(Path(outdir).resolve())
    
    ortho = orthomcl(args.input, outdir)
    data = ortho.mclcount()
    
    records = SeqIO.parse(args.fasta, 'fasta')
    ortho.sequences(records, data)
    
if __name__ == "__main__":
    main()
    