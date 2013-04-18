import cairosvg
from os import listdir
from os.path import isfile, join
import os
import glob
 
path = 'graphs/'
for infile in glob.glob( os.path.join(path, '*.svg') ):
    print "current file is: " + infile
    cairosvg infile -f png

cairosvg.

"""
svg_code = ""

cairosvg.svg2png(bytestring=svg_code,write_to=fout)

fout.close()
"""