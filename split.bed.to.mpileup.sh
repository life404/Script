#! /bin/awk -f

BEGIN {FS="\t";}

{
  start = $2;
  for(i = 1; i<1000; i++){
    end = i*int($3/1000);
    printf("%s\t%s\t%s\n", $1"-"i, start, end);
    start = end
  }
  
  printf("%s\t%s\t%s\n", $1"-"i, start, $3)
  
}
