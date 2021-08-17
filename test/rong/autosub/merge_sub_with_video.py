import os

sourceVideo = "media/IMG_958999.mp4"
subtitles = "'media/IMG_958999.srt'"
force_style = ":force_style='Fontsize=24'"
outputVideo = "media/IMG_958999out817.mp4"
os.system("ffmpeg -i "+sourceVideo+" -i "+subtitles+" -c:s mov_text -c:v copy -c:a copy "+outputVideo)
#ffmpeg -i program/video/media/IMG_95899.mp4 -vf "subtitles='program/video/media/IMG_9589.srt'" program/video/media/IMG_95899out817.mp4
#ffmpeg -f concat -safe 0 -i mp4files.txt -c copy ConcatenatedVideo.MP4
#ffmpeg -i inputfile.mp4 -i subtitles.srt -c:s mov_text -c:v copy -c:a copy outputfile.mp4"