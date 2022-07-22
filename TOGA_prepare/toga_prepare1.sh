#! /bin/bash

while getopts ":t:q:n:o:h" opt_name
do
    case "$opt_name" in
    't')
        target="$OPTARG"
        ;;
    'q')
        query="$OPTARG"
        ;;
    'n')
		num="$OPTARG"
		;;
	'o')
		output="$OPTARG"
		;;
	'h')
		echo "$0 -t target.2bit -q query.2bit -n threads"
		exit 2
		;;
    '?')
        echo "unknown arguments."
        exit 2
        ;;

    esac
done

shift $((OPTIND-1))

if [ ! -d lastz_out ];then
    mkdir lastz_out
else
    rm -rf lastz_out
    mkdir lastz_out
fi

if [ ! -d log ];then
    mkdir log
else
    rm -rf log
    mkdir log
fi

if [ ! -d tParts ];then
    mkdir tParts
else
    rm -rf tParts
    mkdir tParts
fi

if [ ! -d qParts ];then
    mkdir qParts
else
    rm -rf qParts
    mkdir qParts
fi

echo "************split fasta file and transforme fasta to 2bit*****************"
faSplit byname <(twoBitToFa ${target} stdout) tParts/
faSplit about <(twoBitToFa ${query}  stdout) 20000000 qParts/

L1=$(ls tParts/*.fa|wc -l)
L2=$(ls qParts/*.fa|wc -l)

L=$(echo $L1 $L2|awk '{print $1*$2}')
echo "cluster batch jobList size: $L = $L1 * $L2"

for tPart in tParts/*.fa
do
    echo "faToTwoBit ${tPart} ${tPart/fa/2bit}"
done|parallel -j 200 --joblog $PWD/log/${target}.fa2bit.log

for qPart in qParts/*.fa
do
    echo "faToTwoBit ${qPart} ${qPart/fa/2bit}"
done|parallel -j 200 --joblog $PWD/log/${query}.fa2bit.log

rm -rf tParts/*.fa
rm -rf qParts/*.fa



echo "*****************************Generage lastz jobs**************************"
for tPart in tParts/*.2bit
do
    num=$(echo "$num 1"|awk '{printf("%03d",$1+$2)}')
    for qPart in qParts/*.2bit
    do 
        pre1=$(basename $tPart)
        pre2=$(basename $qPart)
        echo "lastz ${output}/${tPart} ${output}/${qPart} K=2400 H=2000 Y=9400 L=3000 --format=axt > ${output}/lastz_out/${pre1%.*}-${pre2%.*}.axt"
    done
done > $PWD/log/lastz.jobs

echo "****************************Staring parallel lastz*************************"
#for job in $PWD/log/*.job
#do 
#    echo "parallel run the joblist ${job}"
#	pre=$(basename job)
#    cat ${job}|parallel -j ${num} --bar --joblog $PWD/log/${pre%.*}.log
#done
#cat $PWD/log/lastz.jobs|parallel -j ${num} --bar --joblog $PWD/log/lastz.log
