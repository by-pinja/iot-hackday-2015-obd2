#ODB2 datalogger

import obd
import signal
import sys
import configparser
import argparse
import time
from firebase import firebase
from multiprocessing import Process, freeze_support

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

activeCommand = ''

if __name__ == '__main__':
	freeze_support()

	#Initialize firebase connection
	fconn = firebase.FirebaseApplication('https://iot-hackday-obd2.firebaseio.com/')

	asyncConnection = obd.Async(config.get('Connection', 'serial_port'))

	list = []
	for command in asyncConnection.supported_commands:
		list.append(command.name)
	#fconn.patch('', {'SUPPORTED_COMMANDS':list})

	#What to do when we receive a signal
	def signal_handler(signal, frame):
		stopSession()

		asyncConnection.close()
		sys.exit(0)

	#Register our signal handler
	signal.signal(signal.SIGINT, signal_handler)

	def resetActiveCommand():
		activeCommand = ''

		fconn.patch('', {'ACTIVE_COMMAND':activeCommand})

	def valueReceived(response):
		global process_pool
		if response.command.name == 'STATUS':
			return

		if response.value == None:
			response.value = 0

		addr = 'LIVE_DATA/'+ response.command.name
		data = {'value':response.value, 'unit':response.unit,'time':response.time}

		fconn.post(addr , data)

	def dashboardValueReceived(response):
		global process_pool

		if response.command == None:
			return

		if response.value == None:
			response.value = 0

		addr = 'DASHBOARD/'
		data = {response.command.name:response.value}
		fconn.patch(addr, data)


	def stopSession():
		if activeCommand == 'ERROR_CODES' or activeCommand == 'ERROR_CODE_RESET' or activeCommand == 'ERROR_CODE_FREEZE_FRAME':
			return

		asyncConnection.stop()
		asyncConnection.unwatch_all()

	def readErrorCodes():
		global asyncConnection
		asyncConnection.close()

		time.sleep(1)
		connection = obd.OBD(config.get('Connection', 'serial_port'))
		r = connection.query(obd.commands.GET_DTC)
		connection.close()
		time.sleep(1)
		asyncConnection = obd.Async(config.get('Connection', 'serial_port'))

		addr = 'ERROR_CODES/'
		data = r.value
		print(data)
		if data == None:
			data = {'time':str(int(time.time())), 'DTCs':['None']}
		else:
			data = {'time':str(int(time.time())), 'DTCs':data}
		fconn.post(addr , data)
		resetActiveCommand()

	def resetErrorCodes():
		global asyncConnection
		asyncConnection.close()

		time.sleep(1)
		connection = obd.OBD(config.get('Connection', 'serial_port'))
		connection.query(obd.commands.CLEAR_DTC)
		connection.close()
		time.sleep(1)
		asyncConnection = obd.Async(config.get('Connection', 'serial_port'))
		readErrorCodes()

	def readFreezeErrorCodes():
		print('NOT IMPLEMENTED!')
		resetActiveCommand()

	def startSession():
		#read PID configuration
		sessionConfig = fconn.get('LIVE_PID_CODES', '')

		if sessionConfig != None:
			for key,  pids in sessionConfig.items():
				if pids == None:
					continue

				for pid, command in pids.items():
					asyncConnection.watch(obd.commands[command], callback=valueReceived)

		asyncConnection.start()


	def startDashboard():
		print('startDashboard')

		asyncConnection.watch(obd.commands.FUEL_LEVEL, callback=dashboardValueReceived)
		asyncConnection.watch(obd.commands.RPM, callback=dashboardValueReceived)
		asyncConnection.watch(obd.commands.COOLANT_TEMP, callback=dashboardValueReceived)
		asyncConnection.watch(obd.commands.SPEED, callback=dashboardValueReceived)
		asyncConnection.watch(obd.commands.INTAKE_TEMP, callback=dashboardValueReceived)
		asyncConnection.watch(obd.commands.OIL_TEMP, callback=dashboardValueReceived)

		asyncConnection.start()


	startDashboard()

	while True:
		newCommand = fconn.get('','ACTIVE_COMMAND')

		if activeCommand != newCommand:
			stopSession()
			activeCommand = newCommand

			if activeCommand == 'ERROR_CODES':
				readErrorCodes()
			elif activeCommand == 'ERROR_CODE_RESET':
				resetErrorCodes()
			elif activeCommand == 'ERROR_CODE_FREEZE_FRAME':
				readFreezeErrorCodes()
			elif activeCommand == 'LIVE_DATA':
				startSession()
			else:
				#activeCommand == 'DASHBOARD'
				startDashboard()


