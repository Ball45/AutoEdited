import os

inputfile = "media\\guitar.mp3"
os.system("ffmpeg - i " + inputfile + " - af silencedetect - f null")
