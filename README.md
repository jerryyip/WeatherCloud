#Weather Cloud

Visualize the weather condition as you asked.

<div class="text-center">
<img src="https://github.com/respeaker/get_started_with_respeaker/blob/master/img/weathercloud.jpg?raw=true" width="50%" height="50%">
</div>

Weather Cloud is an awesome project for ReSpeaker. This cool build turns a ReSpeaker into a Weather Cloud, which is able to show you the whether with vivid light and sounds.

In this project, Openwrt is in charge of getting realtime weather information from the Internet, making voice interaction and audio output, while Arduino is responsible for controlling the colorful RGB LEDs.

###Getting started

1. `git clone https://github.com/jerryyip/WeatherCloud.git` on ReSpeaker, download the repository 
2. Download [ReSpeaker Arduino Library](https://github.com/respeaker/respeaker_arduino_library) in your computer
3. Upload [pixels_pattern.ino](https://github.com/respeaker/respeaker_arduino_library/blob/master/examples/pixels_pattern/pixels_pattern.ino) in ReSpeaker Arduino  Library to ReSpeaker's Arduino 
4. Get OpenWeatherMap appid from [here](http://openweathermap.org/appid) and copy it to `appID = ""` in `main.py`, don't forget to add your city in `city=""`
5. Stop mopidy service on OpenWrt before using SPI bridge
`/etc/init.d/mopidy stop`
6. Run `python main.py` and say "ReSpeaker, what is the weather like?" to ReSpeaker.
7. For more details about how to make a Weather Could, please click [here](http://www.instructables.com/id/How-to-DIY-an-in-House-Weather-telling-Cloud/).
