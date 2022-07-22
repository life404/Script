#! /bin/bash

while getopts ":t:q:o:d:n:h" opt_name
do
    case "$opt_name" in
    't')
        target="$OPTARG"
        ;;
    'q')
        query="$OPTARG"
        ;;
	'd')
		dir="$OPTARG"
		;;
	'o')
		out="$OPTARG"
		;;
	'n')
		threads="$OPTARG"
		;;
	'h')
		echo "$0 -d /prepare1/dir -t target 2bit -q query 2bit -o axtChain/output"
		exit 2
		;;
    '?')
        echo "unknown arguments."
        exit 2
        ;;

    esac
done

echo ${out} ${dir}


if [ -d ${out} ];then
	rm -rf ${out}
fi

mkdir ${out}

echo "staring parallel translate axt to chain"

for axt in ${dir}/*.axt
do
	file=$(basename ${axt})
	echo "~/TOOLS/UCSCtools/axtChain ${axt} ${target} ${query} ${out}/${file%.*}.chain -linearGap=loose"
done > axtChain.jobs

cat axtChain.jobs|parallel -j ${threads} --bar --joblog parallel.axtChain.log

for chain in ${out}/*.chain
do
	echo $chain >> input.tmp
done

echo "staring merge all chain files"

~/TOOLS/UCSCtools/chainMergeSort -inputList=input.tmp > merge.chain 

rm -rf input.tmp

echo "staring RepeatFiller"
time RepeatFiller.py -c merge.chain -T2 ${target} -Q2 ${query} -o filled.chain

echo "Staring clean chain"


twoBitInfo ${target} stdout|sort -k2rn > ${target/2bit/size}
twoBitInfo ${query}  stdout|sort -k2rn > ${query/2bit/size}

~/TOOLS/UCSCtools/chainCleaner filled.chain ${target} ${query} clean.chain removedSuspects.bed -tSizes=${target/2bit/size} -qSizes=${query/2bit/size} -doPairs -minBrokenChainScore=75000 -linearGap=loose
echo "All jobs finish"
