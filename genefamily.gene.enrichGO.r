#! /usr/bin/env Rscript


library(clusterProfiler)

args <- commandArgs(T)

setwd(args[1])

expansions = read.table("Ia-io.Expansions.genes", header = F)
expansions = expansions$V1

contractions = read.table("Ia-io.Contraction.genes", header = F)
contractions = contractions$V1

gene2term = read.table("/disk/panda2bat/Data/La_io/H101SC19112982-resultsanno_hic/04.function_annotation/gene2go", sep = "\t", header = F)
gene2term = gene2term[, c(2,1)]

term2name = read.table("/disk/DataBase/GOTERM2ID", quote = "", sep = "\t", header = F)
term2name = term2name[, c(1,2)]

expansions_go = enricher(gene = expansions, pvalueCutoff = 0.05, pAdjustMethod = "fdr", TERM2GENE = gene2term, TERM2NAME = term2name)
contractions_go = enricher(gene = contractions, pvalueCutoff = 0.05, pAdjustMethod = "fdr", TERM2GENE = gene2term, TERM2NAME = term2name)

write.csv(expansions_go@result, file = "Ia-io.Expansisons.GO", sep = "\t", quote = FALSE)
write.csv(contractions_go@result, file = "Ia-io.Contractions.GO", sep = "\t", quote = FALSE)

