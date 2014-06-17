#!/usr/bin/env python 

## feature importance comparison 
#-> the idea is to take a OTU or a group of OTU filter them and compare the results 

## [number of otus, otu table path , feature path , score , output path ]

import argparse
import os





def parse_argument():
	parser = argparse.ArgumentParser(description = "" , prog = "feature_importance_comparison")

	parser.add_argument("-i", help = "",required = True,dest = "features_path",type = str)
	parser.add_argument("-t",help = "",required = True,dest = "otu_table",type = str)
	parser.add_argument("-o",help = "",required = True , dest = "output_path",type = str)
	parser.add_argument("-a",help = "",default = 2 , dest = "accuracy",type = int)
	parser.add_argument("-n",help = "",default = 99999, dest = "features",type = int)

	opt = parser.parse_args()

	return opt