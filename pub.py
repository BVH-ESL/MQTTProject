#!/usr/bin/env python
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-ps", "--payloadsize", required = True, help = "payloadsize)
ap.add_argument("-n", "--numpub", required = True, help = "numpub)
args = vars(ap.parse_args())

cnt = args["numpub"]
payloadsize = args["payloadsize"]
