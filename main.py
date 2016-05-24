import ball_tracking
import motorDriver
import threading
import time
import servo

#Create a ball tracker, and start the thread
cameraThread = ball_tracking.BallTracker()
cameraThread.start()

FPS = 30
delay = 1/FPS
pctOn = 0.8

prevAngle = 0

def reduceSpeed():
	time.sleep(pctOn*delay)
	motorDriver.motorsOff()
	time.sleep((1-pctOn)*delay)

#Loop a couple of times
while True:
	#Get the new camera update from the 
	info = cameraThread.getBallInfo()
	if (info):
		if (not info == True):
		#so that we can break at any point
			x = info[0]
			y = info[1]
			#print(x)
			radius = info[2]
			theta = info[3]

			#If the ball is off center left, spin that way
			if (x < (cameraThread.width/2 - 100)):
				motorDriver.right(False)
				motorDriver.left(True)
				reduceSpeed()

			#If the ball is off center right, spin that way
			elif (x > (cameraThread.width/2 + 100)):
				motorDriver.right(True)
				motorDriver.left(False)
				reduceSpeed()

			# For now, if the ball is centered, charge it head on
			else:
				if prevAngle > theta:
					servo.setServoPos(prevAngle - 4, 10)
					prevAngle -= 4
				elif prevAngle < theta:
					servo.setServoPos(prevAngle + 4, 10)
					prevAngle += 4
				motorDriver.forward()
				reduceSpeed()
				
		else:
			motorDriver.left(True)
			motorDriver.right(False)
			reduceSpeed()
