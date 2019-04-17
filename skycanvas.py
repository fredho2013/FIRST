# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-

# Author : 魏明择(达内北京)
# Date   : 2018
# 版权所有©


'''飞机大战地图模块

此地图继承自tkinter的canvas #F:check google for detail
'''
import sys

if (sys.version_info > (3, 0)):
    from tkinter import *
    from tkinter import messagebox
else:
    from Tkinter import *

import res


class SkyCanvas(Canvas):
    '''游戏天空画布类

    此类用于创建空战地图画布对象，此画布用于显示飞机对象，子弹对象等
    '''

    def __init__(self, parent, *args, **kwargs):
        super(SkyCanvas, self).__init__(parent, *args, **kwargs)
        # 画布尺寸
        # self.__width = int(canvas.config('width')[-1])
        # self.__height = int(canvas.config('height')[-1])
        self.__width = kwargs.get('width', 100)
        self.__height = kwargs.get('height', 100)

    def width(self):
        return self.__width

    def height(self):
        return self.__height

    def top(self):
        return 0

    def bottom(self):
        return self.__height

    def left(self):
        return 0

    def right(self):
        return self.__width
