import os

mp4file = "media\\train.mp4"
mp3file = "media\\railway.mp3"
os.system("ffmpeg -i "+mp4file+" "+mp3file)
