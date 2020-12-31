import socket
import json
import time
import sys
user = input("Enter username :: ")
Client = socket.socket()
host = "127.0.0.1"
port = 2777
Client.connect((host,port))

data = Client.recv(2048)

print(data.decode())

choice = 9
while choice:
	print("Enter Choice :: \n1 | Create \n2 | Delete\n3 | Read\n0 | Exit")
	choice = int(input("Enter>> "))
	if (choice == 1):

		data = user + "/create"
		
		Client.send(data.encode())
		
		data = Client.recv(2048)
		print(data.decode())
		
		data = input("Enter File Path :: ")
		Client.send(data.encode())
		
		mes = {}
		
		flag = 1
		while flag:
			key = input("Enter Key (32 char.) :: ")
			if len(key) == 32:
				flag = 0
			else:
				print("Keys' size is does not match with 32 char. .Please enter again.")
		
		ts = int(input("Enter Time-To-Live in seconds (if not enter -1):: "))
		if ts > -1:
			ts = time.time() + ts 
		
		mes[key] = {}
		mes[key]["time"] = ts
		
		flag = 1
		while flag:
			lst = list(map(str,input("Enter Fields Name (separation with comma',') :: ").split(",")))
			for i in lst:
				mes[key][i] = input("Please enter value for "+i+" :: ")
			if sys.getsizeof(mes) < 16*1024:
				flag = 0
			else:
				print("Datasize exceeded....please enter data less then 16kb.")
		print(mes)
		
		mes = json.dumps(mes)
		Client.send(mes.encode())
		
		data = Client.recv(2048*8)
		print(data.decode())
		
		
	elif (choice == 2):
		data = user + "/delete"
		Client.send(data.encode())
		data = Client.recv(2048)
		print(data.decode())
		
		path = input("Enter file path :: ")
		Client.send(path.encode())
		data = Client.recv(2048)
		print(data.decode())
		
		data = data.decode()
		if data == "Invalid Key":
			continue
		flag = 1
		while flag:
			Key = input("Enter Key (32 char.) :: ")
			if len(Key) == 32:
				flag = 0
			else:
				print("Invalid key constraint.Please enter 32 char. key")
		Client.send(Key.encode())
		data = Client.recv(2048)
		print(data.decode())
		
		
	elif (choice == 3):
		data = user + "/read"
		Client.send(data.encode())
		data = Client.recv(2048)
		print(data.decode())
		
		path = input("Enter file path :: ")
		Client.send(path.encode())
		data = Client.recv(2048)
		print(data.decode())
		
		data = data.decode()
		if data == "Invalid path":
			continue
		flag = 1
		while flag:
			Key = input("Enter Key (32 char.) :: ")
			if len(Key) == 32:
				flag = 0
			else:
				print("Invalid key constraint.Please enter 32 char. key")
		Client.send(Key.encode())
		data = Client.recv(204800)
		data = data.decode()
		#data = json.loads(data)
		print(data)
		
	elif (choice == 0):
		data = user + "/exit"
		Client.send(data.encode())
		data = Client.recv(2048)
		print(data.decode())
	else:
		print("Invalid Input, try once again.")
	print("\n")
