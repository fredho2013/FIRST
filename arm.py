# -*- coding:utf-8 -*-

class Arm:
    '''此类是武器类的基类，用来检测的碰幢条件等'''
    def __init__(self, *, position=None , size=(2, 2), speed=(0, 3)):
        if position is None:
            position = [0, 0]
        self.__pos = list(position)  # 中心点(列表)
        self.__size = size # 宽和高(元组)
        self.__speed = speed # 默认移动速度

    def set_position(self, position):
        self.__pos[:] = position

    def left(self):
        '''得到左边的x坐标'''
        return self.__pos[0] - self.__size[0] / 2

    def right(self):
        '''得到右边的x坐标'''
        return self.__pos[0] + self.__size[0] / 2

    def bottom(self):
        '''得到底边的y坐标'''
        return self.__pos[1] + self.__size[1] / 2

    def top(self):
        '''得到顶边的y坐标'''
        return self.__pos[1] - self.__size[1] / 2

    def get_size(self):
        '''得到飞行器的宽和高的元组: (宽, 高)'''
        return self.__size

    def width(self):
        '''返回飞行器的宽度'''
        return self.__size[0]

    def height(self):
        '''返回飞行器的高度'''
        return self.__size[1]

    def pos(self):
        '''返回飞行器的中心位置'''
        return self.__pos

    def int_position(self):
        '''返回飞行器的中心位置'''
        return (int(self.__pos[0]), int(self.__pos[1]))

    def move(self, offset=None):
        '''移动位置'''
        if offset:
            self.__pos[0] += offset[0]
            self.__pos[1] += offset[1]
        else:
            self.__pos[0] += self.__speed[0]
            self.__pos[1] += self.__speed[1]

    def is_touch(self, other):
        '''检测两个物体是否碰幢。如果碰幢返回True,否则返回False'''
        if self.bottom() < other.top():
            return False
        if self.top() > other.bottom():
            return False
        if self.left() > other.right():
            return False
        if self.right() < other.left():
            return False
        return True
