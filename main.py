#ODB2 datalogger

import obd
import firebaseComm

connection = obd.OBD()

while True:
    request = connection.query(obd.commands.RPM)  

    if not request.is_null():
        print(request.value)
        firebaseComm.send('RPM', str(request.value))