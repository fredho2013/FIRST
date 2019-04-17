# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-

# Author : 魏明择(达内北京)
# Date   : 2018
# 版权所有©


import res

from gamelist import EventObject


class PauseButton(EventObject):
    '''此类用于描述暂停控件'''
    __image = res.load_image("game_pause_nor.gif")

    def __init__(self, canvas, *, callback=None):
        self.__canvas = canvas
        image = self.__image
        self.__pos = position = (image.width() * 0.75, image.height() * 0.75)
        self.__images_id = self.__canvas.create_image(*position,
                                                      image=self.__image)
        self.__click_cb = callback

        self.__size = (image.width(), image.height())  # 宽和高(元组)

    def on_key_down(self, event):
        '''处理按键按下'''
        if event.keysym == 'p':
            if self.__click_cb:
                self.__click_cb()
                return True

    def is_touch(self, x, y):
        if y > self.__pos[1] + self.__size[1] / 2:
            return False
        if x < self.__pos[0] - self.__size[0] / 2:
            return False
        if x > self.__pos[0] + self.__size[0] / 2:
            return False
        if y < self.__pos[1] - self.__size[1] / 2:
            return False
        return True

    def on_mouse_down(self, event):
        '''处理鼠标左键按键按下'''
        if event.num == 1 and self.is_touch(event.x, event.y):
            if self.__click_cb:
                self.__click_cb()
                return True
