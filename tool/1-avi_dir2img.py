'''
avi2img.py
video2img.py
only crop avi

setting :fpsIn
INPUT: InputVideos(video dir)
OUTPUT: OutputVideos(frame)
'''

import os
import numpy as np
import cv2
import glob
import copy
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import time

def CreateFolder (folderName):
    print folderName
    if not os.path.exists(folderName):
        try:
            os.makedirs(folderName)
        except OSError as exc: 
            if exc.errno != errno.EEXIST:
                raise

ROOT_PATH = "/TOOL/1-avi2img.py/"

INPUT_VIDEOS_PATH = os.path.join(ROOT_PATH,'InputVideos')
OUTPUT_VIDEOS_PATH = os.path.join(ROOT_PATH,'OutputVideos')
CreateFolder(OUTPUT_VIDEOS_PATH)


## Process Single Video ##    
def ProcessSingleVideo(FileName):
    # Get Video Name #
    fileName = FileName
    #Create Input Video Object #
    video = cv2.VideoCapture(os.path.join(INPUT_VIDEOS_PATH,fileName))
    # Set Output fps (use cutRate to control) #
    fpsIn = int(video.get(cv2.cv.CV_CAP_PROP_FPS))
    fpsOut =  30      #fpsIn 5   #----------------------
    cutRate = int(1.0*fpsIn/fpsOut)
    print 'fpsIn: {}, fpsOut: {}, cuteRate: {}'.format(fpsIn,fpsOut,cutRate)

    # Create Folder For Output Video And Corresponding Image #
    #-- saveDetails
    CreateFolder(os.path.join(OUTPUT_VIDEOS_PATH,fileName))
    framePath = os.path.join(OUTPUT_VIDEOS_PATH,fileName,'Frame')
    CreateFolder(framePath)
    # Initial FrameNumber #
    frameNumber = 0

    while(True):
        # Read Each Frame From Video #
        ret, frame = video.read()        
        if(ret):
            # Flip Output Frame From Webcam#
            if (frameNumber%cutRate) == 0:
                cv2.imwrite(os.path.join(framePath,'{}'.format(fileName.split('.')[0])+'-{0:06}.jpg'.format(frameNumber) ),frame)
                print "frameNumber:", frameNumber
            frameNumber = frameNumber +1
        else:
            break

    # Release Input  Video #
    video.release()
    cv2.destroyAllWindows()
    print 'job done!'


## Process WebcamVideo Or All Videos In Project Folder Named InputVideos ##   
for i,fileName in enumerate(os.listdir(INPUT_VIDEOS_PATH)): 
    ProcessSingleVideo(fileName)
