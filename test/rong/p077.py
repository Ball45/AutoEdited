import os
songmp3 = "media/test.mp3"
songwav = "media/test.wav"
os.system("ffmpeg -i "+songmp3+" "+songwav)