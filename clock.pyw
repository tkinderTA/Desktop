# written by Sangyoun Kwak
# modified by Jaejun Ha

import time, math
from tkinter import *
from tkinter.font import *
from tkinter.messagebox import *
import requests
import os
import sys

"""
Global variance
"""

# window
main_window = None

# date label
label_date = None

# time label
label_time = None

# stock label
label_stock = None

# alpha (used at hide mode)
value_alpha = 1

# todo list
list_todo = []

# check button related to todo
list_check = []

"""
Constant
"""

# time delay
UNIT_DELAY = 500

# window location
POS_WINDOW = "-0-40"

# week day
DAY_WEEK = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

"""
Hide(semi) mode
"""
def hideWindow():
	global value_alpha

	if value_alpha == 1:
		value_alpha = 0.1
	else:
		value_alpha = 1

	main_window.attributes("-alpha", value_alpha)



"""
Print time
"""
def printTime():
	global label_date, label_time, label_stock

	# get time
	time_now = time.localtime(time.time())

	# set date
	year_now = time_now.tm_year
	mon_now = time_now.tm_mon
	day_now = time_now.tm_mday
	week_now = time_now.tm_wday

	str_now = "%04d-%02d-%02d %s" % (year_now, mon_now, day_now, DAY_WEEK[week_now])

	label_date.configure(text = str_now)
	

	# set time
	hour_now = time_now.tm_hour % 12
	if hour_now == 0:
		hour_now = 12
	min_now = time_now.tm_min
	sec_now = time_now.tm_sec
	
	if time_now.tm_hour >= 12:
		str_now = "PM %02d:%02d:%02d" % (hour_now, min_now, sec_now)
	else:
		str_now = "AM %02d:%02d:%02d" % (hour_now, min_now, sec_now)

	label_time.configure(text = str_now)


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



	# exit program
	if time_now.tm_hour == 0 and time_now.tm_min == 0:
		main_window.destroy()
	else:
		main_window.after(UNIT_DELAY, printTime)

"""
Load todo
"""
def loadTodo():
	global list_todo

	# for rebooting
	if len(list_todo) > 0:
		del(list_todo)
		list_todo = []	

	if not(os.path.isdir("C:\\Desktop")):
		os.makedirs(os.path.join("C:\\Desktop"))

	# get time
	time_now = time.localtime(time.time())

	# set date
	year_now = time_now.tm_year
	mon_now = time_now.tm_mon
	day_now = time_now.tm_mday

	str_now = "%04d-%02d-%02d" % (year_now, mon_now, day_now)

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
	global list_check
	
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

	list_check[index][0].after(UNIT_DELAY, list_check[index][0].destroy)


	# get time
	time_now = time.localtime(time.time())

	# set date
	year_now = time_now.tm_year
	mon_now = time_now.tm_mon
	day_now = time_now.tm_mday

	str_now = "%04d-%02d-%02d" % (year_now, mon_now, day_now)

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
Main function
"""
def main():
	global main_window, label_time, label_date, label_stock
	global list_check

	loadTodo()

	main_window = Tk()
	main_window.configure(background = "white")

	# coordinate
	main_window.geometry(POS_WINDOW)
	main_window.resizable(False, False)

	# attribute setting for "always on top"
	main_window.wm_attributes("-topmost", 1)
	main_window.overrideredirect(True)
	main_window.attributes('-alpha', value_alpha)

	label_date = Label(main_window)
	label_date.configure(background = "white")
	label_date.configure(font = Font(family = "Sandoll 미생", size = 15))
	label_date.pack()

	label_time = Label(main_window)
	label_time.configure(background = "white")
	label_time.configure(font = Font(family = "맑은 고딕", size = 20))
	label_time.pack()


	label_todo = Label(main_window)
	label_todo.configure(background = "white")
	label_todo.configure(anchor = W)
	label_todo.configure(text = "\n- 할일 -")
	label_todo.pack(fill = BOTH)


	# for rebooting
	if len(list_check) > 0:
		del(list_check)
		list_check = []

	check_todo = None
	check_var = None
	for item in list_todo:
		check_var = IntVar()
		check_todo = tkinter.Checkbutton(main_window, text = item, command = checkTodo, variable = check_var)
		check_todo.configure(background = "white")
		check_todo.configure(font = Font(family = "Sandoll 미생", size = 15))
		check_todo.configure(anchor = "w")
		check_todo.pack(fill = BOTH)
		list_check.append((check_todo, check_var))

	label_stock = Label(main_window)
	label_stock.configure(background = "white")
#	label_stock.configure(font = Font(family = "맑은 고딕", size = 20))
	label_stock.pack()


	button_alpha = Button(main_window, command = hideWindow, text = "Hide mode")
	button_alpha.pack()

	main_window.after(UNIT_DELAY, printTime)
	main_window.mainloop()

"""
Start application
"""
if __name__ ==  "__main__":
	while True:
		main()
		time.sleep(1)
	
