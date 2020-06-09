import os
import glob
import time
import RPi.GPIO as GPIO



os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

temp = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
p = GPIO.PWM(17,50)

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp = float(temp_string) / 1000.0
		print temp
		#temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp

def idle_read():
	global temp
	print "System is in Idle state"
	while True:
		temp = read_temp()
		if temp < 25:
			led_heating()
		elif temp > 25:
			fan_cooling()
		else:
			print "System is in Idle state"

def led_heating():
	global temp
	GPIO.output(18, True)
	print "System is in heating state"
	while temp < 25:
		temp = read_temp()
	GPIO.output(18,False)
	idle_read()

def fan_cooling():
	temp = read_temp()
	print "System is in cooling state"
	while temp > 25:
		if temp > 25 and temp < 27:
			print "Fan ON with Duty Cycle 50%"
			p.start(50)
			while temp < 27:
				temp = read_temp()
			p.stop()
		elif temp > 27 and temp < 29:
			print "Fan ON with Duty Cycle 75%"
			p.start(75)
			while temp < 29:
				temp = read_temp()
			p.stop()
		elif temp > 29:
			print "Fan ON with Duty Cycle 100%"
			p.start(100)
			while temp > 29:
				temp = read_temp()
			p.stop()
		temp = read_temp()
	GPIO.output(17, False)
	idle_read()



try:
	idle_read()


finally:
	GPIO.cleanup()
