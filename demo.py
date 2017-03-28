#!/usr/bin/python

import create
import time

ROOMBA_PORT='/dev/ttyAMA0'
robot = create.Create(ROOMBA_PORT)

robot.printSensors() 
#while True:
#    robot.printSensors() # debug output
#    time.sleep(0.5)

