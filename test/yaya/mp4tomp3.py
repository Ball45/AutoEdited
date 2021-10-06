import os

<<<<<<< Updated upstream
mp4file = "media\\08141.m4a"
mp3file = "media\\08141.wav"
=======
mp4file = "media\\test1_out.mp4"
mp3file = "media\\test1_out.mp3"
>>>>>>> Stashed changes
os.system("ffmpeg -i "+mp4file+" "+mp3file)
