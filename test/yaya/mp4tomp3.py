import os

mp4file = "media\\08141.m4a"
mp3file = "media\\08141.wav"
os.system("ffmpeg -i "+mp4file+" "+mp3file)
