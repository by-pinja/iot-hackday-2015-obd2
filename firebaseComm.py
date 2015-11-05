def send(fconn, id, key, values) :
	print(values)
	addr = '/'+id+'/'+key
	result = fconn.post(addr , values)
	#result = fconn.push(addr , values)