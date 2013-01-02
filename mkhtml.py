#!/usr/bin/python
"""
mkhtml - generate HTML files from snippets
"""
import pdb
import sys
import toolframe
import unittest

from optparse import *

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
    
    # process arguments
    for filename in a[1:]:
        q = Assembler(filename, o.output)
        q.process()
        # process(filename, o)

# ---------------------------------------------------------------------------
def assemble(input, output):
    global ofile, ifile
    ofile = output
    ifile = input
    for line in input:
        if line[0] == '%':
            cmd = line[1:]
            eval(cmd)
        else:
            output.write(line)

# ---------------------------------------------------------------------------
def ifeq(parent, target):
    # get the first line past the %ifeq() line
    line = ifile.readline()
    # process lines until we hit '%else' or '%endif'
    while line.strip() not in ['%else', '%endif']:
        # writing out lines in the ifeq branch if the comparands are equal
        if parent == target:
            ofile.write(line)
        line = ifile.readline()

    # at this point, line is either '%else' or '%endif'. If it's '%endif',
    # this second loop will fail immediately and we'll return. If it's
    # '%else', this will process lines on down to the '%endif'
    while line.strip() != '%endif':
        # writing out the lines if the comparands are unequal
        if parent != target:
            ofile.write(line)
        line = ifile.readline()

# ---------------------------------------------------------------------------
def include(filename):
    global ofile
    f = open(filename, 'r')
    for line in f:
        ofile.write(line)
    f.close()
    
# ---------------------------------------------------------------------------
def process(filename, opts):
    if not filename.endswith('.src'):
        print("I don't know what to do with %s" % filename)
        return

    if opts.output.startswith('.'):
        ext = opts.output
    elif opts.output != '':
        ext = '.' + opts.output
    else:
        ext = '.html'

    outname = filename.replace('.src', ext)
    f = open(filename, 'r')
    g = open(outname, 'w')

    assemble(f, g)

    f.close()
    g.close()
    
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
        # for line in self.ifile:
        line = self.ifile.readline()
        while line != '':
            if line[0] == '%':
                cmd = line[1:]
                eval('self.%s' % cmd)
            else:
                self.ofile.write(line)
            line = self.ifile.readline()

    # -----------------------------------------------------------------------
    def ifeq(self, a, b):
        line = self.ifile.readline()
        while line.strip() not in ['%else', '%endif']:
            if a == b:
                self.ofile.write(line)
            line = self.ifile.readline()

        if line.strip() == '%endif':
            return
        else:
            line = self.ifile.readline()
            
        while line.strip() != '%endif':
            if a != b:
                self.ofile.write(line)
            line = self.ifile.readline()

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
