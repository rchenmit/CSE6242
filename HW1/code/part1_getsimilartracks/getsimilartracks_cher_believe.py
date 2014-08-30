##
## CSE 6242 Pset 1 Part 1
## Robert Chen
## due Sept 8, 2014
##
## grab similar tracks to Cher's "Believe" from last.fm
##

import urllib2
import time
from lxml import etree
from StringIO import StringIO


print "this script pulls from last.fm 100 similar tracks to what is specified"

