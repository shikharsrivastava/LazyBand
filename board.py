
import time
import pygame
import numpy

pygame.mixer.init()
pygame.mixer.set_num_channels(100)
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

		self.EPOCH = int(time.time())
		self.INTERVAL = 5
		
		self.board = [[[] for _ in range(self.col)] for _ in range(self.row)]

	def broadcast(self):
		pass

		# todo
	def getRelativeTime(self):
		return 1

	def getCellInfo(self, x, y):
		
		unit = (self.maxAmp - self.minAmp) / self.col
		vol = self.minAmp + unit * y

		unit = (self.maxFreq - self.minFreq) / self.row
		dur = self.minFreq + unit * x

		return vol, dur


		

	def play(self, sound):
		channelObj = pygame.mixer.Channel(sound.id)
		channelObj.set_volume(sound.volume)
		channelObj.play(sound.sound, loops = -1)

	def getFreeId(self):
		return self.freeIds.pop()


	def add(self, soundName, x, y):

		# get relative time from epoch
		ahead = self.getRelativeTime()

		vol, dur = self.getCellInfo(x, y)

		id = self.getFreeId()

		sound = Sound(id, soundName, ahead, dur, vol)
		
		self.board[x][y].append(sound)

		#self.broadcast(sound)

		self.play(sound)


if __name__ == '__main__':
	# row, col, minFreq, maxFreq, minAmp, maxAmp
	b = MusicBoard(5, 5, 0.5, 1.5, 0.5, 1)

	b.add('./sounds/drum.wav', 2, 0)
	b.add('./sounds/piano.wav', 2,1)
	b.add('./sounds/drum.wav', 2, 2)
	b.add('./sounds/piano.wav', 3, 3)
	b.add('./sounds/drum.wav', 1, 4)
	b.add('./sounds/piano.wav', 4,2)
	b.add('./sounds/drum.wav', 1, 1)
	b.add('./sounds/piano.wav', 2, 3)

	while True:
		pass



