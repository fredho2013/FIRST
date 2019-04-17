# -*- coding:utf-8 -*-

# Author : 魏明择(达内北京)
# Date   : 2018
# 版权所有©

import res

from gamelist import EventObject
#self.resume_widget = ResumeWidet(
 #           self.__canvas, resume_cb=self.begin_resume_game, destroy_cb=self.resume_game)

class ResumeWidet(EventObject):
    '''此类用于描述临停窗口'''
    __image = res.load_image("pause.gif")

    # 此窗口的状态:
    # NORMAL = 1  # 显示状态
    # DESTROY = 2  # 销毁状态
    def __init__(self, canvas, *, resume_cb=None, destroy_cb=None):
        # self.__status = self.NORMAL  # 设置显示状态
        self.__canvas = canvas
        self.__image_id = self.__canvas.create_image(canvas.width() / 2, canvas.height() / 2,
                                                     image=self.__image)
        self.__resume_cb = resume_cb
        self.__destroy_cb = destroy_cb
        self.__destroy_count = 75
        print("in resume Fred")

    # def __del__(self):
    #     print("PauseWidget 对象已销毁")

    def resume(self):
        if self.__resume_cb:
            self.__resume_cb()
        self.__canvas.delete(self.__image_id)
        canvas = self.__canvas
        self.__image_id = canvas.create_text(canvas.width() / 2,
                                             canvas.height() / 2,
                                             text="3",
                                             font=("黑体", 200),
                                             fill='yellow')

    def on_key_down(self, event):
        '''处理按键按下'''
        if event.keysym == 'r':
            self.resume()
            print("Fred in resume on_key_down")
        return True

    def on_mouse_down(self, event):
        '''处理鼠标左键按键按下'''
        if event.num == 1:
            self.resume()
        return True

    def on_timer(self):
        self.__destroy_count -= 1
        if self.__destroy_count % 25 == 0:
            n = self.__destroy_count // 25
            self.__canvas.itemconfigure(self.__image_id, text=str(n))
        if self.__destroy_count <= 0:
            self.__canvas.delete(self.__image_id)
            if self.__destroy_cb:
                self.__destroy_cb()
        return True
