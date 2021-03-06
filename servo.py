import RPi.GPIO as g
import time, random

pin = 21

g.setmode(g.BCM)
g.setup(pin, g.OUT)

def delayMS(x):
	time.sleep(x/1000)

def angleToTime(angle):
	angleDecimal = 1.2*angle*2/180
	return 1.325+angleDecimal

def setServoPos(angle, count):
	if count == 0:
		return
	dTime = angleToTime(angle)
	g.output(pin, True)
	delayMS(dTime)
	g.output(pin, False)
	delayMS(20-dTime)
	setServoPos(angle, count-1)
