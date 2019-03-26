
import os
import shutil 

def getBestScoresFromSingleWithSequence():

    path_to_results = 'C:/ShareSSD/scop/clustering_results_seq/'
    path_to_best = 'C:/ShareSSD/scop/best_results_with_seq/'

    maxv = 0.0
    maxv_filename = ''

    algorithms = ['complete','average','kmedoids']
    measures = ['rmsd','gdt_2','gdt_4','tm','maxsub']
    samples = ['a.1','a.3','b.2','b.3']

    for spl in samples:
        for m in measures:
            for alg in algorithms:
            
                for filename in os.listdir(path_to_results):
                    if alg in filename and m in filename and spl in filename:
                        with open(path_to_results+filename, 'r') as fp:
                            line = fp.readline()
                            while line:
                                if 'Homogeneity' in line or 'Completeness' in line or 'V-measure' in line or 'AMI' in line:
                                    current = str(line).strip().split()[1]
                                    if float(current) > float(maxv):
                                        maxv = current
                                        maxv_filename = filename
                                line = fp.readline()

                print(maxv)
                print(maxv_filename)
                shutil.copy(path_to_results+maxv_filename, path_to_best+maxv_filename)
                maxv = 0.0
                maxv_filename = ''

getBestScoresFromSingleWithSequence()