
import sys
if (sys.version_info > (3, 0)):
    from tkinter import *
else:
    from Tkinter import *


class MainApp:
    def __init__(self):
        self.__root = root = Tk()
        root.title("飞机大战(达内科技)")
        from skycanvas import SkyCanvas
        self.__canvas = canvas = SkyCanvas(root, width=480, height=654)
        canvas.pack()

        # 处理按键事件和鼠标事件
        from gamelist import EventList
        self.__event_list = event_list = EventList()  # 创建能够接收控制事件的列表
        root.bind('<Key>', lambda event: event_list.on_key_down(event))
        root.bind('<KeyRelease>', lambda event: event_list.on_key_up(event))
        root.bind('<Button>', lambda event: event_list.on_mouse_down(event))
        root.bind('<Motion>', lambda event: event_list.on_mouse_move(event))
        root.bind('<ButtonRelease>',
                  lambda event: event_list.on_mouse_up(event))
    def run(self):
		# 进入主事件循环
        self.__root.mainloop()


if __name__ == '__main__':
    app = MainApp()
    app.run()
