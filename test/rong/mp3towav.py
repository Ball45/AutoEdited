import os
songmp3 = "media/testa.mp3"
songwav = "media/testa.wav"
os.system("ffmpeg -i "+songmp3+" "+songwav)