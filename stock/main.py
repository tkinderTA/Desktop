from tkinter import *

from sub.system import *

"""
Constant
"""
# window location
POS_WINDOW = "-0+0"

"""
Main function
"""
def program():

	window_main = Tk()
	window_main.configure(background = "white")

	# coordinate
	window_main.geometry(POS_WINDOW)
	window_main.resizable(False, False)

	# attribute setting for "always on top"
	window_main.wm_attributes("-topmost", True)
	window_main.overrideredirect(True)

	button_alpha = Button(window_main, command = lambda: hideWindow(window_main), text = "Hide")
	button_alpha.pack(fill = BOTH, side = LEFT)

	button_exit = Button(window_main, command = lambda: exitProgram(), text = "Exit")
	button_exit.pack(fill = BOTH, side = RIGHT)

	window_main.mainloop()


"""
Parsing thead

def threadParsing(play, stock):
	global data_stock
	data_stock = {}

	#	233160 150 2
	#	252710 200 -2
	test = "233160"
	data_stock[test] = {}
	min = 999
	max = -999


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
						data_stock[code]["cost"] = int(str_temp[1].replace(",", ""))
						if str_temp[5] == "마이너스":
							data_stock[code]["change"] = -int(str_temp[4].replace(",", ""))
							data_stock[code]["percent"] = -float(str_temp[6])
						else:
							data_stock[code]["change"] = int(str_temp[4].replace(",", ""))
							data_stock[code]["percent"] = float(str_temp[6])
						break
  
			
		
			if data_stock[test]["percent"] > -1.81:
				showinfo("알림", "Hello!")
			if data_stock[test]["percent"] < -2.81:
				showinfo("알림", "Hello!")
			
			str_now = ""
			
			for i, code in enumerate(data_stock):
#				str_now += str(data_stock[code]["percent"]) + "% / "	
				str_now += str(data_stock[code]["percent"])	
				
				if min > data_stock[code]["percent"]:
					min = data_stock[code]["percent"]
					showinfo("알림", "Hello")
				if max < data_stock[code]["percent"]:
					max = data_stock[code]["percent"]
					showinfo("알림", "Hello")
				
			
			stock.configure(text = str_now[:-3])
			
			stock.configure(text = str(min) + " " + str_now + " " + str(max))

		# wait
		time.sleep(UNIT_DELAY)

	print("parsing thread die")
"""