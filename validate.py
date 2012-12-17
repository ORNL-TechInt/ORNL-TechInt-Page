#!/usr/bin/env python2.7
"""
Validate html files for techint group website.
"""
import glob
import os
import pdb
import re
import sys

import xml.etree.ElementTree as ET
import HTMLParser

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

    verbose(o.verbose)
    
    if 1 < len(a):
        flist = a[1:]
    else:
        flist = glob.glob("*.html")

    for filename in flist:
        if verbose(): print filename
        check_file(filename)

    sys.exit(exit_value())
    
# ---------------------------------------------------------------------------
def verbose(value=None):
    global verbosity

    if value != None:
        verbosity = value
        
    try:
        rval = verbosity
    except NameError:
        verbosity = False
        rval = verbosity

    return rval

# ---------------------------------------------------------------------------
def loadfile(filename):
    f = open(filename, 'r')
    doctype = f.readline()
    xml = f.read()
    f.close()

    if "\t" in doctype or "\t" in xml:
        errmsg("%s: TAB characters detected. Please use spaces."
               % filename);
    
    tip = TIParser(filename, doctype+xml)
    tip.feed(doctype + xml)
    tip.finish()
    
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
    # check_for_csslink(fash)
    # check_deprecations(fash)
    
# # ---------------------------------------------------------------------------
# def check_deprecations(F):
#     deprecations_present = []
#     recommendations = {'b': '<strong>',
#                        'i': '<em>',
#                        'B': '<strong>',
#                        'I': '<em>',
#                        'A': '<a ...>',
#                        'LI': '<li ...>',
#                        'UL': '<ul ...>',
#                        }

#     for tag in recommendations.keys():
#         for item in F['root'].iter(tag):
#             deprecations_present.append(tag)

#     for dep in deprecations_present:
#         errmsg("%s: deprecated tag <%s> present -- consider using %s instead"
#                % (F['filename'], dep, recommendations[dep]),
#                0)
    
# ---------------------------------------------------------------------------
# def check_for_csslink(F):
#     count = 0
#     link_bad = True
#     for item in F['root'].iter('link'):
#         if item.get('rel') == 'stylesheet' and item.get('type') == 'text/css':
#             link_bad = False

#     if link_bad:
#         errmsg("%s: no stylesheet link tag found in head element" % F['filename'])
    
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
    #if head_missing:
     #   errmsg("%s: head tag not found" % (F['filename']))
    # if stray_present:
        # errmsg("%s: stray '%s' tag found" % (F['filename'], stray))

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

#     if len(hl) != 1:
#         errmsg('%s: wrong number of head elements: %d' % (F['filename'], len(hl)))
#         return
    
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
class TIParser(HTMLParser.HTMLParser):
    # -----------------------------------------------------------------------
    def __init__(self, filename="", text=""):
        """
        Initialize the object with the data and flags we'll need to
        validate the input.
        """
        if verbose(): print("TIParser.__init__")
        HTMLParser.HTMLParser.__init__(self)
        self.filename = filename
        self.text = text.split("\n")
        self.deprecations = {'b': '<strong>',
                             'i': '<em>'}
        self.doctype = "missing"
        self.head = 'missing'
        self.body = 'missing'
        self.css = 'missing'
        self.filetype = 'missing'
        self.stack = []
        
    # -----------------------------------------------------------------------
    def handle_startendtag(self, tag, attrs):
        """
        We'll use this catch <script/>, which doesn't work for loading
        javascripts.
        """
        if verbose(): print("TIParser.handle_startendtag(self, %s, %s)"
                            % (tag, attrs))

        if tag == 'script':
            self.errmsg("<script/> does not load javascript effectively."
                        + " Please use '<script ... > </script>' instead.")
        self.standard_tag_checks(tag, attrs)

    # -----------------------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        """
        At the very first tag, we should have already seen a
        <!doctype...>, so if not, we complain. Once we've complained
        once, we change the string in self.doctype so we won't report
        the missing <!doctype> again.

        Next, we check for unquoted attributes, deprecated tags, and
        uppercase tags.
        """
        if verbose(): print("TIParser.handle_starttag(self, %s, %s)"
                            % (tag, attrs))
        self.standard_tag_checks(tag, attrs)
        if 1 == len(self.stack) and tag != 'head' and tag != 'body':
            self.errmsg("stray '%s' tag found" % tag)
        self.stack.append(tag)
        
    # -----------------------------------------------------------------------
    def handle_endtag(self, tag):
        if verbose(): print("TIParser.handle_endtag(self, %s)" % (tag))
        if tag == 'head':
            self.head = 'closed'
        if tag == 'body':
            self.body = 'closed'
        (line, offset) = self.getpos()
        etag = self.text[line-1][offset:]
        pop = self.stack.pop()
        if tag != pop:
            errmsg("%s does not match %s" % (tag, pop))
        
    # -----------------------------------------------------------------------
    def handle_data(self, data):
        if verbose(): print("TIParser.handle_data(self, '%s')" % (data))
        pass

    # -----------------------------------------------------------------------
    def handle_decl(self, decl):
        if verbose(): print("TIParser.handle_decl(self, '%s')" % (decl))
        if 'doctype' in decl.lower():
            self.doctype = "present"
            
    # -----------------------------------------------------------------------
    def handle_head(self, tag, attrs):
        self.head = 'open'
        
    # -----------------------------------------------------------------------
    def handle_body(self, tag, attrs):
        self.body = 'open'
        
    # -----------------------------------------------------------------------
    def handle_link(self, tag, attrs):
        if ('rel', 'stylesheet') in attrs and ('type', 'text/css') in attrs:
            self.css = "present"
            
    # -----------------------------------------------------------------------
    def handle_meta(self, tag, attrs):
        if ('name', 'filetype') in attrs:
            if attrs[1][0] == 'content':
                self.filetype = 'present'
        
    # -----------------------------------------------------------------------
    def handle_named_tag(self, tag, attrs):
        d = dir(self)
        mname = 'handle_%s' % tag
        if mname in dir(self):
            getattr(self, mname)(tag, attrs)

    # -----------------------------------------------------------------------
    def catch_unquoted_attrs(self, text, attrlist):
        for tup in attrlist:
            xp = "%s=\"%s\"" % (tup)
            if xp not in self.unescape(text):
                (line, offs) = self.getpos()
                self.errmsg("unquoted attribute in '%s'" % (text))
                
    # -----------------------------------------------------------------------
    def catch_deprecated_tags(self, tag):
        if tag in self.deprecations.keys():
            (line, offs) = self.getpos()
            self.errmsg("Tag '<%s>' is deprecated. Consider using %s instead"
                        % (tag, self.deprecations[tag]),
                        0)

    # -----------------------------------------------------------------------
    def catch_uppercase_tags(self, tag):
        raw = self.get_starttag_text()
        q = re.search("<\s*(\w+)\s*", raw)
        txt = q.groups()[0]
        for chr in txt:
            if chr.isupper():
                self.errmsg("Tags like '<%s>' containing uppercase letters are deprecated"
                            % (txt))
                break
                
    # -----------------------------------------------------------------------
    def errmsg(self, msg, exit_val = 1):
        """
        Format an error message -- filename, location in file, and
        message. Optionally, the caller can set the exit value to be
        used when the process terminates. By default that's 1,
        indicating an issue but the caller can set exit_val to 0 for a
        warning that won't prevent downstream processing.
        """
        (line, offset) = self.getpos()
        fmsg = "%s[%d,%d]: %s" % (self.filename, line, offset, msg)
        print(fmsg)
        exit_value(exit_val)
        
    # -----------------------------------------------------------------------
    def finish(self):
        """
        This is the last method called for an HTML file so we can
        report required tags that were never seend, etc.
        """
        if verbose(): print("TIParser.finish()")
        for tag in ['head', 'body']:
            if getattr(self, tag) == 'missing':
                self.errmsg('%s tag not found' % (tag))
            elif getattr(self, tag) != 'closed':
                self.errmsg('%s tag not complete' % (tag))

        if self.filetype == 'missing':
            self.errmsg("Filetype missing. Please add "
                        + "'<meta name=\"filetype\" content=\"[ft]\" /> "
                        + "where 'ft' is one of 'about', 'proj', 'member', "
                        + "'contact', 'jobs', 'nav', 'pub', or 'software' "
                        + "in the <head> section.")

        if self.css == 'missing':
            self.errmsg("No CSS link found in <head>. Please add at least "
                        + "<link rel='stylesheet' type='text/css' "
                        + "href='techint_f.css' />")

    # -----------------------------------------------------------------------
    def standard_tag_checks(self, tag, attrs):
        """
        This method is called by both handle_starttag() and
        handle_startendtag(). It represents the common code that needs
        to be run for each start tag, whether it contains text before
        the end tag or the end is included with the start tag.

        At the very first tag, we should have already seen a
        <!doctype...>, so if not, we complain. Once we've complained
        once, we change the string in self.doctype so we won't report
        the missing <!doctype> again.

        The method handle_named_tag() looks to see whether a method
        named handle_<tagname>() exists or not. If it does,
        handle_named_tag() will call it with the tag and attrs list as
        arguments. This allows makes it quick and easy to add handling
        for a specific tag.

        Next, we check for unquoted attributes, deprecated tags, and
        uppercase tags.
        """
        # if verbose(): print("TIParser.standard_tag_checks(self, %s, %s)"
        #                     % (tag, attrs))
        if self.doctype == "missing":
            self.errmsg("A <!doctype ...> is required at the top of the file")
            self.doctype = "reported"

        self.handle_named_tag(tag, attrs)
        self.catch_unquoted_attrs(self.get_starttag_text(), attrs)
        self.catch_deprecated_tags(tag)
        self.catch_uppercase_tags(tag)
        
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    main(sys.argv)
