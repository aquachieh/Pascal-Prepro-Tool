'''
10-anno2txt.py
'''

import os
import glob

###---setting
VOC_DIR = "/.../test/0515tt/3-Random/"
ANNO_DIRPATH =  VOC_DIR + "Annotations/"
###--------------

if not os.path.exists(VOC_DIR + "ImageSets/"):
    os.makedirs(VOC_DIR + "ImageSets/")
if not os.path.exists(VOC_DIR + "ImageSets/Main/"):
    os.makedirs(VOC_DIR + "ImageSets/Main/")


text_file = open(VOC_DIR + "ImageSets/Main/test.txt","w")

pic_list=sorted(glob.glob(ANNO_DIRPATH + "*.xml"))
#print len(pic_list)

for i in xrange(len(pic_list)):
    kk=pic_list[i].split("/")[-1].split(".")[0]
    text_file.write(kk+"\n")
    
text_file.close()
