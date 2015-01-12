#!/usr/bin/env python
#-*- encoding:utf8 -*-

import argparse
import traceback
import xml.etree.ElementTree as ET

# generate html file
def genhtml(root, fmt, layer):
    if root.tag == 'interface':
        print("<!DOCTYPE html>")
        print((" " * fmt * layer) + "<html><head>")
        print((" " * fmt * layer) + "<link rel=\"stylesheet\" type=\"text/css\" href=\"mystyle.css\" />")
        print((" " * fmt * layer) + "</head>")
        print((" " * fmt * layer) + "<body>")
        for child in root:
            genhtml(child, fmt, layer + 1)
        print((" " * fmt * layer) + "</body></html>")
    elif root.tag == 'object':
        if root.attrib['class'] == 'GtkGrid':
            '''
            for prop in root.findall('property'):
                print("%s=%s" % (prop.attrib['name'], prop.text))
            '''
            mylist = [[None for col in range(20)] for row in range(20)]
            col = 0
            row = 0
            for child in root.findall('child'):
                for packing in child.findall('packing'):
                    for prop in packing.findall('property'):
                        if prop.attrib['name'] == 'left_attach':
                            row = int(prop.text)
                        elif prop.attrib['name'] == 'top_attach':
                            col = int(prop.text)
                mylist[col][row] = child
            for col in range(20):
                print((" " * fmt * (layer + 1)) + "<div id=\"top\">")
                for row in range(20):
                    child = mylist[col][row]
                    if child is not None:
                        print((" " * fmt * (layer + 1)) + "<div id=\"left\">")
                        for obj in child.findall('object'):
                            if obj.attrib['class'] == 'GtkButton':
                                print((" " * fmt * (layer + 2)) + "<form>")
                                # get button label
                                label = ''
                                for prop in obj.findall('property'):
                                    if prop.attrib['name'] == 'label':
                                        label = prop.text
                                        break
                                print((" " * fmt * (layer + 2)) + "<input type=\"button\" value=\"%s\">" % label)
                                print((" " * fmt * (layer + 2)) + "</form>")
                            else:
                                genhtml(obj, fmt, layer + 1)
                        print((" " * fmt * (layer + 1)) + "</div>")
                print((" " * fmt * (layer + 1)) + "</div>")
        elif root.attrib['class'] == 'GtkBox':
            # checking orientation vertical?
            orientation = 'H'
            for prop in root.findall('property'):
                if prop.attrib['name'] == 'orientation':
                    if prop.text == 'vertical':
                        orientation = 'V'
            col = 0
            mylist = [None for col in range(20)]
            for child in root.findall('child'):
                for packing in child.findall('packing'):
                    for prop in packing.findall('property'):
                        if prop.attrib['name'] == 'position':
                            col = int(prop.text)
                mylist[col] = child
            for col in range(20):
                child = mylist[col]
                if child is not None:
                    if orientation == 'H':
                        print((" " * fmt * (layer + 1)) + "<div id=\"left\">")
                    else:
                        print((" " * fmt * (layer + 1)) + "<div id=\"top\">")
                    for obj in child.findall('object'):
                        if obj.attrib['class'] == 'GtkButton':
                            print((" " * fmt * (layer + 2)) + "<form>")
                            # get button label
                            label = ''
                            for prop in obj.findall('property'):
                                if prop.attrib['name'] == 'label':
                                    label = prop.text
                                    break
                            print((" " * fmt * (layer + 2)) + "<input type=\"button\" value=\"%s\">" % label)
                            print((" " * fmt * (layer + 2)) + "</form>")
                        else:
                            genhtml(obj, fmt, layer + 1)
                    print((" " * fmt * (layer + 1)) + "</div>")
        else:
            for child in root:
                genhtml(child, fmt, layer)
    else:        
        for child in root:
            genhtml(child, fmt, layer)

# ###### MAIN #####
if __name__ == '__main__':
    # beautiful print html
    layer = 0
    fmt = 2
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
    genhtml(root, fmt, layer)
