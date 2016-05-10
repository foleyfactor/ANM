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

startingTime = time.time()
writing = False
theta = 90
delayTime = angleToTime(theta)/1000
print(delayTime)
print(startingTime)
while True:
	currentTime = time.time()
	delT = currentTime-startingTime
	if (delT<=delayTime and not writing):
		g.output(pin, True)
		writing = True
	elif (delT>delayTime and writing):
		g.output(pin, False)
		writing = False
	elif (delT>=0.02):
		startingTime = currentTime
##for i in range(-360,361,1):
##	setServoPos(i)
##	time.sleep(0.001)
##for i in range(360,-361,-1):
##	setServoPos(i)
##	time.sleep(0.001)
