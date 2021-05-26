import os

mp4file = "media\\testb.wav"
mp3file = "media\\testb1.wav"
os.system("ffmpeg -i "+mp4file+" "+mp3file)
