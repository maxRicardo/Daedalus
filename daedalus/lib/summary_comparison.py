#!/usr/bin/env python 

#summary_comparison
from __future__ import division
import os
import shutil


import numpy as np
import scipy.stats as stats
from biom.parse import parse_biom_table as pbt

import utils

#asume that each path has a full set of tables to compare 

def make_supervised_summary_set(reference_p,dnovo_p,complete_p = None):
	reference = []
	dnovo = []
	complete = []

	reference_dir = sorted(os.listdir(reference_p))
	dnovo_dir = sorted(os.listdir(dnovo_p))
	


	for i in reference_dir:
		full_p = reference_p+'/'+i+'/summary.txt'
		reference.append(full_p)
		

	for i in dnovo_dir:
		full_p = dnovo_p+'/'+i+'/summary.txt'
		dnovo.append(full_p)
		

	summary_set_list = []
	counter = 0

	for i in dnovo:
		de_novo_sum = utils.parse_supervised_summary(i)
		de_novo_sum['name'] = i.split("summary")[0].replace("/","_")
		summary_set_line = (de_novo_sum["name"],
							de_novo_sum["baseline_error"],
							de_novo_sum["estimated_error"],
							de_novo_sum["ratio"],
							"de_novo")
		summary_set_list.append(summary_set_line)

	for i in reference:
		reference_sum = utils.parse_supervised_summary(i)
		reference_sum['name'] = i.split("summary")[0].replace("/","_")
		summary_set_line = (reference_sum["name"],
							reference_sum["baseline_error"],
							reference_sum["estimated_error"],
							reference_sum["ratio"],
							"reference")
		summary_set_list.append(summary_set_line)


	if complete_p != None :
		complete_dir = sorted(os.listdir(complete_p))

		for i in complete_dir:
			full_p = complete_p+'/'+i+'/summary.txt'
			complete.append(full_p)

		for i in complete:
			complete_sum = utils.parse_supervised_summary(i)
			complete_sum['name'] = i.split("summary")[0].replace("/","_")
			summary_set_line = (complete_sum["name"],
								complete_sum["baseline_error"],
								complete_sum["estimated_error"],
								complete_sum["ratio"],
								"complete")
			summary_set_list.append(summary_set_line)


	return summary_set_list




def make_summary_comparison_output(summary_set_list,output_p):
	header = "GROUP_ID\tBASELINE_ERROR\tESTIMATED_ERROR\tRATIO\tOTU_PICKING\n"
	templ = '{}\t{}\t{}\t{}\t{}\n'

	report = open(output_p+"/summary_inside_compare_results.txt","w")
	report.write(header)

	dnovo_count = 0
	idref_count = 0

	for result in summary_set_list:

		report.write(templ.format(*result))

	report.close()


	pass


