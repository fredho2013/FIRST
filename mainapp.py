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
        print("self of Main_APP: ",self)
        self.__root = root = Tk()
        root.title("飞机大战(达内科技)")
        from skycanvas import SkyCanvas
        self.__canvas = canvas = SkyCanvas(root, width=480, height=654)
        canvas.pack()

        # 处理按键事件和鼠标事件
        from gamelist import EventList
        #F: 创建能够接收控制事件的列表 (pause_button, hero_plane....
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
        self.__plane_label   = PlaneLabel(canvas, count=self.__life_count)

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
        #for i in event_list.get_objs():
        #    print(i)
        #print("@@@@@@@@@@@@@@@@@@@@@@@222")
        #for i in time_list.get_objs():
        #    print(i)

    def create_backgound(self):
        from background import Background
        self.__background = background = Background(self.__canvas)
        self.__timer_list.append(background)

    def create_new_hero(self):
        from heroplane import HeroPlane
        self.__hero_plane = hero_plane = HeroPlane(
            self.__canvas, destroy_cb=self.hero_crush)
        self.__event_list.append(hero_plane)
        self.__timer_list.append(hero_plane)
        self.__life_count -= 1
        self.__plane_label.set_count(self.__life_count)

    def destroy_object(self, obj):
        """删除对象"""
        self.__timer_list.remove(obj)
        self.__event_list.remove(obj)
        self.__enemy_list.remove(obj)

    def start_game(self):
        print("self in start game: ", self)
        self.__timer_list.append(self.__start_window)
        self.__event_list.remove(self.__start_window)
        del self.__start_window  # ??????????????????????????????
        self.start_timer()  #

        #F: plane is a class object randomly selected from random list
        #F: ramdome list: 500 "None" + 3 types enemy plane 
    def random_enemys(self):
        plane = random.choice(self.__random_list)
        if plane:
            ep = plane(self.__canvas, destroy_cb=self.destroy_object)
            self.__timer_list.append(ep)
            self.__enemy_list.append(ep)

    def hero_crush(self, obj):
        '''飞机坠落'''
        # print('''飞机坠落''')
        self.destroy_object(obj) #obj = self.__hero_plane
        self.__hero_plane = None
        if self.__life_count > 0:
            self.create_new_hero()
            # print("剩余生命数为:", self.__life_count)
        else:
            self.game_over()

    def game_over(self):
        self.stop_timer()
        self.__event_list.clear()
        self.__timer_list.clear()
        # self.__enemy_list.clear()
        from game_over import Gameover
        self.__gameover = Gameover(self.__canvas)
        print("游戏结束")

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

    def increase_score(self, score):
        assert type(score) is int, "成现必须为int值"
        self.__score += score
        if score:
            self.__score_label.set_score(self.__score)

    def on_timer(self):
        # 再次启动定时器
        #print("1st line 定时器 in on_timer: ", self.timer_id)
        self.timer_id = self.__canvas.after(
            self.__timer_interval, self.on_timer)  # 让定时器重复启动
        #print("after 定时器 in on_timer: ", self.timer_id)
        self.on_timer_tick()
        self.__tick_count += 1
        if self.__tick_count == 25:
            self.__tick_count = 0
            #self.on_timer_second()
        #print("last 定时器 in on_timer: ", self.timer_id)

    def start_timer(self):        
        self.timer_id = self.__canvas.after(
            self.__timer_interval, self.on_timer)
        #print("已启动定时器 in start_timer: ", self.timer_id)

    def stop_timer(self):
        self.__canvas.after_cancel(self.timer_id)  # 取消定时器
        # print("定时器已取消!")

    def on_timer_tick(self):
        '''定时器触发时调用此方法'''
        # 刷新背景图
        if self.__timer_list.on_timer():
            return
        # 随机生成敌机
        self.random_enemys()
        # 检测飞机得分及飞机是否飞机被摧毁
        if self.__hero_plane:
            score = self.__hero_plane.check_attack(
                self.__enemy_list.get_objs())
            self.increase_score(score)

    def on_timer_second(self):
        '''定时器每秒钟调用一次此方法'''
    # def __del__(self):
    #     print("PauseWidget 对象已销毁")
        if len(self.__random_list) > self.__min_list_len:
            self.__random_list.pop()

    def __del__(self):
        self.stop_timer()

    def run(self):
        # 进入主事件循环
        self.__root.mainloop()


if __name__ == '__main__':
    app = MainApp()
    app.run()
