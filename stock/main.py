from win32api import GetMonitorInfo, MonitorFromPoint
from tkinter import *
from tkinter.ttk import *
import sys
import requests

WIDTH_WINDOW = None
HEIGHT_WINDOW = None

class Window(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
 
		self.master = master
		self.master.title("Finance information")
		self.master.overrideredirect(True)
		self.pack(fill = BOTH, expand = True)
 
		frame_test = Frame(self)
		frame_test.pack(fill = X)
 
		label_test = Label(frame_test, text="Test", width = 10)
		label_test.pack(side = LEFT, padx = 10, pady = 10)

		# 아래 코드 순서 변경하지 말기
		self.master.update()
		self.master.geometry("+%d+%d" % ( (WIDTH_WINDOW - self.master.winfo_width()) / 2, (HEIGHT_WINDOW - self.master.winfo_height()) / 2))
		# 위 코드 순서 변경하지 말기
 
		# 초기에는 비 활성화
		self.master.withdraw()
	
		window_controller = Toplevel()
		window_controller.attributes("-topmost", True)
		window_controller.overrideredirect(True)

		"""
		몰래 보기
		"""
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
		button_peek = Button(window_controller, text = "/", width = 5, command = peekPrice)
		button_peek.pack(side = LEFT)

		"""
		메인 활성화
		"""
		self.makeListGoal()
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
					res = requests.get("https://finance.naver.com/item/main.nhn?code=" + self.dic_item[item]["code"])
					for line in res.text.split("\n"):
						if "저가" in line:
							price = int(line.strip().split(" ")[1].split("<")[0].replace(",", ""))
							self.dic_item[item]["price"] = price
							diff = 100.0 * (self.dic_item[item]["goal"] - price) / price
							list_sort.append((diff, item))
							break
				list_sort.sort(reverse = True)
				for i, item in enumerate(list_sort):
					name = item[1]
					self.list_label_goal[i].configure(text = ("%.2f%%\t%s\t%s\t%s" % (item[0], name.ljust(10), self.dic_item[name]["price"], self.dic_item[name]["goal"])))
				# 나중에 함수화하기


		button_activation = Button(window_controller, text = "+", width = 5, command = activateWindow)
		button_activation.pack(side = LEFT)

		"""
		종료
		"""
		def exitProgram():
			sys.exit()
		button_exit = Button(window_controller, text = "x", width = 5, command = exitProgram)
		button_exit.pack()

		# 아래 코드 순서 변경하지 말기
		window_controller.update()
		window_controller.geometry("+%d+%d" % ( WIDTH_WINDOW - window_controller.winfo_width(), HEIGHT_WINDOW - window_controller.winfo_height()))
		# 위 코드 순서 변경하지 말기
	
	def makeListGoal(self):
		file = open("goal.csv", "r", encoding = "utf-8")
		self.dic_item = {}
		for i, line in enumerate(file.readlines()):
			if i == 0:
				continue
			list_line = line.split(",")
			name = list_line[0].strip()
			code = list_line[1].strip()
			goal = int(list_line[2].strip())
			weight = list_line[3].strip()
			self.dic_item[name] = {"name": name, "code": code, "goal": goal, "weight": weight}
		file.close()

		Label(self.master, text = ("%s(%%)\t%s\t%s\t%s" % ("차이", "이름".ljust(10), "저가", "목표가"))).pack()
		self.list_label_goal = []
		for item in self.dic_item:
			label = Label(self.master, text="")
			label.pack()
			self.list_label_goal.append(label)

def getWindowSize():
	global WIDTH_WINDOW, HEIGHT_WINDOW

	list_area = GetMonitorInfo(MonitorFromPoint((0,0))).get("Work")
	WIDTH_WINDOW = list_area[2]
	HEIGHT_WINDOW = list_area[3]

if __name__ == '__main__':

	getWindowSize()

	root = Tk()
	window = Window(root)
	root.mainloop()