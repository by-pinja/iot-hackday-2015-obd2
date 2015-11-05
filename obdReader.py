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


	
def getValues(connection,carId, command) : 
	request = connection.query(obd.commands[command], force=True)

	if request.is_null():
		print("Could not get value")
		return 
		
	print(request.value)

	firebaseComm.send(str(carId), command, str(request.value))
