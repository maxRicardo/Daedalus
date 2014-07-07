#!/usr/bin/env python 

from __future__ import division

import argparse
import os 
import shutil as sh

import daedalus.lib.utils as du

#categorize_groups


# the idea is to produce a group of files with each parse group
# an their specific caract. so that they can be used out of the 
# proyect env. 



def parse_argument():
	parser = argparse.ArgumentParser()

	parser.add_argument("-i",help = "",required = True , dest = "features_path" , )
	parser.add_argument("-n",help = "total number of features from file to read",default = 99999, dest = "features" , type = int)
	parser.add_argument("--accuracy",help = "will stop reading features at this 'accuracy score'",default = 2,dest = "accuracy" , type = str)
	parser.add_argument("-o",help = "The filename to where the results will be written to. ", default = ".", dest = "working_path", type = str)
	parser.add_argument("-f",help = "force override of the output files if they exist", action='store_true' , dest = "override")
	parser.add_argument("-v",help = " To run verbose form. Useful for debuging ", action= "store_true",dest = "verbose")
	opt = parser.parse_args()

	return opt


def main():
	opt = parse_argument()

	feature_set = du.parse_feature_importance_scores(
		opt.features_path,
		opt.accuracy,
		opt.features
		)

	if not os.path.exists(opt.working_path):
		os.mkdir(opt.working_path)

	elif opt.override:
		sh.rmtree(opt.working_path)
		os.mkdir(opt.working_path)
	else:
		raise OSError(" File already exist!")

	header = "Features	Scores\n"
	tmpl = "{}	{}\n"

	for group in feature_set:
		if not group is "full_set":
			doc = open(opt.working_path+"/features_"+group+".txt","w")
			doc.write(header)
			for f,s in zip(feature_set[group].get_features(),feature_set[group].get_scores()):
				doc.write(tmpl.format(f,s))
			doc.close()

	pass



if __name__ == "__main__":

	main()