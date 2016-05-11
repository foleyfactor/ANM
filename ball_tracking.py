from collections import deque
from picamera.array import PiRGBArray
import math
import threading
import picamera
import io
import numpy as np
import argparse
import imutils
import time
import cv2
import copy

class BallTracker(threading.Thread):

	def __init__(self):
		self.streaming = False
		self.ballInfo = None
		self.width = 640
		self.height = 480
		threading.Thread.__init__(self)

	def kill(self):
		self.streaming = False

	def getBallInfo(self):
		print("ball info received")
		ball = copy.deepcopy(self.ballInfo)
		print(ball)
		self.ballInfo = None
		return ball

	def run(self):
		#Streaming resolution/framerate variables
		self.streaming = True
		stream = io.BytesIO()
		camera = picamera.PiCamera()
		camera.resolution = (640,480)
		camera.framerate = 32

		#Actual image
		rawCapture = PiRGBArray(camera, size=(640, 480))

		#Mask params
		greenLower = (25, 125, 125)
		greenUpper = (50, 255, 255)

		#Streaming video
		for fr in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
			#Apply mask
			frame = fr.array
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			mask = cv2.inRange(hsv, greenLower, greenUpper)
			mask = cv2.erode(mask, None, iterations=2)
			mask = cv2.dilate(mask, None, iterations=2)

			#Find contours
			cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)[-2]
			center = None

			#Any contours found?
			if len(cnts) > 0:
				#Maximal contour information
				c = max(cnts, key=cv2.contourArea)
				((x, y), radius) = cv2.minEnclosingCircle(c)
				M = cv2.moments(c)
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

				#Calculations required for distance
				fov = math.radians(28.5)
				widthPixels = 600
				objectSize = 0.03429
				distance = 1/(2*math.tan(fov))*widthPixels*objectSize*(1/radius)

				#Calculations required for servo angle
				heightReal = objectSize
				heightPixels = 2*radius
				displacementPixels = 240-y
				displacementReal = displacementPixels*(heightReal/heightPixels)
				theta = math.degrees(math.atan(displacementReal/distance))
				
				#Express to the user through print/circle drawn
				print("Ball:\n\t"+str(distance)+"m away.\n\t"+str(theta)+" degrees.")

				cv2.circle(frame, (int(x), int(y)), int(radius),
					(0, 255, 255), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)

				self.ballInfo = [x, y, radius, theta]

			else:
				print("No ball")
				self.ballInfo = True
			
			#Show frame to user
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF

			if self.streaming == False:
				break

			rawCapture.truncate(0)

		camera.release()
		cv2.destroyAllWindows()
