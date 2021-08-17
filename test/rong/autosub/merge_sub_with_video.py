import os

sourceVideo = "media/IMG_958999.mp4"
subtitles = "'media/IMG_958999.srt'"
force_style = ":force_style='Fontsize=24'"
outputVideo = "media/IMG_958999out817.mp4"
os.system("ffmpeg -i "+sourceVideo+" -i "+subtitles+" -c:s mov_text -c:v copy -c:a copy "+outputVideo)
