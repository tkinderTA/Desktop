from tendo import singleton
from main import *

"""
Start application
"""
if __name__ ==  "__main__":
	try:
		python = singleton.SingleInstance()
	except:
		sys.exit()

	print("hello")

	program()
