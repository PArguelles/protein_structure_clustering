
import numpy as np
import matplotlib.pyplot as plt
import os
import re

#path_to_results = 'C:/ShareSSD/scop/best_results/'
path_to_results = 'C:/ShareSSD/scop/best_results_combined/'
path_to_tables = 'C:/ShareSSD/scop/tables_all/table'

columns = ('Homogeneity', 'Completeness', 'V-measure', 'AMI', 'Calinski-Harabasz', 'Silhouette')

rows = ['Average - a.1', 'Average - a.3', 'Average - b.2', 'Complete - a.1', 'Complete - a.3', 'Complete - b.2', 
        'k-Medoids - a.1', 'k-Medoids - a.3', 'k-Medoids - b.2',]

data = [[0.76,0.83,0.79,0.76,12089.56,0.65], #avg a1
        [0.63,0.52,0.57,0.50,450.66,0.34],  #avg a3
        [0.63,0.50,0.56,0.30,1041.40,0.41], #avg b2
        
        [0.76,0.83,0.79,0.76,11616.35,0.67], #complete a1
        [0.66,0.50,0.57,0.48,603.32,0.3], #complete a3
        [0.65,0.51,0.57,0.50,1123.67,0.39], #complete b2
        
        [0.76,0.83,0.79,0.76,12089.56,0.65], # medoids a1
        [0.76,0.83,0.79,0.76,12089.56,0.65],
        [0.76,0.83,0.79,0.76,12089.56,0.65]]

plt.axis('off')

# Add a table at the bottom of the axes
the_table = plt.table(cellText=data,
                    rowLabels=rows,
                    rowColours=None,
                    colLabels=columns,
                    cellLoc='center',
                    loc='center')

plt.savefig('C:/ShareSSD/scop/table_all.jpeg', format='jpeg', bbox_inches="tight", dpi=300)

