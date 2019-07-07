import sys

from tkinter import *

from sub.memo import *

LOW_ALPHA = 0.2
HIGH_ALPHA = 1

# alpha (used at hide mode)
alpha = HIGH_ALPHA

"""
Hide(semi) mode
"""
def hideWindow(window):
	global alpha

	if alpha == HIGH_ALPHA:
		alpha = LOW_ALPHA
		window.wm_attributes("-topmost", False)
	else:
		alpha = HIGH_ALPHA
		window.wm_attributes("-topmost", True)

	window.attributes("-alpha", alpha)

"""
Exit program
"""
def exitProgram(workers, play, free):

	# exit daemon thread
	play[0] = False
	for worker in workers:
		worker.join()

	print("bye")

	# backup
	saveFree(free.get("1.0", END))

	sys.exit()