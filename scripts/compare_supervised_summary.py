#!/usr/bin/env python

#compare_supervised_summary

import os
import shutil as sh
import argparse

import daedalus.lib.summary_comparison as sc


def parse_argument():
	parser = argparse.ArgumentParser(description="Comparse a buch load of otu_table supervised summary results. The comparison can either be done filtering the otu compare dnovo vs idref or filtered id_ref vs closed picking ")

	parser.add_argument("-i",help = "",required = True , dest = "features_path" , )
	parser.add_argument("-o",help = "The filename to where the results will be written to. ",required = True, dest = "working_path", type = str)
	parser.add_argument("-O",help="",required = True,dest = "otu_table_p",type = str)
	parser.add_argument("-m",help="",required = True,dest = "map_path",type=str)
	parser.add_argument("-c",help="",required=True,dest = "category",type = str)
	parser.add_argument("-f",help = "force override of the output files if they exist", action='store_true' , dest = "override")
	parser.add_argument("-v",help = " To run verbose form. Useful for debuging ", action= "store_true",dest = "verbose")
	opt = parser.parse_args()

	return opt

def main():
	opt = parse_argument()

	# making file directory 
	if not os.path.exists(opt.working_path):
		os.mkdir(opt.working_path)

	elif opt.override:
		sh.rmtree(opt.working_path)
		os.mkdir(opt.working_path)
	else:
		raise OSError(" File already exist!")


	#verifying for otu table set ... although it can work with just one 
	#otu table , its expected to have a nice amount of them to run ... 
	otu_tables = []

	try:
		tables_dir = os.listdir(opt.otu_table_p)
		for i in tables_dir:
			otu_tables.append(opt.otu_table_p+"/"+i)
	except OSError:
		out_tables.append(opt.otu_table_p)


	sc.compare_summary_dnovo_idref(
		otu_tables,
		opt.map_path,
		opt.category,
		opt.working_path)

	#watch for results
	pass 





if __name__ == "__main__":

	main()

	