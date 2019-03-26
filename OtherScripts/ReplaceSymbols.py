


import os

path = 'C:/ShareSSD/scop/kernels/'
for filename in os.listdir(path):
    parsed = str(filename).replace('.jpeg','').replace('_','-').replace('.','')
    os.rename(path+filename,path+parsed+'.jpeg')