#!/usr/bin/env bash

echo 'making set of features'
mkdir mega_set_of_features
cd mega_set_of_features
mkdir quantum_tables
echo ' '

for i in $(seq 5)
do
 mkdir supervised_features_$i
 echo 'Running supervised learning group #'$i

  for n in $(seq 20)
   do
    echo 'running supervised learning simulation #'$n
    qiime supervised_learning.py -i ../otu_table.biom -m ../combined_mapping_file.txt -c SampleType -o supervised_output_$n

    echo 're-arranging the files locations '
    mv supervised_output_$n/feature_importance_scores.txt supervised_features_$i/feature_importance_scores_$n.txt
    rm -r supervised_output_$n
   done
   echo 'making quantification tables '
   make_quatification_table.py -i supervised_features_$i -n 30 -o quant_table_results_$i
   mv quant_table_results_$i/quntification_table_30_units.txt quantum_tables/quntification_table_30_units_$i.txt
   rm quant_table_results_$i -r
   echo '  '
done

