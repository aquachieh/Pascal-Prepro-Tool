
'''
6-augImg.py
3 type:
  -randomRotateImg.py
  -randomRotateShiftImg.py
  -randomRotateCropImg.py
'''



'''
randomRotateImg.py
- rotate
'''

import os
import random
import cv2
import copy
import imutils

###---setting
INPUT_DIR = "/.../test/img/"
OUTPUT_DIR = "/.../test/Rotate_img/"
degNumber = 5 
degRange = (30,330)
###--------------

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

for f in os.listdir(INPUT_DIR) :
    fname = f.split('.')[-2]
    print f
    im = cv2.imread(INPUT_DIR + f)
    im2 = copy.deepcopy(im)
    #cv2.imwrite(OUTPUT_DIR + fname +"_r00.jpg",im)
    for i_d in xrange(degNumber):
        deg = random.randint(degRange[0], degRange[1])
        print fname,"---",deg
        im_r = imutils.rotate(im2, deg)   # fixed frame size
        #im_r = imutils.rotate_bound(im2, deg)
        cv2.imwrite(OUTPUT_DIR + fname +"_r"+ str(deg) +".jpg",im_r)



#====================================================================================
#%%
    
'''
randomRotateShiftImg.py
- rotate
- shift(black edge) <----slow
'''

import os
import random
import cv2
import copy
import imutils
import numpy as np
import scipy.ndimage as ndimage

###---setting
INPUT_DIR = "/.../test/img/"
OUTPUT_DIR = "/.../test/RotateShift_img/"
degNumber = 5 
degRange = (30,330)
max_amt = 0.2
###--------------

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    
###--- rotate + shift(black edge)
for f in os.listdir(INPUT_DIR) :
    fname = f.split('.')[-2]
    print f
    im = cv2.imread(INPUT_DIR + f)
    im2 = copy.deepcopy(im)
    #cv2.imwrite(OUTPUT_DIR + fname +"_r00.jpg",im)
    for i_d in xrange(degNumber):
        deg = random.randint(degRange[0], degRange[1])
        print fname,"---",deg
        im_r = imutils.rotate(im2, deg)   # fixed frame size
        #im_r = imutils.rotate_bound(im2, deg)
        max_x = int(im_r.shape[1] * max_amt)
        max_y = int(im_r.shape[0] * max_amt)
        x = np.random.randint(low=-max_x, high=max_x)
        y = np.random.randint(low=-max_y, high=max_y)
        im_r = ndimage.interpolation.shift(im_r,shift=[x,y,0])  #--- slow
        cv2.imwrite(OUTPUT_DIR + fname +"_r"+ str(deg) +".jpg",im_r)
    


#====================================================================================
#%%
    
'''
randomRotateCropImg.py
- rotate
- crop
'''

import os
import random
import cv2
import copy
import imutils

###---setting
INPUT_DIR = "/.../test/img/"
OUTPUT_DIR = "/../test/RotateCrop_img/"
degNumber = 5 
degRange = (30,330)
ratioCrop = (30,70)
###--------------

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    
###--- rotate + crop
for f in os.listdir(INPUT_DIR) :
    fname = f.split('.')[-2]
    print f
    im = cv2.imread(INPUT_DIR + f)
    im2 = copy.deepcopy(im)
    #cv2.imwrite(OUTPUT_DIR + fname +"_r00.jpg",im)
    for i_d in xrange(degNumber):
        deg = random.randint(degRange[0], degRange[1])
        print fname,"---",deg
        im_r = imutils.rotate(im2, deg)   # fixed frame size
        #im_r = imutils.rotate_bound(im2, deg)
        new_x1 = int(random.randint(0,ratioCrop[0])*0.01*im_r.shape[0])
        new_x2 = int(random.randint(ratioCrop[1],100)*0.01*im_r.shape[0])
        new_y1 = int(random.randint(0,ratioCrop[0])*0.01*im_r.shape[1])
        new_y2 = int(random.randint(ratioCrop[1],100)*0.01*im_r.shape[1])
        crop_img = im_r[new_x1:new_x2, new_y1:new_y2]
        cv2.imwrite(OUTPUT_DIR + fname +"_r"+ str(deg) +".jpg",crop_img)


