
import sys
if (sys.version_info > (3, 0)):
    from tkinter import *
else:
    from Tkinter import *

class ORI:
	def __init__(self):
		print("class ORI")
	def A(self):
		print("")

	def B(self):
		print("")

	def C(self):
		print("")

class A1(ORI):
	def __init__(self):
		print("class A1")
	def A(self):
		print("def A")
class B1(ORI):
	def __init__(self):
		print("class B1")
	def B(self):
		print("def B")
		return True
class C1(ORI):
	def __init__(self):
		print("class C1")
	def C(self):
		print("def C")


def call_ABC(L):
	for obj in L:
		print(obj)
		if obj.B():
			return


a = A1()
b = B1()
c = C1()

L = []
L.append(a)
L.append(b)
L.append(c)
L= []
L = [a,b, c]

call_ABC(L)
		

