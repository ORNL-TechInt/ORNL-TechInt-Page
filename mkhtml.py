#!/usr/bin/python
"""
mkhtml - generate HTML files from snippets
"""
import pdb
import re
import sys
import toolframe
import unittest

from optparse import *

# ---------------------------------------------------------------------------
def main(argv = None):
    if argv == None:
        argv = sys.argv

    p = OptionParser()
    p.add_option('-o', '--output',
                 action='store', default='',
                 dest='output',
                 help='output filename extension')
    p.add_option('-d', '--debug',
                 action='store_true', default=False,
                 dest='debug',
                 help='run under debugger')
    (o, a) = p.parse_args(argv)

    if o.debug: pdb.set_trace()
    
    for filename in a[1:]:
        q = Assembler(filename, o.output)
        q.process()

# ---------------------------------------------------------------------------
class Assembler(object):
    # -----------------------------------------------------------------------
    def __init__(self, input_name, ext=None):
        if not input_name.endswith('.src'):
            raise StandardError("I don't know what to do with %s" % filename)
        
        self.iname = input_name
        self.oname = self.output_name(input_name, ext)
        self.instack = []
        self.ifstack = []
        
    # -----------------------------------------------------------------------
    def assemble(self):
        rgx = r"name=['\"]keywords['\"]\s+content=['\"](.*)['\"]"
        line = self.ifile.readline()
        while line != '':
            if line[0] == '%':
                cmd = line[1:]
                eval('self.%s' % cmd)
            else:
                q = re.search(rgx, line)
                if q:
                    self.filetype = q.groups()[0].split()[0]
                    
                self.ofile.write(line)
            line = self.ifile.readline()

    # -----------------------------------------------------------------------
    def ifeq(self, a, b):
        line = self.ifile.readline()
        while line.strip() != '' and line.strip() not in ['%else', '%endif']:
            if a == b:
                self.ofile.write(line)
            line = self.ifile.readline()

        if line.strip() == '%endif':
            return
        elif line.strip() == '':
            raise StandardError('End of file found when expecting %else or %endif')
        else:
            line = self.ifile.readline()
            
        while line.strip() != '' and line.strip() != '%endif':
            if a != b:
                self.ofile.write(line)
            line = self.ifile.readline()

        if line.strip() == '':
            raise StandardError('End of file found when expecting %endif')
            
    # -----------------------------------------------------------------------
    def include(self, filename):
        self.instack.append(self.iname)
        self.ifstack.append(self.ifile)
        self.iname = filename
        self.ifile = open(filename, 'r')

        self.assemble()

        self.ifile.close()
        self.ifile = self.ifstack.pop()
        self.iname = self.instack.pop()
        
    # -----------------------------------------------------------------------
    def output_name(self, iname, ext):
        if ext == None or ext == '':
            ext = '.html'
        elif not ext.startswith('.'):
            ext = '.' + ext
        rval = iname.replace('.src', ext)
        return rval
    
    # -----------------------------------------------------------------------
    def process(self):
        self.ifile = open(self.iname, 'r')
        self.ofile = open(self.oname, 'w')

        self.assemble()

        self.ofile.close()
        self.ifile.close()
        
# ---------------------------------------------------------------------------
class MkhtmlTest(unittest.TestCase):
    def test_example(self):
        pass

toolframe.ez_launch(main)
