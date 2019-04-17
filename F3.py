
import sys
if (sys.version_info > (3, 0)):
    from tkinter import *
else:
    from Tkinter import *


class BB:
	def __init__(self):
		print("class BB")
		self.__CC = CC(start_callback=self.start_game)
	def B(self):
		print("def BB")
		return True
	def start_game(self):
		print("start_game in class B1 self", self)

class CC:
	def __init__(self,start_callback=None):
		print("class C")
		self.__start_fn = start_callback
	def start_game(self):
		self.__start_fn()


b = BB()
b.start_game()
print(b)
		

        