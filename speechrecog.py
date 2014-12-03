import re
import speech_recognition as sr
from twitter import *
import pyaudio
import wave
import serial
from time import sleep

ser = serial.Serial('/dev/ttyACM0', 9600) #Create connection with Arduino through serial monitor


def record():
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	CHUNK = 1024
	RECORD_SECONDS = 5
	WAVE_OUTPUT_FILENAME = "file.wav"
	audio = pyaudio.PyAudio()
	# start Recording
	stream = audio.open(format=FORMAT, channels=CHANNELS,
	rate=RATE, input=True,
	frames_per_buffer=CHUNK)
	print "recording..."
	frames = []
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)

	print "finished recording"

	# stop Recording
	stream.stop_stream()
	stream.close()
	audio.terminate()
	waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()

def post(status_update):
	#status = createTweet(status_update)
	t = Twitter(auth = OAuth(
		"2866728543-ffQOspRpE91aRZTBMC5QT1cafYxh5zhIqm4PisO",
		"7jmQKSTGBU80LZNmq5KwAUARmoiXU58dDJC9mPpGJPjUf",
		"KaLVQbEPXhTsJg3l35DekQopB",
		"P6y08Y5ycMibtZoIjxXHOhaXMPZDYoXkLBhRKj1ZoFKyvIc368"))

	t.statuses.update(status=status_update)

def createTweet(status_update):
	status = "";
	control = 0;
	index = 0;
	for oldString in status_update.split(" "):
		word = re.sub('[^A-Za-z0-9]+', '', oldString)
		if(index == 0):
			if(word.lower() == "hashtag"):
				status = "#"
				control = 1
			else:
				status = word
			index = 1
			continue
		if(word.lower() == "hashtag"):
			status += " #"
			control = 1 
		else:
			if(control == 0):
				status += " " + word
			else:
				status += word.title()
	return status

def createTweet2(status_update):
	words = status_update.split(" ")
	status = ""
	onHash = False
	onTag = False
	onSkip = False

	for x in range(0, len(words)):
		if(onSkip):
			onSkip = False
			continue
		if(x == 0):
			if(words[x].lower() == "hashtag"):
				status = "#"
				onHash = True
			elif(words[x].lower() == "tweet" and len(words) > x+1 
				and words[x+1].lower() == "at"):
				status = "@"
				onTag = True
				onSkip = True
				continue
			else:
				status = words[x]
		else:
			if(onHash):
				if(words[x].lower() == "hashtag"):
					status += " #"
				elif(words[x].lower() == "tweet" and len(words) > x+1 
					and words[x+1].lower() == "at"):
						status += " @"
						onTag = True
						onSkip = True
						onHash = False
						continue
				else:
					status += words[x].title()
			elif(onTag):
				status += words[x]
				onTag = False
			else:
				if(words[x].lower() == "hashtag"):
					status += " #"
					onHash = True
				elif(words[x].lower() == "tweet" and len(words) > x+1 
					and words[x+1].lower() == "at"):
						status += " @"
						onTag = True
						onSkip = True
						continue
				else:
					status += " " + words[x]
	return status


#Loop for reading from Arduino serial, determining whether hashtag has been enabled

while True:
	try:
		serOut = ser.readline()
		#sleep(.1)
	except Exception, e:
		#print "No value read"
		#sleep(.11)
		#sleep(.1)
		continue
	

	if("1000" in serOut):
		print("Recording Audio...")
		record()

		r = sr.Recognizer() #Create speech recognition object
		with sr.WavFile("file.wav") as source:
			audio = r.listen(source) #Listen to created '.wav' file, create audio string with recognized audio

		try:
			tweet = createTweet2(r.recognize(audio)) #Create tweet with recognized audio
			print tweet 
			post(tweet) #Post tweet
		except LookupError:
			print "Could Not Understand What You Said" #If speechrecognition API fails to recognize speech, return error message

		ser = serial.Serial('/dev/ttyACM0', 9600) #Set up connection with Arduino through serial monitor