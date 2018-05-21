#!/usr/bin/env python

'''
7-xmlRotate4deg.py

input : img , anno
rotate[90,180,270]
output : new_img,new_anno
'''


import numpy as np
import os, sys, cv2
import glob
import xml.etree.cElementTree as ET
from shutil import copyfile
import imutils
from xml.etree.ElementTree import ElementTree,Element
import copy

def read_xml(in_path):
    tree = ElementTree()
    tree.parse(in_path)
    return tree

def find_nodes(tree, path):
    return tree.findall(path)
  
def write_xml(tree, out_path):
    tree.write(out_path, encoding="utf-8",xml_declaration=True)  
  

def CreateFolder (folderName):
    print folderName
    if not os.path.exists(folderName):
        try:
            os.makedirs(folderName)
        except OSError as exc: 
            if exc.errno != errno.EEXIST:
                raise

def VOCxml(filename, image , classlabel, bbox):
           #new       #old       #"face"
    height,width = image.shape[0:2]  # h,w
    depth = 3
    #
    root = ET.Element("annotation")
    ET.SubElement(root, "folder").text = "a"   #------------
    ET.SubElement(root, "filename").text = filename+".jpg"
    #
    node1 = ET.SubElement(root, "source")
    ET.SubElement(node1, "database").text = "a7"  #--------------
    ET.SubElement(node1, "annotation").text = "PASCAL VOC"  #------------
    ET.SubElement(node1, "image").text = "a"
    ET.SubElement(node1, "flickrid").text = "no"
    #
    node2 = ET.SubElement(root, "owner")
    ET.SubElement(node2, "flickrid").text = "no"
    ET.SubElement(node2, "name").text = "K7"
    #
    node3 = ET.SubElement(root, "size")
    ET.SubElement(node3, "width").text = str(width)
    ET.SubElement(node3, "height").text = str(height)
    ET.SubElement(node3, "depth").text = str(depth)
    #
    ET.SubElement(root, "segmented").text = "0"
    #-------------------------------------------------------------------
    bbnum=0
    for i in xrange(len(bbox)):
        #print i
        xmin=int(bbox[i][0])
        ymin=int(bbox[i][1])
        xmax=int(bbox[i][2])
        ymax=int(bbox[i][3]) 
        #
        if (bbox[i][2]-bbox[i][0])<5 or (bbox[i][3]-bbox[i][1])<5:          #-------
            continue
        if xmin<1 :
            xmin=1
        if xmax>=width :
            xmax=width-1                      
        if ymin<1 :
            ymin=1
        if ymax>=height :
            ymax=height-1 
        if xmin>=xmax or ymin>=ymax:
            continue  #jump this iteration of the loop
        #check has been passed:
        bbnum=bbnum+1
        #     
        node4 = ET.SubElement(root, "object")
        ET.SubElement(node4, "name").text = classlabel       #-------------------
        ET.SubElement(node4, "pose").text = "unknow"
        ET.SubElement(node4, "truncated").text = "1"
        ET.SubElement(node4, "difficult").text = "0"
        #
        node5 = ET.SubElement(node4, "bndbox")
        ET.SubElement(node5, "xmin").text = str(xmin)
        ET.SubElement(node5, "ymin").text = str(ymin)
        ET.SubElement(node5, "xmax").text = str(xmax)
        ET.SubElement(node5, "ymax").text = str(ymax)
    # noBBox turn none
    if bbnum==0:
        return None
    else:    
        return ET.ElementTree(root)

def VOCxml90(filename, image , classlabel, bbox, im0_H, im0_W):
           #new       #old       #"face"
    height,width = image.shape[0:2]  # h,w
    depth = 3
    #
    root = ET.Element("annotation")
    ET.SubElement(root, "folder").text = "a"   #------------
    ET.SubElement(root, "filename").text = filename+".jpg"
    #
    node1 = ET.SubElement(root, "source")
    ET.SubElement(node1, "database").text = "a7"  #--------------
    ET.SubElement(node1, "annotation").text = "PASCAL VOC"  #------------
    ET.SubElement(node1, "image").text = "a"
    ET.SubElement(node1, "flickrid").text = "no"
    #
    node2 = ET.SubElement(root, "owner")
    ET.SubElement(node2, "flickrid").text = "no"
    ET.SubElement(node2, "name").text = "K7"
    #
    node3 = ET.SubElement(root, "size")
    ET.SubElement(node3, "width").text = str(width)
    ET.SubElement(node3, "height").text = str(height)
    ET.SubElement(node3, "depth").text = str(depth)
    #
    ET.SubElement(root, "segmented").text = "0"
    #-------------------------------------------------------------------
    bbnum=0
    for i in xrange(len(bbox)):
        #print i
        xmin0=int(bbox[i][0])
        ymin0=int(bbox[i][1])
        xmax0=int(bbox[i][2])
        ymax0=int(bbox[i][3]) 
        
        xmin = int(im0_H-ymax0)
        ymin = int(xmin0)
        xmax = int(im0_H-ymin0) 
        ymax = int(xmax0)
        #
        if (bbox[i][2]-bbox[i][0])<5 or (bbox[i][3]-bbox[i][1])<5:          #-------
            continue
        if xmin<1 :
            xmin=1
        if xmax>=width :
            xmax=width-1                      
        if ymin<1 :
            ymin=1
        if ymax>=height :
            ymax=height-1 
        if xmin>=xmax or ymin>=ymax:
            continue  #jump this iteration of the loop
        #check has been passed:
        bbnum=bbnum+1
        #     
        node4 = ET.SubElement(root, "object")
        ET.SubElement(node4, "name").text = classlabel       #-------------------
        ET.SubElement(node4, "pose").text = "unknow"
        ET.SubElement(node4, "truncated").text = "1"
        ET.SubElement(node4, "difficult").text = "0"
        #
        node5 = ET.SubElement(node4, "bndbox")
        ET.SubElement(node5, "xmin").text = str(xmin)
        ET.SubElement(node5, "ymin").text = str(ymin)
        ET.SubElement(node5, "xmax").text = str(xmax)
        ET.SubElement(node5, "ymax").text = str(ymax)
    # noBBox turn none
    if bbnum==0:
        return None
    else:    
        return ET.ElementTree(root)
        
def VOCxml180(filename, image , classlabel, bbox,im0_H,im0_W):
           #new       #old       #"face"
    height,width = image.shape[0:2]  # h,w
    depth = 3
    #
    root = ET.Element("annotation")
    ET.SubElement(root, "folder").text = "a"   #------------
    ET.SubElement(root, "filename").text = filename+".jpg"
    #
    node1 = ET.SubElement(root, "source")
    ET.SubElement(node1, "database").text = "a7"  #--------------
    ET.SubElement(node1, "annotation").text = "PASCAL VOC"  #------------
    ET.SubElement(node1, "image").text = "a"
    ET.SubElement(node1, "flickrid").text = "no"
    #
    node2 = ET.SubElement(root, "owner")
    ET.SubElement(node2, "flickrid").text = "no"
    ET.SubElement(node2, "name").text = "K7"
    #
    node3 = ET.SubElement(root, "size")
    ET.SubElement(node3, "width").text = str(width)
    ET.SubElement(node3, "height").text = str(height)
    ET.SubElement(node3, "depth").text = str(depth)
    #
    ET.SubElement(root, "segmented").text = "0"
    #-------------------------------------------------------------------
    bbnum=0
    for i in xrange(len(bbox)):
        #print i
        xmin0=int(bbox[i][0])
        ymin0=int(bbox[i][1])
        xmax0=int(bbox[i][2])
        ymax0=int(bbox[i][3]) 
        
        xmin = int(im0_W -xmax0)
        ymin = int(im0_H - ymax0)
        xmax = int(im0_W -xmin0)
        ymax = int(im0_H - ymin0)
        #
        if (bbox[i][2]-bbox[i][0])<5 or (bbox[i][3]-bbox[i][1])<5:          #-------
            continue
        if xmin<1 :
            xmin=1
        if xmax>=width :
            xmax=width-1                      
        if ymin<1 :
            ymin=1
        if ymax>=height :
            ymax=height-1 
        if xmin>=xmax or ymin>=ymax:
            continue  #jump this iteration of the loop
        #check has been passed:
        bbnum=bbnum+1
        #     
        node4 = ET.SubElement(root, "object")
        ET.SubElement(node4, "name").text = classlabel       #-------------------
        ET.SubElement(node4, "pose").text = "unknow"
        ET.SubElement(node4, "truncated").text = "1"
        ET.SubElement(node4, "difficult").text = "0"
        #
        node5 = ET.SubElement(node4, "bndbox")
        ET.SubElement(node5, "xmin").text = str(xmin)
        ET.SubElement(node5, "ymin").text = str(ymin)
        ET.SubElement(node5, "xmax").text = str(xmax)
        ET.SubElement(node5, "ymax").text = str(ymax)
    # noBBox turn none
    if bbnum==0:
        return None
    else:    
        return ET.ElementTree(root)
       
def VOCxml270(filename, image , classlabel, bbox,im0_H,im0_W):
           #new       #old       #"face"
    height,width = image.shape[0:2]  # h,w
    depth = 3
    #
    root = ET.Element("annotation")
    ET.SubElement(root, "folder").text = "a"   #------------
    ET.SubElement(root, "filename").text = filename+".jpg"
    #
    node1 = ET.SubElement(root, "source")
    ET.SubElement(node1, "database").text = "a7"  #--------------
    ET.SubElement(node1, "annotation").text = "PASCAL VOC"  #------------
    ET.SubElement(node1, "image").text = "a"
    ET.SubElement(node1, "flickrid").text = "no"
    #
    node2 = ET.SubElement(root, "owner")
    ET.SubElement(node2, "flickrid").text = "no"
    ET.SubElement(node2, "name").text = "K7"
    #
    node3 = ET.SubElement(root, "size")
    ET.SubElement(node3, "width").text = str(width)
    ET.SubElement(node3, "height").text = str(height)
    ET.SubElement(node3, "depth").text = str(depth)
    #
    ET.SubElement(root, "segmented").text = "0"
    #-------------------------------------------------------------------
    bbnum=0
    for i in xrange(len(bbox)):
        #print i
        xmin0=int(bbox[i][0])
        ymin0=int(bbox[i][1])
        xmax0=int(bbox[i][2])
        ymax0=int(bbox[i][3]) 
        
        xmin = int(ymin0)
        ymin = int(im0_W-xmax0)
        xmax = int(ymax0)
        ymax = int(im0_W-xmin0)
        #
        if (bbox[i][2]-bbox[i][0])<5 or (bbox[i][3]-bbox[i][1])<5:          #-------
            continue
        if xmin<1 :
            xmin=1
        if xmax>=width :
            xmax=width-1                      
        if ymin<1 :
            ymin=1
        if ymax>=height :
            ymax=height-1 
        if xmin>=xmax or ymin>=ymax:
            continue  #jump this iteration of the loop
        #check has been passed:
        bbnum=bbnum+1
        #     
        node4 = ET.SubElement(root, "object")
        ET.SubElement(node4, "name").text = classlabel       #-------------------
        ET.SubElement(node4, "pose").text = "unknow"
        ET.SubElement(node4, "truncated").text = "1"
        ET.SubElement(node4, "difficult").text = "0"
        #
        node5 = ET.SubElement(node4, "bndbox")
        ET.SubElement(node5, "xmin").text = str(xmin)
        ET.SubElement(node5, "ymin").text = str(ymin)
        ET.SubElement(node5, "xmax").text = str(xmax)
        ET.SubElement(node5, "ymax").text = str(ymax)
    # noBBox turn none
    if bbnum==0:
        return None
    else:    
        return ET.ElementTree(root)
              

#------------------------ main ------------------------

###--- setting ---###
LABEL_NAME = "person"
Ann_path = "/.../test/0515tt/anno_new/"
Img_path = "/.../test/0515tt/img_new/"

OUTPUT_DIR = "/.../test/0515tt/2-NEW_rotate/"
Ann_path2 = OUTPUT_DIR + "Anno/"
Img_path2 = OUTPUT_DIR + "IMG/"
###------

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
if not os.path.exists(Ann_path2):
    os.makedirs(Ann_path2)
if not os.path.exists(Img_path2):
    os.makedirs(Img_path2)

for xml_file in sorted(os.listdir(Ann_path)):
    print xml_file
    pp = Ann_path + xml_file
    fname = xml_file.split(".")[0]
    im_file = Img_path +fname + ".jpg"
    im = cv2.imread(im_file)
    im_H,im_W = im.shape[0:2]
    #
    tree = read_xml(pp)  
    p = find_nodes(tree,"object")
    bb = []
    for i in xrange(len(p)):
        try:
            #obj_id=p[i][0].text = str(int(float(p[i][0].text))) 
            xmin=int(float(p[i][4][0].text))   #xmin
            ymin=int(float(p[i][4][1].text))   #ymin
            xmax=int(float(p[i][4][2].text))   #xmax
            ymax=int(float(p[i][4][3].text))   #ymax
            bbox = (xmin,ymin,xmax,ymax)
            bb.append(bbox)
        except:
            pass
    #write_xml(tree, pp)  
    #---xml---#
    tree = VOCxml(fname+"_r00" , im, LABEL_NAME, bb)
    if(tree!=None):
        tree.write(Ann_path2 + fname + "_r00.xml") 
        #print "---1---",im.shape
        im2 = copy.deepcopy(im)
        cv2.imwrite(Img_path2 + fname +"_r00.jpg",im)
        im_r90 = imutils.rotate_bound(im2, 90)
        im_r180 = imutils.rotate_bound(im2, 180)
        im_r270 = imutils.rotate_bound(im2, 270)
        #====
        cv2.imwrite(Img_path2 + fname +"_r90.jpg",im_r90)
        tree90 = VOCxml90(fname+"_r90", im_r90, LABEL_NAME, bb,int(im_H),int(im_W))
        tree90.write(Ann_path2 + fname + "_r90.xml")           
        #
        cv2.imwrite(Img_path2 + fname +"_r180.jpg",im_r180)
        tree180 = VOCxml180(fname+"_r180", im_r180, LABEL_NAME, bb,int(im_H),int(im_W))
        tree180.write(Ann_path2 + fname + "_r180.xml") 
        #
        cv2.imwrite(Img_path2 + fname +"_r270.jpg",im_r270)
        tree270 = VOCxml270(fname+"_r270", im_r270, LABEL_NAME, bb, int(im_H),int(im_W))
        tree270.write(Ann_path2 + fname + "_r270.xml")             

