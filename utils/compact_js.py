#!/usr/bin/python
# -*- coding: utf-8 -*-

from sys import argv
from os import listdir,linesep
from os.path import dirname, join, realpath
from jsmin import jsmin

current_dir = join(join(dirname(dirname(realpath(argv[0]))),"static"),"js")
skip = ("rhp.js",)
for i in listdir(join(current_dir,"dev")):
    if i[-3:]==".js" and i not in skip:
        infile  = open(join(current_dir,"dev",i),"r")
        outfile = open(join(current_dir,i),"w")
        outfile.write(jsmin(infile.read()).replace("\n",""))
        infile.close()
        outfile.close()
        print " >>> %s compacted." % i
