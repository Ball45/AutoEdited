FONT_URL='media/wt024.ttf'
from moviepy.editor import *
import os

#IMAGEMAGICK_BINARY = os.getenv('IMAGEMAGICK_BINARY', '.\\magick.exe')


video = VideoFileClip("media/video9589_out.mp4").subclip(0, 10)

# Make the text. Many more options are available.
txt_clip = (TextClip("0325 how are you你好嗎", fontsize=70, color='white', font=FONT_URL)
            .set_position('center')
            .set_duration(10))

result = CompositeVideoClip([video, txt_clip])  # Overlay text on video
result.write_videofile("media/newStory.mp4", fps=25)  # Many options...
