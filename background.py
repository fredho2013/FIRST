# -*- coding:utf-8 -*-

# Author : 魏明择(达内北京)
# Date   : 2018
# 版权所有©

import res


class Background:
    '''此类用于描述背景对象'''
    __image = res.load_image("background.gif")

    def __init__(self, canvas, *, speed=1):
        self.__canvas = canvas
        self.__speed = speed

        # self.__canvas_height = canvas_height = int(canvas.config("height")[-1])
        self.__image_height = image_height = self.__image.height()

        self.__images_pos = [[0, 0], [0, -image_height]]
        self.__images_id = [self.__canvas.create_image(*pos,
                                                   image=self.__image,
                                                   anchor="nw")
                          for pos in self.__images_pos]

    def on_timer(self):
        '''刷新背景'''
        for pos in self.__images_pos:
            pos[1] += self.__speed
            if pos[1] > self.__image_height:
                pos[1] -= self.__image_height * 2
        for i, pos in enumerate(self.__images_pos):
            self.__canvas.coords(self.__images_id[i], *pos)

