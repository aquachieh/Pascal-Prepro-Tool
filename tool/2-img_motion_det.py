"""
2-img_motion_det.py
pick out motion img
"""

# import the necessary packages
import os
import argparse
import datetime
import imutils
import time
import cv2
from shutil import copyfile

###--- setting

MIN_AREA = 1000
RESIZED_WIDTH = 500
BACKGROUND_IMG_PATH = "/TOOL/1-avi2img.py/OutputVideos/C02.mp4/C02-000006.jpg"
FRAME_DIR_PATH = "/TOOL/1-avi2img.py/OutputVideos/C02.mp4/Frame/"
OUTPUT_DIR_PATH ="/TOOL/1-avi2img.py/OutputVideos/C02.mp4/OUTPUT/"
PLOT_DIR_PATH0 ="/TOOL/1-avi2img.py/OutputVideos/C02.mp4/PlotOutput0/"
PLOT_DIR_PATH1 ="/TOOL/1-avi2img.py/OutputVideos/C02.mp4/PlotOutput1/"
MinMotionNumber = 1

###---------

if not os.path.exists(OUTPUT_DIR_PATH):
    os.makedirs(OUTPUT_DIR_PATH)

if not os.path.exists(PLOT_DIR_PATH0):
    os.makedirs(PLOT_DIR_PATH0)

if not os.path.exists(PLOT_DIR_PATH1):
    os.makedirs(PLOT_DIR_PATH1)

# use firstFrame or creat background frame 
firstFrame = cv2.imread(BACKGROUND_IMG_PATH)
firstFrame = imutils.resize(firstFrame, width = RESIZED_WIDTH)  
firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
firstFrame = cv2.GaussianBlur(firstFrame, (21, 21), 0)

for f in os.listdir(FRAME_DIR_PATH) :
    print f
    frame = cv2.imread(FRAME_DIR_PATH + f)
    frame = imutils.resize(frame, width = RESIZED_WIDTH) 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # compute the absolute difference between the current frame and
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]  #----
    thresh = cv2.dilate(thresh, None, iterations= 5)   #--- 2 , more bigger more merge bbox
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    count_cc = 0
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < MIN_AREA:
            continue
        ## plot bbox and save
        print cv2.contourArea(c)
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        count_cc = count_cc +1
    #cv2.imwrite (PLOT_DIR_PATH + f,frame)

    if count_cc >= MinMotionNumber :
        src = FRAME_DIR_PATH + f
        dst = OUTPUT_DIR_PATH + f
        copyfile(src, dst)
        cv2.imwrite (PLOT_DIR_PATH1 + f,frame)
    else:
        cv2.imwrite (PLOT_DIR_PATH0 + f,frame)
    

