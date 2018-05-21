
### 1-avi2img.py
設定FPS, 跳切frame

-### 2-img_motion_det.py 
篩出有motion的img

### 2-2-img_motion_det.py
篩出有motion的img
先與 background 相減比較
再與 last frame 相減比較
選出兩者都有差距的

#--- 3-labelimg.md
標記資料

### 4-check_anno_match_img.py
檢查xml是否有與img對應
隔離出沒有對應到的img

### 5-check_xml_bbox.py
檢查bbox邊界/大小/label name
拿掉零物件的檔
紀錄 ok_file_list.txt  

### 6-augImg.py
(可選擇不做)
3 way:
  -randomRotateImg.py
  -randomRotateShiftImg.py  (slow)
  -randomRotateCropImg.py
轉完需重新標記 ,可先把轉過的圖存起來,之後有時間再標
(6-->3-->4-->5-->8)

### 7-xmlRotate4deg.py
做 augmentation
將 xml & img 轉 00/90/180/270度 (copy file)

#--- 8-mergeAllData_and_PickOutBm.md
merge all anno/img dir data
Pick out Benchmark(testingdata)

### 9-random_rename.py
亂數打亂檔案序(rename,not copy)
format{0:06}

### 10-anno2txt.py
for Pascal VOC format
creat training file list.txt





