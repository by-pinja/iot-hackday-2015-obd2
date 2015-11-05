#ODB2 datalogger

import obd
import firebaseComm
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
    request = connection.query(obd.commands.RPM)

    if not request.is_null():
        print(request.value)
        firebaseComm.send('RPM', str(request.value))