#!/usr/bin/Rscript --vanilla --default-packages=utils

library(ggplot2)
source('~/Documents/MSSM_Proyect/daedalus/daedalus/graphs/summary_graphsR.R')

args<-commandArgs(TRUE)

table <- read.delim(args[1])
graph_boxplot_summary_comparion(table,args[2])
graph_continuos_summary_comparison(table,args[2])
anova_for_summary_comparison(table,args[2])

