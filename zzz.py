#!/usr/bin/env python
# coding: utf-8

from PIL import Image
import numpy as np
import os
from scipy import spatial
import pandas as pd
# import matplotlib.pyplot as plt



def resizeImg(img_path):
    img = Image.open(img_path)
    img = img.resize((150, 200))

    img_array = np.array(img)
    img_array = img_array.flatten()

    img_array = img_array/255

    return img_array


# In[ ]:


def giveCosDist(target_array, comparison_array):
    return spatial.distance_matrix([target_array], [comparison_array], p=2, threshold=1000)


# In[ ]:


def giveWholeCosDist(style, target_array, path):

    dist = []
    # print("1 OK")

    pics = os.listdir(path)


    for pic in pics:
        # print(pic)
        img_path = path + "\\" + pic

        comparison_array = resizeImg(img_path)
        # print(comparison_array)
        distance = giveCosDist(target_array, comparison_array)
        # print(distance[0][0])
        dist.append(distance[0][0])
    return dist


# In[ ]:


def returnArgsort(style_result):
    style_np = np.array(style_result)
    return style_np.argsort()

#
# path1 = "C:/Users/Seunghee Woo/Downloads/removed/boy/formal"
# file_name = "기타 서울_오진택(31) 22-08-08 조회수20.jpg"
# img_path = path1 + "/" + file_name
#
# # 이미지 변환
# img_array = resizeImg(img_path)
#
# # 변환된 이미지 배열과 코사인 거리 구하기
# dists = giveWholeCosDist("formal", img_array)
#
# # 거리가 작은 순서대로 인덱스 반환하기
# idxs = returnArgsort(dists)
# for idx in idxs[2:3]:
#     idx = int(idx)
#     img_name = os.listdir(path1)[idx]
#     original_path = "C:/Users/Seunghee Woo/Downloads/boy/formal/" + img_name
#     original_img = Image.open(original_path)
#     print(f"target 이미지와의 거리: {dists[idx]}")
#     # plt.imshow(original_img)

