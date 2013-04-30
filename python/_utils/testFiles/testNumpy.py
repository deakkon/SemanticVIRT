'''
Created on 14.1.2013.

@author: Jurica Seva

PhD Candidate 
Faculty of Organization and Informatics
University of Zagreb
'''
#imports
import logging

#logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#!/usr/bin/env python                                                           
import numpy
import sys
import timeit
 
try:
    import numpy.core._dotblas
    print 'FAST BLAS'
except ImportError:
    print 'slow blas'
 
print "version:", numpy.__version__
print "maxint:", sys.maxint
print
 
x = numpy.random.random((1000,1000))
 
setup = "import numpy; x = numpy.random.random((1000,1000))"
count = 5
 
t = timeit.Timer("numpy.dot(x, x.T)", setup=setup)
print "dot:", t.timeit(count)/count, "sec"