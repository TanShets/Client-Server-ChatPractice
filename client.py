import socket
import threading

HEADER = 64
PORT = 9000
FORMAT = 'utf-8'
EXIT_LINES = ["exit", "quit", "close connection"]
SERVER_IP = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER_IP, PORT)

def send_message(message, client):
	print(message)
	encoded_message = message.encode(FORMAT)
	message_length = len(message)
	head_length = str(message_length).encode(FORMAT)
	head_length += b' ' * (HEADER - len(head_length))
	print(client.getsockname()[1])
	client.send(head_length)
	client.send(encoded_message)

def receive_message():
	global client
	print(client.recv(2048).decode(FORMAT))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
new_port, assigned_id = map(int, (client.recv(2048).decode(FORMAT)).split())
while not new_port:
	pass
client.close()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, new_port))
send_message(input("Enter a username: "), client)
msg = None
while assigned_id == None:
	pass
thread = None
'''
print("Type a message and press enter to send a message\n")
while msg == None or msg not in EXIT_LINES:
	thread = threading.Thread(target = receive_message, args = ())
	thread.start()
	msg = input()
	send_message(msg, client)
client.close()
'''