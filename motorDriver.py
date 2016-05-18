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

def right(forward):
	g.output(r1, forward)
	g.output(r2, not forward)

def left(forward):
	g.output(l1, forward)
	g.output(l2, not forward)

def motorsOff():
	g.output(l1, False)
	g.output(l2, False)
	g.output(r1, False)
	g.output(r2, False)

def forward():
	left(True)
	right(True)

def backward():
	right(False)
	left(False)
