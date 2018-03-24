import utils
import threading
import queue


send_lock = threading.Lock()
send_queues = []

def client_receive(client_socket,client_address,q):
	print("connected to " + str(client_socket) + " " )
	with send_lock:
		send_queues.append(q)

	th = threading.Thread(target = send_to_client,args = [client_socket,q],daemon = True)
	th.start()

	while True:
		print("trying to receive")
		message = utils.receive_message(client_socket)
		print(message)
		with send_lock:
			for qu in send_queues:
				if qu is not q:
					qu.put(message)


def send_to_client(sock,q):
	while True:
		data = q.get()
		if data == None:
			break
		utils.send_message(sock,data)



if __name__ == '__main__':

	listening_socket = utils.create_listening_socket(utils.HOST, utils.PORT, 100)
	while True:
		print("Waiting")
		client_socket,client_address = listening_socket.accept()
		q = queue.Queue()
		th = threading.Thread(target = client_receive, args = [client_socket,client_address,q], daemon = True)
		th.start()