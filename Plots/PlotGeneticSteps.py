
import random
import numpy as np
from numpy import ma
import matplotlib.pyplot as plt
import re

sample = 'a.1.'
algorithm = 'complete'

NGEN = 30

combinations = [('rmsd','gdt_2'),('rmsd','gdt_4'),
                ('rmsd','maxsub'),('rmsd','tm'),
                ('gdt_2','gdt_4'),('gdt_2','maxsub'),
                ('gdt_2','tm'), ('gdt_4','maxsub'),
                ('gdt_4','tm'), ('maxsub','tm')]

labels = ['RMSD GDT-HA', 'RMSD GDT-TS', 'RMSD MAXSUB', 'RMSD TM-SCORE',
            'GDT-HA GDT-TS', 'GDT-HA MAXSUB', 'GDT-HA TM-SCORE',
            'GDT-TS MAXSUB', 'GDT-TS TM-SCORE', 'MAXSUB TM-SCORE']

internals_x = []
internals_y = []

for m1, m2 in combinations:
    print(m1+' '+m2)

    # read respective files from genetic algorithm
    #with open('C:/ShareSSD/scop/tests/complete_a.1._rmsd_gdt_2', 'r') as fp:
    with open('C:/ShareSSD/scop/genetic_results_pair/gen_'+algorithm+'_'+sample+'_'+m1+'_'+m2, 'r') as fp:
        x = []
        y = []

        line = fp.readline()
        while line:

            # get best individual from a generation
            #if 'Generation:' in line:
            if 'Gen' not in line:
                values = re.findall(r'-?\d+\.?\d*', line)
                x.append(float(values[0]))
                y.append(float(values[1]))

            line = fp.readline()

    internals_x.append(x)
    internals_y.append(y.sort())

    #break


plt.step(x, y, label=labels[0])
plt.step(x, y, label=labels[1])


plt.legend()

plt.xlim(0, 20)
plt.ylim(0, 100)

plt.xlabel("Generations")
plt.ylabel("AMI")

plt.xticks(np.arange(0, NGEN+1, 1.0))

plt.show()