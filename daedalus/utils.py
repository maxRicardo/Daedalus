#!/usr/bin/env python

# Author : Max R. Berrios Cruz
# Date : May 30 2014
# Parser for feature_importance_score 


## ---> Under work to change from R implementation with rpy2 packages to Numpy Scipy and Matplot lib 

# rpy2 for r manipulation from python 


import os
import datetime as dt

from matplotlib import pylab as plb
from scipy import stats
import numpy as np

from feature_group import feature_group as fg




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




def make_html_report(output_path):
	import datetime as dt

	page_head = """
	<html>
	<head>
	<title>Daedalus Report</title> 
	</head>

	<body>

	<h1 align= "center">Graph Reports From Supervised Learning </h1>
	<p> 
	Author : Max R. Berrios Cruz<br>
	email : max.berrios@upr.edu<br>
	Date : {date}<br>
	</p>


	"""


	id_ref_image = """

	<!-- Image content for id_ref -->

	<div align="center">
	<em>Green Gene Summary Behavior</em><br>
	<img src = {id_ref_image} alt = "id_ref graphs" width = "480" height = "480" border = "1">
	</div><br>

	"""

	de_novo_image = """

	<!-- Image content for the De NOVO -->

	<div align="center">
	<em>De Novo Summary Behavior</em><br>
	<img src = {de_novo_image} alt = "de-novo graphs" width = "480" height = "480" border = "1">
	</div>
	"""

	page_tail = """

	</body>

	</html>

	"""

	if Flags["id_ref"]:
		full_page = page_head+id_ref_image

	if Flags["de_novo"]:
		full_page = full_page+de_novo_image

	full_page = full_page+page_tail




	id_ref_image = '"id_ref_summary.jpeg"'
	de_novo_image = '"de_novo_summary.jpeg"'
	dte = dt.date.today()
	date = dte.strftime("%A %B %Y")

	## Creating the html perse!
	doc = open(output_path+"/daedalus_report.html","w")
	doc.write(full_page.format(**locals()))
	doc.close()


