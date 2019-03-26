
import os

path = 'C:/ShareSSD/scop/structures/'
path2 = 'C:/ShareSSD/scop/structures_new/'

counter = 0

for filename in os.listdir(path):
    print(counter)
    with open(path+filename, 'r') as fp:
        with open(path2+filename, 'w') as fp2:
            line = fp.readline()
            while line:
                if 'ATOM' in line:
                    parsed = str(line).strip().split()
                    if 'CA' == parsed[2]:
                        fp2.write(line)
                else:
                    fp2.write(line)
                line = fp.readline()
        counter += 1