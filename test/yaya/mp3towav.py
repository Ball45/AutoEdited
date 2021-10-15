import os
songmp4 = "media\\NewRecording7.m4a"
songwav = "media\\NewRecording7.wav"
os.system("ffmpeg -i "+songmp4+" "+songwav)


## import os

##　mp4file = "media\\shallow.mp4"
##  mp3file = "media\\guitar.mp3"
##  os.system("ffmpeg -i "+mp4file+" "+mp3file)
