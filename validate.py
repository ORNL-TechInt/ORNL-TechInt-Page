#!/usr/bin/env python
"""
   The 'index' file SHOULD have a title, other file types should NOT
"""
import glob
import pdb
import sys
import xml.etree.ElementTree as ET

from optparse import *

def main(args):
    p = OptionParser()
    p.add_option('-d', '--debug',
                 action='store_true', default=False, dest='debug',
                 help='debug')
    (o, a) = p.parse_args(args)
                 
    if o.debug: pdb.set_trace()
    
    for filename in glob.glob("*.html"):
        check_file(filename)

# ---------------------------------------------------------------------------
def check_file(filename):
    try:
        t = ET.parse(filename)
    except ET.ParseError, e:
        print("%s: (%s) %s" % (filename, type(e), str(e)))
        return
    
    I = check_for_meta(filename, t._root)
    print("%s: %s" % (filename, I))
    check_structure(filename, t._root)
    check_for_csslink(filename, t._root)

# ---------------------------------------------------------------------------
def check_for_csslink(F, R):
    count = 0
    for item in R.iter('link'):
        count += 1
    if count <= 0:
        print("%s: no link tag found in header" % F)
    
# ---------------------------------------------------------------------------
def check_for_meta(F, R):
    """
    If there is a meta tag in the header and its name is 'filetype',
    return its 'content' attribute. If no meta tag is found, complain.
    """
    count = 0
    for item in R.iter('meta'):
        count += 1
    ftype = 'unknown'
    if count <= 0:
        print("%s: no meta tag found in header" % F)
    elif item.get('name') == 'filetype':
        ftype = item.get('content')
    if 'unknown' == ftype:
        print("%s: filetype not defined." % F)
        print("    Please add '<meta name=\"filetype\" content=\"<value>\">")

    return ftype

# ---------------------------------------------------------------------------
def check_structure(F, R):
    tl = []
    tl_expect = ['body', 'header']
    for child in R:
        tl.append(child.tag)

    for tag in tl_expect:
        if tag not in tl:
            print("%s: %s tag not found" % (F, tag))

    for tag in tl:
        if tag not in tl_expect:
            print("%s: found extra %s tag" % (F, tag))
    
if __name__ == '__main__':
    main(sys.argv)
