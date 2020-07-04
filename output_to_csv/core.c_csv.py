# /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Homework in git.pdf:
Call it from a subprocess writing the output to a pipe
Collect the output from the pipe
Arrange the output into a indexample data array
Write the entire record to a file
"""

__author__ = "Group No.13"
__copyright__ = "Copyright 2020, Lanzhou University , China"
__license__ = "GPL"
__version__ = "0.2"


from subprocess import Popen, PIPE
import csv


class QueryFile(object):
    def __init__(self, fileName, repo):
        self.fileName = fileName
        self.repo = repo

    def query(self, kernelRange='v3.0..HEAD'):
        cmd = ["git", "-P", "log", "--stat", "--oneline", "--follow", kernelRange, self.fileName]
        p = Popen(cmd, cwd=self.repo, stdout=PIPE)
        data = p.communicate()[0]
        return data.decode("utf-8").split("\n")

    def savecsv(self, save_path):
        with open(save_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            result = self.query()# After the line drop is removed, the result is a list with no content in the last element of the list.Git's one-line output is divided into three elements.
            for i in range(int((len(result) - 1) / 3)):
                author = result[3 * i].split(' ')[0]
                operation = ' '.join(result[3 * i].split(' ')[1:])
                detail = result[3 * i + 2].split(' ')
                one_row = [i+1,author,operation,detail]
                writer.writerow(one_row)  # write into a csv


if __name__ == '__main__':
    file = QueryFile("kernel/sched/core.c", r"D:\linux2\linux-stable")
    file.query('v5.0..HEAD')
    file.savecsv('change_of_corec.csv')
