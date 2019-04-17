# -*- coding:utf-8 -*-

# Author : 魏明择(达内北京)
# Date   : 2018
# 版权所有©


import res


class PlaneLabel:
    '''此类用于描述飞机个数的图片控件'''
    __image = res.load_image("plane_count.gif")

    def __init__(self, canvas, *, count=0):
        self.__canvas = canvas
        image = self.__image
        self.__pos = position = (
            image.width() * .75, canvas.height() - image.height() * .75)
        self.__images_id = self.__canvas.create_image(*position,
                                                      image=self.__image)
        self.__size = size = (image.width(), image.height())  # 宽和高(元组)

        text = self.__get_str(count)
        self.__font_id = canvas.create_text(position[0],
                                            position[1]+20,
                                            text=text,
                                            font=("黑体", 18),
                                            fill='#333')

    def set_count(self, count):
        self.__canvas.itemconfigure(self.__font_id, text=self.__get_str(count))
        self.__canvas.tag_raise(self.__images_id)
        self.__canvas.tag_raise(self.__font_id)

    def __get_str(self, n):
        return "x" + str(n)
