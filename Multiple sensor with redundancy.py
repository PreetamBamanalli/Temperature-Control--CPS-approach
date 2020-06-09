import os
import glob
import time
import RPi.GPIO as GPIO


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices'
 
sensor1 = '/28-3c01a816c2fd'
sensor2 = '/28-3c01a8163747'
sensor3 = '/28-3c01a8161d87'

temp = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
p = GPIO.PWM(17,50)

def read_temp_raw_1(addr):
	base_dir = '/sys/bus/w1/devices'+ addr
	device_file = base_dir + '/w1_slave'
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp_raw(address):
	addr = address
	lines = read_temp_raw_1(addr)
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw_1()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp = float(temp_string) / 1000.0
		#print temp1
		return temp

def read_temp():
	t1 = read_temp_raw(sensor1)
	print "t1="
	print t1
	t2 = read_temp_raw(sensor2)
	print "t2="
	print t2
	t3 = read_temp_raw(sensor3)
	print "t3="
	print t3
	a = t1 - t2
	b = t2 - t3
	c = t3 - t1 
	if (a > 0.75 or a < -0.75) and (c < -0.75 or c > 0.75):
		print "Sensor 1 is faulty"
		return t2
	elif (a > 0.75 or a < -0.75) and (b < -0.75 or b > 0.75):
		print "Sensor 2 is faulty"
		return t3
	elif (b > 0.75 or b < -0.75) and (c < -0.75 or c > 0.75):
		print "Sensor 3 is faulty"
		return t1

def idle_read():
	while True:
		temp = read_temp()
		if temp < 25:
			led_heating()
		elif temp > 25:
			fan_cooling()
		else:
			print "System is in Idle state"

def led_heating():
	temp = read_temp()
	print "System is in heating state"
	while temp < 25:
		GPIO.output(18, True)
		temp = read_temp()
	GPIO.output(18,False)
	idle_read()

def fan_cooling():
	temp = read_temp()
	print "System is in cooling state"
	while temp > 25:
		#print "cooling"
		GPIO.output(17, True)
		temp = read_temp()
	GPIO.output(17, False)
	idle_read()


try:
	idle_read()

finally:
	GPIO.cleanup()
