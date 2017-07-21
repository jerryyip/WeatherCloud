# coding:utf-8
import time
from functools import wraps
import threading
import Queue
import re
import json
import os
from respeaker.pixel_ring import PixelRing


from urllib import urlencode
from urllib2 import Request, urlopen, URLError, HTTPError

pixel_ring = PixelRing()

CITY = 'chengdu'
APPID = '9e0ed3b5248bb3ed915c862b3a684e78'
URL = "http://api.openweathermap.org/data/2.5/weather?q=" + CITY + "&APPID=" + APPID

def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        print "[%s] time running: %fs" % (func.__name__, t1-t0)
        return result
    return wrapper


class Worker(threading.Thread):
    def __init__(self, queue_len=8):
        threading.Thread.__init__(self)
        self.q = Queue.Queue(queue_len)
        self.thread_stop = False

        self.last_time_broadcast = 0
        self.weather = 'none'   # weather string
        
    def set_player(self, ply):
        self.player = ply

    def set_tts(self, texttospeech):
        self.tts = texttospeech

    def wait_done(self):
        self.q.join()

    def push_cmd(self, cmd):
        self.q.put(cmd)

    def get_weather(self):
        request = Request(URL)
        try:
            response = urlopen(request)
            data = response.read()
            result = json.loads(data)
            if result['weather'][0]['main']:
                self.weather = result['weather'][0]['main']
        except Exception:
            self.weather = 'none'


    def run(self):
        while not self.thread_stop:
            self.get_weather()

            cmd = ''
            try:
                cmd = self.q.get(timeout=1)
            except:
                continue
            print("worker thread get cmd: %s" %(cmd, ))
            self._parse_cmd(cmd)
            self.q.task_done()
            len = self.q.qsize()
            if len > 0:
                print("still got %d commands to execute." % (len,))

    def _parse_cmd(self, cmd):
        if re.search(r'(.*)(How|what).*(are|is|were).*(weather|wheather)', cmd, re.I|re.M):
            # text = "The soil humidity is now %.1f percent. I feel thristy." % (self.moispersent)
            # self.player.play_raw(self.tts.synthesize(text))
            print("the weather is {} now".format(self.weather))
            if self.weather == 'Clear':
                pixel_ring.set_color(r=0, g=0, b=100)
            elif self.weather == 'Clouds':
                pixel_ring.set_color(r=255, g=225, b=0)
            elif self.weather == 'Rain':
                pixel_ring.set_color(r=255, g=255, b=255)
                time.sleep(1)
                pixel_ring.set_color(r=0, g=0, b=0)
                time.sleep(1)
                pixel_ring.set_color(r=255, g=255, b=255)
                time.sleep(1)
                pixel_ring.set_color(r=0, g=0, b=0)
                time.sleep(1)
                pixel_ring.set_color(r=255, g=255, b=255)
                time.sleep(1)
        elif re.search(r'shut.*down', cmd, re.I|re.M):
            print "*********shut down*********"
        else:
            # self.player.play(sorry)
            print "sorry i don't know your command."


    def stop(self):
        self.thread_stop = True
        self.q.join()

