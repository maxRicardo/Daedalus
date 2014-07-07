#!/usr/bin/env python

##  Feature Group Class Representation 

import numpy as np 
from scipy import stats
from math import sqrt


class feature_group : 

	def __init__(self,group,name):
		if len(group) is not 0 :

			rep_group = np.asarray(group)
			self.__name = name
			self.__features = np.asarray(rep_group[:, 0] , dtype = "str")
			self.__scores = np.asarray(rep_group[:, 1] , dtype = "float64")
			self.__summary = stats.describe(self.__scores)
			self.__size = len(group)

		else :
			self.__size = 0



	def size(self):
		return self.__size

	def isEmpty(self):
		return self.__size == 0

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

	def summary(self):
		
		__repr = '''
	Summary [{}]
---------------------------------
Min 		: {}
Max 		: {}
Mean 		: {}
Counts 		: {}
Variance 	: {}
St.Deviation 	: {}
Kurtosis 	: {}
Skewness 	: {}
---------------------------------
		'''
		return __repr.format(
			self.__name,
			self.min(),
			self.max(),
			self.mean(),
			self.size(),
			self.variance(),
			self.st_deviation(),
			self.kurtosis(),
			self.skewness())
		
	def toString(self):
		header = 'Feature	Score'
		temp = '{}	{}'
		print header
		for f,s in zip(list(self.__features),list(self.__scores)):
			print temp.format(f,s)
		pass