
import time
import pygame
import numpy
from common import *
import utils
import socket
import threading
import json

pygame.mixer.init()
pygame.font.init()
pygame.mixer.set_num_channels(150)
pygame.init()

# Helper function
def getResizedSound(sound, seconds):

		frequency, bits, channels = pygame.mixer.get_init()

		# Determine silence value
		silence = 0 if bits < 0 else (2**bits / 2) - 1

		# Get raw sample array of original sound
		oldArray = pygame.sndarray.array(sound)

		# Create silent sample array with desired length
		newSampleCount = int(seconds * frequency)
		newShape = (newSampleCount,) + oldArray.shape[1:]
		newArray = numpy.full(newShape, silence, dtype=oldArray.dtype)

		# Copy original sound to the beginning of the
		# silent array, clipping the sound if it is longer
		newArray[:oldArray.shape[0]] = oldArray[:newArray.shape[0]]

		return pygame.mixer.Sound(newArray)



class Sound:
	def __init__(self, id, soundName, ahead, dur, vol):
		
		self.id = id
		self.soundName = soundName
		self.ahead = ahead
		self.duration = dur
		self.volume = vol

		sound = pygame.mixer.Sound(self.soundName) 
		self.sound = getResizedSound(sound, self.duration)



	# channelId, name, 


class MusicBoard:

	def __init__(self,row, col, minFreq, maxFreq, minAmp, maxAmp):
		

		self.minFreq = minFreq
		self.maxFreq =maxFreq
		self.minAmp = minAmp
		self.maxAmp = maxAmp

		self.row = row
		self.col = col

		self.freeIds = set([i for i in range(100)])

		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.sock.connect((utils.HOST,utils.PORT))

		self.t = threading.Thread(target = self.receive)
		self.t.start()

		self.EPOCH = time.time()
		self.INTERVAL = 1

		self.board = [[[] for _ in range(self.col)] for _ in range(self.row)]


	def makeLine(self, x, y, color):
		print("drawing on ", x, y)
		x_side = (ENDING_X - INITIAL_X)/GRID_COLUMN
		y_side = (ENDING_Y - INITIAL_Y)/GRID_ROW
		line_side = y_side / LINE_COUNT

		count = len(self.board[x][y])

		x_cord_start = INITIAL_X + y * x_side
		y_cord_start = INITIAL_Y + x * y_side + line_side*count

		x_cord_end = x_cord_start + x_side
		y_cord_end = y_cord_start 

		pygame.draw.line(DISPLAY, color, (x_cord_start, y_cord_start), (x_cord_end, y_cord_end))


	def saveConfig(self):
		pass

	def addOnTime(self, soundName, x, y, ahead):
		
		current_time = time.time()    
		e = 0.01
		
		print("In add time")
		while True:
			t = time.time()
			print("trying to add", str(t))
			if abs( t - int(t) - ahead) <= e:
				self.add(soundName, x, y, True)
				print("added")
				break 




	def addLater(self, soundName, x, y, ahead):
		print("In add later")

		t = threading.Thread(target = self.addOnTime, args = [soundName, x, y, ahead])
		t.start()

	def broadcast(self, x, y, sound, op):
		ahead = sound.ahead
		name = sound.soundName

		message = json.dumps({
				"x": x,
				"y": y,
				"op": op,
				"id": sound.id,
				"name": name,
				"ahead": ahead
			})

		utils.send_message(self.sock, message) 

	def receive(self):
		while True:
			message = utils.receive_message(self.sock)
			data = json.loads(message)
			print("received")
			print(message)

			if(data['op'] == 'add'):
				self.addLater(data['name'], data['x'], data['y'], data['ahead'])
			elif data['op'] == 'del':
				self.delete(data['x'], data['y'], data['id'], True)
			else:
				print("lode lag gye ")


	def getRelativeTime(self):
		t = time.time()
		return t - int(t)

	def getCellInfo(self, x, y):
		
		unit = (self.maxAmp - self.minAmp) / self.col
		vol = self.minAmp + unit * y

		unit = (self.maxFreq - self.minFreq) / self.row
		dur = self.minFreq + unit * x

		return vol, dur


		

	def play(self, sound):
		channelObj = pygame.mixer.Channel(sound.id)
		print("Volume = ", sound.volume)
		channelObj.set_volume(sound.volume)
		channelObj.play(sound.sound, loops = -1)

	def getFreeId(self):
		return self.freeIds.pop()

	def delete(self, x, y, id, broadcasted = False):
		''' deletes the latest instance of sound on that
				grid'''

		if(len(self.board[x][y]) == 0):
			return

		self.makeLine(x, y, BLACK)

		sound = self.board[x][y].pop()
		pygame.mixer.Channel(sound.id).stop()

		if not broadcasted:
			self.broadcast(x, y, sound, "del")

		self.freeIds.add(sound.id)





	def add(self, soundName, x, y, broadcasted = False):

		# get relative time from epoch
		
		if broadcasted:
			print("reveived broadcast sound")
		vol, dur = self.getCellInfo(x, y)

		id = self.getFreeId()

		
		ahead = self.getRelativeTime()

		sound = Sound(id, soundName, ahead, dur, vol)
		
		self.board[x][y].append(sound)

		self.makeLine(x, y, WHITE)

		if not broadcasted: 
			self.broadcast(x, y, sound, "add")

		self.play(sound)
		return id

if __name__ == '__main__':
	# row, col, minFreq, maxFreq, minAmp, maxAmp
	b = MusicBoard(5, 5, 0.5, 1.5, 0.2, 1)

	b.add('./sounds/High-Agogo.wav', 2, 0)
	

	while True:
		pass



