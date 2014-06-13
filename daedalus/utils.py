#/usr/bin/python2.7

# Author : Max R. Berrios Cruz
# Date : May 30 2014
# Parser for feature_importance_score 


## ---> Under work to change from R implementation with rpy2 packages to Numpy Scipy and Matplot lib 

# rpy2 for r manipulation from python 

#import rpy2.robjects as ro <---- ready for depr.

from matplotlib import pylab as plb
from feature_group import feature_group as fg
from scipy import stats
import datetime as dt
import numpy as np



Flags = { "Lines": False , "Mean_AC": False,"GG":True,"De_Novo":True}
Feature_ID = {}



def parse_feature_importance_scores(opt):
	#opt is a dictionary with all the options given from optget
	
	deNovo  = [] 
	GG = []


	doc = open(opt.features_path,"r") # this depends in the formating on optget from the script
	doc.readline() # Headers ... not much neaded right now 
	line_counter = 0


	for line in doc:
		s = str(line).strip().split("\t")
		line_counter +=1
		
		# e is a touple with (feature id, mean accuracy)
		
		if "De_Novo" in s[0]:
			
			e = (s[0],eval(s[1]))
			deNovo.append(e)
		else:
			
			e = (s[0],eval(s[1]))
			GG.append(e)

		if line_counter == opt.features :
			break
			
	
	doc.close()
	Feature_ID["De_Novo"] = fg(deNovo)
	Feature_ID["GG"] = fg(GG)

	return Feature_ID


	# dict returning the divided parse of features and their respective mean accuracy
	
	##### DATA STRUCT
	## feature_id { 
	#				GG : object [ feature_group ], 
	#				De_Novo : object [feature_group]
	#			  }
	
	
	
	## R Summary from both of the features group as std.out


## Method runs different normality test and return 
#  boolean flag  as  'True' if all of them are rejected 
#viceversa if they are not rejected



def normality_check(feature_group,output_path):

	if feature_group.isEmpty():
		return False

	
	normal_flag = True
	sk_test = stats.skewtest(feature_group.get_scores())
	kr_test = stats.kurtosistest(feature_group.get_scores()) 
	normaltest = stats.normaltest(feature_group.get_scores())

	temp = '''

			Normality Test P-Values
		------------------------------------
		 Kurtosis   |  {0}
		 Skewness   |  {1}
		 NormalTest |  {2}


	'''

	result = temp.format(kr_test[1],sk_test[1],normaltest[1])

	print result


	tests = (sk_test[1] > 0.05 ,kr_test[1] > 0.05 ,normaltest[1] > 0.05)

	return tests



def compare_feature_groups(fg1,fg2):

	if fg1.variance() == fg2.variance():
		ttest = stats.ttest_ind(fg1.get_scores(),fg2.get_scores())
		print "Equal Variance "

	else :
		ttest = stats.ttest_ind(fg1.get_scores(),fg2.get_scores(),equal_var = False)
		print "Different Variance"

	temp = '''

		T-test Results 
	---------------------------
	P value   |    {0}

	'''
	print temp.format(ttest[1])
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


	GG_image = """

	<!-- Image content for GG -->

	<div align="center">
	<em>Green Gene Summary Behavior</em><br>
	<img src = {gg_image} alt = "gg graphs" width = "480" height = "480" border = "1">
	</div><br>

	"""

	De_Novo_image = """

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

	if Flags["GG"]:
		full_page = page_head+GG_image

	if Flags["De_Novo"]:
		full_page = full_page+De_Novo_image

	full_page = full_page+page_tail




	gg_image = '"GG_summary.jpeg"'
	de_novo_image = '"De_Novo_summary.jpeg"'
	dte = dt.date.today()
	date = dte.strftime("%A %B %Y")

	## Creating the html perse!
	doc = open(output_path+"/daedalus_report.html","w")
	doc.write(full_page.format(**locals()))
	doc.close()


