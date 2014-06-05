#!/usr/bin/python2.7
import argparse
import parse_feature_id as pfi




## Script to compare feature in a "feature importance scores" file 

def parse_arguments():
	parser = argparse.ArgumentParser(description = " Script desing to compare state and distrubition of features from Qiime- Supervised Learning ",prog = "compare_supervised_features")

	parser.add_argument("-i",help = "Input Feature Importance Scores. ", required = True , dest = "features_path" , type = str)
	parser.add_argument("-n",help = "total number of features from file to read",dest = "features" , type = int)
	parser.add_argument("--accuracy",help = "will stop reading features at this 'accuracy score'",dest = "accuracy" , type = str)

	opt = parser.parse_args()
	return opt







def main():
	opt = parse_arguments()
	feature_id = pfi.parse_features(opt)
	pfi.stats_summary_with_plots(feature_id)





if __name__ == "__main__":
	main()