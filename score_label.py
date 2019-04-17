# -*- coding:utf-8 -*-

# Author : 魏明择(达内北京)
# Date   : 2018
# 版权所有©


import res

class ScoreLabel:
    '''此类用于描述得到条'''
    def __init__(self, canvas):
        self.__canvas = canvas
        # self.__pos = position = (image.width() * .75, canvas.height() - image.height()  * .75)
        self.__pos = position = (canvas.width() / 2, 35)
        text = self.__get_str(0)
        self.__font_id = canvas.create_text(*position,
                                             text=text,
                                             font=("黑体", 30),
                                             fill='#333')


    def set_score(self, s):
        self.__canvas.itemconfigure(self.__font_id, text=self.__get_str(s))

    @staticmethod
    def __get_str(n):
        return "得分:" + str(n)
