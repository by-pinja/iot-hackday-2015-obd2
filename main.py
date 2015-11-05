#ODB2 datalogger

import odb

connection = obd.OBD()

while true:
    request = connection.query(obd.commands.RPM)

    if not r.is_null():
        print(r.value)