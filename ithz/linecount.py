#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import listdir, getcwd
from os.path import realpath
cuenta = 0
skiplist = ("list_().py","linecount.py","pexpect.py","pxssh.py")
for i in listdir(getcwd()):
    if i[-3:]==".py" and not i in skiplist:
        lines = 0
        file = open(realpath(i),"r")
        for j in file.readlines():
            if len(j.strip())>3:
                lines += 1
        file.close()
        print i,"(",lines,"líneas )"
        cuenta +=lines
print cuenta,"líneas"
