import ball_tracking
import motorDriver
import threading
import time

#Constant control values, TBD
BALL_WIDTH_CONTROL = 20
BALL_CONTROL_Y = 10

#Create a ball tracker, and start the thread
cameraThread = ball_tracking.BallTracker()
cameraThread.start()

#Loop a couple of times
while True:
	#Get the new camera update from the 
	info = cameraThread.getBallInfo()
	if (info):
		if (not info == True):
		#so that we can break at any point
			x = info[0]
			y = info[1]
			radius = info[2]

			#If the ball is off center left, spin that way
			if (x < cameraThread.width/2 + 10):
				motorDriver.right(True)
				motorDriver.left(False)
				break

			#If the ball is off center right, spin that way
			elif (x > cameraThread.width/2 - 10):
				motorDriver.right(False)
				motorDriver.left(True)
				break

			# For now, if the ball is centered, charge it head on
			else:
				motorDriver.forward()

			## Eventually will be calculated using similar triangles
			# ratio = radius/BALL_WIDTH_CONTROL
			# ground = ratio*BALL_CONTROL_Y
			# x -= ground
			# y -= ground		
			#
			## Then use physics to calculate the angle
			# servoControl.angle(physicsAngle)	
			#
			## Then fire the coil gun
			# fire()

		else:
			motorDriver.left(True)
			motorDriver.right(False)