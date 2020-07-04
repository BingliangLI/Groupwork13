#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
__author__ = YueHu
__coptright__ = Copyright 2020, YueHu
__license__ = GPL
__version__ = 0.2
__maintainer__ = YueHu
__email__ = "yhu18@lzu.edu.cn"
__status__ = Done
"""

import os, re, sys, argparse,subprocess
from subprocess import Popen,PIPE,DEVNULL
from datetime import datetime as dt

class InvalidRevError(Exception):
    pass

class InvalidRangeError(Exception):
    pass

#sys,argv only provides simple parameter parsing, while Argparse makes it easierto write a
#user-friendly command-line interface.It requires the program to process the parameter
#definition, argparse will parse sys. Argv better.The Argparse module also automatically
#generates help and prompts for incorrect input parameters.
def getArgv():
    parser = argparse.ArgumentParser(description="The count of kernel submissions")
    parser.add_argument('-v','--rev',type=str,required=True)
    parser.add_argument('-r','--rev_range',type=int,required=True)
    parser.add_argument('-c','--cumulative', default=False,help="Cumulative arguments")
    args = parser.parse_args()
    return args

class Counter:
    def __init__(self,args):
        self.rev = args.rev
        self.rev_range = args.rev_range
        self.cumulative = args.cumulative

    #Get a count of all commits
    def get_commit_cnt(self,git_cmd):
        raw_counts = git_cmd.communicate()[0]
        # if we request something that does not exist -> 0
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)

    #Find the commit time based on the label and convert it to hours
    def get_tag_days(self,git_cmd, base):
        SecPerHour = 3600
        try:
            seconds = git_cmd.communicate()[0]
            print(base)
            print(seconds)
            return ((int(seconds)-base)//SecPerHour)
        except InvalidRangeError:
            print("Invalid Range")

    #Fork a child process through the subprocess package in the standard library and run an external program.
    #Using a try...Except...To check.
    def command(self,rev1,rev2):
        try:
            gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
            gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
            git_rev_list = subprocess.Popen(gitcnt, stdout=PIPE, stderr=DEVNULL, shell=True)
            git_tag_date = subprocess.Popen(gittag, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
            return git_rev_list, git_tag_date
        except InvalidRevError:
            print("Invalid Revesion")

    #~/git/linux-stable$ git log -1 --pretty=format:"%ct" v4.4
    # v44=1452466892`
    def base(self):
        try:
            gittag = "git log -1 --pretty=format:\"%ct\" " + self.rev
            git_base_date = subprocess.Popen(gittag, stdout=PIPE, stderr=DEVNULL, shell=True)
            base = git_base_date.communicate()[0]
            return int(base)
        except InvalidRevError:
            print("Invalid Revesion")

    def run(self):
        rev1 = self.rev
        try:
            for sl in range(1, self.rev_range + 1):
                rev2 = self.rev + "." + str(sl)
                git_rev_list, git_tag_date = self.command(rev1,rev2)
                commit_cnt = self.get_commit_cnt(git_rev_list)
                if self.cumulative == 0:
                    rev1 = rev2
                if commit_cnt:
                    base = self.base()
                    days = self.get_tag_days(git_tag_date, base)
                    print("%d %d %d" % (sl,days,commit_cnt))
                else:
                    break
        except IndexError:
            print("Invalid Range")

if __name__ == "__main__":
    args = getArgv()
    counter = Counter(args)
    print("lv hour bugs")
    counter.run()
    print("#sublevel commits %s stable fixes" % args.rev)
    
