#!/usr/bin/env python
#-*- encoding:utf8 -*-

import argparse
import traceback
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help = "xml file")
parser.add_argument("-o", "--output", help = "output file")
args = parser.parse_args()
if not args.input:
    parser.print_help()
    quit(1)

if not args.output:
    parser.print_help()
    quit(1)

try:
    tree = ET.parse(args.input)
except:
    traceback.print_exc()
    quit(1)

root = tree.getroot()
for child in root:
    print(child.tag, child.attrib)

