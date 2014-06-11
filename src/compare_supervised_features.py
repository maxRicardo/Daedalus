#!/usr/bin/python2.7
import argparse
import utils
import feature_group
import os




## Script to compare feature in a "feature importance scores" file 

def parse_arguments():
	parser = argparse.ArgumentParser(description = " Script desing to compare state and distrubition of features from Qiime- Supervised Learning ",prog = "compare_supervised_features")

	parser.add_argument("-i",help = "Input Feature Importance Scores [REQUIRED] . ", required = True , dest = "features_path" , type = str)
	parser.add_argument("-n",help = "total number of features from file to read",default = 99999, dest = "features" , type = int)
	parser.add_argument("--accuracy",help = "will stop reading features at this 'accuracy score'",dest = "accuracy" , type = str)
	parser.add_argument("-o",help = "The directory to where the results will be written to. ", default = "CSF_output", dest = "output_path", type = str)
	parser.add_argument("-f",help = "force override of the output files if they exist", action='store_true' , dest = "override")
	opt = parser.parse_args()

	return opt







def main():
	opt = parse_arguments()

	try :
		os.mkdir(opt.output_path)
	except OSError:
		if opt.override and os.path.exists(opt.output_path):

			os.rmdir(opt.output_path)
			os.mkdir(opt.output_path)
			
		else:
			raise OSError("File path already exist!")

	feature_id = utils.parse_feature_importance_scores(opt)
	#utils.normal_stats_fit_plots(feature_id,opt.output_path)
	feature_id["GG"].toString()
	print utils.normality_check(feature_id["GG"],opt.output_path)






if __name__ == "__main__":
	main()