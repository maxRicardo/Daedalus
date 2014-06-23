#!/usr/bin/env python 

# importance comparsions

import shutil as sh
import os


import utils as du
'''
	>make otu_list to remove
	>run otu filter for those otus in otu_list
	>run again qiime script
	>summarize results with scripts and test results ....
	## should compare by normal test the results between original and this group to 
	## track any diferences. 
'''




def non_scaling(working_path,feature_group,group_name,units,accuracy,features,out_table,map_path,category):
	
	otus_list = []
	features = feature_group.get_features()

	# making the otu_list
	for i in range(units):
		otus_list.append(features[i])

	#create the file for filtering
	doc = open(working_path+"/otu_list.txt","w")
	for i in otus_list:
		doc.write(str(i)+"\n")
	doc.close()

	#filter the otu table
	filter_command = "qiime filter_otus_from_otu_table.py -i {} -e {} -o {}"

	os.system(filter_command.format(
		out_table,
		working_path+"/otu_list.txt",
		working_path+"_filter_non_scale_"+str(units)+"_otu_table.biom"
		))

	# run new supervised learning

	super_command = "qiime supervised_learning.py -i {} -m {} -c {} -o {}"

	os.system(super_command.format(
		working_path+"_filter_non_scale_"+str(units)+"_otu_table.biom",
		map_path,
		category,
		working_path+"/supervise_results_"+str(units)+"_units"
		))

	# parse and compare results
	summ_command = "summarize_supervise_features.py -i {} -o {}"

	os.system(summ_command.format(
		working_path+"/supervise_results_"+str(units)+"_units/feature_importance_scores.txt",
		working_path
		))

	new_feature_groups = du.parse_feature_importance_scores(
		working_path+"/supervise_results_"+str(units)+"_units/feature_importance_scores.txt",
		accuracy,
		features
		)

	du.compare_feature_groups(feature_group,new_feature_groups[group_name])


	return