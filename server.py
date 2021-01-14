import socket
import threading
import random

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
MIN, MAX = 1, 1000
assigned_id = 1

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = dict()

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
	if(conn):
		new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		new_socket.bind((SERVER_IP, 0))
		connection_val = True
		while connection_val:
			line = str(new_socket.getsockname()[1]) + " " + str(assigned_id)
			conn.send(line.encode(FORMAT))
			connection_val = False
		assigned_id = (assigned_id + 1) % 2
		print(new_socket.getsockname()[1])
		conn.close()
		new_socket.listen()
		while True:
			new_conn, new_addr = new_socket.accept() #Basically gives the connection with client and address
			#print("New port here")
			message_length = new_conn.recv(HEADER).decode(FORMAT)
			if message_length:
				message_length = int(message_length)
				username = new_conn.recv(message_length).decode(FORMAT)
				new_conn.send(str(assigned_id).encode(FORMAT))
				new_client = Client(new_conn, new_addr, username, random.randint(MIN, MAX))
				clients[new_client.id] = new_client
				thread = threading.Thread(target = handle_client, args = (new_conn, new_addr, username, new_client.id))
				thread.start()
			#handle_client(new_conn, new_addr)
	return

def handle_client(conn, addr, username, id):
	print("Made it here fam")
	connection_val = True
	while connection_val:
		message_length = conn.recv(HEADER).decode(FORMAT)
		if message_length:
			message_length = int(message_length)
			message = conn.recv(message_length).decode(FORMAT)
			print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
			print(message)
			print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
			if message in EXIT_LINES:
				connection_val = False
			else:
				sendAll(message, id)
			del message_length
			del message
	conn.close()
	del clients[id]
	print("Exited")
	return

def sendAll(message, id):
	print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
	print(message)
	print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
	global clients
	for i in clients.keys():
		if clients[i].id != id:
			print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
			print(message)
			print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
			clients[i].conn.send(message.encode(FORMAT))

print("Initiating")
start()