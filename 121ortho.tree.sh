#! /bin/bash

while getopts ":i:" arg
do
    case $arg in
    i)
        input=$OPTARG
        ;;
    
    ?)
        echo "Usage: $(basename $0) [-i input] [-o output] [-t tmp directory]"
        exit 1
        ;;
    esac
done

cd ${input}

if [ ! -d "./tmp" ]
then
    mkdir "tmp"
else
    \rm -rf "./tmp"
    mkdir "tmp"
fi



echo "#! /bin/bash " >> `pwd`/tmp/mafft.parallel.jobs
for i in *.fa;
do 
    echo -e "mafft `pwd`/$i > `pwd`/tmp/${i}.alignment"
done >> `pwd`/tmp/mafft.parallel.jobs
cd "./tmp"
chmod +x mafft.parallel.jobs

cat mafft.parallel.jobs|parallel -j 40 

for i in *.fa.alignment; do /disk/tools/Gblocks_0.91b/Gblocks/ $i -t=p -b3=8 -b4=10 -b5=n; done
for i in *.alignment-gb; do echo "iqtree -s $i -m MF"; done > partition.model.selection.parallel.jobs
chmod +x partition.model.selection.parallel.jobs
cat partition.model.selection.parallel.jobs|parallel -n 40

cd ../
~/Scripts/121merge.sequence.py --input ./tmp

cd "./tmp"
echo -n -e '\tcharpartition mine = ' >> partitioned_file
for i in \
    `awk 'BEGIN{part_num=""}{if($0~/charset/){part_num = $2}else{if($0~/#OG/){sub("#","",$0); a[part_num] = $0}}}END{for(i in a) printf("%s=%s\n",i,a[i])}' partitioned_file|sort -t "=" -k 2`; do grep "Best-fit model:" ${i#*=}.log|awk '{printf(" %s:%s,", $3,"'${i%=*}'")}'; done >> partitioned_file
echo -e '\nend;'






mkdir iqtree_result

cat *.fa > ./iqtree_result/iqtree.input.fa
mv partitioned_file ./iqtree_result

cd ./iqtree_result
/disk/tools/OrthoFinder/bin/iqtree -s iqtree.input.fa -spp partitioned_file -m MF+MERGE



