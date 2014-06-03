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
	## feature_id { GG : [ (gg_number , mean accuracy).....] , Feature_ID : [(number , mean accuracy)....]}
	
	
	
	