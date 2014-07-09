#!/usr/bin/env python

# Author : Max R. Berrios Cruz
# Date : May 30 2014
# Parser for feature_importance_score 


import os
import shutil as sh
import datetime as dt

from matplotlib import pylab as plb
from scipy import stats
import numpy as np
from biom.parse import parse_biom_table as pbt

from feature_group import feature_group as fg



def parse_supervised_summary(fp):
	doc = open(fp,"r")
	sum_dir = {}

	for line in doc:
		if 'Estimated error' in line:
			sum_dir["estimated_error"] = line.split("\t")[2] 
		if 'Baseline error' in line:
			sum_dir["baseline_error"] = line.split("\t")[2]
		if 'Ratio baseline error to observed error' in line:
			sum_dir["ratio"] = line.split("\t")[6]


	return sum_dir


def parse_feature_importance_scores(fp,accuracy,features):
	#opt is a dictionary with all the options given from optget
	
	de_novo = [] 
	id_ref = []
	feature_set = {}


	doc = open(fp,"r") # this depends in the formating on optget from the script
	doc.readline() # Headers ... not much neaded right now 
	line_counter = 0


	for line in doc:
		s = str(line).strip().split("\t")
		line_counter +=1
		
		# e is a touple with (feature id, mean accuracy)
		
		if "New" in s[0]:
			
			e = (s[0],eval(s[1]))
			de_novo.append(e)
		else:
			
			e = (s[0],eval(s[1]))
			id_ref.append(e)

		if line_counter == features or accuracy <= eval(s[1]):
			break
			
	
	doc.close()
	feature_set["de_novo"] = fg(de_novo,"de_novo")
	feature_set["id_ref"] = fg(id_ref,"id_ref")
	feature_set["full_set"] = fg(id_ref+de_novo,"full_set")

	return feature_set


	# dict returning the divided parse of features and their respective mean accuracy
	
	##### DATA STRUCT
	## 	 feature_set 
	#			{
	#				id_ref  : object [feature_group], 
	#				de_novo : object [feature_group],
	#				full_set: object [feature_group]
	#			 }
	



def filter_biom_by_de_novo(otu_table_p,output_p):
	os.mkdir(output_p)


	idref = []
	dnovo = []

	biom_table = pbt(open(otu_table_p,"U"))

	#determine filtering objects
	for obj in biom_table.ObservationIds:
		if "New" in obj:
			dnovo.append(obj)
		else:
			idref.append(obj)

	os.mkdir(output_p+"/filters")

	#make filter for the otus
	filter_dnovo = open(output_p+'/filters/filter_dnovo.txt','w')
	filter_idref = open(output_p+'/filters/filter_idref.txt','w') 

	for feature in dnovo:
		filter_dnovo.write(feature+"\n")
	filter_dnovo.close()

	for feature in idref:
		filter_idref.write(feature+'\n')
	filter_idref.close()

	#filtering the otus

	os.mkdir(output_p+'/otus')
	filter_otu_command = "qiime filter_otus_from_otu_table.py -i {} -e {} -o {}"

	os.system(filter_otu_command.format(
		otu_table_p,
		output_p+'/filters/filter_idref.txt',
		output_p+'/otus/de_novo_otu_table.biom'
		))
	os.system(filter_otu_command.format(
		otu_table_p,
		output_p+'/filters/filter_dnovo.txt',
		output_p+'/otus/id_ref_otu_table.biom'
		))

	dnovo_p = output_p+'/otus/de_novo_otu_table.biom'
	idref_p = output_p+'/otus/id_ref_otu_table.biom'

	return dnovo_p,idref_p



## Method runs different normality test and return 
#  boolean flag  as  'True' if all of them are rejected 
#viceversa if they are not rejected



def normality_check(feature_group,group_name):

	if feature_group.isEmpty():
		return False

	
	normal_flag = True
	sk_test = stats.skewtest(feature_group.get_scores())
	kr_test = stats.kurtosistest(feature_group.get_scores()) 
	normaltest = stats.normaltest(feature_group.get_scores())

	temp = '''
  Normality Test P-Values[{}]
------------------------------------
Kurtosis   |  {}
Skewness   |  {}
NormalTest |  {}
	'''

	result = temp.format(group_name,kr_test[1],sk_test[1],normaltest[1])
	tests = (sk_test[1] > 0.05 ,kr_test[1] > 0.05 ,normaltest[1] > 0.05)

	return result,tests



def compare_feature_groups(fg1,fg2,variance=False,name='Comparison'):

	ttest = stats.ttest_ind(fg1,fg2,equal_var = variance)
	ktest = stats.kruskal(fg1,fg2)
	rktest = stats.ranksums(fg1,fg2)

	temp = '''

Stats Comparsion [{1}]
----------------------------------------------
Tests 	  |	P-Value
----------------------------------------------
Student-T   |    {0}
Kruskal     |    {2}
RankSum     |    {3}


	'''
	print temp.format(ttest[1],name,ktest[1],rktest[1])
	return ttest[1] > 0.05



'''
This method quantifies the number of occurences of a group of features 
based on a list of file path given as arguments. The idea is to make a 
table to summarize this number of occurences through a dictionary using 
just telling the number of times it was seen in N first positions of the 
simulation.
'''

def quantify_by_occurence(features_path,features_files_list,accuracy,features,group):
	quan_table = {}

	for f_path in features_files_list:
		
		feature_set = parse_feature_importance_scores(
			features_path+"/"+f_path,
			accuracy,
			features
			)
		


		for f,s in zip(feature_set[group].get_features(),feature_set[group].get_scores()):
			if len(quan_table) == 0:
				quan_table[f] = 1
			elif f in quan_table.keys():
				quan_table[f] += 1
			else:
				quan_table[f] = 1

	quan_table["total"] = len(features_files_list)
	return quan_table

'''
This method takes from the quantify_by_occurence , the results which is a 
dictionary of features and ocurrences of the features through the list of files
given as argument, and presents it into a document output for testing and graphics 
purposes. 

'''

def quantify_occurences_through_table(features_path,features_files_list,accuracy,features,working_path,group = "full_set"):
	quant_table = quantify_by_occurence(features_path,features_files_list,accuracy,features,group)
	header = "feature\toccurence\tpercentege\n"
	templ = "{}\t{}\t{}\n"

	doc = open(working_path+"/quntification_table_"+str(features)+"_units.txt","w")
	doc.write(header)

	for f,o in quant_table.iteritems():
		doc.write(templ.format(f,o,str(o/len(features_files_list))))

	doc.close()
	
	pass