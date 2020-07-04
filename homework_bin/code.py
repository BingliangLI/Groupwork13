import numpy as np
import pandas as pd
import csv
from pandas.core.frame import DataFrame
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

tmp_lst = []
with open('data_v4.4.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        tmp_lst.append(row)
df = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0])
data = df["diff"].tolist()
numbers = list(map(int, data))

for num_bins in range(2,31): #we require bin from 2 to 30
    n, bins, patches = plt.hist(numbers, num_bins, density=1, facecolor='blue', alpha=0.5)
    plt.xlabel('diff') 
    plt.ylabel('Probability')
    plt.title(r'Histogram')
    plt.subplots_adjust(left=0.15)
    plt.savefig("%d.png"%(num_bins))
    plt.cla()
