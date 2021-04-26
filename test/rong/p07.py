import os
mp4file = "media/tainanvlog.mp4"
mp3file = "media/tai.mp3"
os.system("ffmpeg -i "+mp4file+" "+mp3file)