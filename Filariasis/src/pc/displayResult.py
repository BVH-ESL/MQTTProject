import argparse
import sys, os, time, datetime
import numpy as np
from matplotlib import pyplot as plt
import fnmatch

# define variable
numProcess = 5
mainProcessList = [[] for x in range(numProcess)]

path = "result/"
for file in os.listdir(path):
    if fnmatch.fnmatch(file, 'result_WAKE_RF_DEFAULT2.txt'):
        f = open(path + file, "r")
        for line in f:
            if line.split(',')[0][-1:] == 'm':
                print int(line.split(',')[0][0])
                if(int(line.split(',')[0][0]) != numProcess):
                    mainProcessList[int(line.split(',')[0][0])].append(int(line.split(',')[1]))

print mainProcessList
