#!/usr/bin/python2.7
import argparse
import parse_feature_id as pfi




## Script to compare feature in a "feature importance scores" file 

def parse_arguments():
	parser = argparse.ArgumentParser(description = " Script desing to compare state and distrubition of features from Qiime- Supervised Learning ",prog = "compare_supervised_features")

	parser.add_argument("-i",help = "Input Feature Importance Scores. ", required = True , dest = "features_path" , type = str)
	parser.add_argument("-n",help = "total number of features from file to read",default = 99999, dest = "features" , type = int)
	parser.add_argument("--accuracy",help = "will stop reading features at this 'accuracy score'",dest = "accuracy" , type = str)
	parser.add_argument("-o",help = "The directory to where the results will be written to. ", default = "CSF_output", dest = "output_path", type = str)
	opt = parser.parse_args()
	print opt.output_path
	return opt







def main():
	opt = parse_arguments()
	feature_id = pfi.parse_features(opt)
	pfi.normal_stats_fit_plots(feature_id,opt.output_path)
	pfi.stats_normality_and_comaprison(feature_id)






if __name__ == "__main__":
	main()