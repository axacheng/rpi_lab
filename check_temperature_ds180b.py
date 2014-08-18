#!/usr/bin/python
import json
import requests
import subprocess
import time

from daemon import runner

### Change it ###
DS18B20_PATH = '/sys/bus/w1/devices/28-000005b89736'
HOT_TEMPERATURE = 30
REG_ID = "APA91bH5jnJvKiM2R2TowvbE2sGNJHwFCYwhHxkcfIOG2iZMncI3awCEFFEnjXx1LLW7Qt2zZqo9IHVBMFnH3Q2w-_ohluhEmOs-n5Z6jNbTpeEjSE8oz75rlzAKjaLLBpTPCN1c3PG8zCMYV6iZs6DNzUJu60jSqQ"
TIMES = 30  # You could set it for 1 minute. (60 seconds)

### Dont change below ###
#CMD = """cat %s/w1_slave |grep -o t=.* | cut -d '=' -f 2""" % DS18B20_PATH
CMD = """echo 30000"""
GCM_URL = "https://android.googleapis.com/gcm/send"
HEADERS = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
          'Authorization': 'key=AIzaSyAR3CczWPVkkUxeuqoM5aOE6nvBM7pbuTo'}


class App():
 def __init__(self):
     self.stdin_path = '/dev/null'
     self.stdout_path = '/dev/tty'
     self.stderr_path = '/dev/tty'
     self.pidfile_path =  '/tmp/probe_temperature_daemon.pid'
     self.pidfile_timeout = 5 

 def run(self):
   while True:
     temperature = float(subprocess.Popen([CMD],
                         stdout=subprocess.PIPE,
                         shell=True).communicate()[0]) / 1000
     print 'Current temperature is: %s' % temperature

     if temperature >= HOT_TEMPERATURE:
       payload = {'registration_id': REG_ID,
                  'data.Temperature':'%s is too HOT now...' % temperature}
       response = requests.post(GCM_URL, data=payload, headers=HEADERS)
       #print response.text  # (TODO) You can save log to /var/log/xxx.log

     time.sleep(TIMES)


app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
