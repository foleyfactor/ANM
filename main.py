import ball_tracking
import motorDriver
import threading
import time
import servo

#Create a ball tracker, and start the thread
cameraThread = ball_tracking.BallTracker()
cameraThread.start()

prevAngle = 0

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
			if (x < cameraThread.width/2 - 25):
				motorDriver.right(False)
				motorDriver.left(True)

			#If the ball is off center right, spin that way
			elif (x > cameraThread.width/2 + 25):
				motorDriver.right(True)
				motorDriver.left(False)

			# For now, if the ball is centered, charge it head on
			else:
				if abs(prevAngle - theta) > 2:
<<<<<<< HEAD
		#			if prevAngle > theta:
		#				servo.setServoPos(prevAngle - 4, 10)
		#				prevAngle -= 4
		#			elif prevAngle < theta:
		#				servo.setServoPos(prevAngle + 4, 10)
		#				prevAngle += 4
=======
>>>>>>> 3b3d512e550af60bc7eae8451e905c697838e55a
					servo.setServoPos(theta, 2)
					prevAngle = theta
				motorDriver.forward()
				
		else:
			motorDriver.left(True)
			motorDriver.right(False)
