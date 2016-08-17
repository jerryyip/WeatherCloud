
import os
import signal
from microphone import Microphone
from bing_voice import *
from player import Player
import pyaudio
import sys
import time
import re
from spi import SPI
import json
import urllib

# weather information
city="hangzhou"
appID = "a9764b47b351cacfc45a5a352af45441"
url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&APPID=" + appID
           
def get_weather():
	try:
		jsonurl = urllib.urlopen(url)                      # open the url
        api_text = json.loads(jsonurl.read())
		weather_desc=api_text["weather"][0]["main"]
		return weather_desc
	except Exception as err:
		print('Get weather error:', err)
		return "Unknow"

try:
    from creds import BING_KEY
except ImportError:
    print('Get a key from https://www.microsoft.com/cognitive-services/en-us/speech-api and create creds.py with the key')
    sys.exit(-1)

script_dir = os.path.dirname(os.path.realpath(__file__))

hi = os.path.join(script_dir, 'audio/hi.wav')
thunder = os.path.join(script_dir, 'audio/thunder-01.wav')
spi = SPI()
spi.write('offline\n')

bing = BingVoice(BING_KEY)

mission_completed = False
awake = False

pa = pyaudio.PyAudio()
mic = Microphone(pa)
player = Player(pa)

spi.write('online\n');

def handle_int(sig, frame):
    global mission_completed
    mission_completed = True
    mic.close()


signal.signal(signal.SIGINT, handle_int)

while not mission_completed:
    if not awake:
        if mic.detect():
            spi.write('wakeup\n')
            awake = True
            player.play(hi)
        continue

    data = mic.listen()
    spi.write('wait\n')

    # recognize speech using Microsoft Bing Voice Recognition
    try:
        text = bing.recognize(data, language='en-US')
        spi.write('answer\n')
        print('Bing:' + text.encode('utf-8'))
        
        if re.search(r'weather', text) or re.search(r'what.*(weather).*', text):
            try:
                weather_info = get_weather()
                if weather_info == "Clear":
                    spi.write('sunny\n')
				if weather_info == "Clouds":
					spi.write('cloudy\n')
				if weather_info == "Rain":		
					spi.write('lightning\n')
					player.play(thunder)
			except Exception as err2:
				print ('spi write error: ',err2)
        else:
            print 'unknown command, ignore.' 
        
    except UnknownValueError:
        print("Microsoft Bing Voice Recognition could not understand audio")
    except RequestError as e:
        print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

    spi.write('sleep\n')
    awake = False
