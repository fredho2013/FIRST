# -*- coding:utf-8 -*-

# Author : 魏明择(达内北京)
# Date   : 2018
# 版权所有©


import res

class HeroPlaneImageManager:
    '''此对象负责处理图片切换，但并不关心图片位置'''
    def __init__(self, canvas, image_id, images, position=None):
        self.__canvas = canvas  # 画布
        self.__image_id = image_id  # 图片ID
        self.__images = images  # 要切换的图
        self.__position = position

        self.__accelerator = False  # 加速状态(默认不加速)
        self.__will_accelerator = False  # 下次更新时要转换的状态状态
        if position:
            canvas.coords(image_id, *position)

    def set_acelerator(self, will=True):
        '''设置加速状态'''
        self.__will_accelerator = will  # 设置即要触发指令

    def draw(self, position):
        '''
        更新图片，并刷新图片及更新图片位置
        args 如果不为空，则记录当前的新位置
        '''
        if self.__accelerator != self.__will_accelerator:  # 状态有所变量
            # 需发重新设置图片
            if self.__will_accelerator:
                self.__canvas.itemconfigure(
                    self.__image_id, image=self.__images[1])
            else:
                self.__canvas.itemconfigure(
                    self.__image_id, image=self.__images[0])
            self.__accelerator = self.__will_accelerator  # 状态切换完毕
        if self.__position != position:
            self.__canvas.coords(self.__image_id, *position)
            self.__position = position


from aerocraft import DestroyImageAnimate
from aerocraft import FlyingImageManager
from arm import Arm


class Bullet(Arm):
    __images = [
        res.load_image("bullet.gif")
    ]
    # image = res.load_image("bullet.gif")

    def __init__(self, canvas,  *, position, destroy_cb=None):
        self.__canvas = canvas
        image = self.__images[0]
        # 先算宽和高
        size = (image.width(), image.height())
        self.__image_id = canvas.create_image(*position, image=image)
        # self.__image = image
        self.__destroy_cb = destroy_cb

        super().__init__(position=position, size=size, speed=(0, -20))
        # 图片管理器
        self.__image_manager = FlyingImageManager(canvas,
                                                  self.__image_id,
                                                  position)

    def set_destroy(self):
        '''设置为击中销毁状态'''
        self.__canvas.delete(self.__image_id)
        if self.__destroy_cb:
            self.__destroy_cb(self)
   
    def on_timer(self):
        self.move()
        self.__image_manager.draw(self.pos())
        if self.pos()[1] < 0:
            self.set_destroy()



from arm import Arm


class HeroPlane(Arm):
    """此类是英雄飞机类,此类继承自飞机对象，所有的飞机地象有相同的行为:
    移动、发射子弹等的对象是一个或多个同样的英雄飞机
    """
    __images = [
        res.load_image("hero2.gif"),
        res.load_image("hero1.gif"),
        res.load_image("hero_blowup_n1.gif"),
        res.load_image("hero_blowup_n2.gif"),
        res.load_image("hero_blowup_n3.gif"),
        res.load_image("hero_blowup_n4.gif"),
    ]
    # 飞机的状态:
    NORMAL = 1  # 正常飞行状态
    DESTROY = 2  # 被击中状态，正在销毁中

    def __init__(self, canvas, *, destroy_cb=None):

        self.__status = self.NORMAL  # 设置飞行状态为正常飞行
        self.__canvas = canvas
        self.__destroy_cb = destroy_cb

        image = self.__images[0]
        # self.old_image = self.new_image = self.__images[0]  # 设置当前显示图片

        # 画布尺寸
        canvas_width = canvas.width()
        canvas_height = canvas.height()
        # canvas_width = int(canvas.config("width")[-1])
        # canvas_height = int(canvas.config("height")[-1])

        # 计算飞机能够飞行的的上下左右边缘
        self.__left_side = image.width()/2  # 左边缘
        self.__right_side = canvas_width - image.width()/2  # 右边缘
        self.__top_side = image.height()/2  # 上边缘
        self.__bottom_side = canvas_height - image.height()/2  # 下边缘

        # 把飞机的初始放在图片的底部 (x坐标，y轴坐标)
        x = int(canvas_width / 2)
        y = int(canvas_height - image.height() / 2)
        pos = (x, y)
        # self.set_position((x, y))
        size = (image.width(), image.height())
        super().__init__(position=pos, size=size)

        # 此集合用于存放用户操作的按键或鼠标事件
        self.__key_evens = set()

        # 设置飞机的初始图片
        self.__image_id = canvas.create_image(pos, image=image)

        # 正常飞行时采用正常飞行图片管理器
        self.__image_manager = HeroPlaneImageManager(canvas,
                                                     self.__image_id,
                                                     self.__images[:2],
                                                     pos)
        # 鼠示的按下状态
        self.__mouse_down = False

        # -----子弹相关----
        from gamelist import TimerList
        self.__bullet_list = TimerList()
        self.__bullet_interval = 10  # 每秒钟2.5 发子弹
        self.__bullet_count = 0  # 子弹计数
    
    # def __del__(self):
    #     print("英雄飞机已销毁..........")

    def destory_self(self):
        self.__image_manager = None
        self.__canvas.delete(self.__image_id)
        self.__bullet_list.clear()
        if self.__destroy_cb:
            self.__destroy_cb(self)

    def is_flying(self):
        '''判断是否是正常飞行状态'''
        return self.__status == self.NORMAL

    def is_destroy(self):
        '''判断是否是击中销毁状态'''
        return self.__status == self.DESTROY

    def set_destroy(self):
        '''设置为击中销毁状态'''
        self.__status = self.DESTROY
        # self.__image_manager = DestroyImageAnimate(self.__canvas,
        #                                             self.__image_id,
        #                                             self.__destroy_images,
        #                                             callback=self.destory_self)
        self.__image_manager = DestroyImageAnimate(
            self.__canvas, self.__image_id, self.__images[2:],
            callback=self.destory_self)

    def __adjust_pos(self, position):
        '''校正飞机的坐标，如果超出地图，则修改正回来'''
        x, y = position
        if x < self.__left_side:
            x = self.__left_side
        if x > self.__right_side:
            x = self.__right_side
        if y < self.__top_side:
            y = self.__top_side
        if y > self.__bottom_side:
            y = self.__bottom_side
        super().set_position((x, y))

    def set_position(self, position):
        self.__adjust_pos(position)

    def move(self, offset):
        '''根据偏移量移动，当超出范围时较正位置'''
        x, y = self.pos()
        x += offset[0]
        y += offset[1]
        self.__adjust_pos((x, y))
        if offset[1] < 0:
            self.__image_manager.set_acelerator()
        else:
            self.__image_manager.set_acelerator(False)

    def on_key_down(self, event):
        '''处理按键按下'''
        # 当有铵键按下,把按键加入到集合中记录下来
        self.__key_evens.add(event.keysym.lower())

    def on_key_up(self, event):
        '''处理按键抬起'''
        # 当有铵键抬起,把按键从集合中移除
        self.__key_evens.discard(event.keysym.lower())

    def on_mouse_down(self, event):
        '''处理鼠标左键按键按下'''
        if event.num == 2:
            # self.set_destroy()
            self.fire()
            return
        if event.num != 1:
            return

        self.__mouse_down = True
        self.mouse_pos = (event.x, event.y)

    def on_mouse_up(self, event):
        '''处理鼠标左键按键抬起'''
        if event.num != 1:
            return
        self.__mouse_down = False
        if self.is_flying():
            self.__image_manager.set_acelerator(False)

    def on_mouse_move(self, event):
        '''处理鼠标左键按下的同时移动'''
        if not self.__mouse_down:
            return

        # x = event.x
        # y = event.y
        offset = (event.x - self.mouse_pos[0], event.y - self.mouse_pos[1])
        self.mouse_pos = (event.x, event.y)  # 用新位置替换旧位置
        self.move(offset)

    def process_key_event(self):
        '''检查键盘状态，计算飞机飞行移动位置'''
        if self.is_destroy():  # 如果飞机已被击中，键盘无效
            return
        if self.__mouse_down:
            return

        assert self.is_flying()
        speed = 5
        self.__image_manager.set_acelerator(False)
        if 'a' in self.__key_evens or 'left' in self.__key_evens:
            self.move((-speed, 0))
        if 'd' in self.__key_evens or 'right' in self.__key_evens:
            self.move((speed, 0))
        if 'w' in self.__key_evens or 'up' in self.__key_evens:
            self.move((0, -speed))
            self.__image_manager.set_acelerator()
        if 's' in self.__key_evens or 'down' in self.__key_evens:
            self.move((0, speed))

    def fire(self):
        '''英雄飞机开火 '''
        x, y = self.pos()
        # y -= 60

        if False:
            # 单子弹位置(0, -60)
            pos = (x, y-60)
            b1 = Bullet(self.__canvas, position=pos,
                        destroy_cb=self.__bullet_list.remove)
            self.__bullet_list.append(b1)
        else:
            # 双子弹位置(-32, -18)和 (32, -18)
            pos1 = (x-32, y-18)
            pos2 = (x+32, y-18)
            b1 = Bullet(self.__canvas, position=pos1, destroy_cb=self.__bullet_list.remove)
            self.__bullet_list.append(b1)
            b1 = Bullet(self.__canvas, position=pos2, destroy_cb=self.__bullet_list.remove)
            self.__bullet_list.append(b1)

    def check_attack(self, lst):
        '''此方法检测英雄飞机及子弹是否打印敌机，以及是否与英雄飞机进行碰幢
        返回元组:
           第一个元素: 飞机是否幢True/False
           第二个元素: 本次得分
           return (False, 20)  # 本次得到20飞机没有被幢到
        '''
        score = 0
        # 检查子弹是否打到敌机
        i = 0
        bullet_list = self.__bullet_list.get_objs()
        while i < len(bullet_list):
            bullet = bullet_list[i]
            for j, ep  in enumerate(lst):
                if bullet.is_touch(ep):
                    ep.set_destroy()
                    del lst[j]
                    bullet.set_destroy()
                    score += 1
                    break
            else:
                i += 1

        # 检查飞机是否被幢 
        for i, ep in enumerate(lst):
            if self.is_touch(ep):
                ep.set_destroy()
                self.set_destroy()
                del lst[i]
                break
        return score

    # def is_touch(self, other):
    #     '''自定义飞机的碰幢检测'''
    #     if super().is_touch(other):
    #         return True
    #     return False

    def on_timer(self):
        if self.is_flying():
            self.process_key_event()  # 先处理按键事件
            # --- begin处理子弹是否发射---------
            self.__bullet_count += 1
            if self.__bullet_count >= self.__bullet_interval:
                self.__bullet_count = 0
                self.fire()
            # --- end 处理子弹是否发射---------
            self.__image_manager.draw(self.int_position())
        elif self.is_destroy():
            if self.__image_manager:
                self.__image_manager.draw()
        self.__bullet_list.on_timer()
