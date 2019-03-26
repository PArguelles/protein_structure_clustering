import numpy as np
import matplotlib.pyplot as plt
import os
import re

#path_to_results = 'C:/ShareSSD/scop/best_results/'
path_to_results = 'C:/ShareSSD/scop/best_results_combined/'
path_to_tables = 'C:/ShareSSD/scop/tables_combined/table'
path_to_weights = 'C:/ShareSSD/scop/best_weights/'

for spl in ['a.1', 'a.3', 'b.2']:
    for alg in ['complete','average','kmedoids']:

        data = []
        labels = [] 
        values = []
        weights = []

        for filename in os.listdir(path_to_results):
            if alg in filename and spl in filename:

                parsed = filename.split('_')
                i = 2
                measure1 = parsed[i]
                if 'rmsd' in measure1:
                    lab1 = 'RMSD'
                elif 'gdt' in measure1:
                    i += 1
                    if '2' in parsed[i]:
                        lab1 = 'GDT-HA'
                        measure1 = 'gdt_2'
                    else:
                        lab1 = 'GDT-TS'
                        measure1 = 'gdt_4'
                elif 'tm' in measure1:
                    lab1 = 'TM-Score'
                elif 'maxsub' in measure1:
                    lab1 = 'MaxSub'

                i += 1
                measure2 = parsed[i]
                if 'rmsd' in measure2:
                    lab2 = 'RMSD'
                elif 'gdt' in measure2:
                    i += 1
                    if '2' in parsed[i]:
                        lab2 = 'GDT-HA'
                        measure2 = 'gdt_2'
                    else:
                        lab2 = 'GDT-TS'
                        measure2 = 'gdt_4'
                elif 'tm' in measure2:
                    lab2 = 'TM-Score'
                elif 'maxsub' in measure2:
                    lab2 = 'MaxSub'

                with open(path_to_weights+alg+'_'+spl+'_'+measure1+'_'+measure2, 'r') as fp2:

                    values2 = []
                    line = fp2.readline()
                    while line:
                        values2.append(round(float(str(line).strip().split()[0]),2))
                        line = fp2.readline()


                w1 = round(float(parsed[-3]),2)
                weights.append(w1)
                #w2 = round(float(parsed[-3]),2)

                label = lab1+' '+lab2

                labels.append(label)

                values.append(str(min(values2))+','+str(max(values2)))
                
                # read results
                with open(path_to_results+filename,'r') as fp:
                    line = fp.readline()
                    while line:
                        # start reading metrics
                        if 'Weights:' in line:
                            i = 0
                            #print(line)   
                            #values.append(w1)
                            #values.append(w2)

                            while i < 6: #6 metrics
                                line = fp.readline()
                                num = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)]
                                values.append(num[0])
                                i += 1
                                #print(line)   
                        line = fp.readline()
                    data.append(values)
                    values = []

        #print(reference_value)

        columns = ('W1', 'Homogeneity', 'Completeness', 'V-measure', 'AMI', 'Calinski-Harabasz', 'Silhouette')
        rows = labels

        plt.axis('off')

        # Add a table at the bottom of the axes
        the_table = plt.table(cellText=data,
                            rowLabels=rows,
                            rowColours=None,
                            colLabels=columns,
                            cellLoc='center',
                            loc='center')

        plt.savefig(path_to_tables+alg+spl+'combinednocolor.jpeg', format='jpeg', bbox_inches="tight", dpi=300)

