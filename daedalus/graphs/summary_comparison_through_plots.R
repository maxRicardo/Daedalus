#!/usr/bin/Rscript --vanilla --default-packages=utils

library(ggplot2)
reference = paste(args[4],"daedalus/graphs/summary_graphsR.R",sep="/")
source(reference)

args<-commandArgs(TRUE)

table <- read.delim(args[1])
graph_boxplot_summary_comparion(table,args[2],args[3])
graph_continuos_summary_comparison(table,args[2],args[3])
anova_for_summary_comparison(table,args[2],args[3])

