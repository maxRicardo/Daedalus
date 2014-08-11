#!/usr/bin/Rscript --vanilla --default-packages=utils

library(ggplot2)
args<-commandArgs(TRUE)

reference = paste(args[1],"daedalus/graphs/summary_graphsR.R",sep="/")
source(reference)


table <- read.delim(args[2])
graph_boxplot_summary_comparion(table,args[3],args[4],args[5])
#graph_continuos_summary_comparison(table,args[3],args[4],args[5])
anova_for_summary_comparison(table,args[3],args[4],args[5])

