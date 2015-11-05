def send(key, value) :
    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://iot-hackday-2015-obd.firebaseio.com/#-K2MNiBPat6HFvMTPzvH|538e987b441a5745a2104b9327323650', None)

    result = firebase.post('/'+key , value)
    print(result)

