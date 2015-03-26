#!/usr/bin/python
# -*- coding: utf-8 -*-

from sys import argv
from os import listdir,linesep
from os.path import dirname, join,realpath

inComment = False
#inSwitch = False
#inSwitchLevel = 0
#inSwitchLevelMinimum = -1

def compact(line):
    #global inComment, inSwitch, inSwitchLevel, inSwitchLevelMinimum
    global inComment
    
    if inComment and "*/" in line:
        line = line[line.index("*/")+2:]
        inComment=False
                
    if not inComment:
        while "/*" in line:
            if "*/" in line:
                line = line[:line.index("/*")]+line[line.index("*/")+2:]
            else:
                line = line[line.index("/*"):]
                inComment = True
                break
            
    if not inComment:
        if "//" in line:
            line = line[:line.index("//")]
                    
    if not inComment:
        '''
        if not inSwitch and "switch" in line:
            print "inswitch %s" % line,
            inSwitch = True
            inSwitchLevel = 0
            inSwitchLevelMinimum = -1
            
        if inSwitch:
            if "{" in line:
                inSwitchLevel += 1
                if inSwitchLevelMinimum == -1:
                    inSwitchLevelMinimum = 0
                
            if "}" in line:
                inSwitchLevel -= 1
            print inSwitchLevel
            if inSwitchLevel == inSwitchLevelMinimum:
                print "outswitch"
                inSwitch = False
        '''
        line = line.strip()
        '''
        if inSwitch:
            line += linesep
        '''
    else:
        line = ""
    
    return line

current_dir = join(join(dirname(dirname(realpath(argv[0]))),"static"),"style")
skip = ()
for i in listdir(join(current_dir,"dev")):
    if i[-4:]==".css" and i not in skip:
        infile  = open(join(current_dir,"dev",i),"r")
        outfile = open(join(current_dir,i),"w")
        outfile.writelines([compact(j) for j in infile.readlines()]+["\n",])
        infile.close()
        outfile.close()
        print " >>> %s compacted." % i
