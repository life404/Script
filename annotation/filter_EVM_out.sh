#! /bin/bash

for contig_path in $(cut -f 2 $1|sort|uniq)
do
	grep -n "^# EVM prediction:" ${contig_path}/evm.out|cut -f 1 -d":" > _tmp.start
	grep -n "^$" ${contig_path}/evm.out|cut -f 1 -d":" > _tmp.end
	paste -d "," _tmp.start _tmp.end > _tmp.location
	
	for block in $(cat _tmp.location)
	do
		sed -n "${block}p" ${contig_path}/evm.out | \
		awk '{content[NR]=$0; if($0!~/#/) evidence=evidence";"$NF}END{match(evidence,"PASA",a);match(evidence,"Stringtie",b);match(evidence,"gth",c);if(length(a)!=0||length(b)!=0||length(c)!=0){for(i in content) print content[i]}}'
	done > ${contig_path}/evm.valid.out
done

rm -rf _tmp.*
