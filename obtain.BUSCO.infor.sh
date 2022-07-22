#!/bin/bash

cat \
	<(echo -e "#group\tgene_name\torthodb_url\tevolutionary_rate\tmedian_exon_count\tstdev_exon_count\tmedian_protein_length\tstdev_protein_length") \
	<(cat $1 | cuf -f 1 | while read id; do wget -qO - https://dev.orthodb.org/group\?id=\$\{id\}|jq -r '.|[.data.id, .data.name, .url, .data.evolutionary_rate, .data.gene_architecture.exon_median_counts, .data.gene_architecture.exon_stdev_counts, .data.gene_architecture.protein_median_length, .data.gene_architecture.protein_stdev_length] | @tsv';|sleep 1s;done)
