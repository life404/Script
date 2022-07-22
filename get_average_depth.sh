#! /bin/bash


BAM=$1

SAMTOOLS="/home/panda2bat/TOOLS/samtools-0.1.19/samtools"


#for i in Hic_asm_{0..30}
for i in $(grep "CM" ~/DATABASE/Chiroptera/Rhinolophus/R.sinicus/genome/R.sinicus.genome.fa.fai|awk '{print $1}')
do 
	echo "$SAMTOOLS depth -r $i $BAM|awk '{sum += \$3}END{print sum/NR}' >> depth.tmp"
done | parallel -j 31

awk '{sum += $0}END{print "'$BAM'", sum/NR}' depth.tmp

rm -rf depth.tmp
