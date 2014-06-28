#!/usr/bin/env python 

# importance comparsions

import shutil as sh
import os

import numpy as np

import utils as du
'''
	>make otu_list to remove
	>run otu filter for those otus in otu_list
	>run again qiime script
	>summarize results with scripts and test results ....
	## should compare by normal test the results between original and this group to 
	## track any diferences. 
'''




def inside_group_comparison(working_path,feature_group,group_name,units,accuracy,features,out_table,map_path,category):
	
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

	du.compare_feature_groups(
		feature_group.get_scores(),
		new_feature_groups[group_name].get_scores(),
		feature_group.variance()==new_feature_groups[group_name].variance()
		)


	return

'''
	this applies same logic as last "inside_group_comparsion" but
	instead of doing it in a scale mode, it will make a full comparison in the 
	listed manners: 
		
		-> no_denovo vs full_dataset
		-> no_refseq vs full_dataset
		-> no_denovo vs no_refseq

'''




def group_set_comparison(features_set,otu_table,map_path,category,accuracy,features,working_path):

	#making docs for otu elimination

	os.mkdir(working_path+"/filter_list")

	doc1 = open(working_path+"/filter_list/no_denovo_otus.txt","w")
	for i in features_set["de_novo"].get_features():
		doc1.write(str(i)+"\n")
	doc1.close()

	doc2 = open(working_path+"/filter_list/no_refseq_otus.txt","w")
	for i in features_set["id_ref"].get_features():
		doc2.write(str(i)+"\n")
	doc2.close()

	

	#filter out otu features
	
	otu_filter_command = "qiime filter_otus_from_otu_table.py -i {} -e {} -o {}"
	
	os.mkdir(working_path+"/filter_otus")

	## making denovo filtered 

	os.system(otu_filter_command.format(
		otu_table,
		working_path+"/filter_list/no_denovo_otus.txt",
		working_path+"/filter_otus/no_denovo_otu_table.biom"
		))

	##making refseq filtered 

	os.system(otu_filter_command.format(
		otu_table,
		working_path+"/filter_list/no_refseq_otus.txt",
		working_path+"/filter_otus/no_refseq_otu_table.biom"
		))

	

	#making new supervised features run 
	supervised_command = "qiime supervised_learning.py -i {} -m {} -c {} -o {}"

	##supervised with no-denovo
	os.system(supervised_command.format(
		working_path+"/filter_otus/no_denovo_otu_table.biom",
		map_path,
		category,
		working_path+"/no_denovo_supervised"
		))

	## supervised with no_refseq
	os.system(supervised_command.format(
		working_path+"/filter_otus/no_refseq_otu_table.biom",
		map_path,
		category,
		working_path+"/no_refseq_supervised"
		))

	#Parse feature set per system 
	

	no_denovo_feaure_set = du.parse_feature_importance_scores(
		working_path+"/no_denovo_supervised/feature_importance_scores.txt",
		accuracy,
		features
		)
	

	no_refseq_feaure_set = du.parse_feature_importance_scores(
		working_path+"/no_refseq_supervised/feature_importance_scores.txt",
		accuracy,
		features
		)

	#making full set !

	features_full_scores = features_set["full_set"].get_scores()

	feature_full_scores_variance = features_set["full_set"].variance()


	du.compare_feature_groups(
		no_denovo_feaure_set["id_ref"].get_scores(),
		features_full_scores,
		no_denovo_feaure_set["id_ref"].variance() == feature_full_scores_variance,
		"No De-Novo vs Full Feature Set"
		)


	du.compare_feature_groups(
		no_refseq_feaure_set["de_novo"].get_scores(),
		features_full_scores,
		no_refseq_feaure_set["de_novo"].variance() == feature_full_scores_variance,
		"No id_ref vs Full Feature Set"
		)

	du.compare_feature_groups(
		no_denovo_feaure_set["id_ref"].get_scores(),
		no_refseq_feaure_set["de_novo"].get_scores(),
		no_refseq_feaure_set["de_novo"].variance() == no_denovo_feaure_set["id_ref"].variance(),
		"No-denovo vs No id_ref"
		)



	return