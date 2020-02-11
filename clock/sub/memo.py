from tkinter import *
import shutil
import os

"""
Save free memo
"""
def saveFree(text):

	os.chdir("C:\\Desktop")
	
	shutil.copyfile("memo.txt", "memo.bak1")
	
	file = open("memo.txt", "w")
	file.write(text.strip())
	file.close()

	shutil.copyfile("memo.txt", "memo.bak2")

"""
Load free memo
"""
def loadFree(free):

	try:
		os.chdir("C:\\Desktop")
		file = open("memo.txt", "r")

		for line in file.readlines():
			free.insert(END, line)
		file.close()
	except NameError:
		return
	except FileNotFoundError:
		file = open("memo.txt", "w")
		file.close()
		return 