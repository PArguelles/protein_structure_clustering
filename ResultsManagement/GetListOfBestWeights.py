


import os

path_to_best = 'C:/ShareSSD/scop/best_results_combined_test/'
path_to_results = 'C:/ShareSSD/scop/best_weights/'

combinations = [('rmsd','gdt_2'),('rmsd','gdt_4'),
                ('rmsd','maxsub'),('rmsd','tm'),
                ('gdt_2','gdt_4'),('gdt_2','maxsub'),
                ('gdt_2','tm'), ('gdt_4','maxsub'),
                ('gdt_4','tm'), ('maxsub','tm')]

for spl in ['a.1','a.3','b.2']:
    for alg in ['complete','average','kmedoids']:
        for m1, m2 in combinations:
            with open(path_to_results+alg+'_'+spl+'_'+m1+'_'+m2, 'w') as nf:
                for filename in os.listdir(path_to_best):
                    if spl in filename and alg in filename and m1 in filename and m2 in filename:
                        parsed = str(filename).strip().split('_')
                        w1 = round(float(parsed[-3]),2)
                        nf.write(str(w1)+'\n')
            
            with open(path_to_results+alg+'_'+spl+'_'+m1+'_'+m2, 'r') as fp:

                values = []
                line = fp.readline()
                while line:
                    values.append(round(float(str(line).strip().split()[0]),2))
                    line = fp.readline()

                print(min(values))
                print(max(values))
                print(values)
