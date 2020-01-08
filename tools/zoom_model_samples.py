#!/usr/bin/env python

import sys
import os
import getopt
import re
import cv2
from tdlib.common import zoomImage

def usage():
    ''' 显示帮助
    '''
    print("Zoom Model Sample Images Tool")

if __name__ == "__main__":
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "i:o:t:", ["help"])
    except getopt.GetoptError:
        print("argv error")
        sys.exit(1)

    input_dir, output_dir, total_pixels = None, None, None
    for cmd, arg in opts:
        if cmd in "-i":
            input_dir = arg
        elif cmd in "-o":
            output_dir = arg
        elif cmd in "-t":
            total_pixels = int(arg)
        else:
            usage()
            sys.exit(1)
    if None in [input_dir, output_dir, total_pixels]:
        print("Args Error.")
        sys.exit(1)

    files = os.listdir(input_dir)
    for fname in files:
        fpath = input_dir+'/'+fname
        if not os.path.isfile(fpath):
            continue
        if re.search('jpg$|JPG$', fname) is None:
            continue
        image = cv2.imread(fpath, cv2.IMREAD_GRAYSCALE)
        zoomed = zoomImage(image, total_pixels)
        cv2.imwrite(output_dir+'/'+fname, zoomed)
