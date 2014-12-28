#!/usr/bin/env python
#-*- encoding:utf8 -*-

import argparse
import traceback
import xml.etree.ElementTree as ET

tags = {
        'property' : True,
        'packing' : True,
        'placeholder' : True,
        }

def genhtml(element):
    if element.tag == 'object':
        print(element.attrib)
        print(element.attrib['id'])
        for child in element.findall('child'):
            genhtml(child)
        print(element.attrib['id'])
    elif tags.has_key(element.tag):
        pass
    else:
        for child in element:
            genhtml(child)

if __name__ == '__main__':
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
    genhtml(root)
