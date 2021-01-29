#! /bin/bash

while getopts ":i:I:o:" arg; do
    case $arg in
    i)
        input=$OPTARG
        ;;
    I)
        ideogram=$OPTARG
        ;;
    o)
        output=$OPTARG
        ;;
    ?)
        echo "Usage: $(basename $0) [-i gff3 file path] [-I path of ideogram file][-o prefix of output file]"
        exit 1
        ;;
    esac
done

tmp='./tmp'

if [ ! -d "${tmp}" ]; then
    mkdir ${tmp}
else
    \rm -rf ${tmp}
    mkdir ${tmp}
fi

for i in `awk '{print $4}' "${ideogram}"`
do 
    grep -w ${i} ${input} | \
    sort -t $'\t' -k 4 -n > ${tmp}/${i}.tmp
done

## analysising distrubution of TE
python3 /home/panda2bat/Scripts/circos.histogram.prepare.py --ideogram ${ideogram} \
                                                            --input ${tmp} \
                                                            --output ${output}




