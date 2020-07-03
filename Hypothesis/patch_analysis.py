'''
MIT License

Copyright (c) 2020 Bingliang Li, Bolin Cui, Yue Hu, Yuhe Zhang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import numpy as np
import matplotlib.pyplot as plt
# import sklearnBO
from scipy.optimize import curve_fit

date_commit =dict()

def readFileRows(fileadd, endver): # File address; when reach the certain version, stop collection

    file = open(fileadd, 'r', encoding='gb18030', errors='ignore')
    context = str(file.read())

    row_date_commits = list(context.split("\n\"\n")) # Turn each pair of date & commit to an element of list

    for d_c in row_date_commits:
        if d_c[29:] == endver: # When reach tag v5.6, quit the loop(the log file start with v5.7)
            return None
        if len(d_c) <= 10: # Ignore blank and exceptional line
            pass
        else:
            if not d_c[1:11] in date_commit.keys():
                date_commit[d_c[1:11]] = [d_c[29:]] # Set key(date) and value(commit)
            else:
                date_commit[d_c[1:11]].append(d_c[29:]) # If key(date) exists, append the value(commit)


def func(x, a, b, c):
    return a * np.exp(-b * x) + c

readFileRows('log_cs_B.csv', 'Linux 5.6')

date_count = dict()

for k, v in date_commit.items(): # Get dict of {date:patch amount} pair. Actuall this is highly inaccurate
    count = 0
    for commit in v:
        if 'fix' or 'bug' or 'patch' in v:
            count += 1
    date_count[k] = count

# Fit and draw
num_of_date = len(date_count.keys())
x = np.arange(1,num_of_date + 1)

x_labels = sorted(date_count.keys())
plt.xticks(x,x_labels, rotation=300)
y = list(reversed(date_count.values()))
plt.scatter(x,y)

popt, pcov = curve_fit(func, x, y)
y2 = [func(i, popt[0],popt[1],popt[2]) for i in x]
plt.plot(x, y2)
plt.show()
