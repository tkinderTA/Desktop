# written by Sangyoun Kwak
# modified by Jaejun Ha

from tendo import singleton
from main import *
import time

"""
Start application
"""
if __name__ ==  "__main__":
	try:
		python = singleton.SingleInstance()
	except:
		sys.exit()

	print("hello")

	program(time.localtime(time.time()).tm_mday)
