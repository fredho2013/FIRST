
import sys
if (sys.version_info > (3, 0)):
    from tkinter import *
else:
    from Tkinter import *

class GameList:
    def __init__(self):
        self.__objs = []

    def append(self, obj):
        "把需要触发键盘鼠标事件的地象加入到列表的末尾"
        self.__objs.append(obj)
    
    def remove(self, obj):
        for i, o in enumerate(self.__objs):
            if o is obj:
                del self.__objs[i]
                return

    def get_objs(self):
        return self.__objs        
    
    def clear(self):
        self.__objs.clear()

class EventObject:
    '''事件对象类，此类的子类对象将存放于事件列表中待触发相应的事件'''
    def on_key_down(self, event):
        '''处理按键按下'''

    def on_key_up(self, event):
        '''处理按键抬起'''

    def on_mouse_down(self, event):
        '''处理鼠标左键按键按下'''
    
    def on_mouse_up(self, event):
        '''处理鼠标左键按键抬起'''

    def on_mouse_move(self, event):
        '''处理鼠标左键按下的同时移动'''

class EventList(GameList):
    '''事件列表类，此列表保存需要处理键盘事件和鼠标事件的类'''
    def __init__(self):
        super(EventList, self).__init__()

    def on_key_down(self, event):
        '''处理按键按下'''
        for obj in reversed(self.get_objs()):
            if obj.on_key_down(event):
                return

    def on_key_up(self, event):
        '''处理按键抬起'''
        for obj in reversed(self.get_objs()):
            if obj.on_key_up(event):
                return

    def on_mouse_down(self, event):
        '''处理鼠标左键按键按下'''
        for obj in reversed(self.get_objs()):
            if obj.on_mouse_down(event):
                return
    
    def on_mouse_up(self, event):
        '''处理鼠标左键按键抬起'''
        for obj in reversed(self.get_objs()):
            if obj.on_mouse_up(event):
                return

    def on_mouse_move(self, event):
        '''处理鼠标左键按下的同时移动'''
        for obj in reversed(self.get_objs()):
            if obj.on_mouse_move(event):
                return

class TimerList(GameList):
    def on_timer(self):
        for obj in self.get_objs():
            if obj.on_timer():
                return True

    def append_head(self, obj):
        "把触发事件对象插放在头部位置"
        lst = self.get_objs()
        lst.insert(0, obj)

class A:
	print("in A")
	def on_timer(self):
		print("in func A")
class B:
	print("in B")
	def on_timer(self):
		print("in func B")
		return True
class C:
	print("in C")
	def on_timer(self):
		print("in func C")

a = A()
b = B()
c = C()

t = TimerList()

t.append(a)
t.append(b)
t.append(c)

t.on_timer()

print("end of program")



