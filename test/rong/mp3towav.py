import os
songmp3 = "media/testb.mp3"
songwav = "media/testb.wav"
os.system("ffmpeg -i "+songmp3+" "+songwav)