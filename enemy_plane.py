# -*- coding:utf-8 -*-

# Author : 魏明择(达内北京)
# Date   : 2018
# 版权所有©


import res

from aerocraft import Aerocraft


class EnemyPlane1(Aerocraft):
    '''敌机类1'''
    __images = [
        res.load_image('enemy1.gif'),
        res.load_image('enemy1_down1.gif'),
        res.load_image('enemy1_down2.gif'),
        res.load_image('enemy1_down3.gif'),
        res.load_image('enemy1_down4.gif'),
    ]

    def __init__(self, canvas, *, destroy_cb=None):
        super().__init__(canvas,
                         image=self.__images[0], destroy_images=self.__images[1:], destroy_cb=destroy_cb, speed=(0, 5))

    # def __del__(self):
    #     print("EnemyPlane1 对象已销毁")


class EnemyPlane1_2(Aerocraft):
    '''敌机类1'''
    __images = [
        res.load_image('enemy1.gif'),
        res.load_image('enemy1_down1.gif'),
        res.load_image('enemy1_down2.gif'),
        res.load_image('enemy1_down3.gif'),
        res.load_image('enemy1_down4.gif'),
    ]

    def __init__(self, canvas, *, destroy_cb=None):
        super().__init__(canvas,
                         image=self.__images[0], destroy_images=self.__images[1:], destroy_cb=destroy_cb, speed=(0, 7))

    # def __del__(self):
    #     print("EnemyPlane1_2 对象已销毁")

class EnemyPlane2(Aerocraft):
    '''敌机类1'''
    __images = [
        res.load_image('enemy2.gif'),
        res.load_image('enemy2_down1.gif'),
        res.load_image('enemy2_down2.gif'),
        res.load_image('enemy2_down3.gif'),
        res.load_image('enemy2_down4.gif'),
    ]

    def __init__(self, canvas, *, destroy_cb=None):
        super().__init__(canvas,
                         image=self.__images[0], destroy_images=self.__images[1:], destroy_cb=destroy_cb, speed=(0, 4))

    # def __del__(self):
    #     print("EnemyPlane2 对象已销毁")


class EnemyPlane3(Aerocraft):
    '''敌机类3'''
    __images = [
        res.load_image('enemy3_n1.gif'),
        res.load_image('enemy3_hit.gif'),
        res.load_image('enemy3_down1.gif'),
        res.load_image('enemy3_down2.gif'),
        res.load_image('enemy3_down3.gif'),
        res.load_image('enemy3_down4.gif'),
        res.load_image('enemy3_down5.gif'),
        res.load_image('enemy3_down6.gif'),
    ]

    def __init__(self, canvas, *, destroy_cb=None):
        super().__init__(canvas,
                         image=self.__images[0], destroy_images=self.__images[1:], destroy_cb=destroy_cb, speed=(0, 2))

    # def __del__(self):
    #     print("EnemyPlane3 对象已销毁")
