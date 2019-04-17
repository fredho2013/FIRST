
import sys
if (sys.version_info > (3, 0)):
    from tkinter import *
else:
    from Tkinter import *

class Arm1:
    '''此类是武器类的基类，用来检测的碰幢条件等'''
    def __init__(self, a, b, p = False):
        if p:
            print("arm1 OKAY")
class Arm2:
    '''此类是武器类的基类，用来检测的碰幢条件等'''
    def __init__(self, a, b, p = False):
        if p:
            print("arm2 OKAY")

class MainApp:
    def __init__(self):

        self.__random_list = [Arm1] * 10 + [Arm2] * 20 
        self.__min_list_len = len(self.__random_list)
        #self.__random_list.extend([None] * 500)
        print('size of list', len(self.__random_list))
        print('type of list item', type(self.__random_list[0]))
        arm = self.__random_list[10]( 10,20, p=True)

app = MainApp()  

#print('size of list', len(app.__random_list))