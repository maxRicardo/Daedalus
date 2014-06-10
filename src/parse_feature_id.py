#/usr/bin/python2.7

# Author : Max R. Berrios Cruz
# Date : May 30 2014
# Parser for feature_importance_score 


## ---> Under work to change from R implementation with rpy2 packages to Numpy Scipy and Matplot lib 

# rpy2 for r manipulation from python 

#import rpy2.robjects as ro <---- ready for depr.

from matplotlib import pylab as plb
from scipy import stats
import datetime as dt
import numpy as np
import os



Flags = { "Lines": False , "Mean_AC": False,"GG":True,"De_Novo":True}
Feature_ID = {}



def parse_features(opt):
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
			
			e = (s[0],s[1])
			deNovo.append(e)
		else:
			
			e = (s[0],s[1])
			GG.append(e)

		if line_counter == opt.features :
			print line_counter
			print Features_ID
			break
			
	
	doc.close()
	Feature_ID["De_Novo"] = np.array(deNovo,dtype = float)
	Feature_ID["GG"] = np.array(GG,dtype = float)

	return Feature_ID


	# dict returning the divided parse of features and their respective mean accuracy
	
	##### DATA STRUCT
	## feature_id { 
	#				GG : array ([feature id] [score] ), 
	#				De_Novo : array( [feature id] [score] )
	#			  }
	
	
	
	## R Summary from both of the features group as std.out



## feature group here is send as an np array 
# test should be done in a indivudal form 

def group_summary(feature_group,output_path):
	Summ = ''' 
			Summary
	------------------------
	Mean         : {mean}
	St.Deviation : {std}
	Normal Test  : {normal_value}
	P-Value      : {p_value}

	'''

	summ = {}

	summ["mean"] = np.mean(feature_group)
	summ["std"] = np.std(feature_group)

	data = sorted(feature_group)
	fit = stats.ttest_ind(data,summ["mean"],summ["std"])

	summ["normal_value"],summ["p_value"] = stats.normaltest(feature_group)

	plb.figure()
	plb.hist(data,color = 'green')
	plb.plot(data,fit,'r*-')
	plb.savefig(output_path+"normal_group_fit.jpeg")

	return 0




def normal_stats_fit_plots(Feature_ID,output_path):


	for group in Feature_ID:
		group_list = Feature_ID[group][:,1]
		

		if len(group_list) == 0:
			# should add info here to evaluation log!
			Flags[group] = False
			continue


		group_list_ro = ro.FloatVector(group_list)
		summ = str(r.summary(group_list_ro)).split("\n")

		## Plot making part ...
		r.jpeg(output_path+"/"+group+"_summary.jpeg")
		r.hist(group_list_ro,main = group+" Histogram", xlab = group , prob = True)
		ro.globalenv["group_list_ro"] = group_list_ro
		r('curve(dnorm(x,mean = mean(group_list_ro), sd = sd(group_list_ro)), col = "red" , add = T)')
		r('dev.off')()

	#function to making the html part .....

	make_html_report(output_path)


	# making stats comparison ( simple t-test betwee groups ) 
		 



			



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

	<p align = "center">
	Representation from these graphs just gives a initial platform of<br> 
	visualization for the results to be seen in the future from this graph<br>
	analyses on the supervised learning script from Qiime<br>
	</p><br>

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


