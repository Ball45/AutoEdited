import os
songm4a = "media/testre.m4a"
songmp3 = "media/testre.mp3"
os.system("ffmpeg -i "+songmp3+" -acodec libmp3lame -ab 256k "+songmp3)



