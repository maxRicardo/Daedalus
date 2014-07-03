#!/usr/bin/env bash

mkdir supervised_features_20

for n in $(seq 20)
 do
  qiime supervised_learning.py -i otu_table.biom -m combined_mapping_file.txt -c SampleType -o supervised_output_$n
  mv supervised_output_$n/feature_importance_scores.txt supervised_features_20/feature_importance_scores_$n.txt
  rm -r supervised_output_$n
 done
