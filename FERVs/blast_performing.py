#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import subprocess
from pathlib import Path
import logging
from Bio import SeqIO
from Bio.Seq import Seq
import shutil

LOGGER = logging.getLogger(Path(__file__).stem)

class ERVs:
    'find ERVs from target genome'
    
    def __init__(self,target, query, output):
        self.target = target
        self.query  = query
        self.output = output
        
    def mkoutput(self):
        OP_DIR = Path.cwd().joinpath(self.output)
        Path.mkdir(OP_DIR, exist_ok=True)
        return OP_DIR
    
    def makeblastdb(self, target, index_dir, type, echo):
        ID_DIR = index_dir
        Path.mkdir(ID_DIR, exist_ok=True)
        INDEX_NAME = "{index}.index".format(index = Path(target).stem)
        abs_INDEX_NAME = ID_DIR.joinpath(INDEX_NAME)
        """
        Determine if an index file exists
        """
        IDF_list = list(Path(ID_DIR).glob("{IDN}*".format(IDN = INDEX_NAME)))
        if len(IDF_list) == 0:
            MAKE_BLASTDB_CMD = "makeblastdb -dbtype {type} -in {target} -out {abs_INDEX_NAME}"
            cmd = MAKE_BLASTDB_CMD.format(target = Path(target).resolve(),
                                          abs_INDEX_NAME = abs_INDEX_NAME,
                                          type = type)
            results=subprocess.run(cmd, check = True, shell = True, capture_output= True)
            LOGGER.debug(results)
        else:
            if echo != 0:
                print("the index of {target} have been made".format(target=Path(target).stem))
        return abs_INDEX_NAME

#    def merge_blast()
    
    def parse_fb_results(self,FB_RESULTS, flength):
        """
        Filter the results of first blast, and rename the filtered sequence.
        The first_blast_filted.fa is the renamed sequence;
        The first_blast_filted.cor is the corresponding relationship between raw and filtered sequence
        """
        FB_RESULTS_seq_n = Path(FB_RESULTS).resolve().parent.joinpath("first_blast_filted.seq")
        FB_RESULTS_cor_n = Path(FB_RESULTS).resolve().parent.joinpath("first_blast_filted.cor")
        
        FB_RESULTS_seq = open(FB_RESULTS_seq_n, "w")
        FB_RESULTS_cor = open(FB_RESULTS_cor_n, "w")
        
        blast_records = open(FB_RESULTS, "r")
        num = 0
        for blast_record in blast_records:
            hsp = blast_record.strip().split("\t")
            if int(hsp[6]) >= int(flength):
                num += 1
                FB_RESULTS_seq.write(">{seqid}-{num}\n".format(seqid = hsp[1], num = num))
                FB_RESULTS_seq.write("{seq}\n".format(seq=hsp[8]))
                FB_RESULTS_cor.write("{sseqid}-{num}\t{qseqid}\t{sseqid}\t{slen}\t{sstart}\t{send}\n".format(sseqid=hsp[1],
                                                                                                            qseqid=hsp[0],
                                                                                                            slen=hsp[2],
                                                                                                            sstart=hsp[3],
                                                                                                            send=hsp[4],
                                                                                                            num=num))
        blast_records.close()
        FB_RESULTS_seq.close()
        FB_RESULTS_cor.close()
        return FB_RESULTS_seq_n, FB_RESULTS_cor_n
    
    def first_blast(self, threads,fevalue, flength):
        OP_DIR = self.mkoutput()
        index_dir = OP_DIR.joinpath("INDEX")
        abs_INDEX_NAME = self.makeblastdb(self.target, index_dir, "nucl", 1)
        FB_RESULTS = OP_DIR.joinpath("first_blast.tbl")
        TBLASTN_CMD = "tblastn -query {query} -db {db} -out {output} -outfmt \"6 qseqid sseqid slen sstart send evalue length qseq sseq sframe sstrand\" -num_threads {threads} -evalue {evalue}"
        cmd = TBLASTN_CMD.format(query = self.query,
                                 db = abs_INDEX_NAME,
                                 output = FB_RESULTS,
                                 threads = threads,
                                 evalue = fevalue)
        results = subprocess.run(cmd, capture_output = True, check= True, shell= True)
        LOGGER.debug(results)
        #print(cmd)
        
        FB_RESULTS_seq, FB_RESULTS_name = self.parse_fb_results(FB_RESULTS, flength)
        
        return FB_RESULTS_seq, FB_RESULTS_name
    
    def rbh_blast(self,query, db, output):
        BLASTP_CMD = "blastp -query {query} -db {db} -out {output} -outfmt  \"6 qseqid sseqid slen sstart send evalue length bitscore\""
        cmd = BLASTP_CMD.format(query = query,
                                db = db,
                                output = output)
        results = subprocess.run(cmd, capture_output=True, check=True, shell=True)
        LOGGER.debug(results)
        max = 0
        best1 = ""
        with open (output, "r") as file:
            for line in file:
               hsp = line.strip().split("\t")
               if  float(hsp[-1]) >= max:
                 best1 = hsp[1]
                 max = float(hsp[-1])
        return best1 
            
    def rbh(self, FB_RESULTS_seq, first_blast_cor, final_results):
        OP_DIR = self.mkoutput()
        RBH_DIR = OP_DIR.joinpath("RBH")
        shutil.rmtree(RBH_DIR, ignore_errors=True)
        Path.mkdir(RBH_DIR)
        TMP_DIR = RBH_DIR.joinpath("TMP")
        Path.mkdir(TMP_DIR)
        index_dir = RBH_DIR.joinpath("INDEX")
        virus_INDEX_NAME = self.makeblastdb(self.query, index_dir, "prot", 0)
        rbh_results = open (OP_DIR.joinpath(final_results), "w")
        cor_list = {}
        with open (first_blast_cor, "r") as file:
            for line in file:
                array = line.strip().split("\t")
                cor_list[array[0]] = array[1]

        fasta_records = SeqIO.parse(FB_RESULTS_seq, "fasta")
        for record in fasta_records:
            tmp_file = TMP_DIR.joinpath("{id}.faa".format(id = record.id))
            out_file1 = TMP_DIR.joinpath("{id}.virus.rbh1".format(id = record.id))
            record.seq = Seq(str(record.seq).replace("-",""))
            SeqIO.write(record, tmp_file, "fasta")
            best1 = self.rbh_blast(tmp_file, virus_INDEX_NAME, out_file1)
            
            print("rbh1:{best1}\trbh2:{best2}\n".format(best1=best1, best2 = cor_list[record.id]))
            if record.id in cor_list.keys():
                if best1 == cor_list[record.id]:
                    rbh_results.write("{results}\n".format(results = record.id))
        rbh_results.close()
            
        
        