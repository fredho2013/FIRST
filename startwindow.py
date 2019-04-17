# -*- coding:utf-8 -*-

# Author : 魏明择(达内北京)
# Date   : 2018
# 版权所有©

import res

from gamelist import EventObject


class StartWindow(EventObject):
    """此类用于实现开始窗口对象
    """
    __images = [
        res.load_image("start2.gif"),
        res.load_image("start_label.gif")
    ]
    # 此窗口的状态:
    NORMAL = 1  # 显示状态
    DESTROY = 2  # 销毁状态

    def __init__(self, canvas, *, start_callback=None, destroy=None):
        self.__status = self.NORMAL  # 设置显示状态
        self.__canvas = canvas
        self.__start_fn = start_callback
        self.__destroy_cb = destroy

        image = self.__images[0]

        # 画布尺寸
        canvas_width = canvas.width()
        canvas_height = canvas.height()

        self.__pos = [canvas_width / 2, canvas_height / 2 + 3]

        # 设置飞机的初始图片
        self.__image_id = canvas.create_image(*self.__pos, image=image)
        self.__start_id = canvas.create_image(
            self.__pos[0], self.__pos[1] + 20, image=self.__images[1])

    def move(self, offset):
        '''根据偏移量移动，当超出范围时较正位置'''
        self.__pos[0] += offset[0]
        self.__pos[1] += offset[1]

    def start_game(self):
        print("self in startwinodw class: ", self)
        self.__start_fn()
        self.__status = self.DESTROY

    def on_key_down(self, event):
        '''处理按键按下'''
        if event.keysym == 'space':
            self.start_game()
            return True

    def on_mouse_down(self, event):
        '''处理鼠标左键按键按下'''
        if event.num == 1:
            self.start_game()
            return True

    def on_timer(self):
        self.move((0, -20))
        self.__canvas.coords(self.__image_id, *self.__pos)
        self.__canvas.coords(
            self.__start_id, self.__pos[0], self.__pos[1] + 20)
        # if self.__pos[1] < -100 and self.__destroy_cb:  # 调试用
        if self.__pos[1] < -500 and self.__destroy_cb:
            self.__canvas.delete(self.__image_id)
            self.__canvas.delete(self.__start_id)
            self.__destroy_cb(self)
