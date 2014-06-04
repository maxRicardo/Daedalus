#/usr/bin/python2.7

# Author : Max R. Berrios Cruz
# Date : May 30 2014
# Parser for feature_importance_score 

# rpy2 for r manipulation from python 

Flags = { "Lines": False , "Mean_AC": False}
Options = {"Lines": -1 , "Mean_AC": -1}
Features_ID = {"GG": [],"De_Novo":[]}


def Parse_Feature_ID(opt):
	#opt is a dictionary with all the options given from optget
	
	doc = open(opt["-i"],"r") # this depends in the formating on optget from the script
	doc.readline() # Headers ... not much neaded right now 
	
	for line in doc:
		s = str(line).strip().split(" ")
		
		# e is a touple with (feature id, mean accuracy)
		
		if "De_Novo" in s[0]:
			e = (s[0],s[1])
			Feature_ID["De_Novo"].append(e)
		else:
			e = (s[0],s[1])
			Feature_ID["GG"].append(e)
			
			doc.close()
			
			return Feature_ID 
	# dict returning the divided parse of features and their respective mean accuracy
	
	##### DATA STRUCT
	## feature_id { 
	#				GG : [ (gg_number , mean accuracy).....] , 
	#				De_Novo : [(number , mean accuracy)....]
	#			  }
	
	
	
	## R Summary from both of the features group as std.out


def stats_summary_with_plots(Feature_ID):
	import rpy2.robjects as ro
	import os

	r = ro.r
		
	for group in Feature_ID:
		group_list = ro.IntVector(Feature_ID[group])
		summ = str(r.summary(group_list)).split("\n")

		os.mkdir("Output_Images")
		r.x11()
		## Plot making part ...
		r.jpeg("Output_Images/"+group+"_summary.jpeg")
		r.hist(group_list,main = group+" Histogram", xlab = group)
		r.curve(dnorm(x,mean = mean(group_list), sd = sd(group_list)), col = "red", add = T)
		div.off()
		#function to making the html part .....

			



def make_html_report():
	import datetime as dt

	page_template = """
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


	<!-- Image content for GG -->

	<div align="center">
	<em>Gren Gene Summary Behavior</em><br>
	<img src = {gg_image} alt = "gg graphs" width = "480" height = "480" border = "1">
	</div><br>

	<!-- Image content for the De NOVO -->

	<div align="center">
	<em>De Novo Summary Behavior</em><br>
	<img src = {de_novo_image} alt = "de-novo graphs" width = "480" height = "480" border = "1">
	</div>

	</body>

	</html>

	"""

	gg_image = "/Output_Images/gg_summary.jpeg"
	de_novo_image = "/Output_Images/De_Novo_summary.jpeg"
	dte = dt.date.today()
	date = dte.strftime("%A %B %Y")

	## Creating the html perse!
	doc = open("daedalus_report.html","w")
	doc.write(page_template.format(**locals()))
	doc.close()


