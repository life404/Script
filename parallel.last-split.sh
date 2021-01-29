#! /bin/bash

dir_list=$1

for i in `cat $1`
do
	echo "$i/*.maf"
done > parallel.last-split.jobs

cat parallel.last-split.sh | parallel --log parallel.last-split.log  



