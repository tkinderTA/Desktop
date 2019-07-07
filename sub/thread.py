import time
import requests

from sub.memo import *

# for call by reference
FOR_REF = 0

# time constant
UNIT_DELAY = 0.5
PERIOD_PARSING = 10
PERIOD_MEMO = 10

# week day
DAY_WEEK = ["월", "화", "수", "목", "금", "토", "일"]

"""
Time thread
"""
def threadTime(play, clock, date, start):

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

		# reboot program
		if start[FOR_REF] != now_day:
			rebootProgram()
			start[FOR_REF] = now_day
		
		# wait
		time.sleep(UNIT_DELAY)

	print("time thread die")


"""
Parsing thead
"""
def threadParsing(play, stock):
	global data_stock
	data_stock = {}

	data_stock["069500"] = {}
	data_stock["229200"] = {}

	unit = PERIOD_PARSING - 1

	while play[FOR_REF]:

		unit += 1

		# according to period
		if unit == PERIOD_PARSING:
			unit = 0
		
			# update stock information
			str_temp = None
			for code in data_stock:
				http_res = requests.get("https://finance.naver.com/item/main.nhn?code=" + code)
				for line in http_res.text.split("\n"):
					if "<dd>종목명" in line:
						data_stock[code]["name"] = line.strip()[8:-5]
					elif "현재가" in line:
						str_temp = line.strip().split(" ")
						data_stock[code]["cost"] = str_temp[1].replace(",", "")
						if str_temp[5] == "마이너스":
							data_stock[code]["change"] = -int(str_temp[4])
							data_stock[code]["percent"] = -float(str_temp[6])
						else:
							data_stock[code]["change"] = int(str_temp[4])
							data_stock[code]["percent"] = float(str_temp[6])
						break

			"""
			if float(str_now[:-1]) > 0:
				showinfo("알림", "hello")
			"""	

			str_now = ""
			for code in data_stock:
				str_now += str(data_stock[code]["change"]) + "% / "
			#	print(data_stock[code]["name"], data_stock[code]["cost"], data_stock[code]["change"], data_stock[code]["percent"])

			stock.configure(text = str_now[:-3])

		# wait
		time.sleep(UNIT_DELAY)

	print("parsing thread die")

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