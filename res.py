# -*- coding:utf-8 -*-

# Author : 魏明择(达内北京)
# Date   : 2018
# 版权所有©


import sys
import os.path
import os

if (sys.version_info > (3, 0)):
    from tkinter import *
else:
    from Tkinter import *


work_dir = os.getcwd()  # 得到当前的工作路径

paths = [
    'images',
    'weimz/python/project/planwar_project/planewar/images'
]
def load_image(filename):
    '''根据给定的文件名自动找开图片资源返回。
    如果没有找天图片资源则会返回None
    '''
    for pth in paths:
        path1 = os.path.join(pth, filename)
        if os.path.exists(path1):
            return PhotoImage(file=path1)

    # img = None
    # for pth in paths:
    #     path1 = os.path.join(work_dir, pth, filename)
    #     if os.path.exists(path1):
    #         img = PhotoImage(file=path1)
    # # print("加载图片: ", filename, '宽:', img.width(), "高:", img.height(), path1)
    # return img



    