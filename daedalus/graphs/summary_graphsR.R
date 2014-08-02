#!/usr/bin/R --slave --vanilla
library(ggplot2)


anova_for_summary_comparison<- function(table,title = "Comparison Summary SL",output='output',saving=T){
  
  aov(RATIO ~ OTU_PICKING,table)-> stats
  capture.output(summary(stats),file=paste(output,"anova.txt",sep="_"))
  capture.output(TukeyHSD(stats),file=paste(output,"anova.txt",sep="_"),append=T)
  
}


graph_boxplot_summary_comparion <- function(table,title= "Comparison Summary SL",output='output',saving=T){
  
  HEIGHT = .1
  if ( max(table$RATIO) > (100*HEIGHT)){
    HEIGHT= 3
  }
  g <- ggplot(table,aes(OTU_PICKING,RATIO,colour = OTU_PICKING),ymax=max(table$RATIO))
  g <- g + geom_boxplot(outlier.colour=NA)+geom_point(position = position_jitter(width =.5, height = HEIGHT)) + stat_boxplot(geom='errorbar')
  g <- g + ggtitle(title)+xlab(" ")+ylab("IMPROVEMENT RATIO")
  
  if( saving == T){
  g
  ggsave(file=paste(output,"boxplot.jpeg",sep = "_"))
  }
  return (g)
}

graph_continuos_summary_comparison <- function(table,title="Comparison Summary SL",output=''){
  
  
ggplot(table,aes(x=seq(as.integer(length(table$RATIO)/length(levels(table$OTU_PICKING)))))) -> g

for (i in levels(table$OTU_PICKING)){
  g + geom_line(aes(y = RATIO,colour = OTU_PICKING),data = table[which(table$OTU_PICKING == i),]) -> g
  
}

g = g+ggtitle(title)+xlab("GROUP_ID")+ylab("IMPROVEMENT RATIO")

if ( saving == T){
g
ggsave(file=paste(output,"continuos.jpeg",sep = "_"))
}
return(g)
  
}



make_summary_pie_chart <- function(group_data,name=NULL){
  hist(group_data,plot=F)->gp_hist
  par(xpd=TRUE)
  pie3D(gp_hist$counts,cex = 1.2,main = name)
  legend("topright",as.character(gp_hist$mids),fill = rainbow(length(gp_hist$mids)),cex = 0.65)
  return(gp_hist)
}

summarize_group_stability_through_plots<- function(data){
  order_data = data[order(data$occurence),]
  
  par(mfrow=c(3,1))
  
  hist(data$occurence)
  plot(seq(length(data$occurence)),data$occurence,col = "red",type = "l")
  plot(seq(length(order_data$occurence)),order_data$occurence,col = "red",type = "l")
  
  
}

plot_comparative_group_occurence <- function(data_list){
  #initialize variables 
  par(mfrow = c(1,1))
  list_size = length(data_list)
  colors = rainbow(list_size)
  
  #making first case graph
  group = data_list[[1]]
  ordered_group = group[order(group$occurence),]
  plot(seq(length(group$occurence)),ordered_group$occurence,col = colors[1],type = "l")
  
  #make the other group of graphs 
  for (i in 2:list_size){
    group = data_list[[i]]
    ordered_group = group[order(group$occurence),]
    lines(seq(length(group$occurence)),ordered_group$occurence,col = colors[i])
  }
  
  group_labels = c()
  for (k in seq(list_size)){
    group_labels[[k]] = paste("feature_set",k*30,sep = "_")
  }
  legend("topleft",legend = group_labels , fill = colors)
}


plot_comparative_group_occurence_through_hist <- function(data_list){
  #initialize variables 
  par(mfrow = c(1,1))
  list_size = length(data_list)
  colors = rainbow(list_size)
  
  #making first case graph
  group = data_list[[5]]
  hist_group = hist(group$occurence,plot=F)
  plot(seq(hist_group$mids),hist_group$density,col = colors[1],type = "l")
  
  #make the other group of graphs 
  for (i in 2:list_size){
    group = data_list[[i]]
    hist_group = hist(group$occurence,plot=F)
    lines(seq(hist_group$mids),hist_group$density,col = colors[i])
  }
  
  group_labels = c()
  for (k in seq(list_size)){
    group_labels[[k]] = paste("feature_set",k*30,sep = "_")
  }
  legend("topleft",legend = group_labels , fill = colors)
}

