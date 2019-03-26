



import os

def getStructureList(sample):
    path_to_sample = 'C:/ShareSSD/scop/samples/sample_'+sample
    path_to_structures = 'C:/ShareSSD/scop/samples/sample_structures_'+sample
    path_to_location = 'C:/ShareSSD/scop/structures/'

    with open(path_to_sample, 'r') as fp:
        with open(path_to_structures, 'w') as fp2:

            line = fp.readline()
            while line:
                print(line)
                fp2.write(path_to_location+str(line).strip().split()[0]+'\n')

                line = fp.readline()


