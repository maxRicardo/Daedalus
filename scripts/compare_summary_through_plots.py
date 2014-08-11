#!/usr/bin/env python

import os , sys
import subprocess as sub
import shutil as sh
import argparse




def parse_argument():
	parser = argparse.ArgumentParser()

	parser.add_argument("-i",help = "",required = True , dest = "summary_table" , type = str)
	parser.add_argument("-o",help = "The filename to where the results will be written to. ", default = ".", dest = "working_path", type = str)
	parser.add_argument("-f",help = "force override of the output files if they exist", action='store_true' , dest = "override")
	parser.add_argument("-c,--correct_inf_cases",help="",action="store_false",dest='inf_case')
	opt = parser.parse_args()

	return opt


def main():
	opt = parse_argument()
	opt.working_path = opt.working_path.strip("/")

	if not os.path.exists(opt.working_path):
		os.mkdir(opt.working_path)

	elif opt.override:
		sh.rmtree(opt.working_path)
		os.mkdir(opt.working_path)
	else:
		raise OSError(" File already exist!")

	PROJECT_PATH = "/".join(sys.argv[0].split("/")[:-2])

	command = "Rscript --slave --vanilla {}/daedalus/graphs/summary_comparison_through_plots.R {} {} {} {}"
	os.system(command.format(
				PROJECT_PATH,
				PROJECT_PATH,
				opt.summary_table,
				opt.working_path,
				opt.working_path+"/"+opt.working_path.split("/")[0],
				opt.inf_case
				))

	return 



if __name__ == '__main__':
	main()


