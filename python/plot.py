'''
Created on Apr 3, 2017

@author: quangvu
'''

import matplotlib.pyplot as plt

filename = 'traces//traces.txt'

with open(filename, 'r') as file_in:
    lines = file_in.readlines()

traces = []
for line in lines:
    traces.append([float(f) for f in line.rstrip().lstrip().split()])

plt.plot(traces[0])
plt.show()
    
