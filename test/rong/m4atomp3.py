import os
songm4a = "media/testb.m4a"
songmp3 = "media/testb.mp3"
os.system("ffmpeg -i "+songm4a+" -acodec libmp3lame -ab 256k "+songmp3)


