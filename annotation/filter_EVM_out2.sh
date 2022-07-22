#! /bin/bash

for contig_path in $(cut -f 2 $1|sort|uniq)
do
	grep -n "^# EVM prediction:" ${contig_path}/evm.out|cut -f 1 -d":" > _tmp.start
	grep -n "^$" ${contig_path}/evm.out|cut -f 1 -d":" > _tmp.end
	paste -d "," _tmp.start _tmp.end > _tmp.location
	
	for block in $(cat _tmp.location)
	do
		sed -n "${block}p" ${contig_path}/evm.out | \
		awk -F"\t" '{content[NR]=$0;if($0!~/#/){split($NF,a,"},{"); for(i in a){split(a[i],b,";");sub("}","",b[2]);evidence[b[2]]++}}}END{if(length(evidence) >= 2){for(i in content) print content[i]}}'	
	done > ${contig_path}/evm.valid.out
done

rm -rf _tmp.*
