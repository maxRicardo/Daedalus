#!/usr/bin/env python

from __future__ import division

import argparse
import os

import daedalus.lib.utils


## Script to compare feature in a "feature importance scores" file 


def parse_arguments():
	parser = argparse.ArgumentParser(description = "Summarize supervise features group data, simple descriptive stats from the data for reference",prog = "summarize_supervised_features")

	parser.add_argument("-i",help = "Input Feature Importance Scores [REQUIRED] . ", required = True , dest = "features_path" , type = str)
	parser.add_argument("-n",help = "total number of features from file to read",default = 99999, dest = "features" , type = int)
	parser.add_argument("--accuracy",help = "will stop reading features at this 'accuracy score'",default = 2,dest = "accuracy" , type = str)
	parser.add_argument("-o",help = "The filename to where the results will be written to. ", default = ".", dest = "output_path", type = str)
	parser.add_argument("-f",help = "force override of the output files if they exist", action='store_true' , dest = "override")
	parser.add_argument("-v",help = " To run verbose form. Useful for debuging ", action= "store_true",dest = "verbose")
	opt = parser.parse_args()

	return opt


def main():
	opt = parse_arguments()
	feature_id = daedalus.utils.parse_feature_importance_scores(opt.features_path,opt.accuracy,opt.features)
	doc = open(opt.output_path+"/summarize_output.txt","w")

	for group in feature_id:
		if not feature_id[group].isEmpty():
			normality = daedalus.utils.normality_check(feature_id[group],group)

			if opt.verbose:
				print feature_id[group].summary()
				print normality[0]
			
			doc.write(feature_id[group].summary())
			doc.write(normality[0])
			doc.write(" ")
	doc.close()



if __name__ == "__main__":
	main()
