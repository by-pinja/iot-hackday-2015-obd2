def send(id, key, values) :
	from firebase import firebase
	firebase = firebase.FirebaseApplication('https://iot-hackday-2015-obd.firebaseio.com/#-K2MNiBPat6HFvMTPzvH|538e987b441a5745a2104b9327323650', None)

	print(values)
	addr = '/'+id+'/'+key	
	result = firebase.post(addr , values)
