#/usr/bin/python2.7

# Author : Max R. Berrios Cruz
# Date : May 30 2014
# Parser for feature_importance_score 

# rpy2 for r manipulation from python 

Flags = { "Lines": False , "Mean_AC": False,"GG":True,"De_Novo":True}
Options = {"Lines": -1 , "Mean_AC": -1}
Features_ID = {"GG": [],"De_Novo":[]}


def parse_features(opt):
	#opt is a dictionary with all the options given from optget
	
	doc = open(opt.features_path,"r") # this depends in the formating on optget from the script
	doc.readline() # Headers ... not much neaded right now 
	
	for line in doc:
		s = str(line).strip().split("\t")
		
		# e is a touple with (feature id, mean accuracy)
		
		if "De_Novo" in s[0]:
			
			e = (s[0],s[1])
			Features_ID["De_Novo"].append(e)
		else:
			
			e = (s[0],s[1])
			Features_ID["GG"].append(e)
			
	
	doc.close()
	return Features_ID


	# dict returning the divided parse of features and their respective mean accuracy
	
	##### DATA STRUCT
	## feature_id { 
	#				GG : [ (gg_number , mean accuracy).....] , 
	#				De_Novo : [(number , mean accuracy)....]
	#			  }
	
	
	
	## R Summary from both of the features group as std.out


def normal_stats_fit_plots(Feature_ID):

	import rpy2.robjects as ro
	import os,shutil

	r = ro.r
	
	try :
		os.mkdir("Output_Images")
	except OSError:
		shutil.rmtree("Output_Images")
		os.mkdir("Output_Images")

		
	

	for group in Feature_ID:
		group_list = []
		for i in Feature_ID[group]:
			group_list.append(eval(i[1]))
		

		if len(group_list) == 0:
			# should add info here to evaluation log!
			Flags[group] = False
			continue


		group_list_ro = ro.FloatVector(group_list)
		summ = str(r.summary(group_list_ro)).split("\n")

		## Plot making part ...
		r.jpeg("Output_Images/"+group+"_summary.jpeg")
		r.hist(group_list_ro,main = group+" Histogram", xlab = group)
		ro.globalenv["group_list_ro"] = group_list_ro
		r('curve(dnorm(x,mean = mean(group_list_ro), sd = sd(group_list_ro)), col = "red" , add = T)')
	#function to making the html part .....
	make_html_report()


	# making stats comparison ( simple t-test betwee groups ) 
		 



			



def make_html_report():
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
	Representation from this graphs just gives a initial platform of<br> 
	visualization for the results to be seen in the future from this graph<br>
	analises on the supervised learning script from Qiime<br>
	</p><br>

	"""
	GG_image = """

	<!-- Image content for GG -->

	<div align="center">
	<em>Gren Gene Summary Behavior</em><br>
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
	doc = open("Output_Images/daedalus_report.html","w")
	doc.write(full_page.format(**locals()))
	doc.close()


