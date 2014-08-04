#!/usr/bin/env python 


import os
import shutil as sh
import argparse

def parse_argument():
	parser = argparse.ArgumentParser()

	parser.add_argument("-m",help = "",required = True , dest = "mapping_file" , type = str)
	parser.add_argument("-c",help = "",required = True , dest = "category",type = str)
	parser.add_argument("-v",help = "",required = True , dest = "value",type = str)
	parser.add_argument("-o",help = "The filename to where the results will be written to. ", default = ".", dest = "working_path", type = str)
	opt = parser.parse_args()

	return opt



def main():
	opt = parse_argument()

	split_map_by_field_value(opt.mapping_file,opt.category,opt.value)
	return 



def split_map_by_field_value(map_file,category,value):

	doc,newDoc = [],[]
	catPos = -1
	outputName = map_file.strip(".txt")+"split_"+category+"_"+value+"_.txt"  

	for i in open(map_file,"r"):
		doc.append(i)


	catPos = doc[0].split("\t").index(category)
	newDoc.append(doc[0])

	for i in doc[1:]:
		line = i.split("\t")
		if value == line[catPos].strip():
			newDoc.append(i)

	new_map = open(outputName,"w")

	for i in newDoc:
		new_map.write(i)

	new_map.close()

	return 

if __name__ == "__main__":
	main()