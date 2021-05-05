import os
songmp3 = "media\\time2.mp3"
songwav = "media\\time3.wav"
os.system("ffmpeg -i "+songmp3+" "+songwav)
