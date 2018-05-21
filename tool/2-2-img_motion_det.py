"""
2-2-img_motion_det.py
pick out motion img

step 1 : absdiff(background, new_frame)
step 2 : absdiff(last frame, new_frame)

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
BACKGROUND_IMG_PATH = "/TOOL/1-avi2img.py/OutputVideos/C02.mp4/C02-000000.jpg"

ROOT_DIR_PATH = "/TOOL/1-avi2img.py/OutputVideos/C02.mp4/"
FRAME_DIR_PATH = ROOT_DIR_PATH + "Frame/"

OUTPUT_DIR_PATH = ROOT_DIR_PATH + "2_OUTPUT/"
PLOT_DIR_PATH0 = ROOT_DIR_PATH + "2_PlotOutput0/"
PLOT_DIR_PATH1 = ROOT_DIR_PATH + "2_PlotOutput1/"
PLOT_DIR_PATH2 = ROOT_DIR_PATH + "2_PlotOutput2/"
PLOT_DIR_PATH3 = ROOT_DIR_PATH + "2_PlotOutput3/"
MinMotionNumber = 1
###---------
if not os.path.exists(ROOT_DIR_PATH):
    os.makedirs(ROOT_DIR_PATH)
if not os.path.exists(OUTPUT_DIR_PATH):
    os.makedirs(OUTPUT_DIR_PATH)
if not os.path.exists(PLOT_DIR_PATH0):
    os.makedirs(PLOT_DIR_PATH0)
if not os.path.exists(PLOT_DIR_PATH1):
    os.makedirs(PLOT_DIR_PATH1)
if not os.path.exists(PLOT_DIR_PATH2):
    os.makedirs(PLOT_DIR_PATH2)
if not os.path.exists(PLOT_DIR_PATH3):
    os.makedirs(PLOT_DIR_PATH3)
    
# use firstFrame or creat background frame 
firstFrame = cv2.imread(BACKGROUND_IMG_PATH)
firstFrame = imutils.resize(firstFrame, width = RESIZED_WIDTH)  
firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
firstFrame = cv2.GaussianBlur(firstFrame, (21, 21), 0)
# initialize last frame in the video stream
lastFrame = None

for f in os.listdir(FRAME_DIR_PATH) :
    print f

#--- case 1 ---#

    frame = cv2.imread(FRAME_DIR_PATH + f)
    frame = imutils.resize(frame, width = RESIZED_WIDTH) 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # compute the absolute difference between the current frame and
    frameDelta = cv2.absdiff(firstFrame, gray)   #-----
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]  #----
    thresh = cv2.dilate(thresh, None, iterations= 5)   #--- 2 , more bigger more merge bbox
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    count_cc = 0
    for c in cnts:
        # if the contour is too small, ignore it
        print "--1--:",cv2.contourArea(c)
        if cv2.contourArea(c) < MIN_AREA:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            continue
        ## plot bbox and save
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        count_cc = count_cc +1
    #cv2.imwrite (PLOT_DIR_PATH + f,frame)


#--- case 2 ---#
    # if the last Frame is None, initialize it
    if lastFrame is None:
        lastFrame = firstFrame

    frameDelta = cv2.absdiff(gray, lastFrame) 
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]  #----
    thresh = cv2.dilate(thresh, None, iterations= 2)   #--- 2 , more bigger more merge bbox
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    count_cc2 = 0
    for c in cnts:
        print "--2--:",cv2.contourArea(c)
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < MIN_AREA:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 1)
            continue
        ## plot bbox and save
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 3)
        count_cc2 = count_cc2 +1
    
    lastFrame = gray
     
    if count_cc >= MinMotionNumber and count_cc2 >= MinMotionNumber :
        src = FRAME_DIR_PATH + f
        dst = OUTPUT_DIR_PATH + f
        copyfile(src, dst)
        cv2.imwrite (PLOT_DIR_PATH2 + f,frame)
    elif count_cc >= MinMotionNumber and count_cc2 < MinMotionNumber :
        cv2.imwrite (PLOT_DIR_PATH1 + f,frame)                
    elif count_cc < MinMotionNumber and count_cc2 < MinMotionNumber:
        cv2.imwrite (PLOT_DIR_PATH0 + f,frame)
    else :
        cv2.imwrite (PLOT_DIR_PATH3 + f,frame)
        #pass
