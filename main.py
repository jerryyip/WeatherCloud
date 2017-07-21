#!/usr/bin/env python

import os
import signal
import time
from respeaker.bing_speech_api import BingSpeechAPI
from respeaker.microphone import Microphone
from respeaker.player import Player
from worker_weather import Worker


BING_KEY = '3560976f779d4095a7109bc55a3b0c79'

mic = Microphone()
bing = BingSpeechAPI(key=BING_KEY)
player = Player(mic.pyaudio_instance)
worker = Worker()
worker.set_player(player)
worker.set_tts(bing)

# script_dir = os.path.dirname(os.path.realpath(__file__))
# hello = os.path.join(script_dir, 'hello.wav')

mission_completed = False
awake = False
awake_count = 0


mission_completed = False
# awake = False
awake = True

def handle_int(sig, frame):
    global mission_completed

    print "terminating..."
    # pixel_ring.off()
    mission_completed = True
    mic.close()
    player.close()
    worker.stop()


signal.signal(signal.SIGINT, handle_int)
worker.start()

# pixel_ring.set_color(r=0, g=0, b=100)
# time.sleep(3)
# player.play(hello)


while not mission_completed:
    
    if mic.wakeup('respeaker'):
        print "wakeup, please speak your command"
        time.sleep(0.5)
        data = mic.listen()
        data = b''.join(data)

    # recognize speech using Microsoft Bing Voice Recognition
        try:
            text = bing.recognize(data, language='en-US')
            print('Bing:' + text.encode('utf-8'))
            worker.push_cmd(text)
            worker.wait_done()

            if text.find('shut down') > -1:
                handle_int(0,0)
        except Exception as e:
            print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
    
        

