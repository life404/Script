#! /bin/bash

fasta=$1
mat=$2
db=$3
prefix=${mat##*/}

/disk/tools/seqkit split -i -f --quiet -O ./${prefix%%.*}.tmp.split $fasta


mkdir ${prefix%%.*}

for i in ${prefix%%.*}.tmp.split/*
do
	echo "lastal -m50 -E0.05 -C2 -p $mat $3 $i|last-split -m1 > ${prefix%%.*}/${i##*/}-1.maf"
done > ${prefix%%.*}.parallel.jobs


cat ${prefix%%.*}.parallel.jobs|parallel --joblog ${prefix%%.*}.parallel.log -j 70 --bar


