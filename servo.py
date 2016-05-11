import RPi.GPIO as g
import time, random

pin = 21

g.setmode(g.BCM)
g.setup(pin, g.OUT)

currAngle = 0

def delayMS(x):
	time.sleep(x/1000)

def angleToTime(angle):
	global currAngle
	angleDecimal = abs(angle-currAngle)/360
	currAngle = angle
	return 1.25+angleDecimal

def setServoPos(angle):
	dTime = angleToTime(angle)
	g.output(pin, True)
	delayMS(dTime)
	g.output(pin, False)