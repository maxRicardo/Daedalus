#!/usr/bin/env python 


import os
import shutil as sh
import argparse

from biom.parse import parse_biom_table as pbt

import daedalus.lib.utils as du
import daedalus.lib.summary_comparison as sc


def parse_argument():
	parser = argparse.ArgumentParser()

	parser.add_argument("-r",help = "",required = True , dest = "ref_supervised_p" , type = str)
	parser.add_argument("-d",help = "",required = True ,  dest = "dnovo_supervised_p",type = str)
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
		opt.ref_supervised_p,
		opt.dnovo_supervised_p)

	for i in summary_set_list:
		print i
		print '\n'

	raw_input(" ")

	sc.make_summary_comparison_output(summary_set_list,opt.working_path)


	return 



if __name__ == '__main__':
	main()

	