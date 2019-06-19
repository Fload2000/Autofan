import os
import time 
import datetime
import sys
import RPi.GPIO as GPIO
from time import sleep

# The Pin ID of the Fan
fanPin = 17

# The maximum temperature in Celsius after which we trigger the fan
desiredTemp = 36
# The amplitdue to the temperature the fan should cool the CPU
amplitudeTemp = 2

# Time in secounds
delay = 5

# Max Fan Speed
maxValue = 100
# Min Fan Speed
minValue = 85

# The desired temp the fan cools the chip
coolingTemp = desiredTemp - amplitudeTemp

# The difference between the two fan speeds
diffValue = maxValue - minValue

# Variable for the current state of the fan
fanRunning = False

# Variable for the fan speed the fan will be set to
fanSpeed = 100


# Start time when fan should not run
starttime = datetime.time(0,0,0)
# End time till fan should not run
endtime = datetime.time(8,0,0)
# Delay between checking if current time is between starttime and endtime
delaytime = 600


# Function for getting the current temperature of the CPU
def getCPUtemperature():
	res = os.popen('vcgencmd measure_temp').readline()
	return float(res.replace("temp=","").replace("'C\n",""))


# Function for switching the fan off
def fanOFF():
	global fanRunning
	fanRunning = False
	# switch fan off
	myPWM.ChangeDutyCycle(0)
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
		# Check if current time is in timerange when fan should not spinning
		if time_in_range(starttime, endtime, datetime.datetime.now().time()): 
			# Switch the fan off
			fanOff()
			# Wait delaytime until to rerun the loop
			sleep(delaytime)
		else:
			# Call function autofan
			autofan()
			# Read the temperature every 5 secounds
			sleep(delay)
# trap a CTRL+C keyboard interrupt 
except KeyboardInterrupt:
	# Switch the fans off
	fanOFF()
finally:
	# Reset all GPIO ports used by this script
	GPIO.cleanup()
