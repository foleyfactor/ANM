import RPi.GPIO as g
import time

g.setmode(g.BCM)

r1 = 12
r2 = 16
l1 = 7
l2 = 8


g.setup(r1, g.OUT)
g.setup(r2, g.OUT)
g.setup(l1, g.OUT)
g.setup(l2, g.OUT)
def getTime():
	return round(time.time()*1000)

def right(forward):
	if (getTime()%8):
		g.output(r1, forward)
		g.output(r2, not forward)
	else:
		motorsOff()

def left(forward):
	if (getTime()%8):
		g.output(l1, forward)
		g.output(l2, not forward)
	else:
		motorsOff()

def motorsOff():
	g.output(l1, False)
	g.output(l2, False)
	g.output(r1, False)
	g.output(r2, False)

def forward():
	if (getTime()%8):
		left(True)
		right(True)
	else:
		motorsOff()

def backward():
	if (getTime()%8):
		right(False)
		left(False)
	else:
		motorsOff()
