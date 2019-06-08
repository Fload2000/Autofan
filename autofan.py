import os
import time 
import datetime
import sys
import RPi.GPIO as GPIO
from time import sleep

# INPUTS
fanPin = 17 # The Pin ID of the Fan

desiredTemp = 36 # The maximum temperature in Celsius after which we trigger the fan
amplitudeTemp = 2 # The amplitdue to the temperature the fan should cool the CPU

delay = 5	# time in secounds

maxValue = 100	# Max Fan Speed
minValue = 85 	# Min Fan Speed


coolingTemp = desiredTemp - amplitudeTemp	# The desired temp the fan cools the chip

diffValue = maxValue-minValue	# The defference between the two fan speeds

fanRunning = False	# Variable for knowing the current state of the fan

fanSpeed = 100	# Variable for the fan speed the fan will be set to

starttime = datetime.time(0,0,0)	# Start time when fan should not run
endtime = datetime.time(8,0,0)		# End time till fan should not run
delaytime = 600

# Function for getting the current temperature of the CPU
def getCPUtemperature():
	res = os.popen('vcgencmd measure_temp').readline()
	return float(res.replace("temp=","").replace("'C\n",""))

# Function for switching the fan off
def fanOFF():
	global fanRunning
	fanRunning = False
	myPWM.ChangeDutyCycle(0)   # switch fan off
	return()

# Function for mapping the temperature to the right fan speed
def mapSpeed(difference):
	global diffValue
	value = maxValue - (diffValue/difference)
	if value < minValue:
		return minValue
	elif value >= minValue:
		return value
	elif value > maxValue:
		return 100

# Function for setting the fan speed automatically
def autofan():
	global fanSpeed, fanRunning
	temperature = getCPUtemperature()
	print(temperature)
	if fanRunning:
		if temperature <= coolingTemp:
			fanRunning = False
			fanSpeed = 0
		elif temperature > coolingTemp:
			difference = temperature - coolingTemp
			fanSpeed = mapSpeed(difference)
	elif not fanRunning:
		if temperature <= desiredTemp:
			fanSpeed = 0
		elif temperature > desiredTemp:
			fanRunning = True
			difference = temperature - coolingTemp
			fanSpeed = mapSpeed(difference)
	print(fanSpeed)
	myPWM.ChangeDutyCycle(fanSpeed)
	return()

# Function for checking time in timerange
def time_in_range(start, end, x):
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end	
	
# MAIN
try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(fanPin, GPIO.OUT)
	myPWM = GPIO.PWM(fanPin,50)
	myPWM.start(50)
	GPIO.setwarnings(False)
	
	fanOFF()
	
	while True:
		if time_in_range(starttime, endtime, datetime.datetime.now().time()): # Check if current time is in timerange when fan should not spinning
			fanOff()			# switch the fan off
			sleep(delaytime)	# Wait delaytime until to rerun the loop
		else:
			autofan()				# call def autofan
			sleep(delay) # Read the temperature every 5 sec, increase or decrease this limit if you want 
except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt 
	fanOFF()	# switch the fans off
finally:
	GPIO.cleanup() # resets all GPIO ports used by this program

