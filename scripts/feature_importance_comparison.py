#!/usr/bin/env python 

## feature importance comparison 
#-> the idea is to take a OTU or a group of OTU filter them and compare the results 

## [number of otus, otu table path , feature path , score , output path ]

import argparse
import os


import daedalus.utils as du


def parse_argument():
	parser = argparse.ArgumentParser(description = "" , prog = "feature_importance_comparison")

	parser.add_argument("-i", help = "features score file ",required = True,dest = "features_path",type = str)
	parser.add_argument("-t",help = "otu table of the analysis",required = True,dest = "otu_table",type = str)
	parser.add_argument("-o",help = "output folder for the analysis",required = True , dest = "output_path",type = str)
	parser.add_argument("-a",help = "accuracy to stop the picking of sample ",default = 2 , dest = "accuracy",type = int)
	parser.add_argument("-n",help = "number of features to parse from features file",default = 1, dest = "features",type = int)

	opt = parser.parse_args()

	return opt



def main():

	opt = parse_argument()
	feature_groups = du.parse_feature_importance_scores(opt)

	for group in feature_groups:
		if not feature_groups[group].isEmpty():
			doc = open(opt.output_path+"/importance_otus.txt","w")
			for i in range(opt.features):
				doc.write(feature_group[group].get_features())
			doc.close()
	pass



if __name__ == "__main__":

	main()