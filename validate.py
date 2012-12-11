#!/usr/bin/env python2.7
"""
Validate html files for techint group website.
"""
import glob
import os
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
    p.add_option('-v', '--verbose',
                 action='store_true', default=False, dest='verbose',
                 help='more output')
    (o, a) = p.parse_args(args)
                 
    if o.debug: pdb.set_trace()

    for filename in glob.glob("*.html"):
        if o.verbose: print filename
        check_file(filename)

    sys.exit(exit_value())
    
# ---------------------------------------------------------------------------
def loadfile(filename):
    f = open(filename, 'r')
    doctype = f.readline()
    xml = f.read()
    f.close()

    if "\t" in doctype or "\t" in xml:
        errmsg("%s: TAB characters detected. Please use spaces."
               % filename);
    
    if '<!doctype ' not in doctype.lower():
        raise StandardError('%s: <!DOCTYPE ...> required' % filename)
    try:
        rval = ET.fromstring(xml)
    except ET.ParseError, e:
        errmsg("%s (%s) %s [%d]" % (filename, type(e), str(e), e.code))
        
    return rval

# ---------------------------------------------------------------------------
def check_file(filename):
    try:
        t = loadfile(filename)
    except Exception, e:
        errmsg(str(e))
        return
        
    fash = {}
    fash['filename'] = filename
    fash['root'] = t

    check_for_meta(fash)
    check_structure(fash)
    check_title(fash)
    check_for_csslink(fash)
    check_deprecations(fash)
    
# ---------------------------------------------------------------------------
def check_deprecations(F):
    deprecations_present = []
    recommendations = {'<b>': '<strong>', '<i>': '<em>'}
    
    for item in F['root'].iter('b'):
        deprecations_present.append("<b>")

    for item in F['root'].iter('i'):
        deprecations_present.append("<i>")
        
    for dep in deprecations_present:
        errmsg("%s: deprecated tag %s present -- consider using %s instead"
               % (F['filename'], dep, recommendations[dep]),
               0)
    
# ---------------------------------------------------------------------------
def check_for_csslink(F):
    count = 0
    link_bad = True
    for item in F['root'].iter('link'):
        if item.get('rel') == 'stylesheet' and item.get('type') == 'text/css':
            link_bad = False

    if link_bad:
        errmsg("%s: no stylesheet link tag found in head element" % F['filename'])
    
# ---------------------------------------------------------------------------
def check_for_meta(F):
    """
    If there is a meta tag in the head element and its name is 'filetype',
    return its 'content' attribute. If no meta tag is found, complain.

    There should also be a <meta charset="utf-8"> tag as well.
    """
    ft_missing = True
    charset_missing = True
    F['filetype'] = 'unknown'
    for item in F['root'].iter('meta'):
        if item.get('name') == 'filetype':
            F['filetype'] = item.get('content')
            ft_missing = False
        elif item.get('charset') != None:
            charset_missing = False

    if ft_missing:
        errmsg("%s: no filetype specified. " % F['filename']
               + "Please add '<meta name=\"filetype\" content=\"<filetype>\" />'")

    if charset_missing:
        errmsg("%s: no charset specified. " % F['filename']
               + "Please add '<meta charset=\"utf-8\" />'")

# ---------------------------------------------------------------------------
def check_structure(F):
    lang = F['root'].get('lang')
    if lang != 'en':
        print("%s: html lang attribute should be 'en'" % (F['filename']))

    body_missing = True
    head_missing = True
    stray_present = False
    stray = ''
    
    for child in F['root']:
        if child.tag == 'body':
            body = child
            body_missing = False
        elif child.tag == 'head':
            head_missing = False
        else:
            stray_present = True
            stray = child.tag

    if body_missing:
        errmsg("%s: body tag not found" % (F['filename']))
    if head_missing:
        errmsg("%s: head tag not found" % (F['filename']))
    if stray_present:
        errmsg("%s: stray '%s' tag found" % (F['filename'], stray))

    body_class_bad = True
    ctypes = ['proj', 'about', 'member', 'contact', 'conf', 'pub',
              'software', 'jobs']
    body_class = body.get('class')
    if None != body_class and 'content_frame' in body_class:
        body_class_bad = False
    if F['filetype'] in ctypes and body_class_bad:
        errmsg("%s: body should have class 'content_frame'" % (F['filename']))
        
# ---------------------------------------------------------------------------
def check_title(F):
    hl = []
    for item in F['root'].iter('head'):
        hl.append(item)

    if len(hl) != 1:
        errmsg('%s: wrong number of head elementss: %d' % (F['filename'], len(hl)))
        return
    
    tl = []
    for item in F['root'].iter('title'):
        tl.append(item)

    if (F['filetype'] == 'index') and (len(tl) != 1):
        errmsg("%s: should have title but does not" % (F['filename']))
    elif (F['filetype'] != 'index') and (len(tl) != 0):
        errmsg("%s: should not have title but does" % (F['filename']))

# ---------------------------------------------------------------------------
def errmsg(msg, status=1):
    print(msg)
    exit_value(status)
    
# ---------------------------------------------------------------------------
def exit_value(val=0):
    global xval

    try:
        rval = xval
    except:
        xval = 0

    if val != 0:
        xval = val

    return xval

# ---------------------------------------------------------------------------
if __name__ == '__main__':
    main(sys.argv)
