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
        process(filename, o)

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
class MkhtmlTest(unittest.TestCase):
    def test_example(self):
        pass

toolframe.ez_launch(main)
