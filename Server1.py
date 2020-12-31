import socket
import threading
import sys
import os
import json
import time
message = {"CON_MSG" : "Connected to server.\n",
			"CON_ACK" : "Connected to IP address ",
			"CON_ERROR" : "Bad connection attempt.",
			"CRE_W":"Wait for while.....",
			"KEY_EXIST":"Key already exist.",
			"KEY_UPDATE":"Key updated.....",
			"MEM_EXC":"Memory limts exceed......"}
temp = 0

def Create(conn):
	global temp
	global WriteOperation
	while WriteOperation:
		continue
	WriteOperation = 1
	Path = conn.recv(2024)
	Path = Path.decode()
	if os.path.exists(Path) == True:
		with open(Path, 'r') as f:
			data = json.load(f)
		data = dict(data)
		Rec = conn.recv(2024*8)
		Rec = Rec.decode()
		Rec = json.loads(Rec)
		print(Rec,type(Rec))
		lst = list(Rec.keys())
		print(lst,type(lst))
		Key = lst[0]
		if Key in data:
			print(message["KEY_EXIST"])
			conn.send("Keys already exist....\n".encode())
		else:
			if os.path.getsize(Path) + sys.getsizeof(Rec) < 1024*1024*1024 :
				data.update(Rec)
				with open(Path, 'w') as json_file:
					json.dump(data, json_file)
				conn.send("New key updated....\n".encode())
				print(message["KEY_UPDATE"])
				f.close()
			else:
				conn.send("Memory Limits Exceed....\n".encode())
				print(message["MEM_EXC"])
	else:
		Rec = conn.recv(2024*8)
		Rec = Rec.decode()
		Rec = json.loads(Rec)
		print(Rec)
		sttr = "file"+str(temp)+".json"
		conn.send("Keys updated at current file location....\n".encode())
		with open(sttr, 'w') as json_file:
			json.dump(Rec, json_file)
		print(message["KEY_UPDATE"])
		temp+=1
	WriteOperation = 0

def HandleConnection(conn,i):
	global WriteOperation
	while True :
		choice = conn.recv(2048)
		choice = choice.decode()
		lst = choice.split("/")
		choice = lst[-1]
		if (choice == "create"):
			data = "Create Operation by user "+lst[0]
			print(data)
			conn.send(" ".encode())
			Create(conn)
		elif (choice == "delete"):
			while WriteOperation:
				continue
			WriteOperation = 1
			data = "Delete Operation by user "+lst[0]
			conn.send(data.encode())
			print(data)
			
			data = conn.recv(2048)
			path = data.decode()
			if os.path.exists(path) == True:
				conn.send(str("Valid path").encode())
			else:
				conn.send(str("Invalid path").encode())
				WriteOperation = 0
				continue
			data = conn.recv(2048)
			Key = data.decode()
			print(data)
			
			with open(path,"r") as f:
				data = json.load(f)
			data = dict(data)
			
			
			#print(data[str(Key)])
			if Key in data:
				if data[str(Key)]["time"] == -1 or int(data[str(Key)]["time"]) > int(time.time()):
					del  data[str(Key)]
					conn.send("Data deleted successfully".encode())
				else:
					conn.send("Data expired".encode())
			else:
				conn.send("Invalid Key".encode())
			#json.dumps(data)
			with open(path, 'w') as json_file:
				json.dump(data, json_file)
			WriteOperation = 0
		elif (choice == "read"):
			while WriteOperation:
				continue
			WriteOperation = 1
			data = "Read Operation by user "+lst[0]
			conn.send(data.encode())
			print(data)
			
			data = conn.recv(2048)
			path = data.decode()
			if os.path.exists(path) == True:
				conn.send(str("Valid path").encode())
			else:
				conn.send(str("Invalid path").encode())
				WriteOperation = 0
				continue
			data = conn.recv(2048)
			Key = data.decode()
			print(data)
			
			with open(path,"r") as f:
				data = json.load(f)
			data = dict(data)
			
			
			#print(data[str(Key)])
			if Key in data:
				if data[str(Key)]["time"] == -1 or int(data[str(Key)]["time"]) > int(time.time()):
					msg = json.dumps(data[str(Key)])
					conn.send(msg.encode())
				else:
					conn.send("Data expired".encode())
			else:
				conn.send("Invalid Key".encode())
			#json.dumps(data)
			
			
			WriteOperation = 0
		elif (choice == "exit"):
			data = "Exiting user ("+lst[0]+")"
			conn.send(data.encode())
			del Thread[i]
			print(data)
			break

def ConnectToClients():
	global Connections
	global server
	global host
	global port
	i=0
	while True:
		conn,add = server.accept()
		conn.send(message["CON_MSG"].encode())
		print(message["CON_ACK"],add[0])
		Connections[str(add[0])] = conn
		th = threading.Thread(target=HandleConnection,args = (conn,i,))
		th.daemon = True
		th.start()
		Thread[i] = th
		i+=1

Thread = {}
WriteOperation = 0
Accept = True
Connections = {}
FilePath = ''
server = socket.socket()
#host = "10.42.0.1"
host = ""
port = 2777

server.bind((host,port))
server.listen(5)
print("Server Started....")
th = threading.Thread(target=ConnectToClients)
th.daemon = True
th.start()
th.join()

