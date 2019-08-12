'''
count_xml(gender)_bbox.py
'''

from xml.etree.ElementTree import ElementTree,Element
import os


LABEL_NAME = ["female","male","unknown"]
num_ff = 0
num_mm = 0
num_uu = 0
num_box = 0

ANNO_DIRPATH = "../1020/Annotations/"

### ------

def read_xml(in_path):
  tree = ElementTree()
  tree.parse(in_path)
  return tree

def find_nodes(tree, path):
  return tree.findall(path)

for xml_file in os.listdir(ANNO_DIRPATH):
    print  "--xml_file--", xml_file
    pp = ANNO_DIRPATH + xml_file
    tree = read_xml(pp)    
    root = tree.getroot()  
    objs = root.findall("object")
    for oo in objs:
        num_box = num_box+1
        if oo[0].text =="female":
            num_ff = num_ff+1
        elif oo[0].text =="male":
            num_mm = num_mm+1
        elif oo[0].text =="unknown":
            num_uu = num_uu+1

num_pic = len(os.listdir(ANNO_DIRPATH))
print "~~~~~ job done ^_^b ~~~~~"
print "num_pic",num_pic
print "num_box:",num_box," num_female:",num_ff," num_male:",num_mm," num_unknown:",num_uu,
