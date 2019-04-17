# -*- coding:utf-8 -*-


from arm import Arm


class FlyingImageManager:
    '''此类的对象只负责处理飞行过程中图片及图片的自动切换，但并不关心图片位置'''
    def __init__(self, canvas, image_id, position=None):
        self.__canvas = canvas  # 画布
        self.__image_id = image_id  # 图片ID
        self.__position = list(position)
        
        if position:
            canvas.coords(image_id, *position)

    def draw(self, position=None):
        '''更新图片，并刷新图片及更新图片位置
        args 如果不为空，则记录当前的新位置
        '''
        if position is None:
            return
        if self.__position != position:
            self.__canvas.coords(self.__image_id, *position)
            self.__position[:] = position

class DestroyImageAnimate:
    '''此对象负责处理图片切换，但并不关心图片位置'''
    def __init__(self, canvas, image_id, images, *, tick_times=5, callback=None):
        self.__canvas = canvas  # 画布
        self.__image_id = image_id  # 图片ID
        self.__images = images  # 要切换的图
        self.__tick_times = tick_times  # ticks 为切换图片的时间／默认为10/25秒换一张片
        self.__callback = callback  # 图片插放完比毕后触发回调

        self.__position = None
        self.__image_index = 0  # 当前图片的索引
        self.__canvas.itemconfigure(self.__image_id, image=images[0])
        self.__cur_ticks = 0

    def draw(self, position=None):
        '''
        更新图片，并刷新图片及更新图片位置
        args 如果不为空，则记录当前的新位置
        '''
        self.__cur_ticks += 1
        if self.__cur_ticks >= self.__tick_times:  # 需要更新图片 或停止动画
            self.__cur_ticks = 0
            self.__image_index += 1
            if self.__image_index >= len(self.__images):
                # 终止动画
                if self.__callback:
                    self.__callback()
            else:
                # 更新画现
                self.__canvas.itemconfigure(self.__image_id, image=self.__images[self.__image_index])

        #if self.__position != position:
        #    self.__canvas.coords(self.__image_id, *position)
        #    self.__position = position


import random  as R

class Aerocraft(Arm):
    '''此类是飞行器类的基类，用来检测飞行器的碰幢条件等'''
    NORMAL = 1  # 正常飞行状态
    DESTROY = 2  # 被击中状态，正在销毁中
    def __init__(self, canvas,  *, position=None, image=None, destroy_images=[], destroy_cb=None, **kwargs):
        self.__status = self.NORMAL  # 设置飞行状态为正常飞行

        self.__canvas = canvas
        # 先算出飞机的宽和高
        size = (image.width(), image.height())
        if position is None:
            # 随机指定飞机的位置
            x = R.randint(int(image.width() / 2), int(canvas.width() - image.width() / 2))
            y = -int(image.height() / 2)
            # 设置飞机的初始图片
            position = [x, y]
        self.__image_id = canvas.create_image(*position, image=image)
        self.__image = image
        self.__destroy_images = destroy_images
        self.__destroy_cb = destroy_cb

        # 把飞机的初始放在图片的上部 (x坐标，y轴坐标)
        super().__init__(position=position, size=size, **kwargs)


        # 正常飞行时采用正常飞行图片管理器
        self.__image_manager = FlyingImageManager(canvas,
                                                    self.__image_id,
                                                    position)
    def set_image_manager(self, image_manager):
        self.__image_manager = image_manager

    def get_image_manager(self):
        return self.__image_manager

    def get_image_id(self):
        return self.__image_id

    def is_flying(self):
        '''判断是否是正常飞行状态'''
        return self.__status == self.NORMAL

    def is_destroy(self):
        '''判断是否是击中销毁状态'''
        return self.__status == self.DESTROY
    def set_destroy(self):
        '''设置为击中销毁状态'''
        self.__status = self.DESTROY
        self.__image_manager = DestroyImageAnimate(self.__canvas,
                                                    self.__image_id,
                                                    self.__destroy_images,
                                                    callback=self.destory_self)
    
    def destory_self(self):
        self.__canvas.delete(self.__image_id)
        self.__image_manager = None
        if self.__destroy_cb:
            self.__destroy_cb(self)
    
    def on_timer(self):
        if self.is_flying():
            self.move()
            self.__image_manager.draw(self.pos())
            # 销毁飞机对象
            if self.pos()[1] > self.__canvas.height() + self.height() / 2:
                # self.set_destroy()
                self.destory_self()
        elif self.is_destroy():
            if self.__image_manager:
                self.__image_manager.draw()


