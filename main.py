#ODB2 datalogger

import obd
import firebaseComm
import signal
import sys
import os
import configparser
import argparse
import time

#Parse arguments
argparser = argparse.ArgumentParser(description="Collect OBD2 data and send it to Firebase")
argparser.add_argument('-c', '--config', default='obd2logger.conf')
args = argparser.parse_args()

#Get settings from configfile
config = configparser.ConfigParser()
config.optionxform = str
try:
	config.read(args.config)
except(Exception, e):
	print(e)

#What to do when we receive a signal
def signal_handler(signal, frame):
	connection.close()
	sys.exit(0)
	
#Register our signal handler
signal.signal(signal.SIGINT, signal_handler)

#Connect OBD adapter
connection = obd.OBD(config.get('Connection', 'serial_port'))

while True:
	for command, value in config.items('Collection'):
		if value == "1":
			request = connection.query(obd.commands[command])
			if not request.is_null():
				print(request.value)
				firebaseComm.send(command, str(request.value))
	time.sleep(1)