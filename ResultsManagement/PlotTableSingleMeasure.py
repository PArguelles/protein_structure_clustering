import numpy as np
import matplotlib.pyplot as plt
import os
import re

#path_to_results = 'C:/ShareSSD/scop/best_results/'
path_to_results = 'C:/ShareSSD/scop/clustering_results_single_matrix/'
path_to_tables = 'C:/ShareSSD/scop/tables_single_matrix/table'

color = False

for spl in ['a.1', 'a.3', 'b.2', 'b.3']:
    for alg in ['complete','average','kmedoids']:

        algorithm = alg
        sample = spl
        standard = "rmsd"

        data = []
        labels = [] 
        values = []

        counter = 0
        reference_value = 0

        for filename in os.listdir(path_to_results):
            if algorithm in filename and sample in filename:
                parsed = filename.split('_')
                measure1 = parsed[2]
                if 'rmsd' in measure1:
                    lab1 = 'RMSD'
                elif 'gdt' in measure1:
                    if '2' in parsed[3]:
                        lab1 = 'GDT-HA'
                    else:
                        lab1 = 'GDT-TS'
                elif 'seq' in measure1:
                    lab1 = 'Sequence'
                elif 'tm' in measure1:
                    lab1 = 'TM-Score'
                elif 'maxsub' in measure1:
                    lab1 = 'MaxSub'

                label = lab1

                labels.append(label)
                with open(path_to_results+filename,'r') as fp:
                    line = fp.readline()
                    while line:
                        # start reading metrics
                        if '# Cluster evaluation:' in line:
                            i = 0
                            #print(line)   
                            while i < 6: #6 metrics
                                line = fp.readline()
                                num = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)]
                                values.append(num[0])
                                i += 1
                                #print(line)   
                        line = fp.readline()
                    data.append(values)
                    values = []
                if standard in filename:
                    reference_value = counter
                else: counter += 1

        #print(reference_value)

        columns = ('Homogeneity', 'Completeness', 'V-measure', 'AMI', 'Calinski-Harabasz', 'Silhouette')
        rows = labels

        plt.axis('off')

        # Add a table at the bottom of the axes
        the_table = plt.table(cellText=data,
                            rowLabels=rows,
                            rowColours=None,
                            colLabels=columns,
                            cellLoc='center',
                            loc='center')

        plt.savefig(path_to_tables+algorithm+sample+'nocolor.jpeg', format='jpeg', bbox_inches="tight", dpi=300)
