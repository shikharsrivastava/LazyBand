import socket
import pygame


BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED= (255,0,0)
GREEN = (0, 255,0)
BLUE = (0,0, 255)
AQUA=(0, 255, 255)
FUCHSIA=(255,0, 255)
GRAY=(128, 128, 128)
OLIVE=(128, 128,0)
PURPLE=(128,0, 128)
YELLOW=(255, 255,0)
TEAL=( 0, 128, 128)

pygame.init()
DISPLAY = pygame.display.set_mode((1360,650))
pygame.display.set_caption('LazyBand')

DISPLAY.fill(BLACK)






INITIAL_X=120
INITIAL_Y=80
ENDING_X = 800
ENDING_Y = 600
LINE_COUNT = 4

SOUND_BOARD_LENGTH = 350
GAP = 50

SOUND_INX = ENDING_X + GAP
SOUND_EX = SOUND_INX + SOUND_BOARD_LENGTH
PLAY_CHANNEL = 101

GRID_ROW = 5
GRID_COLUMN = 5

HOST = '127.0.0.1'
PORT = 8401

def send_data(sock,data):
	sock.sendall(data)

def receive_data(sock,size = 4096):
	data = bytes()
	while size:
		recv = sock.recv(size)
		if not recv:
			raise ConnectionError()
		data += recv
		size -= len(recv)
	return data

def nDigit(s,size):
	s = str(s)
	if(len(s)<size):
		s = '0'*(size-len(s))+s
	return s

def send_bytes(sock,data):
	size = nDigit(len(data),5).encode('utf-8')
	send_data(sock,size+data)

def receive_bytes(sock):
	size = receive_data(sock,5).decode('utf-8')
	data = receive_data(sock,int(size))
	return data

def create_listening_socket(host,port,size):
	listening_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	listening_socket.bind((host,port))
	listening_socket.listen(100)
	return listening_socket

def receive_message(sock):
	size = receive_data(sock,5).decode('utf-8')
	msg = receive_data(sock,int(size)).decode('utf-8')
	return msg

def send_message(sock,message):
	message = message.encode('utf-8')
	size = nDigit(len(message),5).encode('utf-8')
	message = size+message
	send_data(sock,message)
