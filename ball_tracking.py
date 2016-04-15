# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

# import the necessary packages
from collections import deque
from picamera.array import PiRGBArray
import threading
import picamera
import io
import numpy as np
import argparse
import imutils
import time
import cv2

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
		ball = self.ballInfo
		self.ballInfo = None
		return ball

	def run(self):
		self.streaming = True
		# construct the argument parse and parse the arguments
		stream = io.BytesIO()
		camera = picamera.PiCamera()
		camera.resolution = (640,480)
		camera.framerate = 32

		rawCapture = PiRGBArray(camera, size=(640, 480))
		#resize(600, 338)

		# define the lower and upper boundaries of the "green"
		# ball in the HSV color space, then initialize the
		# list of tracked points
		greenLower = (29, 56, 6)
		greenUpper = (64, 255, 255)
		pts = deque(maxlen=64)

		for fr in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
			frame = fr.array
			#data = np.fromstring(stream.getvalue(), dtype=np.uint8)

			#frame = cv2.imdecode(image,1)

			# resize the frame, blur it, and convert it to the HSV
			# color space
			#frame = imutils.resize(frame, width=600)
			# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

			# construct a mask for the color "green", then perform
			# a series of dilations and erosions to remove any small
			# blobs left in the mask
			mask = cv2.inRange(hsv, greenLower, greenUpper)
			mask = cv2.erode(mask, None, iterations=2)
			mask = cv2.dilate(mask, None, iterations=2)

			# find contours in the mask and initialize the current
			# (x, y) center of the ball
			cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)[-2]
			center = None

			# only proceed if at least one contour was found
			if len(cnts) > 0:
				# find the largest contour in the mask, then use
				# it to compute the minimum enclosing circle and
				# centroid
				c = max(cnts, key=cv2.contourArea)
				((x, y), radius) = cv2.minEnclosingCircle(c)
				M = cv2.moments(c)
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

				# only proceed if the radius meets a minimum size
				if radius > 10:
					# draw the circle and centroid on the frame,
					# then update the list of tracked points
					print(radius)
					cv2.circle(frame, (int(x), int(y)), int(radius),
						(0, 255, 255), 2)
					cv2.circle(frame, center, 5, (0, 0, 255), -1)

				self.ballInfo = [x, y, radius]

			else:
				self.ballInfo = True

			# update the points queue
			pts.appendleft(center)

			# loop over the set of tracked points
			for i in range(1, len(pts)):
				# if either of the tracked points are None, ignore
				# them
				if pts[i - 1] is None or pts[i] is None:
					continue

				# otherwise, compute the thickness of the line and
				# draw the connecting lines
				thickness = int(np.sqrt(64/ float(i + 1)) * 2.5)
				cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

			# show the frame to our screen
			cv2.imshow("Frame", frame)
			#cv2.imshow("k", mask)
			key = cv2.waitKey(1) & 0xFF

			# if the 'q' key is pressed, stop the loop
			if self.streaming == False:
				break

			rawCapture.truncate(0)

		# cleanup the camera and close any open windows
		camera.release()
		cv2.destroyAllWindows()