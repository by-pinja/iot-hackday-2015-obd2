#ODB2 datalogger

import obd
import obdReader
import signal
import sys

#What to do when we receive a signal
def signal_handler(signal, frame):
	connection.close()
	sys.exit(0)
	
#Register our signal handler
signal.signal(signal.SIGINT, signal_handler)

#Find and connect OBD adapter
connection = obd.OBD()

while True:
	carId = obdReader.getCarId(connection)
	if not carId :
		print("Unable to read car ID")
		carId = 'TestCar'
	
	obdReader.getValues(carId, connection)
		
