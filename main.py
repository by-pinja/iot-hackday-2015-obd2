#ODB2 datalogger

import obd

connection = obd.OBD()

while true:
    request = connection.query(obd.commands.RPM)

    if not r.is_null():
        print(r.value)