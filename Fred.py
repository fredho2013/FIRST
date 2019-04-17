#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Author : 魏明择(达内北京)
# Date   : 2018
# 版权所有©


'''《飞机大战》游戏的主运行模块

此模块为....
'''


# 以下为了同时赚容python2和python3
import sys
if (sys.version_info > (3, 0)):
    from tkinter import *
else:
    from Tkinter import *

import random


class MainApp:
    def __init__(self):
        self.__root = root = Tk()
        root.title("飞机大战(达内科技)")
        from skycanvas import SkyCanvas #F画布
        self.__canvas = canvas = SkyCanvas(root, width=480, height=654)
        canvas.pack()

        # 处理按键事件和鼠标事件
        from gamelist import EventList

        # 创建能够接收控制事件的列表 (pause_button, hero_plane, 
        self.__event_list = event_list = EventList()  # 创建能够接收控制事件的列表
        root.bind('<Key>', lambda event: event_list.on_key_down(event))
        root.bind('<KeyRelease>', lambda event: event_list.on_key_up(event))
        root.bind('<Button>', lambda event: event_list.on_mouse_down(event))
        root.bind('<Motion>', lambda event: event_list.on_mouse_move(event))
        root.bind('<ButtonRelease>',
                  lambda event: event_list.on_mouse_up(event))

        # 创建游戏中能接收定时器事5件的列表
        from gamelist import TimerList
        self.__timer_list = time_list = TimerList()
        self.__timer_interval = 40  # 设定刷新时间为40ms
        self.__tick_count = 0

        # 创建敌方武器对象列表
        from gamelist import GameList
        self.__enemy_list = GameList()
        # 创建游戏方的武器对象列表
        # self.player_list = GameList()

        self.create_backgound()

        self.__life_count = 3  # 生命数

        # 创建飞机个数的图标
        from planes_label import PlaneLabel
        self.__plane_label = PlaneLabel(canvas, count=self.__life_count)

        self.create_new_hero()

        # 创建得分标签:
        from score_label import ScoreLabel
        self.__score_label = ScoreLabel(canvas)
        self.__score = 0

        # 创建暂停按钮
        from pause_button import PauseButton
        self.__pause_btn = PauseButton(canvas, callback=self.pause_game)
        self.__event_list.append(self.__pause_btn)

        from enemy_plane import EnemyPlane1, EnemyPlane2, EnemyPlane3, EnemyPlane1_2
        self.__random_list = [EnemyPlane1] * 10 + \
            [EnemyPlane2] * 3 + [EnemyPlane3] + [EnemyPlane1_2] * 2
        self.__min_list_len = len(self.__random_list)
        self.__random_list.extend([None] * 500)
        # self.__random_list = [EnemyPlane1] * 10 + [EnemyPlane2] * 3 + [EnemyPlane3] + [None] * 10

        from startwindow import StartWindow
        self.__start_window = start_window = StartWindow(
            canvas, start_callback=self.start_game, destroy=self.destroy_object)
        event_list.append(start_window)      

    def create_backgound(self):
        from background import Background
        self.__background = background = Background(self.__canvas)
        self.__timer_list.append(background)
    def on_timer(self):
        # 再次启动定时器
        self.timer_id = self.__canvas.after(
            self.__timer_interval, self.on_timer)  # 让定时器重复启动
        self.on_timer_tick()
        self.__tick_count += 1
        if self.__tick_count == 25:
            self.__tick_count = 0
            self.on_timer_second()

    def start_timer(self):
        # print("已启动定时器")
        self.timer_id = self.__canvas.after(
            self.__timer_interval, self.on_timer)
    def on_timer_tick(self):
        '''定时器触发时调用此方法'''
        # 刷新背景图
        if self.__timer_list.on_timer():
            return

        # 随机生成敌机
        self.random_enemys()
        # 检测飞机得分及飞机是否飞机被摧毁
        #if self.__hero_plane:
        #    score = self.__hero_plane.check_attack(
        #        self.__enemy_list.get_objs())
        #    self.increase_score(score)

    # Fred: What would happen when random list > list_len?
    def on_timer_second(self):
        '''定时器每秒钟调用一次此方法'''
        if len(self.__random_list) > self.__min_list_len:
            self.__random_list.pop()

    def start_game(self):
        self.__timer_list.append(self.__start_window)
        self.__event_list.remove(self.__start_window)
        del self.__start_window  # ??????????????????????????????
        self.start_timer() 
    
    def pause_game(self):
        # print("游戏已暂暂停....")
        self.stop_timer()
        from resume_widget import ResumeWidet
        self.resume_widget = ResumeWidet(
            self.__canvas, resume_cb=self.begin_resume_game, destroy_cb=self.resume_game)
        self.__event_list.append(self.resume_widget)

    def begin_resume_game(self):
        '''开始恢复游戏进入恢复倒计时'''
        # print("游戏开始恢复!!!!!")
        self.__event_list.remove(self.resume_widget)
        self.__timer_list.append_head(self.resume_widget)
        self.start_timer()
        pass

    def resume_game(self):
        '''已恢复，正式开战'''
        # print("游戏已恢复!!!!!")
        self.__timer_list.remove(self.resume_widget)
        del self.resume_widget
    def __del__(self):
        self.stop_timer()

    def stop_timer(self):
        self.__canvas.after_cancel(self.timer_id)  # 取消定时器
        # print("定时器已取消!")   
    def destroy_object(self, obj):
        """删除对象"""
        self.__timer_list.remove(obj)
        self.__event_list.remove(obj)
        self.__enemy_list.remove(obj)
    def create_new_hero(self):
        from heroplane import HeroPlane
        self.__hero_plane = hero_plane = HeroPlane(
            self.__canvas, destroy_cb=self.hero_crush)
        self.__event_list.append(hero_plane)
        self.__timer_list.append(hero_plane)
        self.__life_count -= 1
        self.__plane_label.set_count(self.__life_count)
    def hero_crush(self, obj):
        '''飞机坠落'''
        # print('''飞机坠落''')
        self.destroy_object(self.__hero_plane)
        self.__hero_plane = None
        if self.__life_count > 0:
            self.create_new_hero()
            # print("剩余生命数为:", self.__life_count)
        else:
            self.game_over()

    def random_enemys(self):
        plane = random.choice(self.__random_list)
        if plane:
            ep = plane(self.__canvas, destroy_cb=self.destroy_object)
            self.__timer_list.append(ep)
            self.__enemy_list.append(ep)

    def run(self):
        # 进入主事件循环
        self.__root.mainloop()


if __name__ == '__main__':
    app = MainApp()
    app.run()


#timer list: 
#self.__timer_list.append(background)
#self.__timer_list.append(hero_plane)
#self.__timer_list.append(self.__start_window)
#self.__timer_list.append(ep)  ## enemy plan
#self.__timer_list.append_head(self.resume_widget)

# why resume_widget put at head of time_list?
# ANS: resume_widget 的 on_timer 


#event_list
#self.__event_list.append(self.__pause_btn)
#event_list.append(start_window)
#self.__event_list.append(hero_plane)
#self.__event_list.append(self.resume_widget)
#這些 object 會受到 event(mouse, keyboard) 的影響
#當有 event 時, event_list 內的 object 會 一個一個去 執相對應 的 fucntion

#background
 有 2 個 一樣的 background image 同時隨時間往下移動。 當 buttom image lower than window, 
 move the image to upper (y-pos = y-pos + 2* image_height)


 # after __init__

event_list
<heroplane.HeroPlane object at 0x7f850794d2b0>
<pause_button.PauseButton object at 0x7f850794d4e0>
<startwindow.StartWindow object at 0x7f8507963048>
time_list
<background.Background object at 0x7f850794d080>
<heroplane.HeroPlane object at 0x7f850794d2b0>
