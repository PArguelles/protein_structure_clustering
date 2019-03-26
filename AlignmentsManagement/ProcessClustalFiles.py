
import numpy as np

def processClustalFiles(sample):

    path_to_matrix = 'C:/ShareSSD/scop/data/sequences_'+sample+'pim'
    path_to_new = 'C:/ShareSSD/scop/matrix_'+sample+'_seq'
    path_to_values = 'C:/ShareSSD/scop/values_'+sample+'_seq'

    matrix = []
    values = []

    with open(path_to_matrix, 'r') as fp:

        line = fp.readline()

        while line:

            if ':' in line:
                
                parsed = str(line).strip().split()
                parsed = [float(i) for i in parsed[2:]]

                #values for kernel estimation
                for value in parsed:
                    values.append(value)

                matrix.append(parsed)
                print(parsed[2:])
                print(line)


            line = fp.readline()
        
        final = np.matrix(matrix)
        
        print(final)
        final.dump(path_to_new)

        with open(path_to_values, 'w') as fp2:
            for value in values:
                fp2.write(str(value)+'\n')

