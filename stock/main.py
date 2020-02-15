from win32api import GetMonitorInfo, MonitorFromPoint
from tkinter import *
from tkinter.ttk import *
import sys
import requests

X_PADDING = 5
Y_PADDING = 5

WIDTH_BUTTON_CONTROLLER = 5

WIDTH_WINDOW = None
HEIGHT_WINDOW = None

HEADER_SWING = ["차이", "이름", "현재가", "저가", "목표가", "비중"]

URL_NAVER = "https://finance.naver.com/item/main.nhn?code="

class Window(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.master = master

		self.initializeWindowMain()
		self.initializeWindowController()
	
	def initializeWindowMain(self):
		self.master.title("Finance information")
		self.master.overrideredirect(True)
		self.master.withdraw()
		self.pack(fill = BOTH, expand = True)

		self.makeFrameSwing()

		self.master.update()
		self.master.geometry("+%d+%d" % ( (WIDTH_WINDOW - self.master.winfo_width()) / 2, (HEIGHT_WINDOW - self.master.winfo_height()) / 2))

	def makeFrameSwing(self):
		frame_label = Frame(self)
		frame_label.pack(padx = X_PADDING, pady = Y_PADDING, fill = X)
		label = Label(frame_label)
		label.pack()

		frame_table = Frame(self)
		frame_table.pack(padx = X_PADDING, pady = Y_PADDING, fill = X)

		self.makeDictionaryGoal(label)

		height = len(self.dic_item) + 1
		width = len(HEADER_SWING)
		self.list_text_swing = []
		for i in range(height): #Rows
			self.list_text_swing.append([])
			for j in range(width): #Columns
				self.list_text_swing[i].append(Text(frame_table, width = 10, height = 1))
				self.list_text_swing[i][j].grid(row = i, column = j)
		
		for j in range(width):
			self.list_text_swing[0][j].insert("current", HEADER_SWING[j])
			self.list_text_swing[0][j].config(state = DISABLED)

	def makeDictionaryGoal(self, label):
		file = open("goal.csv", "r", encoding = "utf-8")
		self.dic_item = {}
		sum_weight = 0
		for i, line in enumerate(file.readlines()):
			if i == 0:
				continue
			list_line = line.split(",")
			name = list_line[0].strip()
			code = list_line[1].strip()
			goal = int(list_line[2].strip())
			weight = float(list_line[3].strip())
			sum_weight += weight
			self.dic_item[name] = {"name": name, "code": code, "goal": goal, "weight": weight}
		file.close()

		label.configure(text = "스윙 (비중 %.1f%%)" % sum_weight)

	def makeButtonPeek(self):
		self.window_peek = Toplevel()
		self.window_peek.attributes("-topmost", True)
		self.window_peek.overrideredirect(True)
		self.window_peek.withdraw()
		self.bool_peek = False
		def peekPrice():
			if self.bool_peek:
				self.bool_peek = False
				self.window_peek.withdraw()
			else:
				self.bool_peek = True
				self.window_peek.update()
				self.window_peek.deiconify()
		button_peek = Button(self.window_controller, text = "/", width = WIDTH_BUTTON_CONTROLLER, command = peekPrice)
		button_peek.pack(side = LEFT)

	def makeButtonMain(self):
		self.bool_activation = False
		def activateWindow():
			if self.bool_activation:
				self.bool_activation = False
				self.master.withdraw()
				button_activation.configure(text = "+")
			else:
				self.bool_activation = True
				self.master.update()
				self.master.deiconify()
				button_activation.configure(text = "-")

				# 나중에 함수화하기
				list_sort = []
				for item in self.dic_item:
					res = requests.get(URL_NAVER + self.dic_item[item]["code"])
					for line in res.text.split("\n"):
						if "현재가" in line:
							price = int(line.strip().split(" ")[1].split("<")[0].replace(",", ""))
							self.dic_item[item]["price"] = price
							diff = 100.0 * (self.dic_item[item]["goal"] - price) / price
							list_sort.append((diff, item))
						elif "저가" in line:
							low = int(line.strip().split(" ")[1].split("<")[0].replace(",", ""))
							self.dic_item[item]["low"] = low
							break
				list_sort.sort(reverse = True)

				width = len(self.list_text_swing[0])
				height = len(self.list_text_swing)

				for i in range(1, height):
					for j in range(width):
						self.list_text_swing[i][j].config(state = NORMAL)
						self.list_text_swing[i][j].delete("1.0", END)

				for i, item in enumerate(list_sort):
					diff = item[0]
					name = item[1]

					self.list_text_swing[i + 1][0].insert("current", "%.2f%%" % diff)
					self.list_text_swing[i + 1][1].insert("current", name)
					self.list_text_swing[i + 1][2].insert("current", str(self.dic_item[name]["price"]))
					self.list_text_swing[i + 1][3].insert("current", str(self.dic_item[name]["low"]))
					self.list_text_swing[i + 1][3].tag_add("start", "1.0", "1.20")
					if self.dic_item[name]["low"] <= self.dic_item[name]["goal"]:
						self.list_text_swing[i + 1][3].tag_config("start", foreground = "red")
					else:
						self.list_text_swing[i + 1][3].tag_config("start", foreground = "black")
					self.list_text_swing[i + 1][4].insert("current", str(self.dic_item[name]["goal"]))
					self.list_text_swing[i + 1][5].insert("current", "%.1f%%" % self.dic_item[name]["weight"])

				for i in range(1, height):
					for j in range(width):
						self.list_text_swing[i][j].config(state = DISABLED)
				# 나중에 함수화하기

		button_activation = Button(self.window_controller, text = "+", width = WIDTH_BUTTON_CONTROLLER, command = activateWindow)
		button_activation.pack(side = LEFT)

	def makeButtonExit(self):
		def exitProgram():
			sys.exit()
		button_exit = Button(self.window_controller, text = "x", width = WIDTH_BUTTON_CONTROLLER, command = exitProgram)
		button_exit.pack()

	def initializeWindowController(self):
		self.window_controller = Toplevel()
		self.window_controller.attributes("-topmost", True)
		self.window_controller.overrideredirect(True)

		self.makeButtonPeek()
		self.makeButtonMain()
		self.makeButtonExit()
		
		self.window_controller.update()
		self.window_controller.geometry("+%d+%d" % ( WIDTH_WINDOW - self.window_controller.winfo_width(), HEIGHT_WINDOW - self.window_controller.winfo_height()))

def initializeWindowSize():
	global WIDTH_WINDOW, HEIGHT_WINDOW

	list_area = GetMonitorInfo(MonitorFromPoint((0,0))).get("Work")
	WIDTH_WINDOW = list_area[2]
	HEIGHT_WINDOW = list_area[3]

if __name__ == '__main__':

	initializeWindowSize()

	root = Tk()
	window = Window(root)
	root.mainloop()