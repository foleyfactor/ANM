import RPi.GPIO as g
import time

g.setmode(g.BCM)

g.setup(18, g.OUT)
g.setup(23, g.OUT)

#initialize values
g.output(18, True)
g.output(23, False)

def charge(amt):
	g.output(18, False)
	time.sleep(amt)
	g.output(18, True)

def fire():
	g.output(23, True)
	#Pray that it doesn't break my pi
	time.sleep(0.5)
	g.output(23, False)

charge(15)
fire()