#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# get the commit count per sublevel pointwise or cumulative (c)
# arguments is the tag as displayed by git tag and the number
# of sublevels to be counted. If count is out of range for a
# specific sublevel it will terminate the loop
#
# no proper header in this file
# no legal/copyright ...OMG !
#
# things to cleanup:
# restructure the code - use of functions
# error handling ...where is the try..except ?
# argument handling: you can do better right ?
# documentation: once you understand it - fix the docs !
# transform it into a class rather than just functions !


"""
MIT License Copyright (c) 2020 Permission is hereby granted, free of charge,
to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

#__author__ = Bingliang Li, Bolin Cui, Yue Hu, Yuhe Zhang
#__copyright__ = "Lanzhou Universaty, 2020"
#__license__   = "GPL V2 or later"
#__version__   = 0.2


import sys, os, argparse
from re import findall
from subprocess import Popen, DEVNULL, PIPE

parser = argparse.ArgumentParser()
parser.add_argument("revision", help="git revision")
parser.add_argument("range",type=int, help="input number")
parser.add_argument("accumulation")
args = parser.parse_args()
li = [args.revision, args.range, args.accumulation]

def get_commit_cnt(self, git_cmd):
    cnt = 0
    try:
        raw_counts = git_cmd.communicate()[0]
        if raw_counts == 0:
            raise ContentException
    except ContentException as e:
        print(e)
        sys.exit(2)
# if we request something that does not exist -> 0
    cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
    return len(cnt)


def get_tag_days(self, git_cmd, base):
    t = 3600
    try:
        seconds = git_cmd.communicate()[0]
        if seconds == 0:
            raise ContentException
    except ContentException as e:
        print(e)
        sys.exit(2)
    return ((int(seconds)-base))//t

def gitcntData(kernelVision, repo):
    cmd = ["git rev-list", "--pretty=format:\"%ai\" "]
    p = Popen(cmd,cwd=repo, stout=PIPE, shell=True)
    data, res = p.communicate()
    return data.decode()

def gittagData(kernelVision, repo):
    cmd = ["git -P ","log", "-1", "--pretty=format:"%ct""]
    p = Popen(cmd,cwd=repo, stout=PIPE, shell=True)
    data, res = p.communicate()
    return data.decode()

class ContentException(BaseException):
    def __str__(self):
        excep = 'Found nothing, please check again!'
        return excep

class Log_Collect:
    def __init__(self, li):
        self.rev = li[1]
        cumulative = 0
        if len(li) == 3:
            if (li[2] == "c"):
                cumulative = 1
            else:
                print("Dont know what you mean with %s" % li[3])
                sys.exit(-1)
        rev_range = int(li[1])
        self.git(cumulative, rev_range)


    # setup and fill in the table
    # print("#sublevel commits %s stable fixes" % rev)
    # print("lv hour bugs") #tag for R data.frame

    # base time of v4.1 and v4.4 as ref base
    # fix this to extract the time of the base commit
    # from git !
    #
    # hofrat@Debian:~/git/linux-stable$ git log -1 --pretty=format:"%ct" v4.4
    # 1452466892

    def git(self, cumulative, rev_range):
        rev1 = li[0]
        v44 = 1452466892
        rev_range = li[1]
        for sl in range(1,rev_range+1):
            # It seems that from v4.* there aren't v*.*.* any more
            # At least I can't get it
            # So fix the code
            if sl < int(rev1[-1]):
                continue
            rev2 = self.rev[0:2] + "." + str(sl)
            print(rev2)
        
            gitcnt = gitcntData(rev1 + "..." + rev2, "/home/hofrat/git/linux-stable")
            gittag = gittagData(rev2, "/home/hofrat/git/linux-stable")
            git_rev_list = subprocess.Popen(gitcnt, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
            commit_cnt = get_commit_cnt(git_rev_list)
            print(str(commit_cnt))
            print(cumulative)
            if cumulative == 0:
                rev1 = rev2
            # if get back 0 then its an invalid revision number
            if commit_cnt:
                git_tag_date = subprocess.Popen(gittag, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
                days = self.get_tag_days(git_tag_date, v44)
                print("%d %d %d" % (sl,days,commit_cnt))
            else:
                break


if __name__ == '__main__':
    collecter = Log_Collect(sys.argv)
