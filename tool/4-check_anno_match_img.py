'''
check whether ANNO_file match IMG_file
4-check_anno_match_img.py
'''

import os
import numpy as np

IMG_DIRPATH = "/.../img_new/"
ANNO_DIRPATH = "/.../anno_new/"

IMG_DIRPATH2 = "/.../img_nomatch/"
#ANNO_DIRPATH2 = "/.../anno_no/"

if not os.path.exists(IMG_DIRPATH2):
    os.makedirs(IMG_DIRPATH2)
#if not os.path.exists(ANNO_DIRPATH2):
#    os.makedirs(ANNO_DIRPATH2)

xmls = os.listdir(ANNO_DIRPATH)

for f in os.listdir(IMG_DIRPATH):
    print f
    filename = f.split('.')[0]
    ff = filename + ".xml"
    if ff in xmls:
        continue
    else:  # img not in anno
        os.rename(IMG_DIRPATH+filename+".jpg", IMG_DIRPATH2+filename+'.jpg')
        print "--NO MATCHED-- ",filename
