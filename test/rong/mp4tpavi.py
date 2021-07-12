import os
videomp4 = "media/testc.m4a"
videoavi = "media/testc.mp3"
os.system("ffmpeg -i "+ videomp4 + " -c copy -map 0 " + videoavi)