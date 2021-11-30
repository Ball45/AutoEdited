import os
songmp3 = "media/testc.mp3"
songwav = "media/testc.wav"
os.system("ffmpeg -i "+songmp3+" "+songwav)


songm4a = "media/testc.m4a"
songmp3 = "media/testc.mp3"
os.system("ffmpeg -i "+songm4a+" -acodec libmp3lame -ab 256k "+songmp3)


videomp4 = "media/testc.m4a"
videoavi = "media/testc.mp3"
os.system("ffmpeg -i "+ videomp4 + " -c copy -map 0 " + videoavi)