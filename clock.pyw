# written by Sangyoun Kwak
# modified by Jaejun Ha

import time, math
from tkinter import *
from tkinter.font import *
import requests

"""
Global variance
"""

# window
main_window = None

# date label
label_date = None

# time label
label_time = None

# alpha (used at hide mode)
value_alpha = 1

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
	global label_date, label_time

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
	
	main_window.after(UNIT_DELAY, printTime)


"""
Main function
"""
def main():
	global main_window, label_time, label_date

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

	"""
	label_temp = Label(main_window)
	label_temp.configure(background = "white")
	label_temp.configure(anchor = W)
	label_temp.configure(text = "\n할일")
	label_temp.pack(fill = BOTH)
	"""

	button_alpha = Button(main_window, command = hideWindow, text = "Hide mode")
	button_alpha.pack()

	main_window.after(UNIT_DELAY, printTime)
	main_window.mainloop()

"""
Start application
"""
if __name__ ==  "__main__":
	main()
