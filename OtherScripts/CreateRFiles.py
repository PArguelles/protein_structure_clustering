
import os

measures = ['rmsd','gdt_2','gdt_4','tmscore_high','tmscore_low','maxsub_high','maxsub_low','seq_id']

path = 'C:/ShareSSD/scop2/data/values_a.1._'
path2 = 'C:/ShareSSD/scop2/data/kernel_a.1._'

counter = 0

for measure in measures:
    print(measure)
    with open(path+measure, 'r') as fp:
        with open(path2+measure, 'w') as fp2:
            line = fp.readline()
            while line and 'END' not in line:
                parsed = str(line).strip().split(' ')[2]
                fp2.write(parsed+'\n')
                line = fp.readline()
        counter += 1