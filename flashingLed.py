import RPi.GPIO as g
import time

g.setmode(g.BCM)
g.setup(22, g.OUT)

g.ouput(22, False)
for i in range(10):
	g.output(22, True)
	time.sleep(1)
	g.output(22, False)
	time.sleep(1)