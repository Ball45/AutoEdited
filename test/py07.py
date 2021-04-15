import os
mp4file = "z.wmv"
mp3file = "t.mp3"
os.system("ffmpeg -i "+mp4file+" "+mp3file)