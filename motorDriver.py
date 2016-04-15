import RPi.GPIO as g
import time

g.setmode(g.BCM)

g.setup(20, g.OUT)
g.setup(21, g.OUT)
g.setup(19, g.OUT)
g.setup(26, g.OUT)

def right(forward):
	g.output(20, forward)
	g.output(21, !forward)

def left(forward):
	g.output(19, forward)
	g.output(26, !forward)

def motorsOff():
	g.output(19, False)
	g.output(26, False)
	g.output(20, False)
	g.output(21, False)

def forward():
	left(True)
	right(True)

def backward():
	right(False)
	left(False)

for i in range(10):
	right(True)
	left(True)
	time.sleep(1)
	right(False)
	left(True)
	time.sleep(1)
	right(False)
	left(False)
	time.sleep(1)
	right(True)
	left(False)
	time.sleep(1)