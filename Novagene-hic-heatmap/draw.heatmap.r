#! /usr/bin/Rscript

library(ggplot2)
library(scales)

args <- commandArgs(trailingOnly = TRUE)

hic <- read.table(args[1], sep = "\t", header = T)
line <- read.table(args[2])
chro <- read.table(args[3])

hic$Z = log10(hic$Z)

p <- ggplot(data = hic, aes(x = X, y = Y, fill = Z)) + geom_tile() + 
	theme(panel.)


