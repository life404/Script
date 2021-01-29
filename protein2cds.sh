while getopts ":i:s:g:f:" arg
do
    case $arg in 
    i)
        input=$OPTARG
        ;;
    s)
        species=$OPTARG
        ;;
    g)
        gff=$OPTARG
        ;;
    f)
        fasta=$OPTARG
        ;;
    ?)
        echo "Usage: $(basename $0) [-i input] [-s speceis list] [-g gff] [-f genome.fasta]"
        exit 1
        ;;
    esac
done

name=`echo ${input}|awk 'BEGIN{FS="/"}{print $NF}'`
tmp="tmp.$name"

protein_id=`grep -w $species $input|awk 'BEGIN{FS="|"}{print $2}'`

grep -w $protein_id $gff|/disk/tools/bedops/bin/convert2bed --input=gff -d - > ${tmp}.bed

direction=`awk 'BEGIN{FS="\t"}{print $6}' ${tmp}.bed|sort|uniq`
scribe=`awk 'BEGIN{FS="\t"}{print $10}' ${tmp}.bed|sort|uniq`

echo "get $species 's $protein_id from $fasta"

bedtools getfasta -fi $fasta -bed ${tmp}.bed -fo ${tmp}.fasta

~/Scripts/orthomcl_single_copy_coresponding_cds.py --input ${tmp}.fasta --dir $direction --id "${protein_id}_CDS" --output "${species}.${name}.CDS"


