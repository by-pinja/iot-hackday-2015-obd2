import obd
import firebaseComm

def getCarId(connection) : 
	try: 
		request = connection.query(obd.commands[9][2])
	except:
		return
		
	if not request.is_null():
		print(request.value)
		return request.value


	
def getValues(carId, connection) : 
	request = connection.query(obd.commands.RPM)
	if request.is_null():
		print("Could not get value")
		return 
		
	print(request.value)

	firebaseComm.send(str(carId), 'RPM', str(request.value))
