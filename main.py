# written by Sangyoun Kwak
# modified by Jaejun Ha

import time
from tkinter import *
from tkinter.font import *
from tkinter.messagebox import *
import os
import calendar
import threading

from sub.memo import *
from sub.system import *
from sub.thread import *

"""
Global variance
"""
# todo width and height
width_check = None
height_check = None
size_check = None

"""
Constant
"""
# window location
POS_WINDOW = "-0-40"

# margin
MARGIN_FRAME_X = 5
MARGIN_CHECK_X = 10
MARGIN_TWO_BUTTON_X = 20
MARGIN_TWO_BUTTON_Y = 5

# size
WIDTH_CHECK = 200
WIDTH_FREE = 52
HEIGHT_FREE = 12
WIDTH_TWO_BUTTON = 40

# list unit
UNIT_CHECK = 10

# week
DAY_WEEK = ["월", "화", "수", "목", "금", "토", "일"]

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
Reboot program
"""
def rebootProgram():
	print("rebooting...")



"""
Main function
"""
def program(day):
	global canvas_todo
	global list_check, width_check, height_check, size_check

	# run time
	day_start = [day]

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

	label_clock = Label(frame_top, font = Font(family = "맑은 고딕", size = 20), background = "white")
	label_clock.pack(fill = BOTH)

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

	# calendar
	frame_month = Frame(frame_right)

	now_time = time.localtime(time.time())

	now_year = now_time.tm_year
	now_mon = now_time.tm_mon
	now_day = now_time.tm_mday

	button_pre = Button(frame_month, text = "◀")
	button_pre.grid(row = 0, column = 0, pady = 5)

	button_next = Button(frame_month, text = "▶")
	button_next.grid(row = 0, column = 2, pady = 5)

	label_calendar = Label(frame_month, text = "%04d년 %02d월" % (now_year, now_mon))
	label_calendar.grid(row = 0, column = 1, padx = 10)

	frame_month.pack()

	frame_calendar = Frame(frame_right)

	now_date = calendar.Calendar().monthdatescalendar(now_year, now_mon)

	# To manage each day widget
	list_weeks = []
	widget_week = []
	label_day = None
	button_day = None
	
	for i in range(7):
		label_day = Label(frame_calendar, text = DAY_WEEK[i])
		label_day.grid(row = 0, column = i)
		
		if i == 5:
			label_day["fg"] = "blue"
		elif i == 6:
			label_day["fg"] = "red"
		
		widget_week.append(label_day)
	list_weeks.append(widget_week)

	for i, week in enumerate(now_date):

		widget_week = []

		for j, date in enumerate(week):

			if date.month != now_mon:
				continue
	
			button_day = Button(frame_calendar, text = date.strftime("%d"), width = 6)
			button_day.grid(row = i, column = j, padx = 1, pady = 1)
		
			if date.year == now_year and date.month == now_mon and date.day == now_day:
				button_day["bg"] = "#aaa"
			
			if j == 5:
				button_day["fg"] = "blue"
			elif j == 6:
				button_day["fg"] = "red"
		
			widget_week.append(button_day)
		list_weeks.append(widget_week)

	frame_calendar.pack()

	# free memo
	text_free = Text(frame_right, width = WIDTH_FREE, height = HEIGHT_FREE)
	text_free.pack(fill = BOTH, side = LEFT)
	scroll_free = Scrollbar(frame_right, command = text_free.yview)
	text_free.configure(yscrollcommand = scroll_free.set)
	scroll_free.pack(fill = Y, side = RIGHT)
	
	# load memo, don't change this code location
	loadFree(text_free)

	# for rebooting, don't change this code location
	try:
		if len(thread_workers) > 0:
			del(thread_workers)
			thread_workers = []
	except NameError:
		thread_workers = []
	signal_play = [True]

	button_alpha = Button(frame_bottom, command = lambda: hideWindow(window_main), text = "Hide", width = WIDTH_TWO_BUTTON)
	button_alpha.pack(fill = BOTH, side = LEFT, padx = MARGIN_TWO_BUTTON_X, pady = MARGIN_TWO_BUTTON_Y)

	button_exit = Button(frame_bottom, command = lambda: exitProgram(thread_workers, signal_play, text_free), text = "Exit", width = WIDTH_TWO_BUTTON)
	button_exit.pack(fill = BOTH, side = RIGHT, padx = MARGIN_TWO_BUTTON_X, pady = MARGIN_TWO_BUTTON_Y)

	# make threads

	thread_worker = threading.Thread(target = threadTime, args = (signal_play, label_clock, label_date, day_start))
	thread_worker.daemon = True
	thread_worker.start()
	thread_workers.append(thread_worker)

	thread_worker = threading.Thread(target = threadMemo, args = (signal_play, text_free))
	thread_worker.daemon = True
	thread_worker.start()
	thread_workers.append(thread_worker)

	thread_worker = threading.Thread(target = threadParsing, args = (signal_play, label_stock))
	thread_worker.daemon = True
	thread_worker.start()
	thread_workers.append(thread_worker)

	window_main.mainloop()