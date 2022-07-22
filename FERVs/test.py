from Bio import SeqIO
import sys

id_list = []
with open (sys.argv[1], "r") as file:
    for line in file:
        array = line.strip().split(" ")
        id_list.append(array[0])
        
records = SeqIO.parse(sys.argv[2], "fasta")
record_list = []
for record in records:
    if record.id in id_list:
        record_list.append(record)
        
SeqIO.write(record_list, sys.argv[3], "fasta")

        
        