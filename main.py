#ODB2 datalogger

import obd
import obdReader
import signal
import sys
import os
import configparser
import argparse
import time
from firebase import firebase

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
	
#Initialize firebase connection
fconn = firebase.FirebaseApplication('https://iot-hackday-2015-obd.firebaseio.com/#-K2MNiBPat6HFvMTPzvH|538e987b441a5745a2104b9327323650', None)

#What to do when we receive a signal
def signal_handler(signal, frame):
	connection.close()
	fconn.goOffline()
	sys.exit(0)
	
#Register our signal handler
signal.signal(signal.SIGINT, signal_handler)

#Connect OBD adapter
connection = obd.OBD(config.get('Connection', 'serial_port'))

carId = obdReader.getCarId(connection)
if not carId :
	print("Unable to read car ID")
	carId = 'TestCar'

while True:
	for command, value in config.items('Collection'):
		if value == "1":
			obdReader.getValues(fconn, connection, carId, command)

	time.sleep(1)
	
	
	
	
	
		
