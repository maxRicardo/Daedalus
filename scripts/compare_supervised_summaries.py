#!/usr/bin/env python 


import os
import shutil as sh
import argparse

from biom.parse import parse_biom_table as pbt

import daedalus.lib.utils as du
import daedalus.lib.summary_comparison as sc


def parse_argument():
	parser = argparse.ArgumentParser()

	parser.add_argument("-i",help = "",required = True , dest = "first_set_p" , type = str)
	parser.add_argument("-r",help = "",required = True ,  dest = "second_set_p",type = str)
	parser.add_argument("-o",help = "The filename to where the results will be written to. ", default = ".", dest = "working_path", type = str)
	parser.add_argument("-f",help = "force override of the output files if they exist", action='store_true' , dest = "override")
	opt = parser.parse_args()

	return opt




def main():
	opt = parse_argument()

	if not os.path.exists(opt.working_path):
		os.mkdir(opt.working_path)

	elif opt.override:
		sh.rmtree(opt.working_path)
		os.mkdir(opt.working_path)
	else:
		raise OSError(" File already exist!")

		
	summary_set_list = sc.make_supervised_summary_set(
		opt.first_set_p,
		opt.second_set_p)

	sc.make_summary_comparison_output(summary_set_list,
		list(opt.first_set_p.split["/"][-1],opt.second_set_p.split("/")[-1]),
		opt.working_path)


	return 



if __name__ == '__main__':
	main()

	