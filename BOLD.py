#! /usr/bin/env python3

import requests
import argparse
from Bio import SeqIO
import xml.etree.cElementTree as ET
import os
import time

requests.adapters.DEFAULT_RETRIES = 10


def make_parse():
    parse = argparse.ArgumentParser()
    parse.add_argument("-i", "--input", help = "输入fasta格式序列文件")
    parse.add_argument("-d", "--database",choices=['COX1','COX1_SPECIES','COX1_SPECIES_PUBLIC','COX1_L640bp'],help = "指定查询数据库，可选'COX1','COX_SPECIES','COX1_SPECIES_PUBLIC','COX1_L640bp'")
    parse.add_argument("-o", "--output", help = "指定输出文件")
    args = parse.parse_args()
    return args

def read_fasta(fasta):
    query = {}
    for seq_record in SeqIO.parse(fasta, "fasta"):
        query[seq_record.id] = seq_record.seq
    
    return query

def url(query, database, output):
    results = open(os.path.join(os.getcwd(), output), "w")
    print("%s\t%s\t%s\t%s\t%s\t%s\t%s" %("query", "match", "sequencedescription", "database",
                                                            "citation", "taxonomicidentification", "similarity"))
    results.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" %("query", "match", "sequencedescription", "database",
                                                            "citation", "taxonomicidentification", "similarity"))
    
    sleep_flag = 0

    for key, value in query.items():
        sleep_flag += 1

        if sleep_flag <= 300:   
            url = requests.get("http://www.boldsystems.org/index.php/Ids_xml", params={"db":database, "sequence":str(value)})
            
            if url.reason == "OK":
    #            print("查询网址 %s" %(url.url))
                tree = ET.fromstring(url.content)
                try:
                    for i in range(0,20):
                        a = []
                        for j in range(0,6):
                            a.append(str(tree[i][j].text))
                        print("%s\t%s" %(key, "\t".join(a)))
                        results.write("%s\t%s\n" %(key, "\t".join(a)))
                        
                except IndexError:
                    print("%s\t查询 %s 失败，未找到相关内容" %(key, key))
                    results.write("%s\t查询 %s 失败，未找到相关内容\n" %(key, key))

            else:
                print("%s\t查询 %s 失败，可能是由于网络原因" %(key, key))
                results.write("%s\t查询 %s 失败，可能是由于网络原因\n" %(key, key))
        else:
            print("sleeping")
            time.sleep(150)
            sleep_flag = 0
    

def main():
    args = make_parse()

    fasta = args.input
    database = args.database
    output = args.output

    query = read_fasta(fasta)
    url(query, database, output)

if __name__ == "__main__":
    main()

        
    
        
