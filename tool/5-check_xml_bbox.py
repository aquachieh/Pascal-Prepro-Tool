
'''
5-check_xml_bbox.py
--step1-- modify bbox and remove too small object
--step2-- check labelname & remove 0 object xml/img

'''

from xml.etree.ElementTree import ElementTree,Element
import os

### --- setting
BboxMinWidth = 10    #--- x
BboxMinHeight = 10   #--- y
BboxMinArea = 200    #---x* y

LABEL_NAME = "person"
IMG_DIRPATH = "/.../0515tt/img_new/"
ANNO_DIRPATH = "/.../0515tt/anno_new/"

BboxLimitErr_TEXT = "/.../0515tt/bboxLimitErr.txt"
BboxSizeErr_TEXT = "/.../0515tt/bboxSizeErr.txt"
LabelNameErr_TEXT = "/.../0515tt/labelNameErr.txt"
FinalOkFileList_TEXT = "/.../0515tt/finalOkFileList.txt"

NO_OBJ_DIR = "/.../0515tt/NO_OBJ/"
NO_OBJ_IMG_DIR = NO_OBJ_DIR + "img_NO_OBJ/"
NO_OBJ_ANNO_DIR = NO_OBJ_DIR + "anno_NO_OBJ/"
### ------

if not os.path.exists(NO_OBJ_DIR):
    os.makedirs(NO_OBJ_DIR)
if not os.path.exists(NO_OBJ_IMG_DIR):
    os.makedirs(NO_OBJ_IMG_DIR)
if not os.path.exists(NO_OBJ_ANNO_DIR):
    os.makedirs(NO_OBJ_ANNO_DIR)

def read_xml(in_path):
  tree = ElementTree()
  tree.parse(in_path)
  return tree

def find_nodes(tree, path):
  return tree.findall(path)

###---------------------
#---step1 : modify bbox and remove too small object
newtxt1 = open(BboxLimitErr_TEXT, 'w')
newtxt2 = open(BboxSizeErr_TEXT, 'w')   

for xml_file in os.listdir(ANNO_DIRPATH):
    print "--step1--",xml_file
    pp = ANNO_DIRPATH + xml_file
    filename = xml_file.split(".")[0]
    tree = read_xml(pp)    
    root = tree.getroot()  
    #
    size = root.findall("size")
    ww = size[0].findall("width")[0].text
    hh = size[0].findall("height")[0].text
    size[0].findall("height")[0].text = str(int(float(hh)))  #height  y
    size[0].findall("width")[0].text = str(int(float(ww)))  #width  x
    size_y = int(float(hh))   #---- y
    size_x = int(float(ww))   #---- x
    objs = root.findall("object")
    for oo in objs:
        pp = oo.findall("bndbox")[0] 
        pp[0].text = str(int(float(pp[0].text)))
        pp[1].text = str(int(float(pp[1].text)))
        pp[2].text = str(int(float(pp[2].text)))
        pp[3].text = str(int(float(pp[3].text)))
        xmax = int(float(pp.findall("xmax")[0].text))
        xmin = int(float(pp.findall("xmin")[0].text))
        ymax = int(float(pp.findall("ymax")[0].text))
        ymin = int(float(pp.findall("ymin")[0].text))
        if xmax>=size_x:
            pp.findall("xmax")[0].text = str(size_x-1)
            newtxt1.write(xml_file+"---xmax\n")
        if ymax>=size_y:
            pp.findall("ymax")[0].text = str(size_y-1)
            newtxt1.write(xml_file+"---ymax\n")
        if xmin<=0:
            pp.findall("xmin")[0].text = str(1)
            newtxt1.write(xml_file+"---xmin\n")
        if ymin<=0:
            pp.findall("ymin")[0].text = str(1)
            newtxt1.write(xml_file+"---ymin\n")
        if (xmax-xmin<= BboxMinWidth or ymax-ymin<= BboxMinHeight or (1.0*(xmax-xmin)*(ymax-ymin))<= BboxMinArea ): #-------
            newtxt2.write(xml_file+"---hw\n")
            root.remove(oo) #-----remove too small object
        tree.write(ANNO_DIRPATH + xml_file)
        
newtxt1.close()
newtxt2.close()

###------------------------
##---step2 : check labelname & check len(objs) > 0

text_file = open(LabelNameErr_TEXT, "w") 
ok_file_txt = open(FinalOkFileList_TEXT, "w") 

for xml_file in os.listdir(ANNO_DIRPATH):
    print  "--step2--", xml_file
    filename = xml_file.split('.')[0]
    pp = ANNO_DIRPATH + xml_file
    tree = read_xml(pp)    
    root = tree.getroot()  
    objs = root.findall("object")
    if len(objs) > 0 :
        ok_file_txt.write(filename+"\n")
        for oo in objs:
            if oo[0].text != LABEL_NAME:
                new_line = xml_file + "---" + oo[0].text + "\n"
                text_file.write(new_line)
                oo[0].text = LABEL_NAME    
                tree.write(ANNO_DIRPATH + xml_file)
    else :  # xml has no obj
        os.rename(ANNO_DIRPATH+filename+".xml", NO_OBJ_ANNO_DIR+filename+'.xml')
        os.rename(IMG_DIRPATH+filename+".jpg", NO_OBJ_IMG_DIR+filename+'.jpg')

text_file.close()
ok_file_txt.close()
print "~~~~~ job done ^_^b ~~~~~"



