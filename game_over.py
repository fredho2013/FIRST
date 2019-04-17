# -*- coding:utf-8 -*-

# Author : 魏明择(达内北京)
# Date   : 2018
# 版权所有©


import res


class Gameover:
    '''此类用于描述游戏结束窗口'''
    __image = res.load_image("gameover.gif")

    def __init__(self, canvas):
        self.__canvas = canvas
        self.__images_id = self.__canvas.create_image(canvas.width() / 2, canvas.height() / 2,
                                                      image=self.__image)
