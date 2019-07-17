import time
import requests

from tkinter.messagebox import *
from tkinter.font import *

from sub.memo import *
from sub.todo import *

# for call by reference
FOR_REF = 0

# time constant
UNIT_DELAY = 0.5
PERIOD_MEMO = 10
PERIOD_UPDATE = 60

# check width
WIDTH_CHECK = 200

# list unit
UNIT_CHECK = 10

# week day
DAY_WEEK = ["월", "화", "수", "목", "금", "토", "일"]

"""
Time thread
"""
def threadTime(play, clock, date):

	while play[FOR_REF]:

		# get time
		now_time = time.localtime(time.time())

		# set date label
		now_year = now_time.tm_year
		now_mon = now_time.tm_mon
		now_day = now_time.tm_mday
		now_week = now_time.tm_wday

		str_now = "%04d-%02d-%02d %s" % (now_year, now_mon, now_day, (DAY_WEEK[now_week] + "요일"))

		date.configure(text = str_now)
	
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

		clock.configure(text = str_now)
		
		# wait
		time.sleep(UNIT_DELAY)

	print("time thread die")


"""
Memo thead
"""
def threadMemo(play, free):

	unit = PERIOD_MEMO - 1

	while play[FOR_REF]:
		
		unit += 1

		# according to period
		if unit == PERIOD_MEMO:
			unit = 0
		
			# save free memo
			saveFree(free.get("1.0", END))
		
		# wait
		time.sleep(UNIT_DELAY)

	print("memo thread die")


"""
Update thread
"""
def threadUpdate(play, canvas_todo, frame_check):

	unit = PERIOD_UPDATE - 1
	start_day = -1

	while play[FOR_REF]:

		unit += 1

		# according to period
		if unit == PERIOD_UPDATE:
			unit = 0
		
			now_day = time.localtime(time.time()).tm_mday
			# update things

			if start_day != now_day:

				# Refresh todo function
				list_todo = loadTodo()

				check_todo = None
				size_check = [0]
				list_check = []

				# Remove previous check widget
				for item in frame_check.winfo_children():
					item.destroy()

				for item in list_todo:
					size_check[FOR_REF] += 1
					check_var = IntVar()
					check_todo = tkinter.Checkbutton(frame_check, text = item, command = lambda: checkTodo(canvas_todo, list_todo, list_check, size_check), variable = check_var, font = Font(family = "Sandoll 미생", size = 15), background = "white", anchor = W)
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
				
				# update date
				start_day = now_day
		
		# wait
		time.sleep(UNIT_DELAY)

	print("update thread die")
