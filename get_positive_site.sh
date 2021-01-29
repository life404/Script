#! /bin/bash

file=$1

start=`grep -n 'Bayes Empirical Bayes' $1|awk 'BEGIN{FS=":"}{print $1}'`
end=`grep -n 'The grid (see ternary graph for p0-p1)' $1|awk 'BEGIN{FS=":"}{print $1}'`

let start=start+2
let end=end-3

sed -n "${start},${end}p" $1
