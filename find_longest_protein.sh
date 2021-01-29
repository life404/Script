#! /bin/awk -f

BEGIN{
    header = ""
}

{
    if($0~/>/){
        #------------------------------------------#
        #split可以进行修改，以适应不同数据库下载的文件 #
        #------------------------------------------#
        #match($0, /ENSMUSG[0-9]+.[0-9]+/, id)
        #match($0, /ENSMUSP[0-9]+.[0-9]+/, XP)
        #split($0, id, "/.[0-9]+ /");
        split($0, id, />[A-Z]+_[0-9]+.[0-9]+ /);
        split(id[2], idd, / isoform/);
        split($0, XP, " ");
        #print(id[0], XP[0])
        #split($0, idd, " ")
        header = idd[1];
        if (!(header in longest)){
            longest[header] = ""
        }
    } else {
        if(length($0) > length(longest[header])){
            longest[header] = $0
            idmapping[header] = XP[1]
        }
    }
}

END {
    for (seq in longest){
        printf("%s\n%s\n", idmapping[seq], longest[seq])
    }
}
