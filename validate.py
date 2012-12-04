#!/usr/bin/env python
"""
Validate html files for techint group website.
"""
import glob
import pdb
import sys
import xml.etree.ElementTree as ET

from optparse import *

# ---------------------------------------------------------------------------
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
    
    fash = {}
    fash['filename'] = filename
    fash['root'] = t._root

    check_for_meta(fash)
    check_structure(fash)
    check_title(fash)
    check_for_csslink(fash)

# ---------------------------------------------------------------------------
def check_for_csslink(F):
    count = 0
    for item in F['root'].iter('link'):
        count += 1
    if count <= 0:
        print("%s: no link tag found in head element" % F['filename'])
    
# ---------------------------------------------------------------------------
def check_for_meta(F):
    """
    If there is a meta tag in the head element and its name is 'filetype',
    return its 'content' attribute. If no meta tag is found, complain.

    There should also be a <meta charset="utf-8"> tag as well.
    """
    ft_ok = False
    charset_ok = False
    F['filetype'] = 'unknown'
    for item in F['root'].iter('meta'):
        if item.get('name') == 'filetype':
            F['filetype'] = item.get('content')
            ft_ok = True
        elif item.get('charset') != None:
            charset_ok = True

    if not ft_ok:
        print("%s: no filetype specified. " % F['filename']
              + "Please add '<meta name=\"filetype\" content=\"<filetype>\" />'")

    if not charset_ok:
        print("%s: no charset specified. " % F['filename']
              + "Please add '<meta charset=\"utf-8\" />'")

# ---------------------------------------------------------------------------
def check_structure(F):
    lang = F['root'].get('lang')
    if lang != 'en':
        print("%s: html lang attribute should be 'en'" % (F['filename']))

    tl = []
    tl_expect = ['body', 'head']
    for child in F['root']:
        tl.append(child.tag)

    for tag in tl_expect:
        if tag not in tl:
            print("%s: %s tag not found" % (F['filename'], tag))

    for tag in tl:
        if tag not in tl_expect:
            print("%s: found extra %s tag" % (F['filename'], tag))
    
# ---------------------------------------------------------------------------
def check_title(F):
    hl = []
    for item in F['root'].iter('head'):
        hl.append(item)

    if len(hl) != 1:
        print('%s: wrong number of head elementss: %d' % (F['filename'], len(hl)))
        return
    
    tl = []
    for item in F['root'].iter('title'):
        tl.append(item)

    if (F['filetype'] == 'index') and (len(tl) != 1):
        print("%s: should have title but does not" % (F['filename']))
    elif (F['filetype'] != 'index') and (len(tl) != 0):
        print("%s: should not have title but does" % (F['filename']))
        
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    main(sys.argv)
