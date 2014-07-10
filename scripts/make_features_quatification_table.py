#!/usr/bin/env python 

from __future__ import division

import argparse
import os 
import shutil as sh

import daedalus.lib.utils as du

#make_quantification_table


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

	#making workspace for the script to work on 

	if not os.path.exists(opt.working_path):
		os.mkdir(opt.working_path)

	elif opt.override:
		sh.rmtree(opt.working_path)
		os.mkdir(opt.working_path)
	else:
		raise OSError(" File already exist!")



	if os.path.exists(opt.features_path):
		du.quantify_occurences_through_table(
			opt.features_path,
			os.listdir(opt.features_path),
			opt.accuracy,
			opt.features,
			opt.working_path
			)
		
	elif type([]) is type(opt.features_path.split(",")):
		du.quantify_occurences_through_table(
			".",
			opt.features_path.split(","),
			opt.accuracy,
			opt.features,
			opt.working_path
			)
	else:
		raise OSError( " Dude! you are not giving me a list of files or a folder path!")


if __name__ == "__main__":
	main()
