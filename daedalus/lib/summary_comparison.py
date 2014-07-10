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

def make_supervised_summary_set(gr1_p,gr2_p):
	gr_1_dir = sorted(os.listdir(gr1_p))
	gr_2_dir = sorted(os.listdir(gr2_p))

	gr_1 = []
	gr_2 = []

	for i in gr_1_dir:
		gr_1.append(gr1_p+'/'+i+'/summary.txt')

	for i in gr_2_dir:
		gr_2_dir.append(gr2_p+'/'+i+'summary.txt')

	summary_set_list = []
	counter = 0

	for i,d in zip(gr_1,gr_2):
		id_ref_summ = utils.parse_supervised_summary(i)
		de_novo_summ = utils.aprse_supervosed_summary(d)

		summary_set(
			'group_'+counter,
			id_ref_summ['ratio'],
			de_novo_summ['ratio'],
			id_ref_summ['ratio']-de_novo_summ['ratio'])
		
		summary_set_list.append(summary_set)
		counter+=1

	return summary_set_list




def make_summary_comparison_output(summary_set_list):
	header = " group_name	id_ref	De_Novo	delta_diference\n"
	templ = '{}	{}	{}	{}\n'

	report = open("summary_inside_compare_results_"+category+".txt","w")
	report.write(header)

	dnovo_count = 0
	idref_count = 0

	for result in summary_set_list:

		report.write(templ.format(result))

		if result[3] > 0:
			idref_count+=1

		elif result[3] < 0:
			dnovo_count+=1
			
	report.write("-----------------------------------------------------------\n")
	report.write("'%' of improvement : 	{}	{}\n".format(
		idref_count/len(summary_set_list),
		dnovo_count/len(summary_set_list)
		))

	report.close()


	pass


