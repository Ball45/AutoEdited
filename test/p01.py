from moviepy.editor import *

#IMAGEMAGICK_BINARY = os.getenv ('IMAGEMAGICK_BINARY', 'C:\Program Files\ImageMagick-7.0.8-Q16\convert.exe')

video = VideoFileClip("media/501A.wmv").subclip(50,60)

# Make the text. Many more options are available.
txt_clip = ( TextClip("501A Story",fontsize=70,color='white')
             .set_position('center')
             .set_duration(10) )

result = CompositeVideoClip([video, txt_clip]) # Overlay text on video
result.write_videofile("media/newStory.mp4",fps=25) # Many options...