#!/usr/bin/env python 

## feature importance comparison 
#-> the idea is to take a OTU or a group of OTU filter them and compare the results 

## [number of otus, otu table path , feature path , score , output path ]

import argparse
import os


import daedalus.utils as du


def parse_argument():
	parser = argparse.ArgumentParser(description = "" , prog = "feature_importance_comparison")

	parser.add_argument("-i", help = "features score file ",required = True,dest = "features_path",type = str)
	parser.add_argument("-O",help = "otu table of the analysis",required = True,dest = "otu_table",type = str)
	parser.add_argument("-o",help = "output folder for the analysis",required = True , dest = "working_path",type = str)
	parser.add_argument("-m",help = "Metadata for running the supervised learning",required = True,dest = "map_path",type = str)
	parser.add_argument("-a",help = "accuracy to stop the picking of sample ",default = 2 , dest = "accuracy",type = int)
	parser.add_argument("-n",help = "number of features to parse from features file",default = 99999, dest = "features",type = int)
	parser.add_argument("-d",help = "determine the number of feautres you want to remove from sample",default= 0,dest = "units",type = str)
	parser.add_argument("-e",help = " Only will work if -d given too. Set to scaling instead of in one shot ", action = "store_true",dest = "scale")
	parser.add_argument("-c",help = "Name of the category the supervised run before",dest = "cat",type = str)
	opt = parser.parse_args()

	return opt


'''
	working_dir/ 
		- supervised_results/
		- summarize_data/
		- comp_results_test.txt


'''



def main():

	opt = parse_argument()
	feature_groups = du.parse_feature_importance_scores(opt.features_path,opt.accuracy,opt.features)

	if not os.path.exists(opt.working_path):
		os.mkdir(opt.working_path)

	elif opt.override:
		os.rmdir(opt.working_path)
		os.mkdir(opt.working_path)
	else:
		raise OSError(" File already exist!")



	for group in feature_groups:
		if not feature_groups[group].isEmpty():
			if opt.scale :
				pass
			else:
				non_scaling(
					opt.working_path,
					feature_groups[group],

					)
	pass


# def scaling(working_path,output_path,feature_group,units,map_path,category):
# 	pass

'''
	>make otu_list to remove
	>run otu filter for those otus in otu_list
	>run again qiime script
	>summarize results with scripts and test results ....
	## should compare by normal test the results between original and this group to 
	## track any diferences. 
'''




def non_scaling(working_path,feature_group,group_name,units,out_table,map_path,category):
	
	otus_list = []
	features = feature_group.get_features()

	# making the otu_list
	for i in range(units):
		otus_list.append(features[i])

	#create the file for filtering
	doc = open(working_path+"/otu_list.txt","w")
	for i in otu_list:
		doc.write(str(i))
	doc.close()

	#filter the otu table
	filter_command = "qiime filter_otus_from_otu_table.py -i {} -e {} -o {}"

	os.system(filter_command.format(
		out_table,
		working_path+"/otu_list.txt",
		working_path+"filter_non_scale_"+str(units)+"_otu_table.biom"
		))

	# run new supervised learning

	super_command = "qiime supervised_learning.py -i {} -m {} -c {} -o {}"

	os.system(super_command.format(
		working_path+"filter_non_scale_"+str(units)+"_otu_table.biom",
		map_path,
		category,
		working_path+"/supervise_results_"+str(units)+"units"
		))

	# parse and compare results
	summ_command = "summarize_supervised_features.py -i {} -o {}"

	os.system(summ_command.format(
		working_path+"/supervise_results_"+str(units)+"units/features_importance_scores.txt",
		"summary_supervised_features_units"+str(units)+".txt"
		))

	new_feature_groups = du.parse_feature_importance_scores(
		working_path+"/supervise_results_"+str(units)+"units/features_importance_scores.txt",
		)

	du.compare_feature_groups(feature_group,new_feature_groups[group_name])


	return




if __name__ == "__main__":

	main()