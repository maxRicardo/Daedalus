#!/usr/bin/env python
from __future__ import division

import argparse
import os

import daedalus.utils

## Script to compare feature in a "feature importance scores" file 


def parse_arguments():
	parser = argparse.ArgumentParser(description = " Script desing to compare state and distrubition of features from Qiime- Supervised Learning ",prog = "compare_supervised_features")

	parser.add_argument("-i",help = "Input Feature Importance Scores [REQUIRED] . ", required = True , dest = "features_path" , type = str)
	parser.add_argument("-n",help = "total number of features from file to read",default = 99999, dest = "features" , type = int)
	parser.add_argument("--accuracy",help = "will stop reading features at this 'accuracy score'",dest = "accuracy" , type = str)
	parser.add_argument("-o",help = "The directory to where the results will be written to. ", default = "CSF_output", dest = "output_path", type = str)
	parser.add_argument("-f",help = "force override of the output files if they exist", action='store_true' , dest = "override")
	opt = parser.parse_args()

	return opt


def main():
	opt = parse_arguments()

	try :
		os.mkdir(opt.output_path)
	except OSError:
		if opt.override and os.path.exists(opt.output_path):

			os.rmdir(opt.output_path)
			os.mkdir(opt.output_path)
			
		else:
			print opt.output_path
			raise OSError("File path already exist!")

	feature_id = daedalus.utils.parse_feature_importance_scores(opt)

	for group in feature_id:
		if not feature_id[group].isEmpty():
			feature_id[group].toString()
	
	if not feature_id["GG"].isEmpty() and  not feature_id["De_Novo"].isEmpty():
		daedalus.utils.compare_feature_groups(feature_id["GG"],feature_id["De_Novo"])


if __name__ == "__main__":
	main()
