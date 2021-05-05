import os

mp4file = "media\\shallow.mp4"
mp3file = "media\\guitar.mp3"
os.system("ffmpeg -i "+mp4file+" "+mp3file)
