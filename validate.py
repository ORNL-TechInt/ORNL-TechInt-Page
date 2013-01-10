#!/usr/bin/env python2.7
"""
Validate html files for techint group website.
"""
import glob
import os
import pdb
import re
import sys

import HTMLParser
import urllib2
import xml.sax.saxutils as xml

from optparse import *

# ---------------------------------------------------------------------------
def main(args):
    """
    Handle command line arguments, process the list of files, call sys.exit()
    """
    p = OptionParser()
    p.add_option('-d', '--debug',
                 action='store_true', default=False, dest='debug',
                 help='debug')
    p.add_option('-w', '--w3c',
                 action='store_true', default=False, dest='w3c',
                 help='send file to validator.w3.org')
    p.add_option('-r', '--rm',
                 action='store_true', default=False, dest='passrm',
                 help='rm validation output on pass')
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
        if o.w3c:
            w3c_validate(filename)
        else:
            check_file(filename)

    sys.exit(exit_value())

# ---------------------------------------------------------------------------
def check_file(filename):
    """
    Load the contents of the file, instantiate a parser, and feed it
    the input data.
    """
    f = open(filename, 'r')
    html = f.read()
    f.close()

    tip = TIParser(filename, html)
    tip.feed(html)
    tip.finish()
    
# ---------------------------------------------------------------------------
def exit_value(val=0):
    """
    Record the exit value to be used when the process terminates.
    """
    global xval

    try:
        rval = xval
    except:
        xval = 0

    if val != 0:
        xval = val

    return xval

# ---------------------------------------------------------------------------
def verbose(value=None):
    """
    Cache and return the value of the -v option.
    """
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
def w3c_validate(filename):
    """
    For index.html, the validation URL is http://validator.w3.org/check?uri=http%3A%2F%2Fusers.nccs.gov%2F~tpb%2Ftechint_olcf%2Findex.html&charset=%28detect+automatically%29&doctype=Inline&group=0&user-agent=W3C_Validator%2F1.3
    """
    entities = {':': '%3a',
                '/': '%2F',
                '(': '%28',
                ')': '%29'}
    validator = "http://validator.w3.org"
    host = "http://users.nccs.gov/"
    path = "~tpb/techint"
    uri = xml.escape("uri=%s%s/%s" % (host, path, filename), entities)
    charset = xml.escape("charset=(detect+automatically)", entities)
    doctype = "doctype=Inline"
    group = "group=0"
    agent = xml.escape("user-agent=W3C_Validator/1.3", entities)
    
    url = "%s/check?%s&%s&%s&%s&%s" % (validator, uri, charset, doctype,
                                       group, agent)
    # print url

    page = urllib2.urlopen(url)
    text = page.readlines()
    vname = "validation_%s" % filename
    h = open(vname, 'w')
    h.writelines(text)
    h.close()
    print("Validation output is in %s" % vname)
    assess_validation(vname)
    
# ---------------------------------------------------------------------------
def assess_validation(filename):
    f = open(filename)
    v = f.readlines()
    f.close()

    passed = False
    for line in v:
        if "Passed" in line:
            print line
            passed = True
        if 'class="msg"' in line:
            print line

    if passed:
        os.unlink(filename)

# ---------------------------------------------------------------------------
class TIParser(HTMLParser.HTMLParser):
    # -----------------------------------------------------------------------
    def __init__(self, filename="", text=""):
        """
        Initialize the object with the data and flags we'll need to
        validate the input.

        The general strategy for checking for required elements is to
        create a flag here that starts out with the value 'missing',
        indicating the element has not yet been seen. When/if we come
        across the element, we'll update the flag to 'present' or
        whatever is appropriate. Then in finish(), we can check the
        flag and if it still says 'missing', we know we never found
        the required element.
        """
        if verbose(): print("TIParser.__init__")
        HTMLParser.HTMLParser.__init__(self)
        self.filename = filename
        self.text = text.split("\n")
        self.deprecations = {'applet': '<object>',
                             'basefont': 'CSS',
                             'blackface': 'CSS',
                             'center': 'CSS',
                             'dir': '<ul>',
                             'embed': '<object>',
                             'font': 'CSS',
                             'strike': 'CSS',
                             }
        self.doctype = "missing"
        self.head = 'missing'
        self.body = 'missing'
        self.css = 'missing'
        self.filetype = 'missing'
        self.charset = 'missing'
        self.description = 'missing'
        self.title = 'missing'
        self.nostack = ['p', 'br', 'meta', 'li', 'dd', 'dt']
        self.stack = []

        self.catch_tabs()
            
    # -----------------------------------------------------------------------
    def handle_startendtag(self, tag, attrs):
        """
        Here we catch <script/>, which doesn't work for loading
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
        Run the standard tag checks.
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
        if tag not in self.nostack:
            self.stack.append(tag)
        
    # -----------------------------------------------------------------------
    def handle_endtag(self, tag):
        """
        This gets called when the parser sees an end tag.
        """
        if verbose(): print("TIParser.handle_endtag(self, %s)" % (tag))
        if tag == 'head':
            self.head = 'closed'
        if tag == 'body':
            self.body = 'closed'
        (line, offset) = self.getpos()
        etag = self.text[line-1][offset:]
        if tag not in self.nostack:
            pop = self.stack.pop()
            if tag != pop:
                self.errmsg("</%s> does not match <%s>" % (tag, pop))
        
    # -----------------------------------------------------------------------
    def handle_data(self, data):
        """
        This gets called when the parser sees data between tags.
        """
        if verbose(): print("TIParser.handle_data(self, '%s')" % (data))
        pass

    # -----------------------------------------------------------------------
    def handle_decl(self, decl):
        """
        This gets called when the parser sees a declaration, like
        <!doctype ...>
        """
        if verbose(): print("TIParser.handle_decl(self, '%s')" % (decl))
        if 'doctype' in decl.lower():
            self.doctype = "present"
            
    # -----------------------------------------------------------------------
    def handle_div(self, tag, attrs):
        """
        This gets called on <div> tags
        """
        if 'div' in self.stack:
            # self.errmsg('warning: nested <div> tags detected', 0)
            pass

    # -----------------------------------------------------------------------
    def handle_head(self, tag, attrs):
        """
        This gets called when the parser sees a <head> tag.
        """
        self.head = 'open'
        
    # -----------------------------------------------------------------------
    def handle_body(self, tag, attrs):
        """
        This gets called when the parser sees a <body> tag.
        """
        self.body = 'open'
        
    # -----------------------------------------------------------------------
    def handle_img(self, tag, attrs):
        if 'alt' not in [n for (n, v) in attrs]:
            self.errmsg("<img> tag needs an 'alt' attribute")

    # -----------------------------------------------------------------------
    def handle_input(self, tag, attrs):
        if 'alt' not in [n for (n,v) in attrs]:
            self.errmsg("<input> tag needs an 'alt' attribute")

    # -----------------------------------------------------------------------
    def handle_link(self, tag, attrs):
        """
        This gets called when the parser sees a <link> tag. At least
        one is required to specify the CSS file.
        """
        if ('rel', 'stylesheet') in attrs and ('type', 'text/css') in attrs:
            self.css = "present"
            
    # -----------------------------------------------------------------------
    def handle_meta(self, tag, attrs):
        """
        Handling for meta tags. Two things must be specified with meta
        tags: filetype (e.g., <meta name="keywords" content="index" />) and charset
        (e.g., <meta charset="utf-8" />). They can both be specified in a single
        meta tag or split up.
        """
        ad = {}
        for tup in attrs:
            ad[tup[0]] = tup[1]
        if 'name' in ad.keys() \
           and 'keywords' == ad['name'] \
           and 'content' in ad.keys():
            self.filetype = ad['content']
        if 'name' in ad.keys() \
           and 'description' == ad['name']:
            self.description = 'present'
        if 'charset' in ad.keys():
            self.charset = 'present'

    # -----------------------------------------------------------------------
    def handle_script(self, tag, attrs):
        """
        Handle <script> tags.
        """
        if 'head' in self.stack:
            self.errmsg('Please put your <script> tags at the end of '
                        + '<body> rather than in <head>', 0)

    # -----------------------------------------------------------------------
    def handle_title(self, tag, attrs):
        """
        Note that we've seen a title tag.
        """
        self.title = 'present'

    # -----------------------------------------------------------------------
    def handle_named_tag(self, tag, attrs):
        """
        Look for a method named 'handle_<tagname>'. If it exists, call
        it with the tag and attribute list as arguments. This makes it
        easy to add handlers for specific tags.
        """
        d = dir(self)
        mname = 'handle_%s' % tag
        if mname in dir(self):
            getattr(self, mname)(tag, attrs)

    # -----------------------------------------------------------------------
    def catch_tabs(self):
        """
        Scan the input text and report the location of any TAB
        characters found.
        """
        lnum = 1
        for line in self.text:
            cnum = line.find("\t")
            if 0 <= cnum:
                self.errmsg("TAB detected in input. Please use spaces.",
                            pos=(lnum,cnum))
            lnum += 1
        
    # -----------------------------------------------------------------------
    def catch_unquoted_attrs(self, text, attrlist):
        """
        Here We check to make sure attributes inside HTML tags are quoted.
        """
        for tup in attrlist:
            (an, av) = tup
            rgx = "%s\s*=\s*" % (an) \
                  + "['" \
                  + '"]%s["' % (re.escape(av)) \
                  + "']"
            q = re.search(rgx, self.unescape(text))
            if q == None:
                self.errmsg("unquoted attribute in '%s'" % (text))
                
    # -----------------------------------------------------------------------
    def catch_deprecated_tags(self, tag):
        """
        Here we report any deprecated tags we encounter.
        """
        if tag in self.deprecations.keys():
            (line, offs) = self.getpos()
            self.errmsg("Tag '<%s>' is deprecated. Consider using %s instead"
                        % (tag, self.deprecations[tag]),
                        0)

    # -----------------------------------------------------------------------
    def catch_uppercase_tags(self, tag):
        """
        Here we report uppercase tags.
        """
        raw = self.get_starttag_text()
        q = re.search("<\s*(\w+)\s*", raw)
        txt = q.groups()[0]
        for chr in txt:
            if chr.isupper():
                self.errmsg("Tags like '<%s>' containing uppercase letters are deprecated"
                            % (txt))
                break
                
    # -----------------------------------------------------------------------
    def errmsg(self, msg, exit_val = 1, pos = None):
        """
        Format an error message -- filename, location in file, and
        message. Optionally, the caller can set the exit value to be
        used when the process terminates. By default that's 1,
        indicating an issue but the caller can set exit_val to 0 for a
        warning that won't prevent downstream processing.
        """
        if pos == None:
            (line, offset) = self.getpos()
        else:
            (line, offset) = pos
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
                        + "'<meta name=\"keywords\" content=\"[ft]\" /> "
                        + "where 'ft' is one of 'about', 'proj', 'member', "
                        + "'contact', 'jobs', 'nav', 'pub', or 'software' "
                        + "in the <head> section.")
        elif self.title == 'missing':
            self.errmsg("A <title> tag is needed for this file.", 0)
            
        if self.charset == 'missing':
            self.errmsg("Charset not specified. Please add "
                        + "<meta charset='utf-8' /> "
                        + "in the <head> section.")

        if self.css == 'missing':
            self.errmsg("No CSS link found in <head>. Please add at least "
                        + "<link rel='stylesheet' type='text/css' "
                        + "href='techint_f.css' />")

        if self.description == 'missing':
            self.errmsg("File description not found. Please add at least "
                        + '<meta name="description" content="page description"> '
                        + 'in the <head> section.')
                        
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
        if self.doctype == "missing":
            self.errmsg("A <!doctype ...> is required at the top of the file")
            self.doctype = "reported"

        if 0 == len(self.stack) and tag != 'html':
            self.errmsg("The top level tag should be <html>")
        elif 1 == len(self.stack) and tag != 'head' and tag != 'body':
            self.errmsg("stray '%s' tag found" % tag)

        if tag == 'style' or 'style' in [n for (n,v) in attrs]:
            self.errmsg('warning: external styling is prefered', 0)
            
        self.handle_named_tag(tag, attrs)
        self.catch_unquoted_attrs(self.get_starttag_text(), attrs)
        self.catch_deprecated_tags(tag)
        self.catch_uppercase_tags(tag)
        
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    main(sys.argv)
