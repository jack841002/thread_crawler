#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import numpy as np  
from bs4 import BeautifulSoup
import re #抓圖片
from urllib.request import urlretrieve #存照片
import os #為了建立資料夾
import sys #控制抓取文章頁數 system的縮寫
import threading
import time

with open('thread_train_img.txt','r') as fp:
    img = fp.read().splitlines()

errf = open("thread_example.txt", "a")

error=[] #len(img) 16078
outNum = 0 # sync

# num = 10

def func(url):
    global outNum
    lock.acquire()
    time.sleep(0.01)
    #num = num - 1
    
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text,"html.parser")
        if soup.find('div').find('img') != None:
            image = soup.find('div').find('img')['src']
            f = image.split('/')[-1]
            f = f.split('_')[0]
            local = os.path.abspath('./image/{}.jpg'.format(f))
            try:
                urlretrieve(image,local) #image是下載的網址 local是儲存圖片的檔案位址
                outNum = outNum +1
                print("process {} urls ".format(outNum))
            except Exception as e:
                print(url)
                errf.writelines(str(url) + "\n")                
                error.append(url)
                print(e)
        else:
            print(url)
            errf.writelines(str(url) + "\n")
            error.append(url)
    except Exception as e:
        print(url)
        errf.writelines(str(url) + "\n")
        error.append(url)
    
    lock.release()
    #print(num)

threads = []

lock = threading.BoundedSemaphore(10) #最多允許5個執行緒同時執行
for i in range(0,300):
#     print("process {} urls ".format(i+1))
    # errf.writelines(str(i)+'\n')
    url = img[i]    
    t = threading.Thread(target=func,args=(url,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("主執行緒：", threading.current_thread().name)


# In[ ]:




