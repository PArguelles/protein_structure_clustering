import numpy as np
import matplotlib.pyplot as plt
import os
import re

#path_to_results = 'C:/ShareSSD/scop/best_results/'
path_to_results = 'C:/ShareSSD/scop/best_results_combined/'
path_to_tables = 'C:/ShareSSD/scop/tables_combined/table-'

for spl in ['a.1', 'a.3', 'b.2', 'b.3']:
    for alg in ['complete','average','kmedoids']:

        data = []
        labels = [] 
        values = []

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
                    else:
                        lab1 = 'GDT-TS'
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
                    else:
                        lab2 = 'GDT-TS'
                elif 'tm' in measure2:
                    lab2 = 'TM-Score'
                elif 'maxsub' in measure2:
                    lab2 = 'MaxSub'

                w1 = round(float(parsed[-2]),2)
                #w2 = round(float(parsed[-3]),2)

                label = lab1+' '+lab2

                labels.append(label)
                with open(path_to_results+filename,'r') as fp:
                    line = fp.readline()
                    while line:
                        # start reading metrics
                        if 'Weights:' in line:
                            i = 0
                            #print(line)   
                            values.append(w1)
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

        # Read RMSD reference values
        reference_values = ['-','-']
        with open('C:/ShareSSD/scop/clustering_results_single_matrix/'+alg+'_'+spl+'._rmsd_rmsd') as fp:
            line = fp.readline()
            while line:
                i = 0
                if '# Cluster evaluation:' in line:
                    while i < 6:
                        line = fp.readline()
                        num = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)]
                        reference_values.append(num[0])
                        i += 1
                line = fp.readline()

        data.append(reference_values)
        rows.append('RMSD')

        # Add a table at the bottom of the axes
        the_table = plt.table(cellText=data,
                            rowLabels=rows,
                            rowColours=None,
                            colLabels=columns,
                            cellLoc='center',
                            loc='center')


        # Color matrix
        for i,j in the_table._cells:
            print(str(the_table._cells[(i, j)]._text.get_text()))
            if i > 0 and j > 1:
                if float(the_table._cells[(i, j)]._text.get_text()) > float(the_table._cells[(len(data), j)]._text.get_text()):
                    the_table._cells[(i, j)]._text.set_color('green')
                if float(the_table._cells[(i, j)]._text.get_text()) == float(the_table._cells[(len(data), j)]._text.get_text()):
                    the_table._cells[(i, j)]._text.set_color('blue')
                if float(the_table._cells[(i, j)]._text.get_text()) < float(the_table._cells[(len(data), j)]._text.get_text()):
                    the_table._cells[(i, j)]._text.set_color('red')

        plt.savefig(path_to_tables+alg+'-'+spl+'combined.jpeg', format='jpeg', bbox_inches="tight", dpi=300)

