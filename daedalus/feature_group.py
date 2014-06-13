#!/usr/bin/env python2.7

##  Feature Group Class Representation 

import numpy as np 
from scipy import stats
from math import sqrt


class feature_group : 

	def __init__(self,group):
		if len(group) is not 0 :

			rep_group = np.asarray(group)
			self.__features = rep_group[:, 0]
			self.__scores = np.asarray(rep_group[:, 1] , dtype = "float64")
			self.__summary = stats.describe(self.__scores)
			self.__empty = False

		else :
			print "Empty group presented! "
			self.__empty = True 




	def isEmpty(self):
		return self.__empty

	def get_features(self):
		return self.__features

	def get_scores(self):
		return self.__scores

	def mean(self):
		return self.__summary[2]

	def variance(self):
		return self.__summary[3]

	def st_deviation(self):
		return sqrt(self.variance())

	def min(self):
		return self.__summary[1][0]

	def max(self):
		return self.__summary[1][1]

	def kurtosis(self):
		return self.__summary[5]

	def skewness(self):
		return self.__summary[4]

	def toString(self):
		__repr = '''
			
			Summary 
		---------------------------------

		Min 		: {0}
		Max 		: {1}
		Mean 		: {2}
		Variance 	: {3}
		St.Deviation 	: {4}
		Kurtosis 	: {5}
		Skewness 	: {6}

		---------------------------------

		'''

		print __repr.format(self.min(),self.max(),self.mean(),self.variance(),self.st_deviation(),self.kurtosis(),self.skewness())

