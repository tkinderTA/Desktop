﻿# written by Sangyoun Kwak
# modified by Jaejun Ha

import time
import math
from tkinter import *
from tkinter.font import *
from tkinter.messagebox import *
import requests
import os
import sys
import calendar
import threading

from sub.memo import *
from sub.system import *
"""
Global variance
"""

# todo width and height
width_check = None
height_check = None
size_check = None

# for exit signal
signal_play = True

"""
Constant
"""
# time delay
UNIT_DELAY = 0.5
UNIT_MIN = 60
PERIOD_PARSING = 10
PERIOD_MEMO = 10

# window location
POS_WINDOW = "-0-40"

# week day
DAY_WEEK = ["월", "화", "수", "목", "금", "토", "일"]

# margin
MARGIN_FRAME_X = 5
MARGIN_CHECK_X = 10
MARGIN_TWO_BUTTON_X = 20
MARGIN_TWO_BUTTON_Y = 5

# size
WIDTH_CHECK = 200
WIDTH_FREE = 50
HEIGHT_FREE = 10
WIDTH_TWO_BUTTON = 40

# list unit
UNIT_CHECK = 8


"""
Load todo
"""
def loadTodo():
	global list_todo

	# for rebooting
	try:
		if len(list_todo) > 0:
			del(list_todo)
			list_todo = []	
	except:
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


"""
Todo event
"""
def checkTodo():
	global canvas_todo
	global list_todo
	global list_check, width_check, height_check, size_check
	
	
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
	size_check -= 1
	if size_check is not None:
		canvas_todo.configure(scrollregion = (0, 0, width_check, height_check * size_check))


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

"""
Exit program
"""
def exitProgram():
	global signal_play
	global thread_workers
	global text_free

	# exit daemon thread
	signal_play = False
	for worker in thread_workers:
		worker.join()

	print("bye")

	# backup
	saveFree(text_free.get("1.0", END))

	sys.exit()

"""
Reboot program
"""
def rebootProgram():
	print("rebooting...")


"""
Time thread
"""
def threadTime():
	global signal_play
	global label_date, label_time
	global start

	while signal_play:

		# get time
		now_time = time.localtime(time.time())

		# set date label
		now_year = now_time.tm_year
		now_mon = now_time.tm_mon
		now_day = now_time.tm_mday
		now_week = now_time.tm_wday

		str_now = "%04d-%02d-%02d %s" % (now_year, now_mon, now_day, (DAY_WEEK[now_week] + "요일"))

		label_date.configure(text = str_now)
	
		# set time label
		now_hour = now_time.tm_hour % 12
		if now_hour == 0:
			now_hour = 12
		now_min = now_time.tm_min
		now_sec = now_time.tm_sec
	
		if now_time.tm_hour >= 12:
			str_now = "PM %02d:%02d:%02d" % (now_hour, now_min, now_sec)
		else:
			str_now = "AM %02d:%02d:%02d" % (now_hour, now_min, now_sec)

		label_time.configure(text = str_now)

		# reboot program
		if start != now_day:
			rebootProgram()
			start = now_day
		
		# wait
		time.sleep(UNIT_DELAY)


"""
Parsing thead
"""
def threadParsing():
	global signal_play
	global label_stock
	global time_parsing

	while signal_play:

		time_parsing += 1

		# according to period
		if time_parsing == PERIOD_PARSING:
			time_parsing = 0
		
			# update stock information
			str_now = None
			str_temp = None
			http_res = requests.get("https://finance.naver.com/item/main.nhn?code=069500")
			for line in http_res.text.split("\n"):
				if "전일대비" in line:
					str_temp = line.strip().split(' ')
					if str_temp[5] == "플러스":
						str_now = "+" + str_temp[6] + "%"
					elif str_temp[5] == "마이너스":
						str_now = "-" + str_temp[6] + "%"
					else:
						str_now = str_temp[6] + "%"
					break
			"""
			if float(str_now[:-1]) > 0:
				showinfo("알림", "hello")
			"""	

			http_res = requests.get("https://finance.naver.com/item/main.nhn?code=229200")
			for line in http_res.text.split("\n"):
				if "전일대비" in line:
					str_temp = line.strip().split(' ')
					if str_temp[5] == "플러스":
						str_now += " / +" + str_temp[6] + "%"
					elif str_temp[5] == "마이너스":
						str_now += " / -" + str_temp[6] + "%"
					else:
						str_now += " / " + str_temp[6] + "%"
					break
	
			label_stock.configure(text = str_now)

		# wait
		time.sleep(UNIT_DELAY)


"""
Memo thead
"""
def threadMemo():
	global signal_play
	global time_memo
	global text_free

	while signal_play:
		
		time_memo += 1

		# according to period
		if time_memo == PERIOD_MEMO:
			time_memo = 0
		
			# save free memo
			saveFree(text_free.get("1.0", END))
		
		# wait
		time.sleep(UNIT_DELAY)


"""
Main function
"""
def program(day):
	global start
	global window_main, label_time, label_date, label_stock, canvas_todo, text_free
	global list_check, width_check, height_check, size_check
	global thread_workers
	global time_parsing, time_memo

	# run time
	start = day

	loadTodo()

	window_main = Tk()
	window_main.configure(background = "white")

	# coordinate
	window_main.geometry(POS_WINDOW)
	window_main.resizable(False, False)

	# attribute setting for "always on top"
	window_main.wm_attributes("-topmost", True)
	window_main.overrideredirect(True)

	frame_top = Frame(window_main)
	frame_top.grid(row = 0, columnspan = 2)

	frame_left = Frame(window_main, background = "white")
	frame_left.grid(row = 1, column = 0, padx = MARGIN_FRAME_X)

	frame_right = Frame(window_main)
	frame_right.grid(row = 1, column = 1, padx = MARGIN_FRAME_X)

	frame_bottom = Frame(window_main, background = "white")
	frame_bottom.grid(row = 2, columnspan = 2)

	label_date = Label(frame_top, font = Font(family = "Sandoll 미생", size = 15), background = "white")
	label_date.pack(fill = BOTH)

	label_time = Label(frame_top, font = Font(family = "맑은 고딕", size = 20), background = "white")
	label_time.pack(fill = BOTH)

	label_todo = Label(frame_left, text = "\n- 할일 -", anchor = W, background = "white")
	label_todo.pack(fill = BOTH)

	frame_todo = Frame(frame_left, background = "white")
	frame_todo.pack(fill = X)

	canvas_todo = Canvas(frame_todo, width = 1, height = 1)
	canvas_todo.pack(fill = BOTH, side = LEFT, expand = True)
	scroll_todo = Scrollbar(frame_todo, command = canvas_todo.yview, background = "white")
	canvas_todo.configure(yscrollcommand = scroll_todo.set)
	scroll_todo.pack(fill = Y, side = RIGHT)

	frame_check = Frame(canvas_todo, background = "white")
	canvas_todo.create_window(0, 0, window = frame_check, anchor = NW)

	# for rebooting
	try:
		if len(list_check) > 0:
			del(list_check)
			list_check = []
	except NameError:
		list_check = []

	check_todo = None
	check_var = None
	size_check = 0
	for item in list_todo:
		size_check += 1
		check_var = IntVar()
		check_todo = tkinter.Checkbutton(frame_check, text = item, command = checkTodo, variable = check_var, font = Font(family = "Sandoll 미생", size = 15), background = "white", anchor = W)
		check_todo.pack(fill = BOTH)
		list_check.append((check_todo, check_var))
	
	if check_todo is not None:
		check_todo.update()
		width_check = check_todo.winfo_width()
		height_check = check_todo.winfo_height()
		if width_check < WIDTH_CHECK:
			canvas_todo.configure(width = WIDTH_CHECK)
		else:
			canvas_todo.configure(width = (width_check + MARGIN_CHECK_X))
		canvas_todo.configure(height = (height_check * UNIT_CHECK), scrollregion = (0, 0, width_check, height_check * len(list_todo)), background = "white")

	label_stock = Label(frame_left, background = "white")
	label_stock.pack(fill = BOTH, side = LEFT)

	text_free = Text(frame_right, width = WIDTH_FREE, height = HEIGHT_FREE)
	text_free.pack(fill = BOTH, side = LEFT)
	scroll_free = Scrollbar(frame_right, command = text_free.yview)
	text_free.configure(yscrollcommand = scroll_free.set)
	scroll_free.pack(fill = Y, side = RIGHT)
	
	# load memo, don't change this code location
	loadFree(text_free)

	button_alpha = Button(frame_bottom, command = lambda: hideWindow(window_main), text = "Hide", width = WIDTH_TWO_BUTTON)
	button_alpha.pack(fill = BOTH, side = LEFT, padx = MARGIN_TWO_BUTTON_X, pady = MARGIN_TWO_BUTTON_Y)

	button_exit = Button(frame_bottom, command = exitProgram, text = "Exit", width = WIDTH_TWO_BUTTON)
	button_exit.pack(fill = BOTH, side = RIGHT, padx = MARGIN_TWO_BUTTON_X, pady = MARGIN_TWO_BUTTON_Y)
	
	# for rebooting
	try:
		if len(thread_workers) > 0:
			del(thread_workers)
			thread_workers = []
	except NameError:
		thread_workers = []

	# make threads
	time_parsing = PERIOD_PARSING - 1
	time_memo = PERIOD_MEMO - 1

	thread_worker = threading.Thread(target = threadTime)
	thread_worker.daemon = True
	thread_worker.start()
	thread_workers.append(thread_worker)

	thread_worker = threading.Thread(target = threadMemo)
	thread_worker.daemon = True
	thread_worker.start()
	thread_workers.append(thread_worker)

	thread_worker = threading.Thread(target = threadParsing)
	thread_worker.daemon = True
	thread_worker.start()
	thread_workers.append(thread_worker)

	window_main.mainloop()