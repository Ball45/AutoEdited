import os
songmp3 = "media/testc.mp3"
songwav = "media/testc.wav"
os.system("ffmpeg -i "+songmp3+" "+songwav)