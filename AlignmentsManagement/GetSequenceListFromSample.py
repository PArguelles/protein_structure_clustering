

def getSequenceList(sample):
    path_to_sample = 'C:/ShareSSD/scop/samples/sample_'+sample
    path_to_structures = 'C:/ShareSSD/scop/samples/sample_structures_'+sample

    with open(path_to_sample, 'r') as fp:
        with open(path_to_structures, 'w') as fp2:

            line = fp.readline()
            while line:
                print(line)
                fp2.write(str(line).strip().split()[0]+'\n')

                line = fp.readline()


