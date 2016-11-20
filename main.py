import os
import logging
import time
from threading import Thread, Event
from respeaker import Microphone
from respeaker.bing_speech_api import BingSpeechAPI
from respeaker import spi
from respeaker import Player
import pyaudio
import json
import urllib

# get a key from https://www.microsoft.com/cognitive-services/en-us/speech-api
BING_KEY = 'c1fefcacc66842939663cc6a45058762'

# weather information 
# get appid from http://openweathermap.org/appid
city="shenzhen"
appID = ""
url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&APPID=" + appID


script_dir = os.path.dirname(os.path.realpath(__file__))
hi = os.path.join(script_dir, 'audio/hi.wav')
#thunder = os.path.join(script_dir, 'audio/thunder-01.wav')
pa = pyaudio.PyAudio()
player = Player(pa)

#set led red
spi.write(data = bytearray([1, 0, 0, 50]), address = 0x00)

def getWeather():
    try:
        jsonurl = urllib.urlopen(url)                 
        api_text = json.loads(jsonurl.read())
        weather_desc=api_text["weather"][0]["main"]
        return weather_desc
    except Exception as err:
        print('Get weather error:', err)
        return "Unknow"



def task(quit_event):
    mic = Microphone(quit_event=quit_event)
    bing = BingSpeechAPI(key=BING_KEY)

    while not quit_event.is_set():
        if mic.wakeup('respeaker'):
            print('Wake up')
            player.play(hi)
            data = mic.listen()
            try:
                text = bing.recognize(data)
                if text:
                    print('Recognized %s' % text)
                    if 'weather' in text:
                        try:
                            weather_info = getWeather()
                            print ('The weather is *****%s***** in %s!' % weather_info, city)
                            if weather_info == "Clear":
                                #set led golden as sun
                                spi.write(data = bytearray([1, 34, 180, 240]), address = 0x00)
                                time.sleep(3)
                            if weather_info == "Clouds":
                                #set led blue as cloud
                                spi.write(data = bytearray([1, 255, 245, 152]), address = 0x00)
                                time.sleep(3)
                            if weather_info == "Rain":      
                                #set led blink as thunder
                                spi.write(data = bytearray([1, 255, 255, 255]), address = 0x00)
                                time.sleep(0.1)
                                spi.write(data = bytearray([0]), address = 0x00)
                                time.sleep(0.2)
                                spi.write(data = bytearray([1, 100, 100, 100]), address = 0x00)
                                time.sleep(0.25)
                                spi.write(data = bytearray([0]), address = 0x00)
                                time.sleep(0.2)
                                spi.write(data = bytearray([1, 255, 255, 255]), address = 0x00)
                                time.sleep(0.1)
                                spi.write(data = bytearray([0]), address = 0x00)
                                time.sleep(0.2)
                                spi.write(data = bytearray([1, 100, 100, 100]), address = 0x00)
                                time.sleep(0.25)
                                spi.write(data = bytearray([0]), address = 0x00)
                                time.sleep(0.2)
                                #play sound of thunder
                                player.play(thunder)
                        except Exception as err2:
                            print ('spi write error: ',err2)
            except Exception as e:
                print(e.message)


def main():
    logging.basicConfig(level=logging.DEBUG)

    quit_event = Event()
    thread = Thread(target=task, args=(quit_event,))
    thread.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('Quit')
            quit_event.set()
            break
    thread.join()

if __name__ == '__main__':
    main()