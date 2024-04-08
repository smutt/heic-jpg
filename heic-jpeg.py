#!/usr/local/bin/python3

import sys
import os
import argparse
from PIL import Image
from pi_heif import register_heif_opener

class Ifile():
  def __init__(self, img, fname):
    self.img = img # A Pillow object
    self.in_name = fname
    self.left_name = fname.split(".")[:-1][0]
    self.out_name = self.left_name + ".jpeg"
    
  def __repr__(self):
    return self.in_name

  def debug(self):
    return "name:" + self.in_name + " format:" + self.img.format + " size:" + str(self.img.width) + "x" + str(self.img.height) \
      + " mode:" + self.img.mode + " animated:" + str(self.img.is_animated)

register_heif_opener()

ap = argparse.ArgumentParser(description='Convert HEIC image file to JPEG')
ap.add_argument(nargs='+', dest='infile', type=str, default=None,
                  help='Image file to convert')
ap.add_argument('-d', '--dump', default=False, dest='dump', action='store_true', required=False,
                  help='Dump info on image file and exit.')
ap.add_argument('-q', '--quality', default=None, nargs=1, dest='quality', type=str, required=False,
                  help='Output quality')
ap.add_argument('-f', '--format', default='.jpg', nargs=1, dest='ext', type=str, required=False,
                  help='Output format') #make enum

ap.add_argument('-v', '--verbose', default=False, dest='verbose', action='store_true', required=False,
                  help='Verbose output during processing.')
args = ap.parse_args()

i_files = []
for ff in args.infile:
  i_files.append(Ifile(Image.open(ff), ff))

if args.dump:
  for ii in i_files:
    print(ii.debug())
  exit(0)

for ii in i_files:
  try:
      ii.img.save(ii.out_name)
  except OSError:
    print("cannot convert", repr(ii))
