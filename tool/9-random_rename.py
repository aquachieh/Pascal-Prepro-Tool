'''
9-random_rename.py
random rename files as format{0:06}
'''

import os
import numpy as np
from shutil import copyfile

###---setting 
IMG_DIRPATH = "/.../test/0515tt/2-NEW_rotate/IMG/"
ANNO_DIRPATH = "/.../test/0515tt/2-NEW_rotate/Anno/"

OUTPUT_DIR = "/.../test/0515tt/3-Random/"
IMG_DIRPATH2 = OUTPUT_DIR + "JPEGImages/"
ANNO_DIRPATH2 = OUTPUT_DIR + "Annotations/"
###---
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
if not os.path.exists(IMG_DIRPATH2):
    os.makedirs(IMG_DIRPATH2)
if not os.path.exists(ANNO_DIRPATH2):
    os.makedirs(ANNO_DIRPATH2)


imgs = os.listdir(IMG_DIRPATH)
arr = np.arange(len(imgs))
np.random.shuffle(arr)
#print len(imgs)

for f,ff in enumerate(sorted(os.listdir(IMG_DIRPATH))):
    print f,ff
    print arr[f]
    filename = ff.split('.')[0]
    #copyfile(IMG_DIRPATH+filename+".jpg", IMG_DIRPATH2+'{0:06}'.format(arr[f])+'.jpg')
    #copyfile(ANNO_DIRPATH+filename+".xml",ANNO_DIRPATH2+'{0:06}'.format(arr[f])+'.xml')
    os.rename(IMG_DIRPATH+filename+".jpg", IMG_DIRPATH2+'{0:06}'.format(arr[f])+'.jpg')
    os.rename(ANNO_DIRPATH+filename+".xml",ANNO_DIRPATH2+'{0:06}'.format(arr[f])+'.xml')

