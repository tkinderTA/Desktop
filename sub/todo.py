import os
import time

from tkinter.messagebox import *

# for call by reference
FOR_REF = 0
"""
Load todo
"""
def loadTodo():

	list_todo = []

	if not(os.path.isdir("C:\\Desktop")):
		os.makedirs(os.path.join("C:\\Desktop"))

	# get time
	now_time = time.localtime(time.time())

	# set date
	now_year = now_time.tm_year
	now_mon = now_time.tm_mon
	now_day = now_time.tm_mday

	str_now = "%04d-%02d-%02d" % (now_year, now_mon, now_day)

	if not(os.path.isdir("C:\\Desktop\\data")):
		os.makedirs(os.path.join("C:\\Desktop\\data"))

	# load todo data
	os.chdir("C:\\Desktop\\data")
	if not(os.path.isdir(str_now)):
		os.makedirs(os.path.join(str_now))
		os.chdir("C:\\Desktop")
		try:
			file = open("list.txt", "r")
			for line in file.readlines():
				list_todo.append(line.strip())
			file.close()
		except FileNotFoundError:
			list_todo = []

		os.chdir("C:\\Desktop\\data\\" + str_now)
		file = open("todo.txt", "w")
		for item in list_todo:
			file.write(item + "\\" + "no\n")
		file.close()
		
	else:
		os.chdir("C:\\Desktop\\data\\" + str_now)

		file = open("todo.txt", "r")
		for item in file.readlines():
			if item.split("\\")[1].strip() == "no":
				list_todo.append(item.split("\\")[0])
		file.close()

	return list_todo


"""
Todo event
"""
def checkTodo(canvas_todo, list_todo, list_check, size_check):
	
	# ask question
	result = askquestion("질문", "정말 완료하셨습니까?")

	# if no
	if result == "no":
		for i in range(len(list_todo)):
			if list_check[i][1].get() == 1:
				list_check[i][0].deselect()
				break
		return

	# else
	index = None
	for i in range(len(list_todo)):
		if list_check[i][1].get() == 1:
			list_check[i][0].deselect()
			index = i
			break
	
	list_check[index][0].destroy()
	size_check[FOR_REF] -= 1
	if size_check[FOR_REF] > 0:
		list_check[0][0].update()
		width_check = list_check[0][0].winfo_width()
		height_check = list_check[0][0].winfo_height()
		canvas_todo.configure(scrollregion = (0, 0, width_check, height_check * size_check[FOR_REF]))


	# get time
	now_time = time.localtime(time.time())

	# set date
	now_year = now_time.tm_year
	now_mon = now_time.tm_mon
	now_day = now_time.tm_mday

	str_now = "%04d-%02d-%02d" % (now_year, now_mon, now_day)

	os.chdir("C:\\Desktop\\data\\" + str_now)
	file = open("todo.txt", "r")

	list_content = []	
	str = None
	for line in file.readlines():
		str = line.strip()
		if str.split("\\")[0] == list_todo[index]:
			str = list_todo[index] + "\\" + "ok"
		list_content.append(str)
	file.close()	

	file = open("todo.txt", "w")
	for content in list_content:
		file.write(content + "\n")
	file.close()