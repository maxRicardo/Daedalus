#!/usr/bin/env python 

import os
import argparse
import shutil as sh

import daedalus.lib.utils as du 


#makes data avail for the supervised learning process ... 

def parse_argument():
	parser = argparse.ArgumentParser()

	parser.add_argument("-i",help = "",required = True , dest = "otu_table_p" , )
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

	#soon to be upgraded to filter more than one otu table 

	du.filter_biom_by_de_novo(opt.otu_table_p,opt.working_path)

	
	pass





if __name__ == "__main__":
	main()