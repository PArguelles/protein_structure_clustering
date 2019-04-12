

x = 'C:/Users/pedro.arguelles/Desktop/Repos/oi-mua/src/OI.FFM.InboundServices/pas/'

y = '/'.join(str(x).split('/')[7:])
y = str(y).replace('/','\\')
print(y)