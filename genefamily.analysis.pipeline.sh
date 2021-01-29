#! /bin/bash


### paramter
while getopts ":i:o:ex:" arg;
do
    case $arg in
    i)
        input_dir=$OPTARG
        ;;
    o)
        output_dir=$OPTARG
        ;;
    ?)
        echo "The path of input & output dir is necessary."
        echo "Usage: $(basename $0) [-in path] [-out path]"
        exit 1
        ;;
    esac
done

### Run Orthofinder

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"



if [ ! -d "${output_dir}" ]
then
    mkdir ${output_dir}
else
    \rm -rf ${output_dir}
    mkdir ${output_dir}
fi

### copy the files from input dir to output dir
cp ${input_dir}/Species_Tree/SpeciesTree_rooted.txt ${output_dir}
cp ${input_dir}/Orthogroups/Orthogroups.GeneCount.tsv ${output_dir}
site_num=`awk '{if($0~/>/){printf("\n%s\n", $0)}else{printf("%s", $0)}}' $input_dir/MultipleSequenceAlignments/SpeciesTreeAlignment.fa | awk '{if($0!~/>/){if(length($0)>0) print length($0)}}'|uniq`


cd $output_dir

### RUN r8s
sed -e 's/)1:/):/g' SpeciesTree_rooted.txt > r8s.tmp
echo `sed -e 's/(//g' -e 's/)//g' SpeciesTree_rooted.txt|awk 'BEGIN{FS=","}{for(i=1;i<=NF;i++){split($i, a, ":"); printf("%s, ", a[1])}}'`
 
read -p "Select the pairs-species: " pairs
read -p "Please give the divergence time for you inputed pairs-spcies: " time

python2 /disk/tools/cafe_tutorial/python_scripts/cafetutorial_prep_r8s.py -i r8s.tmp -o r8s.input -s $site_num -p $pairs -c $time
echo "Obtain the r8s ultra tree"
tree=`/disk/tools/r8s1.81/src/r8s -b -f r8s.input|tail -n 1|awk '{split($0, a, " = "); sub("estest", "", a[2]); print a[2]}'`
echo "Obtain the lambda structure coressponding to r8s tree"
lambda=`awk '{gsub(/[a-zA-Z0-9._:]+/, "1", $0)}END{print $0}' <(echo $tree)`

### prepare the cafe input data
awk 'BEGIN{FS=OFS="\t"}{$NF=""; print "Desc", $0}' Orthogroups.GeneCount.tsv > cafe.input

### write cafe run file
echo 'load -i cafe.input -t 32 -l cafe.run.log' >> cafe.run.sh
echo "tree ${tree}" >> cafe.run.sh
echo "lambda -s -t $lambda" >> cafe.run.sh
echo "report cafe.result" >> cafe.run.sh

echo "The cafe configure file is :"
echo -e "\033[32m=======================================================================\033[0m"

sed -i -e 's/.pep.fa.longest//g' -e 's/_/-/g' cafe.input
sed -i -e 's/.pep.fa.longest//g' -e 's/_/-/g' cafe.run.sh

cat cafe.run.sh
echo -e "\033[32m========================================================================\033[0m"

echo -e "\033[32m========================begin run cafe==================================\033[0m"
/disk/tools/miniconda/bin/cafe cafe.run.sh
python2 /disk/tools/cafe_tutorial/python_scripts/cafetutorial_report_analysis.py -i cafe.result.cafe -o cafe.summary
echo -e "\033[32m========================finish run cafe=================================\033[0m"

echo -e "\033[32m===========================enrichment of cafe family====================\033[0m"
awk 'BEGIN{FS="\t"}{if($0~/Ia-io<[0-9]+>:/){split($2, a, ","); for(i in a){if(a[i]~"+"){print a[i]}}}}' cafe.summary_fams.txt|awk '{split($0,a,"["); print a[1]}'> Ia-io.Expansions.family
awk 'BEGIN{FS="\t"}{if($0~/Ia-io<[0-9]+>:/){split($2, a, ","); for(i in a){if(a[i]~"-"){print a[i]}}}}' cafe.summary_fams.txt|awk '{split($0,a,"["); print a[1]}'> Ia-io.Contraction.family


for i in `cat Ia-io.Expansions.family`; do awk '/>IaIo/{split($0, a, "|"); print a[2]}' $input_dir/Orthogroup_Sequences/${i}.fa; done > ./Ia-io.Expansions.genes
for i in `cat Ia-io.Contraction.family`; do awk '/>IaIo/{split($0, a, "|"); print a[2]}' $input_dir/Orthogroup_Sequences/${i}.fa; done > ./Ia-io.Contraction.genes

Rscript $DIR/genefamily.gene.enrichGO.r `pwd`
echo -e "\033[32m===============================finish================================== \033[0m"
