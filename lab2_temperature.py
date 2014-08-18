#!/usr/bin/python
import json
import requests
import RPi.GPIO as GPIO
import subprocess
import time

from daemon import runner


### Change it ###
DHT_GPIO_PIN = 4  # Your DHT-11 sensor attachs to which GPIO PIN
LIGHT_GREEN_RPI_PIN = 11  # Your green led light attachs to which RPI PIN(11 == GPIO#17)
LIGHT_RED_RPI_PIN = 21  # Your green led light attachs to which RPI PIN(21 == GPIO#9)
HOT_TEMPERATURE = 20  # Over NN degree will send notification to browser. 
REG_ID = "APA91bF1h5IRFoSFIi1s1v1xd3QQkMEM5OOnDBK3YqopMPmTpIe09ifHW4gBbdnAKUF3LoU1PRCeRj602n91jvEBAplPpYctyi4c_Qx5InSM5kplm9vbksES0AIxDP1Vy2qcVi54_BuIE8HvctfmI1tR4z58pEOV6Q"
TIMES = 5  # Check by every 5 seconds

### Dont change below ###
CMD = """sudo /home/pi/dht_reader_c 11 %s""" % DHT_GPIO_PIN
GCM_URL = "https://android.googleapis.com/gcm/send"
HEADERS = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
          'Authorization': 'key=AIzaSyAR3CczWPVkkUxeuqoM5aOE6nvBM7pbuTo'}

### Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LIGHT_GREEN_RPI_PIN, GPIO.OUT)
GPIO.setup(LIGHT_RED_RPI_PIN, GPIO.OUT)
GPIO.output(LIGHT_GREEN_RPI_PIN, GPIO.HIGH)
GPIO.output(LIGHT_RED_RPI_PIN, GPIO.LOW)

### Daemon
class App():
 def __init__(self):
     self.stdin_path = '/dev/null'
     self.stdout_path = '/dev/tty'
     self.stderr_path = '/dev/tty'
     self.pidfile_path =  '/tmp/probe_temperature_daemon.pid'
     self.pidfile_timeout = 5 

 def run(self):
   while True:
     temperature = subprocess.Popen([CMD],
                   	stdout=subprocess.PIPE,
                   	shell=True).communicate()[0]
     if temperature:
       print 'Current temperature is: %s' % temperature
       if int(temperature) >= HOT_TEMPERATURE:
         GPIO.output(LIGHT_GREEN_RPI_PIN, GPIO.LOW)
         GPIO.output(LIGHT_RED_RPI_PIN, GPIO.HIGH)

         payload = {'registration_id': REG_ID,
                    'data.Temperature':'%s is too HOT now...' % temperature}
         response = requests.post(GCM_URL, data=payload, headers=HEADERS)
         print "Hot temperature! Sending alert..."

     else:
       print 'We cant catch data from DHT-11 output...Trying in %s sec.' % TIMES

     time.sleep(TIMES)


app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
