#!/usr/bin/env python
#inter group feature importance coparison 



import argparse 
import os
import shutil as sh

import daedalus.utils as du
import daedalus.importance_comparison as ic

def parse_argument():
	parser = argparse.ArgumentParser(description = "" , prog = "feature_importance_comparison")

	parser.add_argument("-i",help = "features score file ",required = True,dest = "features_path",type = str)
	parser.add_argument("-O",help = "otu table of the analysis",required = True,dest = "otu_table",type = str)
	parser.add_argument("-o",help = "output folder for the analysis",required = True , dest = "working_path",type = str)
	parser.add_argument("-m",help = "Metadata for running the supervised learning",required = True,dest = "map_path",type = str)
	parser.add_argument("-a",help = "accuracy to stop the picking of sample ",default = 2 , dest = "accuracy",type = int)
	parser.add_argument("-n",help = "number of features to parse from features file",default = 99999, dest = "features",type = int)
	parser.add_argument("-c",help = "Name of the category the supervised run before",dest = "cat",type = str)
	parser.add_argument("-f",help = "To force overriding the existing output directory path", dest = "override",action = "store_true")
	opt = parser.parse_args()

	return opt



'''
	working_dir/ 
		- supervised_results/
		- summarize_data/
		- comp_results_test.txt


'''


def main():
	opt = parse_argument()
	feature_groups = du.parse_feature_importance_scores(opt.features_path,opt.accuracy,opt.features)

	if not os.path.exists(opt.working_path):
		os.mkdir(opt.working_path)

	elif opt.override:
		sh.rmtree(opt.working_path)
		os.mkdir(opt.working_path)
	else:
		raise OSError(" File already exist!")


	for group in feature_groups:
		if not feature_groups[group].isEmpty():
			os.mkdir(opt.working_path+group)
			ic.non_scaling(
				opt.working_path+group,
				feature_groups[group],
				group,
				feature_groups[group].size(),
				opt.accuracy,
				opt.features,
				opt.otu_table,
				opt.map_path,
				opt.cat
				)
	pass






if __name__ == '__main__':

	main()