#! /bin/bash

#这个脚本可以将Orthofinder生成的OG中的蛋白质序列，转换为对应的
#DNA序列
#用法：test2.sh OGinput.file > output


for i in `grep ">" $1`
do
	ID=$(awk 'BEGIN{FS="|"}{if($2~/CTG/){gsub("CTG", "evm.model.CTG", $2);print $2} else print $2}' <(echo $i)|sed 's/\./\\./g');
	echo $i;
	grep -w $ID -A 1 ~/DATABASE/Chiroptera/tree.species.line|grep -v ">";
done
	
