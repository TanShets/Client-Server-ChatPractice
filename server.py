import socket
import threading
import random
import time

class Client:
	def __init__(self, conn, addr, username, id):
		self.conn = conn
		self.addr = addr
		self.username = username
		self.id = id

HEADER = 64
SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 9000
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
EXIT_LINES = ["exit", "quit", "close connection"]
MIN, MAX = 1, 100

random.seed(time.process_time())
assigned_id = random.randint(MIN, MAX)
id_set = []
covered_id = dict()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = dict()
pair_client = dict()

def start():
	server.listen()
	while True:
		conn, addr = server.accept() #Basically gives the connection with client and address
		thread = threading.Thread(target = reorient_connection, args = (conn, addr))
		thread.start()
		print("Point 1:", threading.activeCount() - 1) #Gives no. of active threads except for main thread
	conn.close()

def reorient_connection(conn, addr):
	global assigned_id
	global id_set
	global covered_id
	paired = False
	assigned_id = random.randint(MIN, MAX)
	temp_assigned_id = assigned_id
	print("Set of available ids:", id_set)
	if len(id_set) != 0:
		while temp_assigned_id % 2 == id_set[0] % 2 or covered_id.get(temp_assigned_id, False):
			temp_assigned_id = random.randint(MIN, MAX)

		print(temp_assigned_id % 2 == id_set[0] % 2)
		print(covered_id.get(temp_assigned_id, False))
		#temp_assigned_id = assigned_id
		paired = True
	covered_id[temp_assigned_id] = True
	print()
	print("Assigned id", temp_assigned_id)
	print()
	if(conn):
		new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		new_socket.bind((SERVER_IP, 0))
		connection_val = True
		while connection_val:
			line = str(new_socket.getsockname()[1]) + " " + str(temp_assigned_id)
			conn.send(line.encode(FORMAT))
			connection_val = False
		print(new_socket.getsockname()[1])
		conn.close()
		print(id_set)
		new_socket.listen()
		while True:
			new_conn, new_addr = new_socket.accept() #Basically gives the connection with client and address
			#print("New port here")
			message_length = new_conn.recv(HEADER).decode(FORMAT)
			if message_length:
				message_length = int(message_length)
				username = new_conn.recv(message_length).decode(FORMAT)
				new_conn.send(str(assigned_id).encode(FORMAT))
				new_client = Client(new_conn, new_addr, username, temp_assigned_id)
				clients[new_client.id] = new_client
				if paired:
					pair_client[new_client.id] = id_set[0]
					pair_client[id_set[0]] = new_client.id
					id_set.pop(0)
				else:
					id_set.append(new_client.id)
				thread = threading.Thread(target = handle_client, args = (new_conn, new_addr, username, new_client.id))
				thread.start()
			#handle_client(new_conn, new_addr)
		del clients[new_client.id]
	return

def handle_client(conn, addr, username, id):
	global pair_client
	global clients
	global covered_id
	print("Made it here fam")
	connection_val = True
	while connection_val:
		try:
			message_length = conn.recv(HEADER).decode(FORMAT)
		except:
			message_length = 0
		if message_length:
			message_length = int(message_length)
			try:
				message = conn.recv(message_length).decode(FORMAT)
			except:
				message = "quit"
			print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
			print(message)
			print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
			if message in EXIT_LINES:
				connection_val = False
			else:
				sendOne(message, id)
			del message_length
			del message
	conn.close()
	try:
		del pair_client[pair_client[id]]
	except:
		pass

	try:
		del pair_client[id]
	except:
		pass

	try:
		del clients[id]
	except:
		pass

	try:
		del covered_id[id]
	except:
		pass
	print("Exited")
	return

def sendAll(message, id):
	print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
	print(message)
	print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
	global clients
	to_be_deleted = []
	for i in clients.keys():
		if clients[i].id != id:
			print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
			print(message)
			print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
			try:
				clients[i].conn.send(message.encode(FORMAT))
			except:
				to_be_deleted.append(i)

	for i in to_be_deleted:
		del clients[i]

def sendOne(message, id):
	print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
	print(message)
	print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
	global clients, pair_client
	to_be_deleted = []

	if clients.get(id, False):
		if pair_client.get(id, False):
			try:
				clients[pair_client[id]].conn.send(message.encode(FORMAT))
			except:
				del clients[pair_client[id]]
				del pair_client[id]
	elif pair_client.get(id, False):
		del pair_client[id]

print("Initiating")
start()