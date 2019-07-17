import time
import calendar

from tkinter import *

# week day
DAY_WEEK = ["월", "화", "수", "목", "금", "토", "일"]
DAY_SAT = 5
DAY_SUN = 6

"""
Update calendar
"""
def updateCalendar(year, month, day, label_calendar, frame_calendar):
	label_calendar.configure(text = "%04d년 %02d월" % (year, month))

	now_date = calendar.Calendar().monthdatescalendar(year, month)

	# To manage each day widget
	list_weeks = []
	widget_week = []
	label_day = None
	button_day = None
				
	for i in range(len(DAY_WEEK)):
		label_day = Label(frame_calendar, text = DAY_WEEK[i])
		label_day.grid(row = 0, column = i)
		
		if i == DAY_SAT:
			label_day["fg"] = "blue"
		elif i == DAY_SUN:
			label_day["fg"] = "red"
		
		widget_week.append(label_day)
	list_weeks.append(widget_week)

	for i, week in enumerate(now_date):

		widget_week = []
			
		for j, date in enumerate(week):

			if date.month != month:
				continue
	
			button_day = Button(frame_calendar, text = date.strftime("%d"), width = 6)
			button_day.grid(row = i, column = j, padx = 1, pady = 1)
		
			if date.year == year and date.month == month and date.day == day:
				button_day["bg"] = "#aaa"
			
			if j == DAY_SAT:
				button_day["fg"] = "blue"
			elif j == DAY_SUN:
				button_day["fg"] = "red"
		
			widget_week.append(button_day)
		list_weeks.append(widget_week)