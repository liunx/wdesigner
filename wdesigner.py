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

# translate gtk class elements to html elements
gtk2html = {
        'GtkWindow' : 'html',
        'GtkBox' : 'box',
        'GtkGrid' : 'grid',
        'GtkButton' : 'button',
        'GtkLabel' : 'label',
        }

html = {}

"""
parse glade xml file
"""
def parse(element, obj):
    try:
        if element.tag == 'object':
            objsub = {}
            ele_class = element.attrib['class']
            #print("<%s>" % gtk2html[ele_class])
            objsub['name'] = gtk2html[ele_class]
            # find properties
            for child in element.findall('property'):
                #print(child.attrib['name'], child.text)
                objsub[child.attrib['name']] = child.text
            for child in element.findall('child'):
                parse(child, objsub)
            #print("</%s>" % gtk2html[ele_class])
            obj[element.attrib['id']] = objsub
        elif tags.has_key(element.tag):
            pass
        else:
            for child in element:
                parse(child, obj)
    except:
        traceback.print_exc()
        quit(1)

"""
generate html string.
"""
layer = -1
def generate(html, fmt, layer):
    try:
        if html.has_key('name'):
            print((" " * fmt * layer) + "<%s>" % html['name'])
        for k, v in html.items():
            if isinstance(v, dict):
                generate(v, fmt, layer + 1)
        if html.has_key('name'):
            print((" " * fmt * layer) + "</%s>" % html['name'])
    except:
        traceback.print_exc()
        quit(1)

if __name__ == '__main__':
    # beautiful print html
    fmt = 4
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
    parse(root, html)
    generate(html, fmt, layer)
